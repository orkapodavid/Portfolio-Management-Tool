"""
Context Menu builder for AG Grid.

Generates a `getContextMenuItems` JS callback that prepends custom items
(e.g. "Rerun", "Kill") before the built-in AG Grid context menu entries.

Architecture:
    - Custom menu item clicks write action + row data to a visually-hidden
      <input> element and fire a React-compatible input event
    - Reflex's on_change handler on that input dispatches to the state
    - This avoids needing direct JS→Reflex websocket dispatch from raw JS

Usage:
    from starter_app.components.shared.ag_grid_config.context_menu import (
        build_context_menu,
        context_menu_dispatch_input,
    )

    # In your component:
    rx.box(
        context_menu_dispatch_input(
            target_id="ops_ctx",
            on_action=OperationsState.handle_context_menu_action,
        ),
        create_standard_grid(
            ...,
            get_context_menu_items=build_context_menu(
                target_id="ops_ctx",
                items=[
                    {"name": "Rerun", "icon": "🔄"},
                    {"name": "Kill",  "icon": "🛑"},
                ],
            ),
        ),
    )
"""

import reflex as rx


def build_context_menu(
    target_id: str,
    items: list[dict],
    *,
    include_defaults: bool = True,
) -> rx.Var:
    """
    Build a getContextMenuItems JS callback for AG Grid Enterprise.

    Args:
        target_id: ID of the hidden input that receives action dispatches.
        items: List of custom menu items. Each dict has:
            - name (str): Display label shown in the menu
            - icon (str, optional): Emoji or short HTML icon string
        include_defaults: Append built-in AG Grid items (copy, export).

    Returns:
        rx.Var containing the JS callback function.
    """
    custom_items_js_parts = []
    for item in items:
        name = item["name"]
        icon = item.get("icon", "")
        icon_html = (
            f'<span style="font-size:14px;margin-right:6px">{icon}</span>'
            if icon
            else ""
        )
        # The action writes a JSON payload to the hidden input then triggers
        # a React-compatible input event so Reflex's on_change fires.
        # We use Object.getOwnPropertyDescriptor to call React's synthetic
        # setter, which is required for React to detect the value change.
        custom_items_js_parts.append(
            f"""{{
                name: '{name}',
                icon: '{icon_html}',
                action: () => {{
                    const el = document.getElementById('{target_id}');
                    if (el) {{
                        const rowData = params.node ? params.node.data : {{}};
                        const payload = JSON.stringify({{
                            action: '{name}',
                            row: rowData
                        }});
                        const nativeSetter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value'
                        ).set;
                        nativeSetter.call(el, payload);
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            }}"""
        )

    # Build the full JS array
    parts = ", ".join(custom_items_js_parts)
    separator = "'separator'," if custom_items_js_parts and include_defaults else ""
    defaults = (
        "'copy', 'copyWithHeaders', 'separator', 'export'"
        if include_defaults
        else ""
    )

    js_body = f"[{parts}, {separator} {defaults}]"
    return rx.Var(f"(params) => {js_body}")


def context_menu_dispatch_input(
    target_id: str,
    on_action,
) -> rx.Component:
    """
    Visually-hidden input that bridges AG Grid context menu JS actions
    to Reflex backend events.

    Uses a real text input (not type=hidden) styled to be invisible,
    because React/Reflex only fires on_change for interactive inputs.

    Args:
        target_id: Must match the target_id used in build_context_menu.
        on_action: State event handler that receives the JSON string payload.
                   Should accept a single str argument (JSON-encoded dict with
                   'action' and 'row' keys).
    """
    return rx.el.input(
        id=target_id,
        type="text",
        on_change=on_action,
        tab_index=-1,
        style={
            "position": "absolute",
            "width": "1px",
            "height": "1px",
            "overflow": "hidden",
            "opacity": "0",
            "pointer_events": "none",
            "z_index": "-1",
        },
    )
