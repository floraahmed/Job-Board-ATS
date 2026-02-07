import reflex as rx
from typing import Optional
from app.states.db_state import DbState
from app.states.auth_state import AuthState


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
            self.temp_phone = user.get("phone", "")
            self.temp_location = user.get("location", "")
            self.temp_bio = user.get("bio", "")
            self.temp_skills = user.get("skills", [])
            self.temp_experience = user.get("experience", "")
            self.temp_education = user.get("education", "")

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
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        uid = auth.current_user["id"]
        for i, u in enumerate(db.users):
            if u["id"] == uid:
                db.users[i].update(
                    {
                        "name": self.temp_name,
                        "phone": self.temp_phone,
                        "location": self.temp_location,
                        "bio": self.temp_bio,
                        "skills": self.temp_skills,
                        "experience": self.temp_experience,
                        "education": self.temp_education,
                    }
                )
                auth.current_user = db.users[i]
                break
        self.is_saving = False
        yield rx.toast("Profile updated", position="bottom-right")