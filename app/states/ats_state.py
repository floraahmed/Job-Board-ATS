import reflex as rx
from typing import Optional, Any
from app.models import (
    Application as ApplicationDict,
    ApplicationHistory as HistoryDict,
    Job as JobDict,
    User as UserDict,
)
from app.database.models import Application, ApplicationHistory, Job, User
from app.states.auth_state import AuthState
from app.database.connection import get_session
from sqlmodel import select, col, or_
import datetime
import uuid


class ATSState(rx.State):
    current_job_id: str = ""
    selected_application_id: str = ""
    search_query: str = ""
    note_input: str = ""
    filter_status: str = "all"
    filter_days: str = "all"
    sort_order: str = "newest"

    @rx.var
    async def current_job(self) -> Optional[JobDict]:
        with get_session() as session:
            job = session.exec(select(Job).where(Job.id == self.current_job_id)).first()
            return job.model_dump() if job else None

    @rx.var
    async def active_application(self) -> Optional[ApplicationDict]:
        if not self.selected_application_id:
            return None
        with get_session() as session:
            app = session.exec(
                select(Application).where(
                    Application.id == self.selected_application_id
                )
            ).first()
            return app.model_dump() if app else None

    @rx.var
    async def application_history(self) -> list[HistoryDict]:
        if not self.selected_application_id:
            return []
        with get_session() as session:
            hist = session.exec(
                select(ApplicationHistory)
                .where(
                    ApplicationHistory.application_id == self.selected_application_id
                )
                .order_by(col(ApplicationHistory.changed_at).desc())
            ).all()
            return [h.model_dump() for h in hist]

    @rx.var
    async def active_applicant_user(self) -> Optional[UserDict]:
        app = await self.active_application
        if not app:
            return None
        with get_session() as session:
            user = session.exec(
                select(User).where(User.id == app["applicant_id"])
            ).first()
            return user.model_dump() if user else None

    @rx.var
    async def filtered_applications(self) -> list[ApplicationDict]:
        with get_session() as session:
            query = select(Application).where(Application.job_id == self.current_job_id)
            if self.search_query:
                q = self.search_query.lower()
                query = query.where(
                    or_(
                        col(Application.cover_letter).contains(q),
                        col(Application.answers).contains(q),
                    )
                )
            apps = session.exec(query).all()
            if self.filter_days != "all":
                days = int(self.filter_days)
                cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
                apps = [
                    a
                    for a in apps
                    if datetime.datetime.strptime(a.applied_at, "%Y-%m-%d") >= cutoff
                ]
            apps.sort(key=lambda x: x.applied_at, reverse=self.sort_order == "newest")
            return [a.model_dump() for a in apps]

    @rx.var
    async def kanban_columns(self) -> dict[str, list[dict]]:
        apps = await self.filtered_applications
        columns = {
            "new": [],
            "under_review": [],
            "interview": [],
            "rejected": [],
            "hired": [],
        }
        with get_session() as session:
            applicant_ids = {a["applicant_id"] for a in apps}
            if applicant_ids:
                users = session.exec(
                    select(User).where(col(User.id).in_(applicant_ids))
                ).all()
                user_map = {u.id: u for u in users}
            else:
                user_map = {}
            for app in apps:
                status = app.get("status", "new")
                if status in columns:
                    app_with_user = dict(app)
                    user = user_map.get(app["applicant_id"])
                    app_with_user["applicant_name"] = user.name if user else "Unknown"
                    columns[status].append(app_with_user)
        return columns

    @rx.event
    async def load_job_data(self):
        self.current_job_id = self.router.page.params.get("job_id", "")
        self.selected_application_id = ""

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def set_filter_days(self, days: str):
        self.filter_days = days

    @rx.event
    def select_application(self, app_id: str):
        self.selected_application_id = app_id

    @rx.event
    def close_detail_view(self):
        self.selected_application_id = ""
        self.note_input = ""

    @rx.event
    def set_note_input(self, val: str):
        self.note_input = val

    @rx.event
    async def move_stage(self, app_id: str, new_stage: str):
        auth = await self.get_state(AuthState)
        from app.states.notification_state import NotificationState

        notes = await self.get_state(NotificationState)
        with get_session() as session:
            app = session.exec(
                select(Application).where(Application.id == app_id)
            ).first()
            if app:
                old_stage = app.status
                if old_stage != new_stage:
                    app.status = new_stage
                    session.add(app)
                    history_entry = ApplicationHistory(
                        id=f"hist_{uuid.uuid4().hex[:8]}",
                        application_id=app_id,
                        old_status=old_stage,
                        new_status=new_stage,
                        changed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        notes=f"Moved from {old_stage} to {new_stage} by {auth.user_name}",
                    )
                    session.add(history_entry)
                    session.commit()
                    await notes.add_notification(
                        app.applicant_id,
                        "Application Update",
                        f"Your application status has been changed to {new_stage.replace('_', ' ')}.",
                        "info",
                    )
                    yield rx.toast(
                        f"Application moved to {new_stage}", position="bottom-right"
                    )

    @rx.event
    async def add_note(self):
        if not self.note_input or not self.selected_application_id:
            return
        auth = await self.get_state(AuthState)
        app = await self.active_application
        current_status = app["status"] if app else "unknown"
        with get_session() as session:
            history_entry = ApplicationHistory(
                id=f"hist_{uuid.uuid4().hex[:8]}",
                application_id=self.selected_application_id,
                old_status=current_status,
                new_status=current_status,
                changed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                notes=f"Note: {self.note_input} (by {auth.user_name})",
            )
            session.add(history_entry)
            session.commit()
        self.note_input = ""
        yield rx.toast("Note added", position="bottom-right")

    @rx.var
    async def all_employer_applications(self) -> list[ApplicationDict]:
        """For the aggregate view"""
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return []
        company_id = auth.current_user["company_id"]
        with get_session() as session:
            jobs = session.exec(select(Job).where(Job.company_id == company_id)).all()
            job_ids = [j.id for j in jobs]
            job_map = {j.id: j.title for j in jobs}
            if not job_ids:
                return []
            apps = session.exec(
                select(Application).where(col(Application.job_id).in_(job_ids))
            ).all()
            if not apps:
                return []
            applicant_ids = [a.applicant_id for a in apps]
            users = session.exec(
                select(User).where(col(User.id).in_(applicant_ids))
            ).all()
            user_map = {u.id: u for u in users}
            enriched = []
            for app in apps:
                d = app.model_dump()
                d["job_title"] = job_map.get(app.job_id, "Unknown")
                user = user_map.get(app.applicant_id)
                d["applicant_name"] = user.name if user else "Unknown"
                d["email"] = user.email if user else ""
                enriched.append(d)
            return enriched