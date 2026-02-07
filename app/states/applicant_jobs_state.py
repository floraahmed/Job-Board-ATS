import reflex as rx
from typing import Optional
from app.models import Job
from app.states.db_state import DbState
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
    async def filtered_jobs(self) -> list[dict]:
        db = await self.get_state(DbState)
        jobs = [j for j in db.jobs if j["status"] == "published"]
        if self.search_query:
            sq = self.search_query.lower()
            jobs = [
                j
                for j in jobs
                if sq in j["title"].lower() or sq in j["industry"].lower()
            ]
        if self.selected_industry != "all":
            jobs = [j for j in jobs if j["industry"] == self.selected_industry]
        if self.selected_location:
            loc = self.selected_location.lower()
            jobs = [j for j in jobs if loc in j["location"].lower()]
        if self.selected_seniority != "all":
            jobs = [j for j in jobs if j["seniority_level"] == self.selected_seniority]
        if self.salary_min_filter > 0:
            jobs = [j for j in jobs if j["salary_max"] >= self.salary_min_filter]
        return jobs

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
    async def selected_job(self) -> Optional[dict]:
        if not self.selected_job_id:
            return None
        db = await self.get_state(DbState)
        return next((j for j in db.jobs if j["id"] == self.selected_job_id), None)

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