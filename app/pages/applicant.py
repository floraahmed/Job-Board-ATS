import reflex as rx
from app.components.layout import applicant_layout
from app.states.db_state import DbState
from app.states.applicant_jobs_state import ApplicantJobsState
from app.states.application_form_state import ApplicationFormState
from app.states.applicant_state import ApplicantState
from app.models import Job


def job_card(job: Job) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src="/placeholder.svg",
                class_name="h-12 w-12 rounded-lg bg-gray-100 border",
            ),
            rx.el.div(
                rx.el.h3(
                    job["title"], class_name="font-semibold text-gray-900 line-clamp-1"
                ),
                rx.el.p(job["industry"], class_name="text-sm text-gray-500"),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-center gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(job["location"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("banknote", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(
                    f"${job['salary_min']:,} - ${job['salary_max']:,}",
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="space-y-2 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                job["required_skills"].to(list[str]),
                lambda skill: rx.el.span(
                    skill,
                    class_name="px-2 py-1 bg-indigo-50 text-indigo-700 text-xs rounded font-medium",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6 h-12 overflow-hidden",
        ),
        rx.el.button(
            "Quick Apply",
            on_click=lambda: ApplicationFormState.start_application(job["id"]),
            class_name="w-full py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all flex flex-col",
    )


def filter_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Filters", class_name="font-bold text-gray-900 mb-6 flex items-center gap-2"
        ),
        rx.el.div(
            rx.el.label(
                "Industry",
                class_name="block text-xs font-bold text-gray-400 uppercase mb-2",
            ),
            rx.el.select(
                rx.foreach(
                    ApplicantJobsState.industries, lambda i: rx.el.option(i, value=i)
                ),
                on_change=ApplicantJobsState.set_selected_industry,
                value=ApplicantJobsState.selected_industry,
                class_name="w-full p-2 border border-gray-200 rounded-lg text-sm bg-white appearance-none",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Seniority",
                class_name="block text-xs font-bold text-gray-400 uppercase mb-2",
            ),
            rx.el.select(
                rx.el.option("All Levels", value="all"),
                rx.el.option("Entry", value="entry"),
                rx.el.option("Mid", value="mid"),
                rx.el.option("Senior", value="senior"),
                on_change=ApplicantJobsState.set_selected_seniority,
                value=ApplicantJobsState.selected_seniority,
                class_name="w-full p-2 border border-gray-200 rounded-lg text-sm bg-white appearance-none",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.label(
                "Min Salary",
                class_name="block text-xs font-bold text-gray-400 uppercase mb-2",
            ),
            rx.el.input(
                type="number",
                placeholder="e.g. 50000",
                on_change=ApplicantJobsState.set_salary_min_filter,
                class_name="w-full p-2 border border-gray-200 rounded-lg text-sm",
                default_value=ApplicantJobsState.salary_min_filter.to_string(),
            ),
            class_name="mb-8",
        ),
        rx.el.button(
            "Clear Filters",
            on_click=ApplicantJobsState.clear_filters,
            class_name="w-full py-2 text-sm text-gray-500 hover:text-indigo-600 transition-colors",
        ),
        class_name="hidden lg:block w-64 bg-white p-6 rounded-xl border border-gray-100 h-fit sticky top-24",
    )


def application_modal() -> rx.Component:
    return rx.cond(
        ApplicationFormState.is_applying,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-[100]",
                on_click=ApplicationFormState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Apply for Position",
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-5 w-5 text-gray-400"),
                            on_click=ApplicationFormState.close_modal,
                        ),
                        class_name="flex items-center justify-between p-6 border-b",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(
                                [1, 2, 3, 4],
                                lambda i: rx.el.div(
                                    class_name=rx.cond(
                                        ApplicationFormState.step >= i,
                                        "h-1 flex-1 bg-indigo-600",
                                        "h-1 flex-1 bg-gray-200",
                                    )
                                ),
                            ),
                            class_name="flex gap-1 mb-6 px-6 pt-6",
                        ),
                        rx.match(
                            ApplicationFormState.step,
                            (
                                1,
                                rx.el.div(
                                    rx.el.h3(
                                        "Step 1: Introduction",
                                        class_name="font-semibold mb-4",
                                    ),
                                    rx.el.p(
                                        "By applying, you agree to share your profile and details with the hiring team.",
                                        class_name="text-sm text-gray-600 mb-6",
                                    ),
                                    class_name="px-6 pb-6",
                                ),
                            ),
                            (
                                2,
                                rx.el.div(
                                    rx.el.h3(
                                        "Step 2: Resume",
                                        class_name="font-semibold mb-4",
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            rx.icon(
                                                "pen",
                                                class_name="h-8 w-8 text-gray-400 mb-2",
                                            ),
                                            rx.el.p(
                                                "Click to upload resume",
                                                class_name="text-sm text-gray-600",
                                            ),
                                            rx.el.span(
                                                ApplicationFormState.resume_filename,
                                                class_name="text-xs text-indigo-600 font-bold mt-2",
                                            ),
                                            rx.upload.root(
                                                id="resume_upload",
                                                on_drop=ApplicationFormState.handle_resume_upload,
                                                multiple=False,
                                            ),
                                            class_name="border-2 border-dashed border-gray-300 rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-indigo-500 transition-colors",
                                        )
                                    ),
                                    class_name="px-6 pb-6",
                                ),
                            ),
                            (
                                3,
                                rx.el.div(
                                    rx.el.h3(
                                        "Step 3: Cover Letter",
                                        class_name="font-semibold mb-4",
                                    ),
                                    rx.el.textarea(
                                        placeholder="Why are you a good fit for this role?",
                                        on_change=ApplicationFormState.set_cover_letter,
                                        class_name="w-full h-48 p-4 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none",
                                    ),
                                    class_name="px-6 pb-6",
                                ),
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Step 4: Review", class_name="font-semibold mb-4"
                                ),
                                rx.el.p(
                                    "Please confirm all details before submitting.",
                                    class_name="text-sm text-gray-600",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        f"Resume: {ApplicationFormState.resume_filename}",
                                        class_name="text-sm font-medium",
                                    ),
                                    class_name="mt-4 bg-gray-50 p-4 rounded-lg",
                                ),
                                class_name="px-6 pb-6",
                            ),
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Back",
                            on_click=ApplicationFormState.prev_step,
                            class_name=rx.cond(
                                ApplicationFormState.step > 1,
                                "px-6 py-2 border rounded-lg hover:bg-gray-50 font-medium",
                                "hidden",
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                ApplicationFormState.step < 4,
                                "Next",
                                "Submit Application",
                            ),
                            on_click=rx.cond(
                                ApplicationFormState.step < 4,
                                ApplicationFormState.next_step,
                                ApplicationFormState.submit_application,
                            ),
                            class_name="ml-auto px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium",
                        ),
                        class_name="flex p-6 border-t",
                    ),
                    class_name="bg-white w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[110] w-full p-4",
            ),
        ),
        rx.fragment(),
    )


def browse_jobs_page() -> rx.Component:
    return applicant_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Explore Opportunities",
                        class_name="text-3xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Find a role that matches your skills and passions",
                        class_name="text-gray-500 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search job title, skills...",
                            on_change=ApplicantJobsState.set_search_query,
                            class_name="w-full pl-12 pr-4 py-4 rounded-2xl border-none shadow-sm ring-1 ring-gray-200 focus:ring-2 focus:ring-indigo-600 outline-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="mb-10",
                ),
                rx.el.div(
                    filter_sidebar(),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                rx.el.span(
                                    ApplicantJobsState.filtered_jobs.length().to_string(),
                                    class_name="font-bold text-gray-900",
                                ),
                                " jobs found matching your criteria",
                                class_name="text-sm text-gray-500 mb-6",
                            ),
                            rx.el.div(
                                rx.foreach(ApplicantJobsState.filtered_jobs, job_card),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                            ),
                            rx.cond(
                                ApplicantJobsState.filtered_jobs.length() == 0,
                                rx.el.div(
                                    rx.icon(
                                        "search-x",
                                        class_name="h-12 w-12 text-gray-200 mb-4",
                                    ),
                                    rx.el.p(
                                        "No jobs found. Try adjusting your filters.",
                                        class_name="text-gray-500",
                                    ),
                                    class_name="py-20 flex flex-col items-center justify-center",
                                ),
                            ),
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex flex-col lg:flex-row gap-8",
                ),
            ),
            application_modal(),
            class_name="max-w-7xl mx-auto",
        )
    )


def application_list_item(app: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    app["job_title"].to(str), class_name="font-bold text-gray-900"
                ),
                rx.el.p(
                    app["company_name"].to(str), class_name="text-sm text-gray-500"
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    app["status"].to(str).replace("_", " ").capitalize(),
                    class_name=rx.match(
                        app["status"].to(str),
                        (
                            "new",
                            "px-2 py-1 text-xs font-bold bg-blue-100 text-blue-700 rounded-full",
                        ),
                        (
                            "under_review",
                            "px-2 py-1 text-xs font-bold bg-yellow-100 text-yellow-700 rounded-full",
                        ),
                        (
                            "interview",
                            "px-2 py-1 text-xs font-bold bg-purple-100 text-purple-700 rounded-full",
                        ),
                        (
                            "hired",
                            "px-2 py-1 text-xs font-bold bg-green-100 text-green-700 rounded-full",
                        ),
                        "px-2 py-1 text-xs font-bold bg-red-100 text-red-700 rounded-full",
                    ),
                )
            ),
            class_name="flex items-start justify-between mb-4",
        ),
        rx.el.div(
            rx.el.p(
                f"Applied: {app['applied_at'].to(str)}",
                class_name="text-xs text-gray-400",
            ),
            rx.el.button(
                "View Status",
                on_click=lambda: ApplicantState.set_selected_app(app["id"].to(str)),
                class_name="text-sm font-semibold text-indigo-600 hover:text-indigo-700",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all cursor-pointer",
        on_click=lambda: ApplicantState.set_selected_app(app["id"].to(str)),
    )


def application_detail_side() -> rx.Component:
    return rx.cond(
        ApplicantState.selected_app_id != "",
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-[80]",
                on_click=ApplicantState.close_detail,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Application Details",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6"),
                            on_click=ApplicantState.close_detail,
                        ),
                        class_name="flex justify-between items-center mb-8",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            ApplicantState.selected_app["job_title"],
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            ApplicantState.selected_app["company_name"],
                            class_name="text-gray-500 mb-4",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Current Status:",
                                class_name="text-sm text-gray-400 mr-2",
                            ),
                            rx.el.span(
                                ApplicantState.selected_app["status"]
                                .to(str)
                                .replace("_", " ")
                                .capitalize(),
                                class_name="font-bold text-indigo-600",
                            ),
                            class_name="mb-8 p-4 bg-indigo-50 rounded-xl",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Status Timeline",
                            class_name="text-sm font-bold text-gray-400 uppercase mb-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ApplicantState.selected_app_history,
                                lambda h: rx.el.div(
                                    rx.el.div(
                                        class_name="h-2 w-2 rounded-full bg-indigo-600 mr-4 mt-1.5 flex-shrink-0"
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            h["notes"],
                                            class_name="text-sm font-semibold text-gray-900",
                                        ),
                                        rx.el.p(
                                            h["changed_at"],
                                            class_name="text-xs text-gray-400",
                                        ),
                                        class_name="pb-6",
                                    ),
                                    class_name="flex",
                                ),
                            ),
                            class_name="ml-1",
                        ),
                    ),
                    class_name="h-full overflow-y-auto p-8",
                ),
                class_name="fixed right-0 top-0 bottom-0 w-full max-w-lg bg-white shadow-2xl z-[90] animate-slide-in-right",
            ),
        ),
        rx.fragment(),
    )


def my_applications_page() -> rx.Component:
    return applicant_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "My Applications", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Track your journey with top companies",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        [
                            "all",
                            "new",
                            "under_review",
                            "interview",
                            "hired",
                            "rejected",
                        ],
                        lambda s: rx.el.button(
                            s.replace("_", " ").capitalize(),
                            on_click=lambda: ApplicantState.set_status_filter(s),
                            class_name=rx.cond(
                                ApplicantState.status_filter == s,
                                "px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-bold",
                                "px-4 py-2 bg-white text-gray-500 hover:text-indigo-600 rounded-lg text-sm font-medium border",
                            ),
                        ),
                    ),
                    class_name="flex flex-wrap gap-2 mb-8",
                ),
                rx.el.div(
                    rx.foreach(
                        ApplicantState.my_applications,
                        lambda app: application_list_item(app.to(dict[str, str])),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.cond(
                    ApplicantState.my_applications.length() == 0,
                    rx.el.div(
                        rx.icon("file-text", class_name="h-12 w-12 text-gray-200 mb-4"),
                        rx.el.p(
                            "You haven't applied to any jobs yet.",
                            class_name="text-gray-500",
                        ),
                        rx.el.a(
                            "Browse Jobs",
                            href="/applicant/jobs",
                            class_name="mt-4 text-indigo-600 font-bold hover:underline",
                        ),
                        class_name="py-20 flex flex-col items-center justify-center",
                    ),
                ),
            ),
            application_detail_side(),
            class_name="max-w-7xl mx-auto",
        )
    )