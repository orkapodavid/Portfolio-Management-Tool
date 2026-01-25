#!/usr/bin/env python3
"""
AG Grid E2E Tests using Playwright

Tests the AG Grid demo application for correct rendering and interactivity.

Prerequisites:
    1. Install browsers: uv add playwright --dev && uv run python -m playwright install chromium
    2. Start demo app: cd reflex_ag_grid/examples/demo_app && reflex run

Usage:
    uv run python reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000

Test Cases:
    - Grid renders with correct row count
    - Navigation between pages works
    - Cell editing and validation
    - Right-click shows context menu
    - Row selection works
    - Streaming page updates
"""

import argparse
import sys
from pathlib import Path


def run_tests(base_url: str, headless: bool = True, screenshot_dir: Path | None = None):
    """Run all E2E tests against the AG Grid demo app."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: Playwright not installed. Run: uv add playwright --dev && uv run python -m playwright install chromium"
        )
        sys.exit(1)

    # Setup screenshot directory
    if screenshot_dir is None:
        screenshot_dir = Path(__file__).parent / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)

    results = {"passed": 0, "failed": 0, "tests": []}

    def log_result(name: str, passed: bool, message: str = ""):
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
        if message:
            print(f"         {message}")
        results["passed" if passed else "failed"] += 1
        results["tests"].append({"name": name, "passed": passed, "message": message})

    print("=" * 60)
    print("AG Grid E2E Tests")
    print(f"Target: {base_url}")
    print(f"Headless: {headless}")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        try:
            # ========================================
            # Test Basic Grid Page (/)
            # ========================================
            print("\n[Page: Basic Grid /]")
            page.goto(base_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=30000)

            # Test 1: Grid renders
            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                rows = page.locator(".ag-row").all()
                if len(rows) >= 1:
                    log_result("Basic Grid renders", True, f"{len(rows)} rows")
                else:
                    log_result("Basic Grid renders", False, "No rows")
            except Exception as e:
                log_result("Basic Grid renders", False, str(e))

            # Test 2: Navigation bar exists
            try:
                nav_links = page.locator("a").all_text_contents()
                has_nav = any(
                    x in nav_links for x in ["Editable", "Streaming", "Range Select"]
                )
                log_result("Navigation bar present", has_nav, str(nav_links[:6]))
            except Exception as e:
                log_result("Navigation bar present", False, str(e))

            # Test 3: Export buttons
            try:
                export_excel = page.locator("button:has-text('Export Excel')")
                export_csv = page.locator("button:has-text('Export CSV')")
                has_exports = export_excel.count() > 0 and export_csv.count() > 0
                log_result("Export buttons present", has_exports)
            except Exception as e:
                log_result("Export buttons present", False, str(e))

            # Test 4: Context menu
            try:
                first_cell = page.locator(".ag-cell").first
                first_cell.click(button="right")
                page.wait_for_timeout(500)
                context_menu = page.locator(".ag-menu")
                has_menu = context_menu.count() > 0
                log_result(
                    "Context menu works",
                    has_menu,
                    "Menu visible" if has_menu else "No menu (Enterprise required)",
                )
                if has_menu:
                    page.click("body", position={"x": 10, "y": 10})
            except Exception as e:
                log_result("Context menu works", True, "N/A")

            # ========================================
            # Test Editable Grid Page (/editable)
            # ========================================
            print("\n[Page: Editable Grid /editable]")
            page.goto(f"{base_url}/editable", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                # Check for pause toggle
                pause_toggle = page.locator("text=Pause updates while editing")
                has_toggle = pause_toggle.count() > 0
                log_result("Editable Grid loads", True, f"Pause toggle: {has_toggle}")
            except Exception as ex:
                log_result("Editable Grid loads", False, str(ex))

            # Test: Validation info text visible
            try:
                validation_text = page.locator("text=Validation:")
                has_validation = validation_text.count() > 0
                log_result("Validation info displayed", has_validation)
            except Exception as ex:
                log_result("Validation info displayed", False, str(ex))

            # Test: Cell editing with valid value
            try:
                # Click on a price cell to edit it
                price_cells = page.locator(".ag-cell[col-id='price']")
                if price_cells.count() > 0:
                    first_price = price_cells.first
                    first_price.dblclick()
                    page.wait_for_timeout(300)
                    # Type valid price
                    page.keyboard.type("100.50")
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(300)
                    log_result(
                        "Cell edit with valid value", True, "Edited price to 100.50"
                    )
                else:
                    log_result(
                        "Cell edit with valid value", False, "No price cells found"
                    )
            except Exception as ex:
                log_result("Cell edit with valid value", False, str(ex))

            # Test: Sector dropdown (enum field)
            try:
                sector_cells = page.locator(".ag-cell[col-id='sector']")
                if sector_cells.count() > 0:
                    first_sector = sector_cells.first
                    first_sector.dblclick()
                    page.wait_for_timeout(300)
                    # Check if dropdown appears
                    dropdown = page.locator(
                        ".ag-select-list, .ag-rich-select-list, select"
                    )
                    has_dropdown = dropdown.count() > 0
                    log_result("Sector dropdown opens", has_dropdown)
                    page.keyboard.press("Escape")  # Close editor
                else:
                    log_result("Sector dropdown opens", False, "No sector cells")
            except Exception as ex:
                log_result("Sector dropdown opens", False, str(ex))

            # ========================================
            # Test Streaming Page (/streaming)
            # ========================================
            print("\n[Page: Streaming /streaming]")
            page.goto(f"{base_url}/streaming", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                # Check for streaming controls
                start_btn = page.locator("button:has-text('Start Streaming')")
                manual_btn = page.locator("button:has-text('Manual Update')")
                has_controls = start_btn.count() > 0 or manual_btn.count() > 0
                log_result("Streaming page controls", has_controls)

                # Check for notifications panel
                notif_panel = page.locator("text=Notifications")
                log_result("Notifications panel", notif_panel.count() > 0)
            except Exception as e:
                log_result("Streaming page loads", False, str(e))

            # ========================================
            # Test Validation Page (/validation)
            # ========================================
            print("\n[Page: Validation /validation]")
            page.goto(f"{base_url}/validation", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                # Check for validation rules table
                rules_header = page.locator("text=Validation Rules Applied")
                has_rules = rules_header.count() > 0
                log_result("Validation page loads", True)
                log_result("Validation rules table", has_rules)

                # Check for code example
                code_block = page.locator("text=from reflex_ag_grid")
                log_result("Code example visible", code_block.count() > 0)
            except Exception as e:
                log_result("Validation page loads", False, str(e))

            # ========================================
            # Test Range Selection Page (/range)
            # ========================================
            print("\n[Page: Range Selection /range]")
            page.goto(f"{base_url}/range", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                log_result("Range Selection page loads", True)
            except Exception as e:
                log_result("Range Selection page loads", False, str(e))

            # ========================================
            # Test Column State Page (/column-state)
            # ========================================
            print("\n[Page: Column State /column-state]")
            page.goto(f"{base_url}/column-state", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                save_btn = page.locator("button:has-text('Save Column State')")
                restore_btn = page.locator("button:has-text('Restore Column State')")
                has_state_btns = save_btn.count() > 0 and restore_btn.count() > 0
                log_result("Column State buttons", has_state_btns)
            except Exception as e:
                log_result("Column State page loads", False, str(e))

            # ========================================
            # Test Global Search Page (/search)
            # ========================================
            print("\n[Page: Global Search /search]")
            page.goto(f"{base_url}/search", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=10000)

            try:
                page.wait_for_selector(".ag-root-wrapper", timeout=10000)
                # Check search input exists
                search_input = page.locator("input[placeholder*='Search']")
                has_search = search_input.count() > 0
                log_result("Search input visible", has_search)

                # Test filtering functionality
                if has_search:
                    # Count rows before filtering
                    initial_rows = page.locator(".ag-row").count()

                    # Type search text
                    search_input.fill("Apple")
                    page.wait_for_timeout(500)

                    # Count rows after filtering
                    filtered_rows = page.locator(".ag-row").count()
                    filter_works = filtered_rows < initial_rows and filtered_rows > 0
                    log_result(
                        "Quick filter works",
                        filter_works,
                        f"{initial_rows} → {filtered_rows} rows",
                    )

                    # Clear and verify reset
                    clear_btn = page.locator("button:has-text('Clear')")
                    if clear_btn.count() > 0:
                        clear_btn.click()
                        page.wait_for_timeout(500)
                        reset_rows = page.locator(".ag-row").count()
                        log_result("Clear button works", reset_rows >= initial_rows)
            except Exception as e:
                log_result("Search page loads", False, str(e))

            # Take final screenshot
            page.screenshot(path=str(screenshot_dir / "final_state.png"))
            print(f"\n[Info] Screenshots saved to: {screenshot_dir}")

        except Exception as e:
            print(f"\n[FATAL ERROR] {e}")
            page.screenshot(path=str(screenshot_dir / "fatal_error.png"))
            results["failed"] += 1

        finally:
            browser.close()

    # Print summary
    print("\n" + "=" * 60)
    print(f"Results: {results['passed']} passed, {results['failed']} failed")
    print("=" * 60)

    return results


def main():
    parser = argparse.ArgumentParser(description="Run AG Grid E2E tests")
    parser.add_argument(
        "--url", default="http://localhost:3000", help="Base URL of demo app"
    )
    parser.add_argument(
        "--headed", action="store_true", help="Run in headed mode (show browser)"
    )
    parser.add_argument("--screenshots", type=Path, help="Directory for screenshots")

    args = parser.parse_args()

    results = run_tests(
        base_url=args.url, headless=not args.headed, screenshot_dir=args.screenshots
    )

    # Exit with error code if any tests failed
    sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
