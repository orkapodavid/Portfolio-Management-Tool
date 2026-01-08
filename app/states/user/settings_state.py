import reflex as rx
from app.services import UserService


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
    is_loading: bool = False

    async def on_load(self):
        """Load settings when page loads."""
        await self.load_settings()
    
    async def load_settings(self):
        """Load settings from UserService."""
        self.is_loading = True
        try:
            service = UserService()
            settings = await service.get_user_settings()
            if settings:
                self.theme_mode = settings.get("theme", self.theme_mode)
                self.currency = settings.get("currency", self.currency)
                self.language = settings.get("language", self.language)
        except Exception as e:
            import logging
            logging.exception(f"Error loading settings: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def toggle_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        yield rx.toast(f"Theme switched to {self.theme_mode}", position="bottom-right")

    @rx.event
    async def update_notification(self, key: str, value: bool):
        """Update notification settings using UserService."""
        if key == "email":
            self.email_notifications = value
        elif key == "push":
            self.push_notifications = value
        elif key == "sms":
            self.sms_notifications = value
        elif key == "marketing":
            self.marketing_emails = value
        
        try:
            service = UserService()
            await service.update_user_settings(notifications={key: value})
            yield rx.toast("Notification preferences updated", position="bottom-right")
        except Exception as e:
            import logging
            logging.exception(f"Error updating settings: {e}")

    @rx.event
    def update_privacy(self, key: str, value: bool):
        if key == "public":
            self.profile_public = value
        elif key == "holdings":
            self.show_holdings = value
        elif key == "data":
            self.allow_data_collection = value
        yield rx.toast("Privacy settings updated", position="bottom-right")

    @rx.event
    def set_currency(self, value: str):
        self.currency = value

    @rx.event
    def set_language(self, value: str):
        self.language = value

    @rx.event
    def export_data(self):
        yield rx.toast(
            "Data export started. You will receive an email shortly.",
            position="bottom-right",
        )

    @rx.event
    def delete_account(self):
        yield rx.toast(
            "Account deletion request sent to support.",
            position="bottom-right",
            color_scheme="red",
        )