import reflex as rx
from app.components.layout import base_layout
from app.pages.auth import login_page, register_page
from app.pages.employer import dashboard_page
from app.pages.employer_jobs import job_form_page, job_listing_page, job_detail_page
from app.pages.applicant import browse_jobs_page, my_applications_page
from app.pages.ats import ats_page
from app.pages.employer_applications import all_applications_page
from app.pages.employer_company import company_profile_page
from app.pages.applicant_profile import applicant_profile_page
from app.states.auth_state import AuthState
from app.states.ats_state import ATSState
from app.states.company_state import CompanyState
from app.states.applicant_profile_state import ApplicantProfileState


def index() -> rx.Component:
    """Landing page"""
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    rx.el.span("Find the job that ", class_name="text-gray-900"),
                    rx.el.span("fits your life", class_name="text-indigo-600"),
                    class_name="text-4xl md:text-6xl font-bold tracking-tight text-center mb-6",
                ),
                rx.el.p(
                    "Connecting the best talent with top companies. Join thousands of job seekers and employers today.",
                    class_name="text-lg md:text-xl text-gray-600 text-center max-w-2xl mx-auto mb-10",
                ),
                rx.el.div(
                    rx.el.a(
                        "Find a Job",
                        href="/register",
                        class_name="px-8 py-4 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-all shadow-lg hover:shadow-indigo-200",
                    ),
                    rx.el.a(
                        "Post a Job",
                        href="/register",
                        class_name="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-xl font-semibold hover:bg-gray-50 transition-all",
                    ),
                    class_name="flex flex-col sm:flex-row gap-4 justify-center",
                ),
                class_name="py-20 md:py-32 px-4",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=AuthState.ensure_data_loaded)
app.add_page(login_page, route="/login", on_load=AuthState.ensure_data_loaded)
app.add_page(register_page, route="/register", on_load=AuthState.ensure_data_loaded)
app.add_page(
    dashboard_page, route="/employer/dashboard", on_load=AuthState.ensure_data_loaded
)
app.add_page(
    job_listing_page, route="/employer/jobs", on_load=AuthState.ensure_data_loaded
)
app.add_page(
    job_form_page, route="/employer/jobs/create", on_load=AuthState.ensure_data_loaded
)
app.add_page(
    job_detail_page,
    route="/employer/jobs/[job_id]",
    on_load=AuthState.ensure_data_loaded,
)
app.add_page(
    ats_page,
    route="/employer/jobs/[job_id]/applications",
    on_load=[AuthState.ensure_data_loaded, ATSState.load_job_data],
)
app.add_page(
    all_applications_page,
    route="/employer/applications",
    on_load=AuthState.ensure_data_loaded,
)
app.add_page(
    company_profile_page,
    route="/employer/company",
    on_load=[AuthState.ensure_data_loaded, CompanyState.load_company],
)
app.add_page(
    browse_jobs_page, route="/applicant/jobs", on_load=AuthState.ensure_data_loaded
)
app.add_page(
    my_applications_page,
    route="/applicant/applications",
    on_load=AuthState.ensure_data_loaded,
)
app.add_page(
    applicant_profile_page,
    route="/applicant/profile",
    on_load=[AuthState.ensure_data_loaded, ApplicantProfileState.load_profile],
)