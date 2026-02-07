import reflex as rx
from typing import Optional
import uuid
import datetime
from app.models import Notification as NotificationDict
from app.database.models import Notification
from app.states.auth_state import AuthState
from app.database.connection import get_session
from sqlmodel import select, col


class NotificationState(rx.State):
    show_notifications: bool = False

    @rx.var
    async def my_notifications(self) -> list[NotificationDict]:
        auth = await self.get_state(AuthState)
        if not auth.current_user:
            return []
        with get_session() as session:
            notes = session.exec(
                select(Notification)
                .where(Notification.user_id == auth.current_user["id"])
                .order_by(col(Notification.created_at).desc())
            ).all()
            return [n.model_dump() for n in notes]

    @rx.var
    async def unread_count(self) -> int:
        notes = await self.my_notifications
        return len([n for n in notes if not n["is_read"]])

    @rx.event
    def toggle_notifications(self):
        self.show_notifications = not self.show_notifications

    @rx.event
    async def mark_as_read(self, note_id: str):
        with get_session() as session:
            note = session.exec(
                select(Notification).where(Notification.id == note_id)
            ).first()
            if note:
                note.is_read = True
                session.add(note)
                session.commit()

    @rx.event
    async def mark_all_read(self):
        auth = await self.get_state(AuthState)
        if auth.current_user:
            with get_session() as session:
                notes = session.exec(
                    select(Notification).where(
                        Notification.user_id == auth.current_user["id"],
                        Notification.is_read == False,
                    )
                ).all()
                for n in notes:
                    n.is_read = True
                    session.add(n)
                session.commit()

    @rx.event
    async def add_notification(
        self, user_id: str, title: str, message: str, n_type: str = "info"
    ):
        with get_session() as session:
            new_note = Notification(
                id=f"note_{uuid.uuid4().hex[:8]}",
                user_id=user_id,
                title=title,
                message=message,
                type=n_type,
                is_read=False,
                created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            session.add(new_note)
            session.commit()
        auth = await self.get_state(AuthState)
        if auth.current_user and auth.current_user["id"] == user_id:
            yield rx.toast(f"{title}: {message}", position="top-right")