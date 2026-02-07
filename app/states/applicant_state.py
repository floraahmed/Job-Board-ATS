import reflex as rx
from typing import Optional
from app.states.db_state import DbState
from app.states.auth_state import AuthState
from app.models import Application, ApplicationHistory


class ApplicantState(rx.State):
    selected_app_id: str = ""
    status_filter: str = "all"

    @rx.var
    async def my_applications(self) -> list[dict]:
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if not auth.current_user:
            return []
        user_id = auth.current_user["id"]
        apps = [a for a in db.applications if a["applicant_id"] == user_id]
        jobs_dict = {j["id"]: j for j in db.jobs}
        comps_dict = {c["id"]: c for c in db.companies}
        enriched = []
        for a in apps:
            job = jobs_dict.get(a["job_id"], {})
            comp = comps_dict.get(job.get("company_id"), {})
            d = dict(a)
            d["job_title"] = job.get("title", "Unknown Job")
            d["company_name"] = comp.get("name", "Unknown Company")
            enriched.append(d)
        if self.status_filter != "all":
            enriched = [e for e in enriched if e["status"] == self.status_filter]
        return sorted(enriched, key=lambda x: x["applied_at"], reverse=True)

    @rx.var
    async def selected_app(self) -> Optional[dict]:
        if not self.selected_app_id:
            return None
        apps = await self.my_applications
        return next((a for a in apps if a["id"] == self.selected_app_id), None)

    @rx.var
    async def selected_app_history(self) -> list[ApplicationHistory]:
        if not self.selected_app_id:
            return []
        db = await self.get_state(DbState)
        return [h for h in db.history if h["application_id"] == self.selected_app_id]

    @rx.event
    def set_selected_app(self, app_id: str):
        self.selected_app_id = app_id

    @rx.event
    def close_detail(self):
        self.selected_app_id = ""