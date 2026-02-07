import reflex as rx
from app.models import Company, User, Job, Application, ApplicationHistory
import random
import datetime
from faker import Faker

fake = Faker()


class DbState(rx.State):
    """
    Simulates a database.
    In a real app, this would be your database connection.
    For this demo, we hold lists of TypedDicts in memory.
    """

    companies: list[Company] = []
    users: list[User] = []
    jobs: list[Job] = []
    applications: list[Application] = []
    history: list[ApplicationHistory] = []
    _is_seeded: bool = False

    @rx.event
    def ensure_seeded(self):
        if self._is_seeded:
            return
        self.seed_data()
        self._is_seeded = True

    @rx.event
    def seed_data(self):
        tech_industries = ["Software", "FinTech", "HealthTech"]
        company_names = ["Acme Corp", "Globex", "Soylent Corp"]
        for i, name in enumerate(company_names):
            comp_id = f"comp_{i + 1}"
            self.companies.append(
                {
                    "id": comp_id,
                    "name": name,
                    "logo": f"/placeholder.svg",
                    "industry": tech_industries[i],
                    "description": fake.catch_phrase() + " " + fake.bs(),
                }
            )
        self.users.append(
            {
                "id": "user_emp_1",
                "email": "employer@acme.com",
                "password_hash": "password",
                "name": "Alice Manager",
                "role": "employer",
                "company_id": "comp_1",
            }
        )
        self.users.append(
            {
                "id": "user_app_1",
                "email": "applicant@gmail.com",
                "password_hash": "password",
                "name": "Bob Developer",
                "role": "applicant",
                "company_id": None,
            }
        )
        job_titles = [
            "Backend Engineer",
            "Frontend Developer",
            "Product Manager",
            "Data Scientist",
        ]
        statuses = ["published", "draft", "closed", "published"]
        for i in range(6):
            comp = self.companies[i % len(self.companies)]
            self.jobs.append(
                {
                    "id": f"job_{i + 1}",
                    "company_id": comp["id"],
                    "title": f"{random.choice(['Senior', 'Junior', 'Lead'])} {random.choice(job_titles)}",
                    "description": fake.paragraph(nb_sentences=5),
                    "location": fake.city(),
                    "salary_min": random.randint(60000, 90000),
                    "salary_max": random.randint(100000, 160000),
                    "required_skills": random.sample(
                        ["Python", "React", "SQL", "AWS", "Docker"], 3
                    ),
                    "deadline": (
                        datetime.datetime.now()
                        + datetime.timedelta(days=random.randint(10, 60))
                    ).strftime("%Y-%m-%d"),
                    "status": statuses[i % len(statuses)],
                    "industry": comp["industry"],
                    "seniority_level": random.choice(["entry", "mid", "senior"]),
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
                }
            )
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
            self.users.append(
                {
                    "id": user_id,
                    "email": f"{fname.lower()}.{lname.lower()}{i}@example.com",
                    "password_hash": "password",
                    "name": f"{fname} {lname}",
                    "role": "applicant",
                    "company_id": None,
                }
            )
            job = random.choice(self.jobs)
            status = random.choice(
                ["new", "under_review", "interview", "rejected", "hired"]
            )
            app_id = f"app_{i + 10}"
            self.applications.append(
                {
                    "id": app_id,
                    "job_id": job["id"],
                    "applicant_id": user_id,
                    "status": status,
                    "resume_filename": f"{lname}_resume.pdf",
                    "cover_letter": fake.paragraph(nb_sentences=3),
                    "answers": fake.sentence(),
                    "applied_at": (
                        datetime.datetime.now()
                        - datetime.timedelta(days=random.randint(0, 60))
                    ).strftime("%Y-%m-%d"),
                }
            )
            if status != "new":
                self.history.append(
                    {
                        "id": f"hist_{i}",
                        "application_id": app_id,
                        "old_status": "new",
                        "new_status": status,
                        "changed_at": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "notes": "Status update",
                    }
                )