import reflex as rx
from app.database.seed import seed_database
from app.database.models import Job
from app.database.connection import get_session
from sqlmodel import select
from app.models import Job as JobDict


class DbState(rx.State):
    """
    Wrapper for DB operations that used to hold memory state.
    Now mainly used to trigger seeding if needed.
    """

    _is_seeded: bool = False

    @rx.var
    def jobs(self) -> list[JobDict]:
        with get_session() as session:
            jobs = session.exec(select(Job).limit(5)).all()
            return [j.model_dump() for j in jobs]

    @rx.event
    def ensure_seeded(self):
        if self._is_seeded:
            return
        seed_database()
        self._is_seeded = True