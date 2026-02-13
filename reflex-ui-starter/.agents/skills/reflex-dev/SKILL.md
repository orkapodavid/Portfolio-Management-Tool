---
name: reflex-dev
description: Reflex UI development patterns, component architecture, and Tailwind styling
---

# Reflex Development Skill

## Key Patterns

### Component Architecture
- All pages use `module_layout()` wrapper from `starter_app/components/shared/module_layout.py`
- State is managed via `rx.State` subclasses in `starter_app/states/`
- Use `@rx.var` for computed properties, `@rx.event` for event handlers
- Use `TypedDict` for structured data in state lists

### Styling
- Tailwind CSS v3 via inline `class_name=` strings
- Design tokens in `starter_app/constants.py`
- Font sizes: `text-[7px]` to `text-[11px]` for compact UI, `text-xs` standard
- Font weights: `font-bold`, `font-black` (900) for emphasis
- Colors: Use constants like `POSITIVE_GREEN`, `NEGATIVE_RED`, `NAV_BG`

### State Management
- `UIState`: Navigation (active module, subtab, sidebar, mobile menu)
- `NotificationSidebarState`: Notification list, filtering, CRUD
- `PerformanceHeaderState`: KPI metrics, top movers
- Page-specific states: Defined alongside pages (e.g., `AnalyticsState`)

### Adding a New Module
1. Create pages in `starter_app/pages/your_module/`
2. Add module config to `UIState.MODULE_SUBTABS` and `MODULE_ICONS`
3. Add nav button in `top_navigation.py`
4. Add routes in `app.py` with `on_load` handlers

### Reflex Gotchas
- Use `rx.cond()` not Python `if` for conditional rendering
- Use `rx.foreach()` not Python loops for iterating state vars
- State vars must be JSON-serializable
- `rx.var` computed vars are cached and reactive
- Always pass event handler references, not calls: `on_click=State.handler`
- For event handlers with args: `on_click=State.handler(arg)`
