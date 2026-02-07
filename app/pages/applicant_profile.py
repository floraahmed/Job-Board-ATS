import reflex as rx
from app.components.layout import applicant_layout
from app.states.applicant_profile_state import ApplicantProfileState


def applicant_profile_page() -> rx.Component:
    return applicant_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("My Profile", class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(
                    "Keep your professional details up to date",
                    class_name="text-gray-500",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Personal Details",
                            class_name="font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Full Name",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    default_value=ApplicantProfileState.temp_name,
                                    on_change=ApplicantProfileState.set_temp_name,
                                    class_name="w-full p-2 border rounded-lg",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Location",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    default_value=ApplicantProfileState.temp_location,
                                    on_change=ApplicantProfileState.set_temp_location,
                                    class_name="w-full p-2 border rounded-lg",
                                ),
                                class_name="flex-1",
                            ),
                            class_name="flex gap-4 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Phone Number",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    default_value=ApplicantProfileState.temp_phone,
                                    on_change=ApplicantProfileState.set_temp_phone,
                                    class_name="w-full p-2 border rounded-lg",
                                ),
                                class_name="flex-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Bio / Summary",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                default_value=ApplicantProfileState.temp_bio,
                                on_change=ApplicantProfileState.set_temp_bio,
                                class_name="w-full p-2 border rounded-lg h-24",
                            ),
                            class_name="mb-6",
                        ),
                        class_name="p-8 bg-white border rounded-2xl shadow-sm mb-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Skills & Expertise",
                            class_name="font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Add a skill...",
                                on_change=ApplicantProfileState.set_new_skill,
                                class_name="flex-1 p-2 border rounded-l-lg",
                                default_value=ApplicantProfileState.new_skill,
                            ),
                            rx.el.button(
                                "Add",
                                on_click=ApplicantProfileState.add_skill,
                                class_name="px-4 bg-indigo-600 text-white rounded-r-lg font-bold",
                            ),
                            class_name="flex mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ApplicantProfileState.temp_skills,
                                lambda s: rx.el.span(
                                    s,
                                    rx.el.button(
                                        rx.icon("x", class_name="h-3 w-3"),
                                        on_click=lambda: ApplicantProfileState.remove_skill(
                                            s
                                        ),
                                        class_name="ml-2",
                                    ),
                                    class_name="inline-flex items-center px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold mr-2 mb-2",
                                ),
                            ),
                            class_name="flex flex-wrap",
                        ),
                        class_name="p-8 bg-white border rounded-2xl shadow-sm mb-6",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Professional Background",
                            class_name="font-bold text-gray-900 mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Work Experience",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                default_value=ApplicantProfileState.temp_experience,
                                on_change=ApplicantProfileState.set_temp_experience,
                                class_name="w-full p-2 border rounded-lg h-32",
                                placeholder="Describe your roles and achievements...",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Education",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                default_value=ApplicantProfileState.temp_education,
                                on_change=ApplicantProfileState.set_temp_education,
                                class_name="w-full p-2 border rounded-lg h-24",
                                placeholder="University, degree, certifications...",
                            ),
                        ),
                        class_name="p-8 bg-white border rounded-2xl shadow-sm mb-6",
                    ),
                    rx.el.button(
                        "Save All Profile Changes",
                        on_click=ApplicantProfileState.save_profile,
                        disabled=ApplicantProfileState.is_saving,
                        class_name="w-full py-4 bg-indigo-600 text-white font-bold rounded-2xl shadow-lg hover:bg-indigo-700 transition-all",
                    ),
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
        )
    )