import reflex as rx
from typing import TypedDict


class LinkedAccount(TypedDict):
    id: str
    institution: str
    account_type: str
    last_four: str
    status: str
    logo: str


class ProfileState(rx.State):
    name: str = "Alex Morgan"
    email: str = "alex.morgan@example.com"
    phone: str = "+1 (555) 012-3456"
    bio: str = "Professional investor with 10+ years of experience in tech and renewable energy markets."
    risk_tolerance: str = "Aggressive"
    investment_goal: str = "Long-term Growth"
    experience_level: str = "Expert"
    is_editing: bool = False
    avatar_url: str = "https://api.dicebear.com/9.x/notionists/svg?seed=Felix"
    linked_accounts: list[LinkedAccount] = [
        {
            "id": "1",
            "institution": "Chase Bank",
            "account_type": "Checking",
            "last_four": "4589",
            "status": "Verified",
            "logo": "landmark",
        },
        {
            "id": "2",
            "institution": "Fidelity",
            "account_type": "Brokerage",
            "last_four": "9921",
            "status": "Verified",
            "logo": "briefcase",
        },
        {
            "id": "3",
            "institution": "Coinbase",
            "account_type": "Crypto",
            "last_four": "1102",
            "status": "Pending",
            "logo": "bitcoin",
        },
    ]

    @rx.event
    def toggle_editing(self):
        self.is_editing = not self.is_editing
        if not self.is_editing:
            yield rx.toast("Profile updated successfully", position="bottom-right")

    @rx.event
    def save_profile(self, form_data: dict):
        self.name = form_data.get("name", self.name)
        self.email = form_data.get("email", self.email)
        self.phone = form_data.get("phone", self.phone)
        self.bio = form_data.get("bio", self.bio)
        self.risk_tolerance = form_data.get("risk_tolerance", self.risk_tolerance)
        self.investment_goal = form_data.get("investment_goal", self.investment_goal)
        self.is_editing = False
        yield rx.toast("Profile saved successfully", position="bottom-right")

    @rx.event
    def upload_avatar(self):
        yield rx.toast("Avatar upload simulation started...", position="bottom-right")