import reflex as rx
from app.components.layout import employer_layout
from app.states.jobs_state import JobsState
from app.states.db_state import DbState


def job_form_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Create Job Posting", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Fill in the details for the new role", class_name="text-gray-500"
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Job Title",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. Senior Software Engineer",
                            on_change=JobsState.set_job_title,
                            class_name="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Industry",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    JobsState.industries,
                                    lambda ind: rx.el.option(ind, value=ind),
                                ),
                                on_change=JobsState.set_selected_industry,
                                class_name="w-full px-4 py-2 border rounded-lg appearance-none bg-white",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Seniority",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    JobsState.seniority_levels,
                                    lambda level: rx.el.option(level, value=level),
                                ),
                                on_change=JobsState.set_selected_seniority,
                                class_name="w-full px-4 py-2 border rounded-lg appearance-none bg-white",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Location",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                placeholder="Remote, New York, etc.",
                                on_change=JobsState.set_job_location,
                                class_name="w-full px-4 py-2 border rounded-lg",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Application Deadline",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="date",
                                on_change=JobsState.set_deadline,
                                class_name="w-full px-4 py-2 border rounded-lg",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Salary Min ($)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                on_change=JobsState.set_salary_min,
                                class_name="w-full px-4 py-2 border rounded-lg",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Salary Max ($)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                on_change=JobsState.set_salary_max,
                                class_name="w-full px-4 py-2 border rounded-lg",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Required Skills",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Press Add to include skill",
                                on_change=JobsState.set_new_skill,
                                class_name="flex-1 px-4 py-2 border rounded-lg rounded-r-none border-r-0",
                                default_value=JobsState.new_skill,
                            ),
                            rx.el.button(
                                "Add",
                                on_click=JobsState.add_skill,
                                class_name="px-4 py-2 bg-indigo-50 text-indigo-600 border border-indigo-200 rounded-r-lg font-medium",
                            ),
                            class_name="flex mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                JobsState.selected_skills,
                                lambda s: rx.el.span(
                                    s,
                                    rx.el.button(
                                        rx.icon("x", class_name="h-3 w-3"),
                                        on_click=lambda: JobsState.remove_skill(s),
                                        class_name="ml-1",
                                    ),
                                    class_name="inline-flex items-center px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-sm mr-2 mb-2",
                                ),
                            ),
                            class_name="flex flex-wrap",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Job Description",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.textarea(
                            placeholder="Enter detailed job description, responsibilities, etc.",
                            on_change=JobsState.set_job_description,
                            class_name="w-full px-4 py-2 border rounded-lg h-40",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Save as Draft",
                            on_click=lambda: JobsState.save_job("draft"),
                            disabled=JobsState.is_submitting,
                            class_name="px-6 py-2 border border-gray-300 rounded-lg font-medium hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Publish Job",
                            on_click=lambda: JobsState.save_job("published"),
                            disabled=JobsState.is_submitting,
                            class_name="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700",
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="bg-white p-8 rounded-xl border shadow-sm",
                ),
                class_name="max-w-4xl",
            ),
        )
    )


def job_listing_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Job Postings", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Manage your company's open roles", class_name="text-gray-500"
                    ),
                ),
                rx.el.a(
                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                    "Create New Job",
                    href="/employer/jobs/create",
                    class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center",
                ),
                class_name="flex justify-between items-end mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            ["all", "active", "draft", "closed"],
                            lambda t: rx.el.button(
                                t.capitalize(),
                                on_click=lambda: JobsState.set_tab(t),
                                class_name=rx.cond(
                                    JobsState.job_tab == t,
                                    "px-4 py-2 text-sm font-bold border-b-2 border-indigo-600 text-indigo-600",
                                    "px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700",
                                ),
                            ),
                        ),
                        class_name="flex gap-4 border-b border-gray-100 mb-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search jobs...",
                            on_change=JobsState.set_search_query,
                            class_name="pl-9 pr-4 py-2 border rounded-lg text-sm w-full max-w-xs",
                        ),
                        class_name="relative mb-6",
                    ),
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Job Title",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Applicants",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Deadline",
                                    class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                JobsState.employer_jobs,
                                lambda job: rx.el.tr(
                                    rx.el.td(
                                        rx.el.div(
                                            rx.el.p(
                                                job["title"],
                                                class_name="font-semibold text-gray-900",
                                            ),
                                            rx.el.p(
                                                job["location"],
                                                class_name="text-xs text-gray-500",
                                            ),
                                        ),
                                        class_name="px-6 py-4",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            job["status"],
                                            class_name=rx.match(
                                                job["status"],
                                                (
                                                    "published",
                                                    "px-2 py-1 text-xs font-bold bg-green-100 text-green-700 rounded-full capitalize",
                                                ),
                                                (
                                                    "draft",
                                                    "px-2 py-1 text-xs font-bold bg-gray-100 text-gray-700 rounded-full capitalize",
                                                ),
                                                "px-2 py-1 text-xs font-bold bg-red-100 text-red-700 rounded-full capitalize",
                                            ),
                                        ),
                                        class_name="px-6 py-4",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            "0", class_name="text-sm text-gray-600"
                                        ),
                                        class_name="px-6 py-4",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            job["deadline"],
                                            class_name="text-sm text-gray-600",
                                        ),
                                        class_name="px-6 py-4",
                                    ),
                                    rx.el.td(
                                        rx.el.div(
                                            rx.el.a(
                                                rx.icon(
                                                    "eye",
                                                    class_name="h-4 w-4 text-gray-400 hover:text-indigo-600",
                                                ),
                                                href=f"/employer/jobs/{job['id']}",
                                            ),
                                            rx.el.button(
                                                rx.icon(
                                                    "power",
                                                    class_name="h-4 w-4 text-gray-400 hover:text-red-600",
                                                ),
                                                on_click=lambda: JobsState.toggle_job_status(
                                                    job["id"]
                                                ),
                                            ),
                                            rx.el.button(
                                                rx.icon(
                                                    "trash",
                                                    class_name="h-4 w-4 text-gray-400 hover:text-red-600",
                                                ),
                                                on_click=lambda: JobsState.delete_job(
                                                    job["id"]
                                                ),
                                            ),
                                            class_name="flex justify-end gap-3",
                                        ),
                                        class_name="px-6 py-4 text-right",
                                    ),
                                    class_name="border-b border-gray-100 hover:bg-gray-50",
                                ),
                            )
                        ),
                        class_name="w-full table-auto",
                    ),
                    rx.cond(
                        JobsState.employer_jobs.length() == 0,
                        rx.el.div(
                            rx.icon(
                                "file-search", class_name="h-12 w-12 text-gray-200 mb-4"
                            ),
                            rx.el.p(
                                "No jobs found matching your criteria.",
                                class_name="text-gray-500",
                            ),
                            class_name="py-20 flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="bg-white border rounded-xl shadow-sm overflow-hidden",
                )
            ),
        )
    )


def job_detail_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                "Back to Listing",
                href="/employer/jobs",
                class_name="flex items-center text-sm font-medium text-gray-500 hover:text-indigo-600 mb-6",
            ),
            rx.el.div(
                rx.el.h1(
                    "Job Detail View",
                    class_name="text-2xl font-bold text-gray-900 mb-8",
                ),
                rx.el.p(
                    "View the details of this job posting below.",
                    class_name="text-gray-500 mb-6",
                ),
                rx.el.a(
                    rx.el.button(
                        rx.icon("users", class_name="h-4 w-4 mr-2"),
                        "View Applications (ATS)",
                        class_name="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl shadow hover:bg-indigo-700 transition-colors flex items-center",
                    ),
                    href=f"/employer/jobs/{rx.State.router.page.params['job_id']}/applications",
                    class_name="inline-block",
                ),
                class_name="bg-white p-8 border rounded-xl",
            ),
        )
    )