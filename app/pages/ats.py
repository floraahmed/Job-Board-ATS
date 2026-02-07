import reflex as rx
from app.components.layout import employer_layout
from app.states.ats_state import ATSState
from app.states.jobs_state import JobsState


def stage_badge(status: str) -> rx.Component:
    return rx.el.span(
        status.replace("_", " ").capitalize(),
        class_name=rx.match(
            status,
            (
                "new",
                "px-2 py-0.5 text-xs font-semibold bg-blue-100 text-blue-700 rounded-full",
            ),
            (
                "under_review",
                "px-2 py-0.5 text-xs font-semibold bg-yellow-100 text-yellow-700 rounded-full",
            ),
            (
                "interview",
                "px-2 py-0.5 text-xs font-semibold bg-purple-100 text-purple-700 rounded-full",
            ),
            (
                "rejected",
                "px-2 py-0.5 text-xs font-semibold bg-red-100 text-red-700 rounded-full",
            ),
            (
                "hired",
                "px-2 py-0.5 text-xs font-semibold bg-green-100 text-green-700 rounded-full",
            ),
            "px-2 py-0.5 text-xs font-semibold bg-gray-100 text-gray-700 rounded-full",
        ),
    )


def kanban_card(app: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    app.get("applicant_name", "Unknown"),
                    class_name="font-semibold text-gray-900 line-clamp-1",
                ),
                rx.el.p(
                    f"Applied: {app['applied_at']}", class_name="text-xs text-gray-500"
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("arrow_right_to_line", class_name="h-4 w-4 text-gray-400"),
                class_name="p-1 hover:bg-gray-100 rounded",
            ),
            class_name="flex justify-between items-start mb-3",
        ),
        rx.el.div(
            rx.el.p(
                "Resume.pdf",
                class_name="text-xs text-indigo-600 flex items-center gap-1 mb-2",
            ),
            rx.el.div(
                rx.el.button(
                    "View",
                    on_click=lambda: ATSState.select_application(app["id"]),
                    class_name="flex-1 text-xs py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded border border-gray-200 font-medium transition-colors",
                ),
                class_name="flex gap-2",
            ),
            class_name="space-y-2",
        ),
        class_name="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer",
        on_click=lambda: ATSState.select_application(app["id"]),
    )


def kanban_column(title: str, status_key: str, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    title,
                    class_name="font-bold text-gray-700 text-sm uppercase tracking-wide",
                ),
                rx.el.span(
                    ATSState.kanban_columns[status_key].length(),
                    class_name=f"text-xs font-bold px-2 py-0.5 rounded-full {color_class} bg-opacity-20 text-opacity-90 ml-2",
                ),
                class_name="flex items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    ATSState.kanban_columns[status_key].to(list[dict]),
                    lambda app: kanban_card(app),
                ),
                class_name="space-y-3 min-h-[200px]",
            ),
            class_name="flex-1 min-w-[280px] bg-gray-50/50 rounded-xl p-4 border border-gray-100 h-full overflow-y-auto",
        ),
        class_name="flex flex-col h-full snap-start",
    )


def history_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-2 w-2 rounded-full bg-gray-300 ring-4 ring-white"),
            class_name="absolute left-0 top-2 -ml-1.5",
        ),
        rx.el.div(
            rx.el.p(item["notes"], class_name="text-sm text-gray-900 font-medium"),
            rx.el.p(item["changed_at"], class_name="text-xs text-gray-500 mt-0.5"),
            class_name="py-0.5",
        ),
        class_name="relative pl-6 pb-6 border-l border-gray-200 last:pb-0 last:border-0",
    )


def applicant_detail_modal() -> rx.Component:
    return rx.cond(
        ATSState.selected_application_id != "",
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 z-[60] backdrop-blur-sm transition-opacity",
                on_click=ATSState.close_detail_view,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            ATSState.active_applicant_user["name"],
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6"),
                            on_click=ATSState.close_detail_view,
                            class_name="text-gray-400 hover:text-gray-600",
                        ),
                        class_name="flex justify-between items-center mb-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            ATSState.active_applicant_user["email"],
                            class_name="text-gray-500 mr-4",
                        ),
                        stage_badge(ATSState.active_application["status"]),
                        class_name="flex items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Move to stage:",
                            class_name="text-xs font-bold text-gray-400 uppercase mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                [
                                    "new",
                                    "under_review",
                                    "interview",
                                    "rejected",
                                    "hired",
                                ],
                                lambda s: rx.el.button(
                                    s.replace("_", " ").capitalize(),
                                    on_click=lambda: ATSState.move_stage(
                                        ATSState.selected_application_id, s
                                    ),
                                    class_name=rx.cond(
                                        ATSState.active_application["status"] == s,
                                        "px-3 py-1.5 text-sm font-medium bg-gray-900 text-white rounded-lg",
                                        "px-3 py-1.5 text-sm font-medium bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-lg",
                                    ),
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mb-8 pb-8 border-b border-gray-100",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Cover Letter",
                                class_name="text-lg font-semibold text-gray-900 mb-3",
                            ),
                            rx.el.p(
                                ATSState.active_application["cover_letter"],
                                class_name="text-gray-600 leading-relaxed bg-gray-50 p-4 rounded-xl text-sm",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Screening Answers",
                                class_name="text-lg font-semibold text-gray-900 mb-3",
                            ),
                            rx.el.p(
                                ATSState.active_application["answers"],
                                class_name="text-gray-600 leading-relaxed bg-gray-50 p-4 rounded-xl text-sm",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Resume",
                                class_name="text-lg font-semibold text-gray-900 mb-3",
                            ),
                            rx.el.div(
                                rx.icon("file-text", class_name="h-8 w-8 text-red-500"),
                                rx.el.div(
                                    rx.el.p(
                                        ATSState.active_application["resume_filename"],
                                        class_name="font-medium text-gray-900",
                                    ),
                                    rx.el.p(
                                        "PDF Document - 2.4 MB",
                                        class_name="text-xs text-gray-500",
                                    ),
                                ),
                                rx.el.button(
                                    rx.icon("download", class_name="h-4 w-4"),
                                    class_name="ml-auto p-2 text-gray-400 hover:text-gray-600",
                                ),
                                class_name="flex items-center gap-4 p-4 border border-gray-200 rounded-xl",
                            ),
                            class_name="mb-8",
                        ),
                        class_name="space-y-6",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Activity & Notes",
                            class_name="text-lg font-semibold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.input(
                                    placeholder="Add an internal note...",
                                    on_change=ATSState.set_note_input,
                                    class_name="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none",
                                    default_value=ATSState.note_input,
                                ),
                                rx.el.button(
                                    "Add",
                                    on_click=ATSState.add_note,
                                    class_name="px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700",
                                ),
                                class_name="flex gap-2 mb-6",
                            ),
                            rx.el.div(
                                rx.foreach(ATSState.application_history, history_item),
                                class_name="space-y-0",
                            ),
                        ),
                        class_name="pt-6 border-t border-gray-100",
                    ),
                    class_name="h-full overflow-y-auto p-6",
                ),
                class_name="fixed right-0 top-0 bottom-0 w-full max-w-2xl bg-white shadow-2xl z-[70] animate-slide-in-right",
            ),
        ),
    )


def ats_page() -> rx.Component:
    return employer_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                        "Back to Job",
                        href=f"/employer/jobs/{ATSState.current_job_id}",
                        class_name="flex items-center text-sm font-medium text-gray-500 hover:text-indigo-600 mb-2",
                    ),
                    rx.el.h1(
                        ATSState.current_job["title"],
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.p("Application Tracking System", class_name="text-gray-500"),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search applicants...",
                            on_change=ATSState.set_search,
                            class_name="pl-9 pr-4 py-2 border rounded-lg text-sm w-64 focus:ring-2 focus:ring-indigo-500",
                        ),
                        class_name="relative",
                    ),
                    rx.el.select(
                        rx.el.option("Any Time", value="all"),
                        rx.el.option("Last 7 Days", value="7"),
                        rx.el.option("Last 30 Days", value="30"),
                        rx.el.option("Last 90 Days", value="90"),
                        on_change=ATSState.set_filter_days,
                        class_name="px-3 py-2 border rounded-lg text-sm bg-white appearance-none",
                    ),
                    class_name="flex items-end gap-3",
                ),
                class_name="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-8",
            ),
            rx.el.div(
                kanban_column("New", "new", "bg-blue-500 text-blue-700"),
                kanban_column(
                    "Under Review", "under_review", "bg-yellow-500 text-yellow-700"
                ),
                kanban_column(
                    "Interview", "interview", "bg-purple-500 text-purple-700"
                ),
                kanban_column("Rejected", "rejected", "bg-red-500 text-red-700"),
                kanban_column("Hired", "hired", "bg-green-500 text-green-700"),
                class_name="flex overflow-x-auto gap-6 pb-6 h-[calc(100vh-16rem)] snap-x",
            ),
            applicant_detail_modal(),
        )
    )