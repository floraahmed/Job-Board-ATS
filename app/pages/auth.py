import reflex as rx
from app.states.auth_state import AuthState
from app.components.navbar import navbar


def login_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Welcome Back",
                        class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.el.p(
                        "Sign in to access your account",
                        class_name="text-gray-500 text-center mb-8",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="you@example.com",
                            on_change=AuthState.set_login_email,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_login_password,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.login_error != "",
                        rx.el.div(
                            rx.icon("wheat", class_name="h-4 w-4 mr-2"),
                            AuthState.login_error,
                            class_name="mb-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm flex items-center",
                        ),
                    ),
                    rx.el.button(
                        "Sign In",
                        on_click=AuthState.login,
                        class_name="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Don't have an account? ", class_name="text-gray-500"
                        ),
                        rx.el.a(
                            "Sign up",
                            href="/register",
                            class_name="text-indigo-600 font-medium hover:text-indigo-700",
                        ),
                        class_name="mt-6 text-center text-sm",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Demo Credentials:",
                            class_name="text-xs font-bold text-gray-400 uppercase mb-2",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Employer: employer@acme.com / password",
                                class_name="text-xs text-gray-500 font-mono",
                            ),
                            rx.el.p(
                                "Applicant: applicant@gmail.com / password",
                                class_name="text-xs text-gray-500 font-mono",
                            ),
                            class_name="space-y-1 bg-gray-50 p-3 rounded border border-gray-100",
                        ),
                        class_name="mt-8 pt-6 border-t border-gray-100",
                    ),
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-[calc(100vh-4rem)] bg-gray-50 p-4",
        ),
        class_name="min-h-screen font-['Inter']",
    )


def register_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Create Account",
                        class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.el.p(
                        "Join us to find or post jobs",
                        class_name="text-gray-500 text-center mb-8",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "I want to...",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("search", class_name="h-5 w-5 mb-1"),
                                "Find a Job",
                                on_click=AuthState.set_reg_role_applicant,
                                class_name=rx.cond(
                                    AuthState.reg_role == "applicant",
                                    "flex-1 py-3 px-4 bg-indigo-600 text-white rounded-l-lg border border-indigo-600 flex flex-col items-center justify-center transition-all",
                                    "flex-1 py-3 px-4 bg-white text-gray-600 hover:bg-gray-50 rounded-l-lg border border-gray-300 flex flex-col items-center justify-center transition-all",
                                ),
                            ),
                            rx.el.button(
                                rx.icon("briefcase", class_name="h-5 w-5 mb-1"),
                                "Hire Talent",
                                on_click=AuthState.set_reg_role_employer,
                                class_name=rx.cond(
                                    AuthState.reg_role == "employer",
                                    "flex-1 py-3 px-4 bg-indigo-600 text-white rounded-r-lg border border-indigo-600 flex flex-col items-center justify-center transition-all",
                                    "flex-1 py-3 px-4 bg-white text-gray-600 hover:bg-gray-50 rounded-r-lg border border-gray-300 border-l-0 flex flex-col items-center justify-center transition-all",
                                ),
                            ),
                            class_name="flex mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="text",
                            placeholder="John Doe",
                            on_change=AuthState.set_reg_name,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.cond(
                        AuthState.reg_role == "employer",
                        rx.el.div(
                            rx.el.label(
                                "Company Name",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="text",
                                placeholder="Acme Inc.",
                                on_change=AuthState.set_reg_company_name,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                            ),
                            class_name="mb-4 animate-fade-in",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email Address",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="email",
                            placeholder="you@example.com",
                            on_change=AuthState.set_reg_email,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_reg_password,
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.reg_error != "",
                        rx.el.div(
                            rx.icon("wheat", class_name="h-4 w-4 mr-2"),
                            AuthState.reg_error,
                            class_name="mb-6 p-3 rounded-lg bg-red-50 text-red-600 text-sm flex items-center",
                        ),
                    ),
                    rx.el.button(
                        "Create Account",
                        on_click=AuthState.register,
                        class_name="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Already have an account? ", class_name="text-gray-500"
                        ),
                        rx.el.a(
                            "Sign in",
                            href="/login",
                            class_name="text-indigo-600 font-medium hover:text-indigo-700",
                        ),
                        class_name="mt-6 text-center text-sm",
                    ),
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-[calc(100vh-4rem)] bg-gray-50 p-4",
        ),
        class_name="min-h-screen font-['Inter']",
    )