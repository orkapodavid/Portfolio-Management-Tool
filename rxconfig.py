"""Reflex configuration file.

Requires:
- Python 3.13 (recommended) or 3.11+
- Python 3.14+ is NOT compatible due to Pydantic V1 limitations
"""

import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[rx.plugins.TailwindV3Plugin()],
    frontend_port=3001,
    backend_port=8001,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
