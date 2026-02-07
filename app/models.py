import reflex as rx
from typing import TypedDict, Optional, Literal

UserRole = Literal["employer", "applicant"]
JobStatus = Literal["draft", "published", "closed"]
ApplicationStatus = Literal["new", "under_review", "interview", "rejected", "hired"]
SeniorityLevel = Literal["entry", "mid", "senior", "lead", "executive"]


class Company(TypedDict):
    id: str
    name: str
    logo: str
    industry: str
    description: str


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    name: str
    role: UserRole
    company_id: Optional[str]


class Job(TypedDict):
    id: str
    company_id: str
    title: str
    description: str
    location: str
    salary_min: int
    salary_max: int
    required_skills: list[str]
    deadline: str
    status: JobStatus
    industry: str
    seniority_level: SeniorityLevel
    created_at: str


class Application(TypedDict):
    id: str
    job_id: str
    applicant_id: str
    status: ApplicationStatus
    resume_filename: str
    cover_letter: str
    answers: str
    applied_at: str
    applicant_name: Optional[str]
    job_title: Optional[str]
    email: Optional[str]


class ApplicationHistory(TypedDict):
    id: str
    application_id: str
    old_status: str
    new_status: str
    changed_at: str
    notes: str