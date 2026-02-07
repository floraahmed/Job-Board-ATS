import reflex as rx
from app.states.auth_state import AuthState
from app.states.notification_state import NotificationState


def notification_item(note: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                note["title"],
                class_name=rx.cond(
                    note["is_read"],
                    "text-sm font-medium text-gray-600",
                    "text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                note["message"], class_name="text-xs text-gray-500 mt-0.5 line-clamp-2"
            ),
            rx.el.p(note["created_at"], class_name="text-[10px] text-gray-400 mt-1"),
            class_name="flex-1",
        ),
        rx.cond(
            ~note["is_read"],
            rx.el.button(
                rx.icon("check", class_name="h-3 w-3"),
                on_click=lambda: NotificationState.mark_as_read(note["id"]),
                class_name="h-6 w-6 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center hover:bg-indigo-100",
            ),
        ),
        class_name="p-3 hover:bg-gray-50 flex gap-3 border-b border-gray-100 transition-colors",
    )


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
                            rx.el.button(
                                rx.icon("bell", class_name="h-5 w-5 text-gray-600"),
                                rx.cond(
                                    NotificationState.unread_count > 0,
                                    rx.el.span(
                                        NotificationState.unread_count.to_string(),
                                        class_name="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-[10px] flex items-center justify-center rounded-full font-bold",
                                    ),
                                ),
                                on_click=NotificationState.toggle_notifications,
                                class_name="relative p-2 rounded-full hover:bg-gray-100 mr-2",
                            ),
                            rx.cond(
                                NotificationState.show_notifications,
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.h3(
                                            "Notifications",
                                            class_name="text-sm font-bold text-gray-900",
                                        ),
                                        rx.el.button(
                                            "Mark all read",
                                            on_click=NotificationState.mark_all_read,
                                            class_name="text-[10px] text-indigo-600 font-semibold hover:underline",
                                        ),
                                        class_name="flex justify-between items-center p-3 border-b",
                                    ),
                                    rx.el.div(
                                        rx.foreach(
                                            NotificationState.my_notifications,
                                            notification_item,
                                        ),
                                        rx.cond(
                                            NotificationState.my_notifications.length()
                                            == 0,
                                            rx.el.div(
                                                "No new notifications",
                                                class_name="p-4 text-xs text-center text-gray-400",
                                            ),
                                        ),
                                        class_name="max-h-80 overflow-y-auto",
                                    ),
                                    class_name="absolute right-0 top-12 w-72 bg-white rounded-xl shadow-2xl border border-gray-100 z-[100] animate-in fade-in zoom-in duration-150",
                                ),
                            ),
                            class_name="relative",
                        ),
                        rx.el.div(
                            rx.el.span(
                                AuthState.user_name,
                                class_name="text-sm font-medium text-gray-700 hidden lg:block",
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