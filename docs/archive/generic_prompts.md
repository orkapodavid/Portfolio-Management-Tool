# Generic Prompt: Migrate Reflex SPA to Route-Based Architecture with Modular State Pattern

## Context

I have a Reflex web application that currently uses a state-based Single Page Application (SPA) pattern where all views are rendered at a single route (typically `/`) with navigation handled entirely through state changes. I want to migrate to a route-based architecture where each page/tab has its own URL route.

## Current Architecture Issues

- All pages/tabs accessible from single route (usually `/`)
- Navigation handled via state changes (e.g., `set_active_page()`, `set_active_tab()`)
- URL doesn't update when switching views
- No deep linking or bookmarking support
- Monolithic state files with all logic combined

## Desired Architecture

**Route Structure:**
- Each major section has its own route: `/{section}`
- Each sub-page/tab has its own route: `/{section}/{sub-page}`
- URLs use kebab-case (e.g., `/user-settings`, `/reports/monthly-summary`)

**State Organization:**
- Modular state structure with dedicated folders per section
- State mixin pattern for reusability
- Flat structure following Reflex best practices
- Each sub-page has its own mixin containing its specific logic

**File Structure:**
```
app/
├── pages/
│   └── {section}/
│       ├── {sub_page}_page.py      # One file per route
│       └── ...
├── states/
│   └── {section}/
│       ├── {section}_state.py      # Main state inheriting all mixins
│       ├── mixins/
│       │   ├── {sub_page}_mixin.py # One mixin per sub-page
│       │   └── ...
│       └── types.py                # TypedDict definitions
└── components/
    └── {section}/
        └── {section}_views.py      # View components
```

## Tasks

### Phase 1: Investigation & Planning (2-4 hours)

1. **Analyze Current Structure:**
   - Identify all pages/tabs that need routes
   - Map current state management approach
   - Document component dependencies
   - List all navigation points

2. **Design URL Structure:**
   - Define route hierarchy
   - Map URLs to file paths
   - Choose naming conventions (kebab-case recommended)
   - Identify default/root routes

3. **Create Design Document:**
   - Document current vs. proposed architecture
   - Create route mapping table
   - Define state organization pattern
   - Outline migration steps

### Phase 2: State Restructuring (8-12 hours per section)

1. **Create Modular State Structure:**
   - Create `app/states/{section}/` folders
   - Extract sub-page logic into separate mixins
   - Create main state class inheriting all mixins
   - Create `types.py` for TypedDict definitions

2. **Mixin Pattern Template:**
```python
# app/states/{section}/mixins/{sub_page}_mixin.py
import reflex as rx
from app.states.{section}.types import {DataItem}
from app.services import {Service}

class {SubPage}Mixin(rx.State, mixin=True):
    """State mixin for {SubPage} sub-page."""
    
    # State variables
    {sub_page}_data: list[{DataItem}] = []
    is_loading_{sub_page}: bool = False
    {sub_page}_error: str = ""
    
    # Data loading
    async def load_{sub_page}_data(self):
        """Load data when page accessed."""
        self.is_loading_{sub_page} = True
        self.{sub_page}_error = ""
        try:
            service = {Service}()
            self.{sub_page}_data = await service.get_{sub_page}()
        except Exception as e:
            self.{sub_page}_error = str(e)
        finally:
            self.is_loading_{sub_page} = False
    
    # Event handlers
    def handle_{sub_page}_action(self, param):
        """Handle user action."""
        pass
    
    # Computed vars
    @rx.var(cache=True)
    def filtered_{sub_page}_data(self) -> list[{DataItem}]:
        """Apply filters to data."""
        return self.{sub_page}_data
```

3. **Module State Composition:**
```python
# app/states/{section}/{section}_state.py
import reflex as rx
from app.states.{section}.mixins.{sub_page1}_mixin import {SubPage1}Mixin
from app.states.{section}.mixins.{sub_page2}_mixin import {SubPage2}Mixin

class {Section}State(
    {SubPage1}Mixin,
    {SubPage2}Mixin,
    rx.State,
):
    """Main {Section} state with all sub-page mixins."""
    
    # Module-level shared state
    active_{section}_tab: str = "Default"
    
    # Coordination methods if needed
    async def refresh_active_tab(self):
        """Refresh data for currently active tab."""
        if self.active_{section}_tab == "SubPage1":
            await self.load_{sub_page1}_data()
        elif self.active_{section}_tab == "SubPage2":
            await self.load_{sub_page2}_data()
```

### Phase 3: Page Creation (4-6 hours per section)

1. **Create Page Files:**
```python
# app/pages/{section}/{sub_page}_page.py
import reflex as rx
from app.states.{section}.{section}_state import {Section}State
from app.components.shared.layout import page_layout
from app.components.{section}.{section}_views import {sub_page}_view

def {sub_page}_page() -> rx.Component:
    """Page for {SubPage} view."""
    return page_layout(
        {sub_page}_view(),
        section="{Section}",
        subtitle="{SubPage}"
    )
```

2. **Create Shared Layout (if needed):**
```python
# app/components/shared/layout.py
import reflex as rx

def page_layout(
    content: rx.Component,
    section: str,
    subtitle: str = ""
) -> rx.Component:
    """Shared layout for all pages."""
    return rx.box(
        # Header/navigation
        # Content area
        content,
        # Footer/sidebar
    )
```

### Phase 4: Route Registration (2-3 hours)

1. **Register Routes in app.py:**
```python
# app/app.py
from app.pages.{section}.{sub_page}_page import {sub_page}_page
from app.states.{section}.{section}_state import {Section}State

app = rx.App()

# Section root - redirect to default sub-page
app.add_page(
    {default_sub_page}_page,
    route="/{section}",
    on_load=[
        {Section}State.load_{default_sub_page}_data,
        lambda: {Section}State.set_active_tab("Default")
    ]
)

# Individual sub-page routes
app.add_page(
    {sub_page}_page,
    route="/{section}/{sub-page}",
    title="{SubPage} | {Section}",
    on_load=[
        {Section}State.load_{sub_page}_data,
        lambda: {Section}State.set_active_tab("{SubPage}")
    ]
)
```

### Phase 5: Navigation Updates (3-4 hours)

1. **Update Navigation Components:**
   - Replace `on_click=state.set_page()` with `href="/{section}"`
   - Use `rx.link()` instead of `rx.button()` for navigation
   - Remove state-based navigation event handlers
   - Add active state highlighting based on current URL

2. **Example Navigation Update:**
```python
# Before (state-based)
rx.button(
    "SubPage",
    on_click=State.set_page("SubPage")
)

# After (route-based)
rx.link(
    "SubPage",
    href="/{section}/{sub-page}",
    class_name="nav-link" if active else "nav-link-inactive"
)
```

### Phase 6: Cleanup (2-3 hours)

1. **Remove Old Code:**
   - Delete deprecated state files
   - Remove obsolete navigation event handlers
   - Clean up unused imports
   - Delete duplicate logic

2. **Update Documentation:**
   - Document new routing structure
   - Update component usage examples
   - Create route reference table

### Phase 7: Testing (3-4 hours)

1. **Manual Testing:**
   - Test all routes return 200
   - Verify URL updates on navigation
   - Test browser back/forward buttons
   - Verify deep linking works
   - Test data loads correctly for each page
   - Check navigation highlights

2. **Run Application:**
```bash
# Reflex command
reflex run
# or with uv
uv run reflex run

# Open browser to http://localhost:3000/
# Test each route manually
```

3. **Testing Checklist:**
   - [ ] All routes accessible
   - [ ] URL updates when clicking navigation
   - [ ] Browser navigation (back/forward) works
   - [ ] Direct URL entry works
   - [ ] Data loads without errors
   - [ ] Navigation highlights active page
   - [ ] No console errors
   - [ ] State persists appropriately

## Key Principles

1. **URL Structure:**
   - Use kebab-case for URLs
   - Mirror file system structure
   - Pattern: `/{section}/{sub-page}`

2. **State Organization:**
   - One mixin per sub-page
   - Main state class inherits all mixins
   - Flat structure (avoid deep inheritance)
   - Module-level shared state in main class

3. **Data Loading:**
   - Load data in `on_load` handler
   - Each mixin has its own `load_*_data()` method
   - Only load data for active page

4. **Navigation:**
   - Use `rx.link()` with `href` for navigation
   - Highlight active page/tab based on URL
   - Remove state-based navigation logic

## Expected Benefits

- ✅ Bookmarkable URLs
- ✅ Deep linking support
- ✅ Browser history works correctly
- ✅ Better SEO (if applicable)
- ✅ Modular, maintainable state organization
- ✅ Clear file structure
- ✅ Easier debugging
- ✅ Standard web navigation patterns

## Estimated Timeline

- **Small project** (3-5 sections, 10-15 pages): 20-30 hours
- **Medium project** (6-10 sections, 20-40 pages): 40-60 hours
- **Large project** (10+ sections, 40+ pages): 60-100 hours

## Common Pitfalls to Avoid

1. **Don't:** Keep state-based navigation alongside route-based navigation
2. **Don't:** Create deep state inheritance hierarchies
3. **Don't:** Load all data upfront for all pages
4. **Don't:** Forget to handle module root routes (redirect to default)
5. **Do:** Test thoroughly after each phase
6. **Do:** Keep backward compatibility during migration
7. **Do:** Document the new structure clearly

---
