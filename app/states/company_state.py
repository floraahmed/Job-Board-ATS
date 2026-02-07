import reflex as rx
from typing import Optional
from app.states.auth_state import AuthState
from app.models import Company as CompanyDict
from app.database.models import Company, Job, Application
from app.database.connection import get_session
from sqlmodel import select, col


class CompanyState(rx.State):
    temp_name: str = ""
    temp_industry: str = ""
    temp_description: str = ""
    temp_logo: str = ""
    is_saving: bool = False

    @rx.var
    async def current_company(self) -> Optional[CompanyDict]:
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return None
        cid = auth.current_user["company_id"]
        with get_session() as session:
            comp = session.exec(select(Company).where(Company.id == cid)).first()
            return comp.model_dump() if comp else None

    @rx.var
    async def stats(self) -> dict[str, int]:
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return {"total_jobs": 0, "total_apps": 0}
        cid = auth.current_user["company_id"]
        with get_session() as session:
            jobs = session.exec(select(Job).where(Job.company_id == cid)).all()
            job_ids = [j.id for j in jobs]
            if not job_ids:
                return {"total_jobs": len(jobs), "total_apps": 0}
            app_count = len(
                session.exec(
                    select(Application).where(col(Application.job_id).in_(job_ids))
                ).all()
            )
            return {"total_jobs": len(jobs), "total_apps": app_count}

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
        auth = await self.get_state(AuthState)
        cid = auth.current_user.get("company_id")
        with get_session() as session:
            comp = session.exec(select(Company).where(Company.id == cid)).first()
            if comp:
                comp.name = self.temp_name
                comp.industry = self.temp_industry
                comp.description = self.temp_description
                comp.logo = self.temp_logo
                session.add(comp)
                session.commit()
        self.is_saving = False
        yield rx.toast("Company profile updated", position="bottom-right")