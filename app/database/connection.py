from sqlmodel import create_engine, SQLModel, Session
import reflex as rx

DATABASE_URL = "sqlite:///job_portal.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)