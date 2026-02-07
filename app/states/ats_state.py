import reflex as rx
from typing import Optional, Any
from app.models import Application, ApplicationHistory, Job, User
from app.states.db_state import DbState
from app.states.auth_state import AuthState
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
    async def current_job(self) -> Optional[Job]:
        db = await self.get_state(DbState)
        return next((j for j in db.jobs if j["id"] == self.current_job_id), None)

    @rx.var
    async def active_application(self) -> Optional[Application]:
        if not self.selected_application_id:
            return None
        db = await self.get_state(DbState)
        return next(
            (a for a in db.applications if a["id"] == self.selected_application_id),
            None,
        )

    @rx.var
    async def application_history(self) -> list[ApplicationHistory]:
        if not self.selected_application_id:
            return []
        db = await self.get_state(DbState)
        hist = [
            h for h in db.history if h["application_id"] == self.selected_application_id
        ]
        return sorted(hist, key=lambda x: x["changed_at"], reverse=True)

    @rx.var
    async def active_applicant_user(self) -> Optional[User]:
        app = await self.active_application
        if not app:
            return None
        db = await self.get_state(DbState)
        return next((u for u in db.users if u["id"] == app["applicant_id"]), None)

    @rx.var
    async def filtered_applications(self) -> list[Application]:
        db = await self.get_state(DbState)
        apps = [a for a in db.applications if a["job_id"] == self.current_job_id]
        if self.search_query:
            q = self.search_query.lower()
            applicant_ids = {a["applicant_id"] for a in apps}
            users = {u["id"]: u for u in db.users if u["id"] in applicant_ids}
            apps = [
                a
                for a in apps
                if q in a.get("cover_letter", "").lower()
                or q in a.get("answers", "").lower()
                or q in users.get(a["applicant_id"], {}).get("name", "").lower()
            ]
        if self.filter_days != "all":
            days = int(self.filter_days)
            cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
            apps = [
                a
                for a in apps
                if datetime.datetime.strptime(a["applied_at"], "%Y-%m-%d") >= cutoff
            ]
        apps.sort(key=lambda x: x["applied_at"], reverse=self.sort_order == "newest")
        return apps

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
        db = await self.get_state(DbState)
        applicant_ids = {a["applicant_id"] for a in apps}
        users = {u["id"]: u for u in db.users if u["id"] in applicant_ids}
        for app in apps:
            status = app.get("status", "new")
            if status in columns:
                app_with_user = dict(app)
                user = users.get(app["applicant_id"])
                app_with_user["applicant_name"] = user["name"] if user else "Unknown"
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
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        app_idx = -1
        for i, a in enumerate(db.applications):
            if a["id"] == app_id:
                app_idx = i
                break
        if app_idx >= 0:
            old_stage = db.applications[app_idx]["status"]
            if old_stage != new_stage:
                db.applications[app_idx]["status"] = new_stage
                history_entry: ApplicationHistory = {
                    "id": f"hist_{uuid.uuid4().hex[:8]}",
                    "application_id": app_id,
                    "old_status": old_stage,
                    "new_status": new_stage,
                    "changed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "notes": f"Moved from {old_stage} to {new_stage} by {auth.user_name}",
                }
                db.history.append(history_entry)
                yield rx.toast(
                    f"Application moved to {new_stage}", position="bottom-right"
                )

    @rx.event
    async def add_note(self):
        if not self.note_input or not self.selected_application_id:
            return
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        app = await self.active_application
        current_status = app["status"] if app else "unknown"
        history_entry: ApplicationHistory = {
            "id": f"hist_{uuid.uuid4().hex[:8]}",
            "application_id": self.selected_application_id,
            "old_status": current_status,
            "new_status": current_status,
            "changed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "notes": f"Note: {self.note_input} (by {auth.user_name})",
        }
        db.history.append(history_entry)
        self.note_input = ""
        yield rx.toast("Note added", position="bottom-right")

    @rx.var
    async def all_employer_applications(self) -> list[Application]:
        """For the aggregate view"""
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return []
        company_id = auth.current_user["company_id"]
        comp_jobs = {j["id"]: j for j in db.jobs if j["company_id"] == company_id}
        relevant_apps = [a for a in db.applications if a["job_id"] in comp_jobs]
        applicant_ids = {a["applicant_id"] for a in relevant_apps}
        users = {u["id"]: u for u in db.users if u["id"] in applicant_ids}
        enriched = []
        for app in relevant_apps:
            d = dict(app)
            d["job_title"] = comp_jobs[app["job_id"]]["title"]
            user = users.get(app["applicant_id"], {})
            d["applicant_name"] = user.get("name", "Unknown")
            d["email"] = user.get("email", "")
            enriched.append(d)
        return enriched