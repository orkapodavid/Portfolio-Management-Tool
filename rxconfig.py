"""Reflex configuration file.

Requires:
- Python 3.13 (recommended) or 3.11+
- Python 3.14+ is NOT compatible due to Pydantic V1 limitations
"""

import reflex as rx
import os

# API_URL is critical for reverse proxy setups (e.g. IIS /pmt)
# It tells the frontend where to connect for websockets and API calls.
api_url = os.getenv("API_URL", "http://localhost:8000")

config = rx.Config(
    app_name="app",
    api_url=api_url,
    frontend_path="/pmt",
    plugins=[rx.plugins.TailwindV3Plugin()],
    frontend_port=3001,
    backend_port=8001,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
