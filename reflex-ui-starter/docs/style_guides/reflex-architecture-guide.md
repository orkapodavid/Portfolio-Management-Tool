# Reflex Architecture Guide

## Key Concepts

### 4-Region Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Region 1: Top Navigation (40px)  — Module tabs, bell, user  │
├─────────────────────────────────────────────────────────────┤
│ Region 2: Performance Header     — KPI strip, top movers    │
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
- **PerformanceHeaderState**: KPI data, top movers, portfolio values
- **NotificationSidebarState**: Notifications, filtering, infinite scroll, mark read
- **Page-specific states**: AG Grid data, form state, etc.

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
# In app.py
app.add_page(
    my_page,
    route="/dashboard/my-tab",
    on_load=[UIState.set_module("Dashboard"), UIState.set_subtab("MyTab")],
    title="Dashboard — MyTab",
)
```

### Key Reflex Patterns

- Use `rx.cond()` for conditionals, not Python `if`
- Use `rx.foreach()` to iterate over state vars
- Use `rx.match()` for multi-value conditionals
- State vars must be serializable (dict, list, str, int, float, bool)
- Use `TypedDict` for structured data in state lists
- `@rx.var` for computed properties, `@rx.event` for event handlers
