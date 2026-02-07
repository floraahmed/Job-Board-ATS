import reflex as rx
from typing import Optional, Any
from app.models import Job as JobDict, JobStatus, SeniorityLevel
from app.database.models import Job
from app.states.auth_state import AuthState
from app.database.connection import get_session
from sqlmodel import select, or_, col
import uuid
import datetime


class JobsState(rx.State):
    job_title: str = ""
    job_description: str = ""
    job_location: str = ""
    salary_min: int = 0
    salary_max: int = 0
    selected_skills: list[str] = []
    new_skill: str = ""
    selected_industry: str = ""
    selected_seniority: str = "mid"
    deadline: str = ""
    job_tab: str = "all"
    is_submitting: bool = False
    search_query: str = ""

    @rx.var
    def industries(self) -> list[str]:
        return ["Software", "FinTech", "HealthTech", "Design", "Marketing", "Sales"]

    @rx.var
    def seniority_levels(self) -> list[str]:
        return ["entry", "mid", "senior", "lead", "executive"]

    @rx.var
    async def employer_jobs(self) -> list[JobDict]:
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            return []
        company_id = auth.current_user["company_id"]
        with get_session() as session:
            query = select(Job).where(Job.company_id == company_id)
            if self.job_tab == "active":
                query = query.where(Job.status == "published")
            elif self.job_tab == "draft":
                query = query.where(Job.status == "draft")
            elif self.job_tab == "closed":
                query = query.where(Job.status == "closed")
            if self.search_query:
                sq = self.search_query.lower()
                query = query.where(
                    or_(col(Job.title).contains(sq), col(Job.location).contains(sq))
                )
            jobs = session.exec(query).all()
            return [j.model_dump() for j in jobs]

    @rx.event
    def add_skill(self):
        if self.new_skill and self.new_skill not in self.selected_skills:
            self.selected_skills.append(self.new_skill)
            self.new_skill = ""

    @rx.event
    def remove_skill(self, skill: str):
        self.selected_skills = [s for s in self.selected_skills if s != skill]

    @rx.event
    async def save_job(self, status: JobStatus = "published"):
        self.is_submitting = True
        auth = await self.get_state(AuthState)
        if not auth.current_user or not auth.current_user.get("company_id"):
            self.is_submitting = False
            yield rx.toast("Error: Company not found", position="bottom-right")
            return
        with get_session() as session:
            new_job = Job(
                id=f"job_{uuid.uuid4().hex[:8]}",
                company_id=auth.current_user["company_id"],
                title=self.job_title,
                description=self.job_description,
                location=self.job_location,
                salary_min=self.salary_min,
                salary_max=self.salary_max,
                required_skills=self.selected_skills,
                deadline=self.deadline,
                status=status,
                industry=self.selected_industry,
                seniority_level=self.selected_seniority,
                created_at=datetime.datetime.now().strftime("%Y-%m-%d"),
            )
            session.add(new_job)
            session.commit()
        self.is_submitting = False
        yield rx.toast("Job posted successfully!", position="bottom-right")
        yield rx.redirect("/employer/jobs")

    @rx.event
    async def toggle_job_status(self, job_id: str):
        with get_session() as session:
            job = session.exec(select(Job).where(Job.id == job_id)).first()
            if job:
                job.status = "closed" if job.status == "published" else "published"
                session.add(job)
                session.commit()
        yield rx.toast("Status updated", position="bottom-right")

    @rx.event
    async def delete_job(self, job_id: str):
        with get_session() as session:
            job = session.exec(select(Job).where(Job.id == job_id)).first()
            if job:
                session.delete(job)
                session.commit()
        yield rx.toast("Job deleted", position="bottom-right")

    @rx.event
    def set_tab(self, tab: str):
        self.job_tab = tab