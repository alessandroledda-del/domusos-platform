from pathlib import Path
import ast
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in ROOT.rglob("*.py"):
    if ".venv" in path.parts:
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        errors.append(f"Python: {path.relative_to(ROOT)}: {exc}")

for path in [
    ROOT / "frontend/package.json",
    ROOT / "frontend/tsconfig.json",
]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON: {path.relative_to(ROOT)}: {exc}")

required = [
    "README.md",
    "VERSION",
    ".env.example",
    ".env.production.example",
    "docker-compose.yml",
    "docker-compose.production.yml",
    "backend/config/settings.py",
    "backend/config/settings_test.py",
    "backend/scripts/entrypoint.sh",
    "frontend/Dockerfile.production",
    "frontend/public/.gitkeep",
    "docs/KNOWN_LIMITATIONS.md",
]

for relative in required:
    if not (ROOT / relative).exists():
        errors.append(f"File mancante: {relative}")

for forbidden in [".env", ".env.production"]:
    if (ROOT / forbidden).exists():
        errors.append(f"File segreto incluso: {forbidden}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Release validation passed.")
