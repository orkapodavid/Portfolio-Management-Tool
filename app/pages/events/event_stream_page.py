import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.event_stream_ag_grid import event_stream_ag_grid
from app.states.ui.ui_state import UIState


def event_stream_page() -> rx.Component:
    return module_layout(
        event_stream_ag_grid(),
        "Events",
        "Event Stream",
        UIState.MODULE_SUBTABS["Events"],
    )
