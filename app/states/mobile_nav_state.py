import reflex as rx


class MobileNavState(rx.State):
    is_open: bool = False

    @rx.event
    def toggle_menu(self):
        self.is_open = not self.is_open

    @rx.event
    def close_menu(self):
        self.is_open = False