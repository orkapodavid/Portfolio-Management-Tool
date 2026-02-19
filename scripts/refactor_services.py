"""
Script to refactor mixin files from per-call Service() instantiation
to use the singleton ServiceRegistry.

Transforms:
    from app.services import PnLService
    ...
    service = PnLService()
    data = await service.method()

Into:
    from app.services import services
    ...
    data = await services.pnl.method()
"""

import re
import os

# Mapping: class name -> registry property name
SERVICE_MAP = {
    "PnLService": "pnl",
    "PositionService": "positions",
    "RiskService": "risk",
    "ComplianceService": "compliance",
    "PortfolioToolsService": "portfolio_tools",
    "MarketDataService": "market_data",
    "EMSXService": "emsx",
    "OperationsService": "operations",
    "ReconciliationService": "reconciliation",
    "UserService": "user",
    "InstrumentsService": "instruments",
    "ReverseInquiryService": "reverse_inquiry",
    "EventCalendarService": "event_calendar",
    "EventStreamService": "event_stream",
    "PerformanceHeaderService": "performance_header",
    "NotificationService": "notifications",
    "NotificationRegistry": "notification_registry",
}

# Root of project
ROOT = r"c:\Users\orkap\Desktop\Programming\Portfolio-Management-Tool\app\states"

# Track stats
files_modified = 0
total_replacements = 0


def process_file(filepath):
    global files_modified, total_replacements

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    replacements = 0

    # Find which service classes are instantiated in this file
    # Pattern: service = XxxService() or xxx_service = XxxService()
    instantiation_pattern = re.compile(
        r"(\w+)\s*=\s*(" + "|".join(re.escape(k) for k in SERVICE_MAP.keys()) + r")\(\)"
    )

    matches = instantiation_pattern.findall(content)
    if not matches:
        return  # No service instantiations

    # Collect unique service classes used and their local var names
    services_used = {}  # class_name -> set of local var names
    for var_name, class_name in matches:
        if class_name not in services_used:
            services_used[class_name] = set()
        services_used[class_name].add(var_name)

    # Step 1: Remove old service class imports
    for class_name in services_used:
        # Remove from "from app.services import XxxService"
        # Handle single import: from app.services import XxxService
        single_import = re.compile(
            r"^from app\.services import " + re.escape(class_name) + r"\s*\n",
            re.MULTILINE,
        )
        content = single_import.sub("", content)

        # Also handle: from app.services.xxx import XxxService
        specific_import = re.compile(
            r"^from app\.services\.\w+(?:\.\w+)* import "
            + re.escape(class_name)
            + r"\s*\n",
            re.MULTILINE,
        )
        content = specific_import.sub("", content)

    # Step 2: Add "from app.services import services" if not already present
    if (
        "from app.services import services" not in content
        and "from app.services.registry import services" not in content
    ):
        # Insert after the last "from app." or "import" line
        # Find the right insertion point
        lines = content.split("\n")
        insert_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("from ") or stripped.startswith("import "):
                insert_idx = i + 1
            elif (
                stripped
                and not stripped.startswith("#")
                and not stripped.startswith('"""')
                and insert_idx > 0
            ):
                break
        lines.insert(insert_idx, "from app.services import services")
        content = "\n".join(lines)

    # Step 3: Replace "service = XxxService()" and subsequent "service.method()" calls
    for class_name, var_names in services_used.items():
        registry_prop = SERVICE_MAP[class_name]

        for var_name in var_names:
            # Remove the instantiation line: "            service = XxxService()"
            instantiation_line = re.compile(
                r"^(\s*)"
                + re.escape(var_name)
                + r"\s*=\s*"
                + re.escape(class_name)
                + r"\(\)\s*\n",
                re.MULTILINE,
            )
            content = instantiation_line.sub("", content)
            replacements += 1

            # Replace "service.method(" with "services.registry_prop.method("
            # But only if var_name is the local variable (e.g., "service", "market_service")
            method_call = re.compile(r"\b" + re.escape(var_name) + r"\.")
            content = method_call.sub(f"services.{registry_prop}.", content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        files_modified += 1
        total_replacements += replacements
        print(
            f"  ✓ {os.path.relpath(filepath, ROOT)} ({replacements} instantiations removed)"
        )


def main():
    global files_modified, total_replacements

    print(f"Scanning {ROOT} for service instantiations...\n")

    for dirpath, dirnames, filenames in os.walk(ROOT):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                process_file(filepath)

    print(f"\n{'=' * 50}")
    print(f"Files modified: {files_modified}")
    print(f"Instantiations removed: {total_replacements}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
