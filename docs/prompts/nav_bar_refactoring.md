# Task: Implement Shared Reflex Navbar with Existing Architecture and Styles

You are working in an existing Reflex app codebase that already follows the architecture described in:

- `docs/style_guides/reflex-architecture-guide.md`
- `docs/style_guides/reflex-style-migration-prompts.md`

Implement a **shared top navigation bar (Region 1)** that matches the **navigation example in Section 3.4 "Region 1: Navigation Component"** of `reflex-architecture-guide.md`, using the **same styling and interaction patterns**.

---

## Context and Constraints

- **Framework**: Reflex (Python)
- **Styling**: Tailwind CSS via `class_name` (not `style={}`)
- **State**:
  - Use a global `UIState` in `app/states/ui/ui_state.py` similar to the guide:
    - `active_module: str`
    - `is_sidebar_open: bool`
    - Event handlers: `set_module()`, `toggle_sidebar()`, etc.
- **Layout**:
  - This navbar is **Region 1** of the multi-region layout:
    - Fixed height: **56px**
    - Background: **dark (`bg-gray-900`)**
    - Text: **white**
    - Used at the top of the app (e.g. in `app/app.py`).

Follow all relevant best practices from the architecture guide:
- Flat state structure based on `rx.State`
- `UIState` for navigation/sidebar toggles
- `rx.el.*` for HTML elements, `rx.*` for Radix components
- Tailwind via `class_name` and numeric sizes for Radix components if used

---

## File and API Requirements

1. **Create/Update file**: `app/components/shared/navigation.py`
2. **Imports**:
   - `import reflex as rx`
   - `from app.states.ui.ui_state import UIState`
3. **Public API**:
   - `nav_item(name: str, icon: str, route: str) -> rx.Component`
   - `navigation() -> rx.Component`
4. **Usage**:
   - `navigation()` will be used in the main layout (e.g. in `app/app.py` as Region 1).

---

## Navbar Behavior and State Integration

Implement the nav in a way that:

- Uses `UIState.active_module` to determine which module is active.
- Optionally calls `UIState.set_module()` when a module nav item is clicked (you can either:
  - use `href` routing only, or
  - combine `on_click=UIState.set_module` with navigation, as long as it remains simple and idiomatic).
- Uses `UIState.toggle_sidebar` for the bell icon button on the right to open/close the sidebar.
- Keeps all logic inside the component **stateless** apart from reading from `UIState`.

---

## Styling and Layout Requirements (Match the Guide Exactly)

Match the styles from the guide as closely as possible:

- **Top nav container**:
  - `rx.el.nav` wrapper
  - Class:  
    `class_name="h-[56px] bg-gray-900 text-white flex items-center shrink-0"`
- **Inner flex container**:
  - `class_name="flex items-center w-full px-4"`

- **Left side: brand**:
  - Icon: `rx.icon("box", size=24, class_name="text-blue-500")`
  - App name text: `"App Name"` (you may adjust name but keep same styling).
  - Brand container:  
    `class_name="flex items-center"`

- **Center: navigation items**:
  - A row of module links using `nav_item(...)`.
  - Container class:  
    `class_name="flex items-center gap-1 ml-8"`
  - Implement `nav_item` as:
    - A `rx.link` wrapping a `rx.el.button`.
    - Button structure:
      - Left: `rx.icon(icon, size=16, class_name=rx.cond(is_active, "text-white", "text-gray-400"))`
      - Right: `rx.el.span(name, class_name="text-sm ml-2 hidden md:inline")`
    - Active vs inactive styles using `rx.cond` on `is_active`:
      - Active: `"flex items-center px-3 py-2 bg-blue-600 rounded-md"`
      - Inactive: `"flex items-center px-3 py-2 hover:bg-gray-700 rounded-md transition-colors"`

- **Right side: actions**:
  - Container class:  
    `class_name="flex items-center ml-auto text-gray-300"`
  - First button: notification/bell
    - Icon: `rx.icon("bell", size=18)`
    - `on_click=UIState.toggle_sidebar`
    - Class: `"p-2 hover:bg-gray-700 rounded-md transition-colors"`
  - Second button: user/profile
    - Icon: `rx.icon("user", size=18)`
    - Class: `"p-2 hover:bg-gray-700 rounded-md transition-colors ml-2"`

The styling should visually match the navigation reference in the architecture guide.

---

## Example Structure (Replicate This, Adjusting Names/Routes Only)

Use the following implementation as the **baseline** and adapt only the module names/routes as needed for this app:

```python
import reflex as rx
from app.states.ui.ui_state import UIState

def nav_item(name: str, icon: str, route: str) -> rx.Component:
    """Single navigation item with active state styling."""
    is_active = UIState.active_module == name
    return rx.link(
        rx.el.button(
            rx.icon(
                icon,
                size=16,
                class_name=rx.cond(
                    is_active,
                    "text-white",
                    "text-gray-400",
                ),
            ),
            rx.el.span(
                name,
                class_name="text-sm ml-2 hidden md:inline",
            ),
            class_name=rx.cond(
                is_active,
                "flex items-center px-3 py-2 bg-blue-600 rounded-md",
                "flex items-center px-3 py-2 hover:bg-gray-700 rounded-md transition-colors",
            ),
        ),
        href=route,
    )

def navigation() -> rx.Component:
    """Top navigation bar (Region 1) matching the architecture guide styles."""
    return rx.el.nav(
        rx.el.div(
            # Left: Brand
            rx.el.div(
                rx.icon("box", size=24, class_name="text-blue-500"),
                rx.el.span(
                    "App Name",
                    class_name="font-bold text-lg ml-2 text-white",
                ),
                class_name="flex items-center",
            ),
            # Center: Module navigation items
            rx.el.div(
                nav_item("Dashboard", "layout-dashboard", "/"),
                nav_item("Module 1", "folder", "/module-1"),
                nav_item("Module 2", "users", "/module-2"),
                nav_item("Settings", "settings", "/settings"),
                class_name="flex items-center gap-1 ml-8",
            ),
            # Right: Actions (sidebar toggle + user)
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", size=18),
                    on_click=UIState.toggle_sidebar,
                    class_name="p-2 hover:bg-gray-700 rounded-md transition-colors",
                ),
                rx.el.button(
                    rx.icon("user", size=18),
                    class_name="p-2 hover:bg-gray-700 rounded-md transition-colors ml-2",
                ),
                class_name="flex items-center ml-auto text-gray-300",
            ),
            class_name="flex items-center w-full px-4",
        ),
        class_name="h-[56px] bg-gray-900 text-white flex items-center shrink-0",
    )
```

**Important**:
- Keep the **structure and Tailwind classes exactly as above** to match the design in the `reflex-architecture-guide.md`.
- You may update:
  - App name string
  - Module names (`"Module 1"`, `"Module 2"`) and routes (`"/module-1"`, etc.)
- Do **not** change:
  - Layout structure
  - Core class names
  - Interaction patterns (active highlighting, hover, sidebar toggle)

---

## Deliverables

- A complete `app/components/shared/navigation.py` file implementing `nav_item` and `navigation` as described.
- Code compiled and formatted consistently with the rest of the Reflex project.
- No changes to business logic or unrelated parts of the app.