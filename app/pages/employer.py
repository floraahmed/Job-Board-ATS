import reflex as rx
from app.components.layout import employer_layout
from app.states.db_state import DbState
from app.states.auth_state import AuthState


def stat_card(title: str, value: str, icon_name: str, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500 mb-1"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.icon(icon_name, class_name=f"h-6 w-6 {color_class}"),
                class_name="p-3 bg-gray-50 rounded-lg",
            ),
            class_name="flex items-start justify-between",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
    )


def dashboard_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Dashboard", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        f"Welcome back, {AuthState.user_name}",
                        class_name="text-gray-500 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.a(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "Post a Job",
                        href="/employer/jobs/create",
                        class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center text-sm font-medium",
                    ),
                    class_name="flex gap-3",
                ),
                class_name="mb-8 flex justify-between items-end",
            ),
            rx.el.div(
                stat_card("Active Jobs", "4", "briefcase", "text-blue-600"),
                stat_card("Total Applicants", "128", "users", "text-purple-600"),
                stat_card("Interviews Scheduled", "8", "calendar", "text-orange-600"),
                stat_card("Avg. Time to Hire", "14 days", "clock", "text-green-600"),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Recent Job Postings",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DbState.jobs,
                            lambda job: rx.el.div(
                                rx.el.div(
                                    rx.el.h4(
                                        job["title"],
                                        class_name="font-semibold text-gray-900",
                                    ),
                                    rx.el.span(
                                        job["status"],
                                        class_name=rx.match(
                                            job["status"],
                                            (
                                                "published",
                                                "px-2 py-0.5 text-xs font-semibold bg-green-100 text-green-700 rounded-full capitalize",
                                            ),
                                            (
                                                "draft",
                                                "px-2 py-0.5 text-xs font-semibold bg-gray-100 text-gray-700 rounded-full capitalize",
                                            ),
                                            "px-2 py-0.5 text-xs font-semibold bg-red-100 text-red-700 rounded-full capitalize",
                                        ),
                                    ),
                                    class_name="flex justify-between items-start mb-2",
                                ),
                                rx.el.p(
                                    job["location"],
                                    class_name="text-sm text-gray-500 mb-3",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        f"Posted: {job['created_at']}",
                                        class_name="text-xs text-gray-400",
                                    ),
                                    rx.el.a(
                                        "Manage",
                                        href=f"/employer/jobs/{job['id']}",
                                        class_name="text-sm font-medium text-indigo-600 hover:text-indigo-700",
                                    ),
                                    class_name="flex justify-between items-center",
                                ),
                                class_name="p-4 rounded-lg border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all bg-white",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
            ),
        )
    )