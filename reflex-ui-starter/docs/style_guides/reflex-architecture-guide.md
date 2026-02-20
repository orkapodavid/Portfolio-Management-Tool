# Reflex Architecture Guide

## Key Concepts

### 4-Region Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Region 1: Top Navigation (40px)  — Module tabs, bell, user  │
├─────────────────────────────────────────────────────────────┤
│ Region 2: App Header             — KPI strip, top movers    │
├───────────────────────────────────────────┬─────────────────┤
│ Region 3: Contextual Workspace           │ Region 4:       │
│  ┌─ Subtab bar (28px) ──────────────┐    │ Notification    │
│  │ Overview | Analytics              │    │ Sidebar (220px) │
│  ├──────────────────────────────────────┤ │                 │
│  │                                      │ │ [Alert cards]   │
│  │  Page Content                        │ │ [Filter tabs]   │
│  │  (scrollable)                        │ │                 │
│  │                                      │ │                 │
│  └──────────────────────────────────────┘ │                 │
└───────────────────────────────────────────┴─────────────────┘
```

### State Architecture

- **UIState**: Global — active module, subtab, sidebar toggle, mobile menu
- **AppHeaderState**: KPI data, top movers, portfolio values
- **NotificationSidebarState**: Notifications, filtering, infinite scroll, mark read, jump-to-row
- **Module states**: Composed via mixins (e.g., `DashboardState = OverviewMixin + AnalyticsMixin`)

### Styling

- **Tailwind CSS v3** via `rx.plugins.TailwindV3Plugin()`
- Constants in `constants.py` for design tokens
- All classes inline via `class_name=`

### Component Patterns

```python
# Standard page pattern
def my_page() -> rx.Component:
    return module_layout(
        content=my_content(),
        module_name="Dashboard",
        subtab_name="MyTab",
        subtabs=UIState.MODULE_SUBTABS["Dashboard"],
    )
```

### Route Pattern

```python
# In starter_app.py
app.add_page(
    my_page,
    route="/dashboard/my-tab",
    on_load=[
        UIState.set_active_module("Dashboard"),
        DashboardState.set_dashboard_subtab("MyTab"),
        DashboardState.load_dashboard_module_data,  # dispatches to mixin
    ],
    title="Dashboard — MyTab",
)
```

### Mixin Event Dispatch

```python
# In the composed state, dispatch to mixin handlers via type(self)
@rx.event
async def load_dashboard_module_data(self):
    if self.active_dashboard_subtab == "Overview":
        yield type(self).load_overview_data      # ← correct
    # NEVER: self.load_overview_data()           # ← wrong
    # NEVER: OverviewMixin.load_overview_data    # ← wrong
```

### Key Reflex Patterns

- Use `rx.cond()` for conditionals, not Python `if`
- Use `rx.foreach()` to iterate over state vars
- Use `rx.match()` for multi-value conditionals
- State vars must be serializable (dict, list, str, int, float, bool)
- Use `TypedDict` for structured data in state lists
- `@rx.var` for computed properties, `@rx.event` for event handlers
