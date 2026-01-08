import reflex as rx
from typing import TypedDict
from app.services import NotificationService


class Notification(TypedDict):
    id: str
    category: str
    title: str
    message: str
    time_ago: str
    is_read: bool
    icon: str
    color: str


class NotificationState(rx.State):
    """
    State for managing notifications.
    
    Uses NotificationService to fetch and manage notifications from the backend.
    Demonstrates async state patterns, loading states, and error handling.
    """
    
    # Data
    notifications: list[Notification] = []
    selected_category: str = "All"
    categories: list[str] = ["All", "Alerts", "Portfolio", "News", "System"]
    
    # UI State
    is_loading: bool = False
    error: str = ""
    
    @rx.var
    def filtered_notifications(self) -> list[Notification]:
        """Computed var: Filter notifications by selected category."""
        if self.selected_category == "All":
            return self.notifications
        return [
            n for n in self.notifications if n["category"] == self.selected_category
        ]
    
    @rx.var
    def unread_count(self) -> int:
        """Computed var: Count of unread notifications."""
        return len([n for n in self.notifications if not n["is_read"]])
    
    # Lifecycle
    async def on_load(self):
        """Load notifications when page/component loads."""
        await self.load_notifications()
    
    # Data Loading
    async def load_notifications(self):
        """
        Load notifications from NotificationService.
        
        Demonstrates:
        - Loading state management
        - Error handling
        - Service integration
        """
        self.is_loading = True
        self.error = ""
        
        try:
            service = NotificationService()
            
            # Fetch notifications (optionally filtered by category)
            category_filter = None if self.selected_category == "All" else self.selected_category
            self.notifications = await service.get_notifications(category=category_filter)
            
        except Exception as e:
            self.error = f"Failed to load notifications: {str(e)}"
        finally:
            self.is_loading = False
    
    # Actions
    @rx.event
    def set_category(self, category: str):
        """
        Change the selected category filter.
        
        Note: Since we're using computed var for filtering,
        we don't need to reload from service.
        """
        self.selected_category = category
    
    @rx.event
    async def mark_all_read(self):
        """Mark all visible notifications as read."""
        try:
            service = NotificationService()
            
            # Mark all as read (respecting current filter)
            category_filter = None if self.selected_category == "All" else self.selected_category
            count = await service.mark_all_as_read(category=category_filter)
            
            # Reload notifications to get updated data
            await self.load_notifications()
            
            return rx.toast.success(
                f"Marked {count} notification(s) as read",
                position="bottom-right"
            )
        except Exception as e:
            return rx.toast.error(
                f"Failed to mark notifications as read: {str(e)}",
                position="bottom-right"
            )
    
    @rx.event
    async def clear_all(self):
        """Clear all visible notifications."""
        try:
            service = NotificationService()
            
            # Delete all (respecting current filter)
            category_filter = None if self.selected_category == "All" else self.selected_category
            count = await service.delete_all(category=category_filter)
            
            # Reload notifications to reflect changes
            await self.load_notifications()
            
            return rx.toast.success(
                f"Cleared {count} notification(s)",
                position="bottom-right"
            )
        except Exception as e:
            return rx.toast.error(
                f"Failed to clear notifications: {str(e)}",
                position="bottom-right"
            )
    
    @rx.event
    async def mark_read(self, notification_id: str):
        """Mark a single notification as read."""
        try:
            service = NotificationService()
            success = await service.mark_as_read(notification_id)
            
            if success:
                # Update the local state instead of full reload for better UX
                updated_notifications = []
                for n in self.notifications:
                    if n["id"] == notification_id:
                        n = {**n, "is_read": True}
                    updated_notifications.append(n)
                self.notifications = updated_notifications
                
        except Exception as e:
            return rx.toast.error(
                f"Failed to mark notification as read: {str(e)}",
                position="bottom-right"
            )
    
    @rx.event
    async  def refresh(self):
        """Refresh notifications from server."""
        await self.load_notifications()
        return rx.toast.info("Notifications refreshed", position="bottom-right")
