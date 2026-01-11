import reflex as rx


def event_coming_soon(title: str) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon("calendar", size=48, class_name="text-gray-300 mb-4"),
            rx.heading(f"{title} - Coming Soon", size="5", class_name="text-gray-500"),
            rx.text("This view is under construction.", class_name="text-gray-400"),
            class_name="h-full justify-center items-center py-20",
        ),
        class_name="w-full h-full bg-white",
    )


def event_calendar_view() -> rx.Component:
    return event_coming_soon("Event Calendar")


def event_stream_view() -> rx.Component:
    return event_coming_soon("Event Stream")


def reverse_inquiry_view() -> rx.Component:
    return event_coming_soon("Reverse Inquiry")
