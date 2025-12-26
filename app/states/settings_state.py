import reflex as rx


class SettingsState(rx.State):
    theme_mode: str = "light"
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = False
    marketing_emails: bool = False
    profile_public: bool = True
    show_holdings: bool = False
    allow_data_collection: bool = True
    currency: str = "USD"
    language: str = "English"

    @rx.event
    def toggle_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        rx.toast(f"Theme switched to {self.theme_mode}", position="bottom-right")

    @rx.event
    def update_notification(self, key: str, value: bool):
        if key == "email":
            self.email_notifications = value
        elif key == "push":
            self.push_notifications = value
        elif key == "sms":
            self.sms_notifications = value
        elif key == "marketing":
            self.marketing_emails = value
        rx.toast("Notification preferences updated", position="bottom-right")

    @rx.event
    def update_privacy(self, key: str, value: bool):
        if key == "public":
            self.profile_public = value
        elif key == "holdings":
            self.show_holdings = value
        elif key == "data":
            self.allow_data_collection = value
        rx.toast("Privacy settings updated", position="bottom-right")

    @rx.event
    def set_currency(self, value: str):
        self.currency = value

    @rx.event
    def set_language(self, value: str):
        self.language = value

    @rx.event
    def export_data(self):
        rx.toast(
            "Data export started. You will receive an email shortly.",
            position="bottom-right",
        )

    @rx.event
    def delete_account(self):
        rx.toast(
            "Account deletion request sent to support.",
            position="bottom-right",
            color_scheme="red",
        )