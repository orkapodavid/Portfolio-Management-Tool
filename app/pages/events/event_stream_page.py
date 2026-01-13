import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.events_views import event_stream_view
from app.states.ui.ui_state import UIState


def event_stream_page() -> rx.Component:
    return module_layout(
        event_stream_view(),
        "Events",
        "Event Stream",
        UIState.MODULE_SUBTABS["Events"],
    )
