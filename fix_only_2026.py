import json
from pathlib import Path

ROOT = Path(r"D:\projects\hantavirus_map")
official_file = ROOT / "data" / "official_records.json"
site_file = ROOT / "data" / "site_records.json"
arcgis_file = ROOT / "data" / "arcgis_signal_records.json"

official = json.loads(official_file.read_text(encoding="utf-8"))

# Оставляем в official_records.json только записи, связанные с Hantavirus 2026 / MV Hondius / Andes.
official_2026 = [
    r for r in official
    if (
        r.get("year") == 2026
        or "hondius" in r.get("id", "").lower()
        or "andes" in r.get("virus_strain", "").lower()
        or "don600" in r.get("id", "").lower()
    )
]

arcgis = []
if arcgis_file.exists():
    arcgis = json.loads(arcgis_file.read_text(encoding="utf-8"))

site = official_2026 + arcgis

official_file.write_text(
    json.dumps(official_2026, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

site_file.write_text(
    json.dumps(site, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"OK: official 2026 records: {len(official_2026)}")
print(f"OK: arcgis signal records: {len(arcgis)}")
print(f"OK: site records total: {len(site)}")