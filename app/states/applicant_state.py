import reflex as rx
from typing import Optional
from app.states.auth_state import AuthState
from app.models import ApplicationHistory as HistoryDict
from app.database.models import Application, ApplicationHistory, Job, Company
from app.database.connection import get_session
from sqlmodel import select, col


class ApplicantState(rx.State):
    selected_app_id: str = ""
    status_filter: str = "all"

    @rx.var
    async def my_applications(self) -> list[dict]:
        auth = await self.get_state(AuthState)
        if not auth.current_user:
            return []
        user_id = auth.current_user["id"]
        with get_session() as session:
            apps = session.exec(
                select(Application).where(Application.applicant_id == user_id)
            ).all()
            if not apps:
                return []
            job_ids = [a.job_id for a in apps]
            jobs = session.exec(select(Job).where(col(Job.id).in_(job_ids))).all()
            job_map = {j.id: j for j in jobs}
            comp_ids = [j.company_id for j in jobs]
            comps = session.exec(
                select(Company).where(col(Company.id).in_(comp_ids))
            ).all()
            comp_map = {c.id: c for c in comps}
            enriched = []
            for a in apps:
                if self.status_filter != "all" and a.status != self.status_filter:
                    continue
                job = job_map.get(a.job_id)
                comp = comp_map.get(job.company_id) if job else None
                d = a.model_dump()
                d["job_title"] = job.title if job else "Unknown Job"
                d["company_name"] = comp.name if comp else "Unknown Company"
                enriched.append(d)
            return sorted(enriched, key=lambda x: x["applied_at"], reverse=True)

    @rx.var
    async def selected_app(self) -> Optional[dict]:
        if not self.selected_app_id:
            return None
        apps = await self.my_applications
        return next((a for a in apps if a["id"] == self.selected_app_id), None)

    @rx.var
    async def selected_app_history(self) -> list[HistoryDict]:
        if not self.selected_app_id:
            return []
        with get_session() as session:
            hist = session.exec(
                select(ApplicationHistory)
                .where(ApplicationHistory.application_id == self.selected_app_id)
                .order_by(col(ApplicationHistory.changed_at).desc())
            ).all()
            return [h.model_dump() for h in hist]

    @rx.event
    def set_selected_app(self, app_id: str):
        self.selected_app_id = app_id

    @rx.event
    def close_detail(self):
        self.selected_app_id = ""