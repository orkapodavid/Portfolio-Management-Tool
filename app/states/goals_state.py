import reflex as rx
from typing import TypedDict, Optional
import datetime
import random
import logging


class Goal(TypedDict):
    id: str
    name: str
    category: str
    target_amount: float
    current_amount: float
    deadline: str
    monthly_contribution: float
    icon: str
    color: str


class ProjectionPoint(TypedDict):
    month: str
    projected: float
    target: float


class GoalsState(rx.State):
    goals: list[Goal] = [
        {
            "id": "1",
            "name": "Retirement Fund",
            "category": "Retirement",
            "target_amount": 1000000.0,
            "current_amount": 250000.0,
            "deadline": "2045-06-01",
            "monthly_contribution": 2500.0,
            "icon": "armchair",
            "color": "indigo",
        },
        {
            "id": "2",
            "name": "House Down Payment",
            "category": "Home Purchase",
            "target_amount": 150000.0,
            "current_amount": 45000.0,
            "deadline": "2026-12-01",
            "monthly_contribution": 3000.0,
            "icon": "home",
            "color": "blue",
        },
        {
            "id": "3",
            "name": "Emergency Fund",
            "category": "Emergency Fund",
            "target_amount": 30000.0,
            "current_amount": 28500.0,
            "deadline": "2024-06-01",
            "monthly_contribution": 500.0,
            "icon": "piggy-bank",
            "color": "emerald",
        },
        {
            "id": "4",
            "name": "Kids' Education",
            "category": "Education",
            "target_amount": 200000.0,
            "current_amount": 15000.0,
            "deadline": "2035-09-01",
            "monthly_contribution": 800.0,
            "icon": "graduation-cap",
            "color": "amber",
        },
    ]
    is_modal_open: bool = False
    editing_goal_id: str = ""
    form_name: str = ""
    form_category: str = "Retirement"
    form_target: float = 0.0
    form_current: float = 0.0
    form_contribution: float = 0.0
    form_deadline: str = datetime.date.today().strftime("%Y-%m-%d")
    categories: list[str] = [
        "Retirement",
        "Emergency Fund",
        "Home Purchase",
        "Education",
        "Custom",
    ]

    @rx.var
    def total_goals_value(self) -> float:
        return sum((g["current_amount"] for g in self.goals))

    @rx.var
    def goals_on_track(self) -> int:
        count = 0
        today = datetime.date.today()
        for g in self.goals:
            try:
                deadline = datetime.datetime.strptime(g["deadline"], "%Y-%m-%d").date()
                months_left = (deadline.year - today.year) * 12 + (
                    deadline.month - today.month
                )
                months_left = max(0, months_left)
                projected = (
                    g["current_amount"] + g["monthly_contribution"] * months_left
                )
                if projected >= g["target_amount"]:
                    count += 1
            except ValueError as e:
                logging.exception(f"Error calculating goals on track: {e}")
                continue
        return count

    @rx.var
    def top_goals(self) -> list[Goal]:
        return self.goals[:3]

    def _get_icon_color(self, category: str) -> tuple[str, str]:
        if category == "Retirement":
            return ("armchair", "indigo")
        elif category == "Emergency Fund":
            return ("piggy-bank", "emerald")
        elif category == "Home Purchase":
            return ("home", "blue")
        elif category == "Education":
            return ("graduation-cap", "amber")
        else:
            return ("target", "gray")

    @rx.event
    def open_add_modal(self):
        self.editing_goal_id = ""
        self.form_name = ""
        self.form_category = "Custom"
        self.form_target = 0.0
        self.form_current = 0.0
        self.form_contribution = 0.0
        self.form_deadline = datetime.date.today().strftime("%Y-%m-%d")
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, goal: Goal):
        self.editing_goal_id = goal["id"]
        self.form_name = goal["name"]
        self.form_category = goal["category"]
        self.form_target = goal["target_amount"]
        self.form_current = goal["current_amount"]
        self.form_contribution = goal["monthly_contribution"]
        self.form_deadline = goal["deadline"]
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    def save_goal(self, form_data: dict):
        icon, color = self._get_icon_color(form_data.get("category", "Custom"))
        new_goal: Goal = {
            "id": self.editing_goal_id
            if self.editing_goal_id
            else str(random.randint(10000, 99999)),
            "name": form_data.get("name", "New Goal"),
            "category": form_data.get("category", "Custom"),
            "target_amount": float(form_data.get("target_amount", 0)),
            "current_amount": float(form_data.get("current_amount", 0)),
            "deadline": form_data.get(
                "deadline", datetime.date.today().strftime("%Y-%m-%d")
            ),
            "monthly_contribution": float(form_data.get("monthly_contribution", 0)),
            "icon": icon,
            "color": color,
        }
        if self.editing_goal_id:
            self.goals = [
                g if g["id"] != self.editing_goal_id else new_goal for g in self.goals
            ]
            rx.toast("Goal updated successfully", position="bottom-right")
        else:
            self.goals.append(new_goal)
            rx.toast("New goal created successfully", position="bottom-right")
        self.is_modal_open = False

    @rx.event
    def delete_goal(self, goal_id: str):
        self.goals = [g for g in self.goals if g["id"] != goal_id]
        rx.toast("Goal deleted", position="bottom-right")

    @rx.event
    def get_projection_data(self, goal: Goal) -> list[ProjectionPoint]:
        points = []
        try:
            start_date = datetime.date.today()
            end_date = datetime.datetime.strptime(goal["deadline"], "%Y-%m-%d").date()
            months_total = (end_date.year - start_date.year) * 12 + (
                end_date.month - start_date.month
            )
            months_total = max(1, months_total)
            current = goal["current_amount"]
            contribution = goal["monthly_contribution"]
            step = max(1, months_total // 10)
            for i in range(0, months_total + step, step):
                projected_val = current + contribution * i + current * 0.005 * i
                points.append(
                    {
                        "month": f"M{i}",
                        "projected": round(projected_val, 2),
                        "target": goal["target_amount"],
                    }
                )
        except Exception as e:
            logging.exception(f"Error getting projection data: {e}")
            pass
        return points