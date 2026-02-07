import reflex as rx
from typing import Optional
import uuid
import datetime
from app.models import Notification
from app.states.db_state import DbState
from app.states.auth_state import AuthState


class NotificationState(rx.State):
    show_notifications: bool = False

    @rx.var
    async def my_notifications(self) -> list[Notification]:
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if not auth.current_user:
            return []
        return sorted(
            [n for n in db.notifications if n["user_id"] == auth.current_user["id"]],
            key=lambda x: x["created_at"],
            reverse=True,
        )

    @rx.var
    async def unread_count(self) -> int:
        notes = await self.my_notifications
        return len([n for n in notes if not n["is_read"]])

    @rx.event
    def toggle_notifications(self):
        self.show_notifications = not self.show_notifications

    @rx.event
    async def mark_as_read(self, note_id: str):
        db = await self.get_state(DbState)
        for n in db.notifications:
            if n["id"] == note_id:
                n["is_read"] = True
                break

    @rx.event
    async def mark_all_read(self):
        db = await self.get_state(DbState)
        auth = await self.get_state(AuthState)
        if auth.current_user:
            for n in db.notifications:
                if n["user_id"] == auth.current_user["id"]:
                    n["is_read"] = True

    @rx.event
    async def add_notification(
        self, user_id: str, title: str, message: str, n_type: str = "info"
    ):
        db = await self.get_state(DbState)
        new_note: Notification = {
            "id": f"note_{uuid.uuid4().hex[:8]}",
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": n_type,
            "is_read": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        db.notifications.append(new_note)
        auth = await self.get_state(AuthState)
        if auth.current_user and auth.current_user["id"] == user_id:
            yield rx.toast(f"{title}: {message}", position="top-right")