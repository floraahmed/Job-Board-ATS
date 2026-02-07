import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(
    label: str, icon_name: str, url: str, is_active: rx.Var[bool] | bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon_name,
            class_name=rx.cond(
                is_active, "h-5 w-5 text-indigo-600", "h-5 w-5 text-gray-400"
            ),
        ),
        rx.el.span(label, class_name="font-medium"),
        href=url,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-3 py-2.5 rounded-lg bg-indigo-50 text-indigo-700 transition-colors",
            "flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors",
        ),
    )


def employer_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "EMPLOYER",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-3",
                ),
                rx.el.nav(
                    sidebar_item(
                        "Dashboard",
                        "layout-dashboard",
                        "/employer/dashboard",
                        is_active=rx.cond(
                            rx.State.router.page.path == "/employer/dashboard",
                            True,
                            False,
                        ),
                    ),
                    sidebar_item(
                        "Job Postings",
                        "file-text",
                        "/employer/jobs",
                        is_active=rx.cond(
                            rx.State.router.page.path.contains("/employer/jobs"),
                            True,
                            False,
                        ),
                    ),
                    sidebar_item("Applications", "users", "/employer/applications"),
                    sidebar_item("Company Profile", "building-2", "/employer/company"),
                    class_name="space-y-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex flex-col h-full py-6 px-4",
        ),
        class_name="hidden md:flex w-64 flex-col border-r border-gray-100 bg-white h-[calc(100vh-4rem)] sticky top-16",
    )


def applicant_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "APPLICANT",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 px-3",
                ),
                rx.el.nav(
                    sidebar_item(
                        "Browse Jobs", "search", "/applicant/jobs", is_active=True
                    ),
                    sidebar_item(
                        "My Applications", "file-stack", "/applicant/applications"
                    ),
                    sidebar_item("My Profile", "user", "/applicant/profile"),
                    class_name="space-y-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex flex-col h-full py-6 px-4",
        ),
        class_name="hidden md:flex w-64 flex-col border-r border-gray-100 bg-white h-[calc(100vh-4rem)] sticky top-16",
    )