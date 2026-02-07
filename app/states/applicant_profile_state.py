import reflex as rx
from typing import Optional
from app.states.auth_state import AuthState
from app.database.models import User
from app.database.connection import get_session
from sqlmodel import select


class ApplicantProfileState(rx.State):
    temp_name: str = ""
    temp_phone: str = ""
    temp_location: str = ""
    temp_bio: str = ""
    temp_skills: list[str] = []
    new_skill: str = ""
    temp_experience: str = ""
    temp_education: str = ""
    is_saving: bool = False

    @rx.event
    async def load_profile(self):
        auth = await self.get_state(AuthState)
        if auth.current_user:
            user = auth.current_user
            self.temp_name = user["name"]
            self.temp_phone = user.get("phone") or ""
            self.temp_location = user.get("location") or ""
            self.temp_bio = user.get("bio") or ""
            self.temp_skills = user.get("skills") or []
            self.temp_experience = user.get("experience") or ""
            self.temp_education = user.get("education") or ""

    @rx.event
    def add_skill(self):
        if self.new_skill and self.new_skill not in self.temp_skills:
            self.temp_skills.append(self.new_skill)
            self.new_skill = ""

    @rx.event
    def remove_skill(self, skill: str):
        self.temp_skills = [s for s in self.temp_skills if s != skill]

    @rx.event
    async def save_profile(self):
        self.is_saving = True
        auth = await self.get_state(AuthState)
        uid = auth.current_user["id"]
        with get_session() as session:
            user = session.exec(select(User).where(User.id == uid)).first()
            if user:
                user.name = self.temp_name
                user.phone = self.temp_phone
                user.location = self.temp_location
                user.bio = self.temp_bio
                user.skills = self.temp_skills
                user.experience = self.temp_experience
                user.education = self.temp_education
                session.add(user)
                session.commit()
                session.refresh(user)
                auth.current_user = user.model_dump()
        self.is_saving = False
        yield rx.toast("Profile updated", position="bottom-right")