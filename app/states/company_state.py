import reflex as rx
from typing import Optional
from app.states.db_state import DbState
from app.states.auth_state import AuthState
from app.models import Company


class CompanyState(rx.State):
    temp_name: str = ""
    temp_industry: str = ""
    temp_description: str = ""
    temp_logo: str = ""
    is_saving: bool = False

    @rx.var
    async def current_company(self) -> Optional[Company]:
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return None
        cid = auth.current_user["company_id"]
        return next((c for c in db.companies if c["id"] == cid), None)

    @rx.var
    async def stats(self) -> dict[str, int]:
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return {"total_jobs": 0, "total_apps": 0}
        cid = auth.current_user["company_id"]
        jobs = [j for j in db.jobs if j["company_id"] == cid]
        job_ids = [j["id"] for j in jobs]
        apps = [a for a in db.applications if a["job_id"] in job_ids]
        return {"total_jobs": len(jobs), "total_apps": len(apps)}

    @rx.event
    async def load_company(self):
        comp = await self.current_company
        if comp:
            self.temp_name = comp["name"]
            self.temp_industry = comp["industry"]
            self.temp_description = comp["description"]
            self.temp_logo = comp["logo"]

    @rx.event
    async def save_company(self):
        self.is_saving = True
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        cid = auth.current_user.get("company_id")
        for i, c in enumerate(db.companies):
            if c["id"] == cid:
                db.companies[i]["name"] = self.temp_name
                db.companies[i]["industry"] = self.temp_industry
                db.companies[i]["description"] = self.temp_description
                db.companies[i]["logo"] = self.temp_logo
                break
        self.is_saving = False
        yield rx.toast("Company profile updated", position="bottom-right")