from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def patch_file(path):
    p = ROOT / path
    if not p.exists():
        print(f"SKIP missing: {path}")
        return

    text = p.read_text(encoding="utf-8")

    text = text.replace(
        'ROOT = Path(r"D:\\projects\\hantavirus_map")',
        'ROOT = Path(__file__).resolve().parents[1]'
    )

    text = text.replace(
        'ROOT=Path(r"D:\\projects\\hantavirus_map")',
        'ROOT=Path(__file__).resolve().parents[1]'
    )

    text = text.replace(
        '"curl.exe",',
        '("curl.exe" if __import__("sys").platform.startswith("win") else "curl"),'
    )

    p.write_text(text, encoding="utf-8")
    print(f"PATCHED: {path}")

for file in [
    "tools/update_official_confirmed.py",
    "tools/update_arcgis_signal.py",
    "tools/build_site_data.py",
    "tools/validate_data.py",
    "tools/audit_2026_cases.py"
]:
    patch_file(file)

(ROOT / ".nojekyll").write_text("", encoding="utf-8")

print("OK: project patched for GitHub Pages / GitHub Actions")