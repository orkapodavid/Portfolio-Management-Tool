"""Reflex configuration file for the starter app.

Requires:
- Python 3.13 (recommended) or 3.11+
- Python 3.14+ is NOT compatible due to Pydantic V1 limitations
"""

import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

frontend_port = int(os.getenv("REFLEX_FRONTEND_PORT", "3000"))
backend_port = int(os.getenv("REFLEX_BACKEND_PORT", "8000"))
api_url = os.getenv("API_URL", f"http://localhost:{backend_port}")

config = rx.Config(
    app_name="starter_app",
    api_url=api_url,
    plugins=[rx.plugins.TailwindV3Plugin()],
    frontend_port=frontend_port,
    backend_port=backend_port,
    state_manager_mode=os.getenv("REFLEX_STATE_MANAGER_MODE", "memory"),
)
