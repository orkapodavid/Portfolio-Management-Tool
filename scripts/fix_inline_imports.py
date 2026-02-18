"""Fix inline imports: move `import logging` and `import random` to module level.

Scans all Python files under app/states/ and:
1. Detects inline `import logging` and `import random` (indented imports)
2. Removes them from inside functions/methods
3. Adds them at the top of the file (after existing imports) if not already present
"""

import re
from pathlib import Path

STATES_DIR = Path(__file__).resolve().parent.parent / "app" / "states"


def fix_file(filepath: Path) -> dict:
    """Fix inline imports in a single file. Returns stats."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Check what's already imported at module level
    has_top_logging = False
    has_top_random = False
    for line in lines:
        stripped = line.strip()
        # Module-level import = no leading whitespace (or just 'import X')
        if (
            stripped == "import logging"
            and not line.startswith(" ")
            and not line.startswith("\t")
        ):
            has_top_logging = True
        if (
            stripped == "import random"
            and not line.startswith(" ")
            and not line.startswith("\t")
        ):
            has_top_random = True

    # Count and remove inline imports
    needs_logging = False
    needs_random = False
    new_lines = []
    removed_logging = 0
    removed_random = 0

    for line in lines:
        stripped = line.strip()
        # Inline = indented import
        if stripped == "import logging" and (
            line.startswith(" ") or line.startswith("\t")
        ):
            needs_logging = True
            removed_logging += 1
            # Remove the line and any blank line immediately after
            continue
        if stripped == "import random" and (
            line.startswith(" ") or line.startswith("\t")
        ):
            needs_random = True
            removed_random += 1
            continue
        new_lines.append(line)

    if removed_logging == 0 and removed_random == 0:
        return {"file": str(filepath), "logging_removed": 0, "random_removed": 0}

    # Clean up any resulting double blank lines
    cleaned = []
    prev_blank = False
    for line in new_lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue  # Skip consecutive blanks
        cleaned.append(line)
        prev_blank = is_blank

    # Find insertion point: after the last top-level import block
    insert_idx = 0
    for i, line in enumerate(cleaned):
        stripped = line.strip()
        if (
            (stripped.startswith("import ") or stripped.startswith("from "))
            and not line.startswith(" ")
            and not line.startswith("\t")
        ):
            insert_idx = i + 1

    # Build imports to add
    imports_to_add = []
    if needs_logging and not has_top_logging:
        imports_to_add.append("import logging\n")
    if needs_random and not has_top_random:
        imports_to_add.append("import random\n")

    if imports_to_add:
        for j, imp in enumerate(imports_to_add):
            cleaned.insert(insert_idx + j, imp)

    filepath.write_text("".join(cleaned), encoding="utf-8")

    return {
        "file": filepath.name,
        "logging_removed": removed_logging,
        "random_removed": removed_random,
        "logging_added": needs_logging and not has_top_logging,
        "random_added": needs_random and not has_top_random,
    }


def main():
    results = []
    for py_file in sorted(STATES_DIR.rglob("*.py")):
        if "__pycache__" in str(py_file):
            continue
        result = fix_file(py_file)
        if result["logging_removed"] > 0 or result["random_removed"] > 0:
            results.append(result)

    print(f"\n{'=' * 60}")
    print(f"Fixed {len(results)} files:")
    print(f"{'=' * 60}")
    for r in results:
        parts = []
        if r["logging_removed"]:
            parts.append(f"logging: -{r['logging_removed']}")
        if r["random_removed"]:
            parts.append(f"random: -{r['random_removed']}")
        print(f"  {r['file']:45s} {', '.join(parts)}")

    total_logging = sum(r["logging_removed"] for r in results)
    total_random = sum(r["random_removed"] for r in results)
    print(
        f"\nTotal: removed {total_logging} inline `import logging`, {total_random} inline `import random`"
    )


if __name__ == "__main__":
    main()
