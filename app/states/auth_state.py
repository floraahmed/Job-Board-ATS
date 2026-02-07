import reflex as rx
from typing import Optional
from app.states.db_state import DbState
from app.models import User
import uuid


class AuthState(rx.State):
    """
    Manages authentication status and current user context.
    """

    current_user: Optional[User] = None
    auth_token: str = ""
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_name: str = ""
    reg_role: str = "applicant"
    reg_company_name: str = ""
    reg_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def is_employer(self) -> bool:
        return self.is_authenticated and self.current_user["role"] == "employer"

    @rx.var
    def is_applicant(self) -> bool:
        return self.is_authenticated and self.current_user["role"] == "applicant"

    @rx.var
    def user_name(self) -> str:
        return self.current_user["name"] if self.current_user else ""

    @rx.var
    def user_initials(self) -> str:
        if not self.current_user:
            return "?"
        name_parts = self.current_user["name"].split()
        if len(name_parts) >= 2:
            return f"{name_parts[0][0]}{name_parts[1][0]}".upper()
        return self.current_user["name"][:2].upper()

    @rx.event
    async def ensure_data_loaded(self):
        """Helper to make sure DB is seeded on app load"""
        db = await self.get_state(DbState)
        db.ensure_seeded()

    @rx.event
    async def login(self):
        db = await self.get_state(DbState)
        db.ensure_seeded()
        self.login_error = ""
        user = next(
            (
                u
                for u in db.users
                if u["email"] == self.login_email
                and u["password_hash"] == self.login_password
            ),
            None,
        )
        if user:
            self.current_user = user
            self.auth_token = str(uuid.uuid4())
            if user["role"] == "employer":
                return rx.redirect("/employer/dashboard")
            else:
                return rx.redirect("/applicant/jobs")
        else:
            self.login_error = "Invalid email or password."

    @rx.event
    async def register(self):
        db = await self.get_state(DbState)
        db.ensure_seeded()
        self.reg_error = ""
        if any((u["email"] == self.reg_email for u in db.users)):
            self.reg_error = "Email already registered."
            return
        company_id = None
        if self.reg_role == "employer":
            if not self.reg_company_name:
                self.reg_error = "Company Name is required for employers."
                return
            company_id = f"comp_{uuid.uuid4().hex[:8]}"
            new_company = {
                "id": company_id,
                "name": self.reg_company_name,
                "logo": "/placeholder.svg",
                "industry": "Unspecified",
                "description": "New company.",
            }
            db.companies.append(new_company)
        new_user = {
            "id": f"user_{uuid.uuid4().hex[:8]}",
            "email": self.reg_email,
            "password_hash": self.reg_password,
            "name": self.reg_name,
            "role": self.reg_role,
            "company_id": company_id,
        }
        db.users.append(new_user)
        self.current_user = new_user
        self.auth_token = str(uuid.uuid4())
        if self.reg_role == "employer":
            return rx.redirect("/employer/dashboard")
        else:
            return rx.redirect("/applicant/jobs")

    @rx.event
    def logout(self):
        self.current_user = None
        self.auth_token = ""
        return rx.redirect("/")

    @rx.event
    def set_reg_role_employer(self):
        self.reg_role = "employer"

    @rx.event
    def set_reg_role_applicant(self):
        self.reg_role = "applicant"