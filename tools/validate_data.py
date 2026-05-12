import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "site_records.json"

need = [
    "id", "title", "country", "region", "group", "year",
    "cases", "deaths", "status", "source_tier", "event_type",
    "lat", "lng", "source_name", "source_url", "comment"
]

rows = json.loads(DATA.read_text(encoding="utf-8"))
ids = set()

for i, r in enumerate(rows, 1):
    for k in need:
        if k not in r:
            raise SystemExit(f"ERROR row {i}: missing {k}")

    if r["id"] in ids:
        raise SystemExit(f"ERROR duplicate id: {r['id']}")
    ids.add(r["id"])

    if r["source_tier"] == "official" and r.get("include_in_totals") is True:
        if r.get("id") != "ecdc-andv-2026-live":
            print("WARNING: official record included in totals but not ECDC live:", r["id"])

ecdc = next((r for r in rows if r.get("id") == "ecdc-andv-2026-live"), None)
if not ecdc:
    raise SystemExit("ERROR: missing ECDC live official record")

if ecdc.get("source_tier") != "official":
    raise SystemExit("ERROR: ECDC live record is not official")

if ecdc.get("include_in_totals") is not True:
    raise SystemExit("ERROR: ECDC live record not included in totals")

print("OK: validated", len(rows), "records")
print("ECDC official total:", ecdc.get("cases"))
print("confirmed:", ecdc.get("confirmed_cases"))
print("probable:", ecdc.get("probable_cases"))
print("suspected:", ecdc.get("suspected_cases"))
print("deaths:", ecdc.get("deaths"))