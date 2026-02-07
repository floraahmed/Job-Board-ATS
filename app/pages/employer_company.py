import reflex as rx
from app.components.layout import employer_layout
from app.states.company_state import CompanyState


def company_profile_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Company Profile", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage your public company identity and branding",
                    class_name="text-gray-500",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=CompanyState.temp_logo,
                                class_name="h-24 w-24 rounded-xl border-4 border-white shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Logo URL",
                                    class_name="text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.input(
                                    default_value=CompanyState.temp_logo,
                                    on_change=CompanyState.set_temp_logo,
                                    class_name="w-full mt-1 p-2 border rounded-lg text-sm",
                                ),
                                class_name="flex-1",
                            ),
                            class_name="flex items-center gap-6 mb-8 p-6 bg-gray-50 rounded-2xl",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Company Name",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    default_value=CompanyState.temp_name,
                                    on_change=CompanyState.set_temp_name,
                                    class_name="w-full p-2 border rounded-lg",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Industry",
                                    class_name="block text-sm font-medium text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    default_value=CompanyState.temp_industry,
                                    on_change=CompanyState.set_temp_industry,
                                    class_name="w-full p-2 border rounded-lg",
                                ),
                                class_name="flex-1",
                            ),
                            class_name="flex gap-4 mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Description",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.textarea(
                                default_value=CompanyState.temp_description,
                                on_change=CompanyState.set_temp_description,
                                class_name="w-full p-2 border rounded-lg h-32",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.button(
                            "Save Changes",
                            on_click=CompanyState.save_company,
                            disabled=CompanyState.is_saving,
                            class_name="w-full py-2.5 bg-indigo-600 text-white font-bold rounded-lg hover:bg-indigo-700 transition-all",
                        ),
                        class_name="p-8",
                    ),
                    class_name="bg-white rounded-2xl border shadow-sm",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Statistics", class_name="font-bold text-gray-900 mb-4"
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Total Jobs Posted", class_name="text-sm text-gray-500"
                            ),
                            rx.el.p(
                                CompanyState.stats["total_jobs"].to_string(),
                                class_name="text-2xl font-bold text-indigo-600",
                            ),
                            class_name="p-4 bg-indigo-50 rounded-xl mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Total Applications", class_name="text-sm text-gray-500"
                            ),
                            rx.el.p(
                                CompanyState.stats["total_apps"].to_string(),
                                class_name="text-2xl font-bold text-green-600",
                            ),
                            class_name="p-4 bg-green-50 rounded-xl",
                        ),
                        class_name="bg-white p-6 rounded-2xl border shadow-sm sticky top-24",
                    )
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
        )
    )