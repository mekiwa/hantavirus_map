import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

official_file = DATA / "official_records.json"
arcgis_file = DATA / "arcgis_signal_records.json"
site_file = DATA / "site_records.json"

official = json.loads(official_file.read_text(encoding="utf-8")) if official_file.exists() else []
arcgis = json.loads(arcgis_file.read_text(encoding="utf-8")) if arcgis_file.exists() else []

# В site_records оставляем official + signal, но official считается главным.
# ArcGIS НЕ участвует в официальных total.
records = []
seen = set()

for r in official + arcgis:
    rid = r.get("id")
    if not rid or rid in seen:
        continue
    seen.add(rid)

    if r.get("source_tier") == "signal":
        r["include_in_totals"] = False
        # Signal не должен выглядеть как official case count.
        # Статус оставляем, но счетчики не используем для total.
        if r.get("status") in {"suspected", "monitoring", "unknown"}:
            r["cases"] = None
            r["deaths"] = None

    records.append(r)

records.sort(
    key=lambda x: (
        0 if x.get("source_tier") == "official" else 1,
        -int(x.get("year") or 0),
        str(x.get("updated_at") or "")
    )
)

site_file.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

headline = next((r for r in records if r.get("id") == "ecdc-andv-2026-live"), None)
if headline:
    print("HEADLINE OFFICIAL:")
    print("total:", headline.get("cases"))
    print("confirmed:", headline.get("confirmed_cases"))
    print("probable:", headline.get("probable_cases"))
    print("suspected:", headline.get("suspected_cases"))
    print("deaths:", headline.get("deaths"))

print("OK: site_records.json built:", len(records))
print("official:", len([r for r in records if r.get("source_tier") == "official"]))
print("signal:", len([r for r in records if r.get("source_tier") == "signal"]))