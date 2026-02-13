#!/usr/bin/env python3
"""
Playwright Browser Setup Script

Run this once to install required browsers for E2E testing.

Usage:
    uv run reflex_ag_grid/tests/setup_browsers.py
"""

import subprocess
import sys


def main():
    """Install Playwright browsers."""
    print("=" * 60)
    print("Playwright Browser Setup")
    print("=" * 60)

    # Check if playwright is installed
    try:
        import playwright

        print(f"✓ Playwright version: {playwright.__version__}")
    except ImportError:
        print("✗ Playwright not installed. Installing...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"], check=True
        )

    # Install browsers
    print("\nInstalling Playwright browsers...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✓ Chromium browser installed successfully")
    else:
        print(f"✗ Browser installation failed: {result.stderr}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Setup complete! You can now run E2E tests:")
    print("  uv run reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000")
    print("=" * 60)


if __name__ == "__main__":
    main()
