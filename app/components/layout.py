import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import employer_sidebar, applicant_sidebar
from app.states.auth_state import AuthState


def base_layout(content: rx.Component) -> rx.Component:
    """Basic layout with just navbar"""
    return rx.el.div(
        navbar(),
        rx.el.main(content, class_name="min-h-[calc(100vh-4rem)] bg-gray-50"),
        class_name="min-h-screen font-['Inter']",
    )


def employer_layout(content: rx.Component) -> rx.Component:
    """Layout for authenticated employers"""
    return rx.el.div(
        navbar(),
        rx.el.div(
            employer_sidebar(),
            rx.el.main(
                rx.cond(
                    AuthState.is_employer,
                    content,
                    rx.el.div(
                        rx.el.div(
                            rx.icon("lock", class_name="h-12 w-12 text-gray-300 mb-4"),
                            rx.el.h2(
                                "Access Denied",
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "You must be an employer to view this page.",
                                class_name="text-gray-500 mt-2",
                            ),
                            rx.el.a(
                                "Go to Login",
                                href="/login",
                                class_name="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700",
                            ),
                            class_name="flex flex-col items-center justify-center h-full text-center p-12",
                        ),
                        class_name="h-full flex items-center justify-center",
                    ),
                ),
                class_name="flex-1 p-6 md:p-8 overflow-y-auto",
            ),
            class_name="flex min-h-[calc(100vh-4rem)] bg-gray-50",
        ),
        class_name="min-h-screen font-['Inter']",
    )


def applicant_layout(content: rx.Component) -> rx.Component:
    """Layout for authenticated applicants"""
    return rx.el.div(
        navbar(),
        rx.el.div(
            applicant_sidebar(),
            rx.el.main(
                rx.cond(
                    AuthState.is_applicant,
                    content,
                    rx.el.div(
                        rx.el.div(
                            rx.icon("lock", class_name="h-12 w-12 text-gray-300 mb-4"),
                            rx.el.h2(
                                "Access Denied",
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "You must be an applicant to view this page.",
                                class_name="text-gray-500 mt-2",
                            ),
                            rx.el.a(
                                "Go to Login",
                                href="/login",
                                class_name="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700",
                            ),
                            class_name="flex flex-col items-center justify-center h-full text-center p-12",
                        ),
                        class_name="h-full flex items-center justify-center",
                    ),
                ),
                class_name="flex-1 p-6 md:p-8 overflow-y-auto",
            ),
            class_name="flex min-h-[calc(100vh-4rem)] bg-gray-50",
        ),
        class_name="min-h-screen font-['Inter']",
    )