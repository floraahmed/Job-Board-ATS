from sqlmodel import Session, select
from app.database.models import (
    Company,
    User,
    Job,
    Application,
    ApplicationHistory,
    Notification,
)
from app.database.connection import engine
from faker import Faker
import random
import datetime
import uuid

fake = Faker()


def seed_database():
    with Session(engine) as session:
        if session.exec(select(User)).first():
            return
        print("Seeding database...")
        tech_industries = ["Software", "FinTech", "HealthTech"]
        company_names = ["Acme Corp", "Globex", "Soylent Corp"]
        companies = []
        for i, name in enumerate(company_names):
            comp = Company(
                id=f"comp_{i + 1}",
                name=name,
                logo="/placeholder.svg",
                industry=tech_industries[i],
                description=fake.catch_phrase() + " " + fake.bs(),
            )
            session.add(comp)
            companies.append(comp)
        session.commit()
        emp = User(
            id="user_emp_1",
            email="employer@acme.com",
            password_hash="password",
            name="Alice Manager",
            role="employer",
            company_id="comp_1",
            skills=[],
        )
        session.add(emp)
        app_user = User(
            id="user_app_1",
            email="applicant@gmail.com",
            password_hash="password",
            name="Bob Developer",
            role="applicant",
            company_id=None,
            skills=["Python", "Reflex"],
        )
        session.add(app_user)
        job_titles = [
            "Backend Engineer",
            "Frontend Developer",
            "Product Manager",
            "Data Scientist",
        ]
        statuses = ["published", "draft", "closed", "published"]
        jobs = []
        for i in range(6):
            comp = companies[i % len(companies)]
            job = Job(
                id=f"job_{i + 1}",
                company_id=comp.id,
                title=f"{random.choice(['Senior', 'Junior', 'Lead'])} {random.choice(job_titles)}",
                description=fake.paragraph(nb_sentences=5),
                location=fake.city(),
                salary_min=random.randint(60000, 90000),
                salary_max=random.randint(100000, 160000),
                required_skills=random.sample(
                    ["Python", "React", "SQL", "AWS", "Docker"], 3
                ),
                deadline=(
                    datetime.datetime.now()
                    + datetime.timedelta(days=random.randint(10, 60))
                ).strftime("%Y-%m-%d"),
                status=statuses[i % len(statuses)],
                industry=comp.industry,
                seniority_level=random.choice(["entry", "mid", "senior"]),
                created_at=datetime.datetime.now().strftime("%Y-%m-%d"),
            )
            session.add(job)
            jobs.append(job)
        session.commit()
        first_names = [
            "John",
            "Jane",
            "Bob",
            "Alice",
            "Charlie",
            "Diana",
            "Evan",
            "Fiona",
        ]
        last_names = [
            "Smith",
            "Doe",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Miller",
            "Davis",
        ]
        for i in range(20):
            user_id = f"user_app_{i + 10}"
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            applicant = User(
                id=user_id,
                email=f"{fname.lower()}.{lname.lower()}{i}@example.com",
                password_hash="password",
                name=f"{fname} {lname}",
                role="applicant",
                company_id=None,
                skills=random.sample(["Python", "Java", "C++", "JavaScript"], 2),
            )
            session.add(applicant)
            job = random.choice(jobs)
            status = random.choice(
                ["new", "under_review", "interview", "rejected", "hired"]
            )
            app_id = f"app_{i + 10}"
            application = Application(
                id=app_id,
                job_id=job.id,
                applicant_id=user_id,
                status=status,
                resume_filename=f"{lname}_resume.pdf",
                cover_letter=fake.paragraph(nb_sentences=3),
                answers=fake.sentence(),
                applied_at=(
                    datetime.datetime.now()
                    - datetime.timedelta(days=random.randint(0, 60))
                ).strftime("%Y-%m-%d"),
            )
            session.add(application)
            if status != "new":
                history = ApplicationHistory(
                    id=f"hist_{i}",
                    application_id=app_id,
                    old_status="new",
                    new_status=status,
                    changed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    notes="Status update",
                )
                session.add(history)
        session.commit()
        print("Seeding complete.")