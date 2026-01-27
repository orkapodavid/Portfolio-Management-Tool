import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.event_calendar_ag_grid import event_calendar_ag_grid
from app.states.ui.ui_state import UIState


def event_calendar_page() -> rx.Component:
    return module_layout(
        event_calendar_ag_grid(),
        "Events",
        "Event Calendar",
        UIState.MODULE_SUBTABS["Events"],
    )
