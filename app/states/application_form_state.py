import reflex as rx
from typing import Optional
import uuid
import datetime
from app.states.db_state import DbState
from app.states.auth_state import AuthState
from app.models import Application, ApplicationHistory


class ApplicationFormState(rx.State):
    step: int = 1
    form_job_id: str = ""
    resume_filename: str = ""
    cover_letter: str = ""
    screening_answers: str = ""
    is_applying: bool = False

    @rx.event
    def start_application(self, job_id: str):
        self.form_job_id = job_id
        self.step = 1
        self.resume_filename = ""
        self.cover_letter = ""
        self.screening_answers = ""
        self.is_applying = True

    @rx.event
    def next_step(self):
        self.step += 1

    @rx.event
    def prev_step(self):
        self.step -= 1

    @rx.event
    async def handle_resume_upload(self, files: list[rx.UploadFile]):
        for file in files:
            self.resume_filename = file.name
        yield rx.toast(
            f"File {self.resume_filename} uploaded (simulated)", position="bottom-right"
        )

    @rx.event
    async def submit_application(self):
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        from app.states.notification_state import NotificationState

        notes = await self.get_state(NotificationState)
        if not auth.current_user:
            yield rx.toast("Please login to apply", position="bottom-right")
            return
        app_id = f"app_{uuid.uuid4().hex[:8]}"
        new_app: Application = {
            "id": app_id,
            "job_id": self.form_job_id,
            "applicant_id": auth.current_user["id"],
            "status": "new",
            "resume_filename": self.resume_filename or "simulated_resume.pdf",
            "cover_letter": self.cover_letter,
            "answers": self.screening_answers,
            "applied_at": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        db.applications.append(new_app)
        history_entry: ApplicationHistory = {
            "id": f"hist_{uuid.uuid4().hex[:8]}",
            "application_id": app_id,
            "old_status": "none",
            "new_status": "new",
            "changed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "notes": "Application submitted by candidate.",
        }
        db.history.append(history_entry)
        job = next((j for j in db.jobs if j["id"] == self.form_job_id), None)
        if job:
            employer = next(
                (
                    u
                    for u in db.users
                    if u["company_id"] == job["company_id"] and u["role"] == "employer"
                ),
                None,
            )
            if employer:
                await notes.add_notification(
                    employer["id"],
                    "New Application",
                    f"You received a new application for '{job['title']}' from {auth.user_name}.",
                    "success",
                )
        self.is_applying = False
        yield rx.toast("Application submitted successfully!", position="bottom-right")
        yield rx.redirect("/applicant/applications")

    @rx.event
    def close_modal(self):
        self.is_applying = False