import reflex as rx
from app.components.layout import employer_layout
from app.states.ats_state import ATSState
from app.models import Application


def application_row(app: Application) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    app["applicant_name"].to(str),
                    class_name="font-semibold text-gray-900",
                ),
                rx.el.p(app["email"].to(str), class_name="text-xs text-gray-500"),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(app["job_title"].to(str), class_name="text-sm text-gray-700"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                app["status"].to(str).replace("_", " ").capitalize(),
                class_name=rx.match(
                    app["status"],
                    (
                        "new",
                        "px-2 py-1 text-xs font-bold bg-blue-100 text-blue-700 rounded-full capitalize",
                    ),
                    (
                        "under_review",
                        "px-2 py-1 text-xs font-bold bg-yellow-100 text-yellow-700 rounded-full capitalize",
                    ),
                    (
                        "interview",
                        "px-2 py-1 text-xs font-bold bg-purple-100 text-purple-700 rounded-full capitalize",
                    ),
                    (
                        "hired",
                        "px-2 py-1 text-xs font-bold bg-green-100 text-green-700 rounded-full capitalize",
                    ),
                    "px-2 py-1 text-xs font-bold bg-red-100 text-red-700 rounded-full capitalize",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(app["applied_at"].to(str), class_name="text-sm text-gray-600"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.a(
                "View in ATS",
                href=f"/employer/jobs/{app['job_id'].to(str)}/applications",
                class_name="text-sm font-medium text-indigo-600 hover:text-indigo-900",
            ),
            class_name="px-6 py-4 text-right",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50",
    )


def all_applications_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "All Applications", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Overview of all candidates across all jobs",
                    class_name="text-gray-500",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Applicant",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Job Role",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "Applied Date",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase",
                            ),
                            rx.el.th(
                                "",
                                class_name="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase",
                            ),
                            class_name="bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ATSState.all_employer_applications, application_row)
                    ),
                    class_name="w-full table-auto",
                ),
                class_name="bg-white border rounded-xl shadow-sm overflow-hidden",
            ),
        )
    )