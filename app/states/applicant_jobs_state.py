import reflex as rx
from typing import Optional
from app.models import Job as JobDict
from app.database.models import Job
from app.database.connection import get_session
from sqlmodel import select, col, or_
import datetime


class ApplicantJobsState(rx.State):
    search_query: str = ""
    selected_industry: str = "all"
    selected_location: str = ""
    selected_seniority: str = "all"
    salary_min_filter: int = 0
    date_filter: str = "all"
    selected_job_id: str = ""

    @rx.var
    async def filtered_jobs(self) -> list[JobDict]:
        with get_session() as session:
            query = select(Job).where(Job.status == "published")
            if self.search_query:
                sq = self.search_query.lower()
                query = query.where(
                    or_(col(Job.title).contains(sq), col(Job.industry).contains(sq))
                )
            if self.selected_industry != "all":
                query = query.where(Job.industry == self.selected_industry)
            if self.selected_location:
                loc = self.selected_location.lower()
                query = query.where(col(Job.location).contains(loc))
            if self.selected_seniority != "all":
                query = query.where(Job.seniority_level == self.selected_seniority)
            if self.salary_min_filter > 0:
                query = query.where(Job.salary_max >= self.salary_min_filter)
            jobs = session.exec(query).all()
            return [j.model_dump() for j in jobs]

    @rx.var
    def industries(self) -> list[str]:
        return [
            "all",
            "Software",
            "FinTech",
            "HealthTech",
            "Design",
            "Marketing",
            "Sales",
        ]

    @rx.var
    async def selected_job(self) -> Optional[JobDict]:
        if not self.selected_job_id:
            return None
        with get_session() as session:
            job = session.exec(
                select(Job).where(Job.id == self.selected_job_id)
            ).first()
            return job.model_dump() if job else None

    @rx.event
    def set_job(self, job_id: str):
        self.selected_job_id = job_id

    @rx.event
    def clear_filters(self):
        self.search_query = ""
        self.selected_industry = "all"
        self.selected_location = ""
        self.selected_seniority = "all"
        self.salary_min_filter = 0
        self.date_filter = "all"