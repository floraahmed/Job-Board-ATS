import reflex as rx
from app.states.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("briefcase", class_name="h-6 w-6 text-indigo-600"),
                    rx.el.span(
                        "JobPortal", class_name="text-xl font-bold text-gray-900"
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                AuthState.user_name,
                                class_name="text-sm font-medium text-gray-700 hidden sm:block",
                            ),
                            rx.el.div(
                                AuthState.user_initials,
                                class_name="h-8 w-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold ring-2 ring-white",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        rx.el.button(
                            rx.icon("log-out", class_name="h-4 w-4"),
                            "Logout",
                            on_click=AuthState.logout,
                            class_name="ml-4 text-sm text-gray-500 hover:text-red-600 transition-colors flex items-center gap-1",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Login",
                            href="/login",
                            class_name="text-sm font-medium text-gray-700 hover:text-indigo-600 px-4 py-2",
                        ),
                        rx.el.a(
                            "Sign Up",
                            href="/register",
                            class_name="text-sm font-medium bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between h-16 px-6 max-w-7xl mx-auto",
        ),
        class_name="bg-white border-b border-gray-100 sticky top-0 z-50",
    )