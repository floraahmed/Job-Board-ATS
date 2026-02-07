import reflex as rx
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Any
from sqlalchemy import Column, JSON
import datetime
import uuid


class Company(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    logo: str = "/placeholder.svg"
    industry: str
    description: str
    users: list["User"] = Relationship(back_populates="company")
    jobs: list["Job"] = Relationship(back_populates="company")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(index=True)
    password_hash: str
    name: str
    role: str
    company_id: Optional[str] = Field(default=None, foreign_key="company.id")
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: list[str] = Field(default=[], sa_column=Column(JSON))
    resume: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    company: Optional[Company] = Relationship(back_populates="users")
    applications: list["Application"] = Relationship(back_populates="applicant")
    notifications: list["Notification"] = Relationship(back_populates="user")


class Job(SQLModel, table=True):
    id: str = Field(primary_key=True)
    company_id: str = Field(foreign_key="company.id")
    title: str
    description: str
    location: str
    salary_min: int
    salary_max: int
    required_skills: list[str] = Field(default=[], sa_column=Column(JSON))
    deadline: str
    status: str
    industry: str
    seniority_level: str
    created_at: str
    company: Optional[Company] = Relationship(back_populates="jobs")
    applications: list["Application"] = Relationship(back_populates="job")


class Application(SQLModel, table=True):
    id: str = Field(primary_key=True)
    job_id: str = Field(foreign_key="job.id")
    applicant_id: str = Field(foreign_key="user.id")
    status: str
    resume_filename: str
    cover_letter: str
    answers: str
    applied_at: str
    job: Optional[Job] = Relationship(back_populates="applications")
    applicant: Optional[User] = Relationship(back_populates="applications")
    history: list["ApplicationHistory"] = Relationship(back_populates="application")


class ApplicationHistory(SQLModel, table=True):
    id: str = Field(primary_key=True)
    application_id: str = Field(foreign_key="application.id")
    old_status: str
    new_status: str
    changed_at: str
    notes: str
    application: Optional[Application] = Relationship(back_populates="history")


class Notification(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str
    message: str
    type: str = "info"
    is_read: bool = False
    created_at: str
    user: Optional[User] = Relationship(back_populates="notifications")