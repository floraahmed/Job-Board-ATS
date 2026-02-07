import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("briefcase", class_name="h-6 w-6 text-indigo-600"),
                        rx.el.span(
                            "JobPortal", class_name="text-xl font-bold text-gray-900"
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                    rx.el.p(
                        "Bridging the gap between ambitious talent and innovative companies worldwide.",
                        class_name="text-sm text-gray-500 max-w-xs",
                    ),
                    class_name="col-span-2",
                ),
                rx.el.div(
                    rx.el.h4("Product", class_name="font-bold text-gray-900 mb-4"),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.a(
                                "Browse Jobs",
                                href="/applicant/jobs",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            ),
                            class_name="mb-2",
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Post a Job",
                                href="/employer/jobs/create",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            ),
                            class_name="mb-2",
                        ),
                        rx.el.li(
                            rx.el.a(
                                "ATS Demo",
                                href="/employer/dashboard",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            )
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.h4("Support", class_name="font-bold text-gray-900 mb-4"),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.a(
                                "Help Center",
                                href="#",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            ),
                            class_name="mb-2",
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Privacy Policy",
                                href="#",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            ),
                            class_name="mb-2",
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Terms of Service",
                                href="#",
                                class_name="text-sm text-gray-600 hover:text-indigo-600",
                            )
                        ),
                    ),
                ),
                class_name="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2024 JobPortal Inc. All rights reserved.",
                    class_name="text-xs text-gray-400",
                ),
                rx.el.div(
                    rx.icon(
                        "twitter",
                        class_name="h-4 w-4 text-gray-400 hover:text-indigo-600 cursor-pointer",
                    ),
                    rx.icon(
                        "linkedin",
                        class_name="h-4 w-4 text-gray-400 hover:text-indigo-600 cursor-pointer",
                    ),
                    rx.icon(
                        "github",
                        class_name="h-4 w-4 text-gray-400 hover:text-indigo-600 cursor-pointer",
                    ),
                    class_name="flex gap-4",
                ),
                class_name="pt-8 border-t border-gray-100 flex justify-between items-center",
            ),
            class_name="max-w-7xl mx-auto px-6 py-12",
        ),
        class_name="bg-white border-t border-gray-100 mt-20",
    )