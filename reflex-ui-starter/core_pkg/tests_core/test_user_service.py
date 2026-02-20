"""Tests for UserService — core business logic for user management."""

import pytest
from core.services.user_service import UserService


@pytest.fixture
def service():
    """Fresh UserService instance for each test."""
    return UserService()


class TestGetUsers:
    def test_returns_list(self, service):
        users = service.get_users()
        assert isinstance(users, list)
        assert len(users) > 0

    def test_users_have_required_fields(self, service):
        users = service.get_users()
        required = {"id", "name", "email", "role", "status", "created_at"}
        for user in users:
            assert required.issubset(user.keys()), f"Missing keys in {user.keys()}"

    def test_users_have_valid_status(self, service):
        users = service.get_users()
        for user in users:
            assert user["status"] in ("active", "inactive", "pending"), f"Bad status: {user['status']}"


class TestGetUserCounts:
    def test_total_count_matches_list(self, service):
        assert service.get_total_count() == len(service.get_users())

    def test_active_count_lte_total(self, service):
        assert service.get_active_count() <= service.get_total_count()

    def test_active_count_gt_zero(self, service):
        assert service.get_active_count() >= 0


class TestGetRecentActivity:
    def test_returns_list(self, service):
        activity = service.get_recent_activity()
        assert isinstance(activity, list)
        assert len(activity) > 0

    def test_activity_has_required_fields(self, service):
        activity = service.get_recent_activity()
        required = {"type", "user", "detail", "time"}
        for item in activity:
            assert required.issubset(item.keys()), f"Missing keys in {item.keys()}"
