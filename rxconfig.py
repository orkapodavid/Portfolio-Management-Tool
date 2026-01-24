"""Reflex configuration file.

Requires:
- Python 3.13 (recommended) or 3.11+
- Python 3.14+ is NOT compatible due to Pydantic V1 limitations
"""

import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

# API_URL is critical for reverse proxy setups (e.g. IIS /pmt)
# It tells the frontend where to connect for websockets and API calls.
frontend_port = int(os.getenv("REFLEX_FRONTEND_PORT", "3001"))
backend_port = int(os.getenv("REFLEX_BACKEND_PORT", "8001"))
api_url = os.getenv("API_URL", f"http://localhost:{backend_port}")

config = rx.Config(
    app_name="app",
    api_url=api_url,
    frontend_path="/pmt",
    plugins=[rx.plugins.TailwindV3Plugin()],
    frontend_port=frontend_port,
    backend_port=backend_port,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    state_manager_mode=os.getenv("REFLEX_STATE_MANAGER_MODE", "redis"),
    redis_url=os.getenv("REFLEX_REDIS_URL"),
)
