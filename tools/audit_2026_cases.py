import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "site_records.json"
REPORT = ROOT / "audit_hantavirus_2026.md"
CSV = ROOT / "audit_hantavirus_2026.csv"

EXPECTED = {
    "ecdc_date": "2026-05-12",
    "total_cases": 11,
    "confirmed": 9,
    "probable": 2,
    "suspected": 0,
    "deaths": 3,
}

def safe(value):
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("\r", " ").strip()

def is_2026_hantavirus_record(r):
    text = " ".join([
        safe(r.get("id")),
        safe(r.get("title")),
        safe(r.get("country")),
        safe(r.get("region")),
        safe(r.get("comment")),
        safe(r.get("virus_strain")),
        safe(r.get("source_name")),
        safe(r.get("source_url")),
    ]).lower()

    if r.get("year") == 2026:
        return True

    keywords = [
        "hondius",
        "andes",
        "andv",
        "don600",
        "cruise",
        "ship",
        "tenerife",
        "south atlantic",
    ]

    return any(k in text for k in keywords)

def classify(r):
    tier = r.get("source_tier", "unknown")
    status = r.get("status", "unknown")
    event_type = r.get("event_type", "unknown")

    if tier == "official":
        if status == "official_total":
            return "OFFICIAL_AGGREGATE"
        return "OFFICIAL_RECORD"

    if tier == "signal":
        if status in {"confirmed", "probable", "deceased"}:
            return "SIGNAL_CASE_NEEDS_OFFICIAL_MATCH"
        if status in {"suspected", "monitoring", "unknown"}:
            return "SIGNAL_NOT_CONFIRMED_CASE"
        if event_type in {"route_point", "contact_monitoring"}:
            return "SIGNAL_ROUTE_OR_MONITORING"
        return "SIGNAL_OTHER"

    return "UNKNOWN_TIER"

def main():
    if not DATA.exists():
        raise SystemExit(f"Не найден файл: {DATA}")

    rows = json.loads(DATA.read_text(encoding="utf-8"))
    rows_2026 = [r for r in rows if is_2026_hantavirus_record(r)]

    by_tier = Counter(r.get("source_tier", "unknown") for r in rows_2026)
    by_status = Counter(r.get("status", "unknown") for r in rows_2026)
    by_class = Counter(classify(r) for r in rows_2026)

    official_rows = [r for r in rows_2026 if r.get("source_tier") == "official"]
    signal_rows = [r for r in rows_2026 if r.get("source_tier") == "signal"]

    official_evidence = []
    for r in official_rows:
        official_evidence.append({
            "id": r.get("id"),
            "title": r.get("title"),
            "cases": r.get("cases"),
            "deaths": r.get("deaths"),
            "source": r.get("source_name"),
            "url": r.get("source_url"),
            "include_in_totals": r.get("include_in_totals"),
        })

    signal_case_like = [
        r for r in signal_rows
        if r.get("status") in {"confirmed", "probable", "deceased", "suspected"}
    ]

    monitoring_like = [
        r for r in signal_rows
        if r.get("status") in {"monitoring", "unknown"}
        or r.get("event_type") in {"contact_monitoring", "route_point"}
    ]

    lines = []
    lines.append("# Аудит карты Hantavirus 2026")
    lines.append("")
    lines.append("## Официальный эталон для проверки")
    lines.append("")
    lines.append(f"- ECDC дата: {EXPECTED['ecdc_date']}")
    lines.append(f"- Всего случаев: {EXPECTED['total_cases']}")
    lines.append(f"- Confirmed: {EXPECTED['confirmed']}")
    lines.append(f"- Probable: {EXPECTED['probable']}")
    lines.append(f"- Suspected: {EXPECTED['suspected']}")
    lines.append(f"- Deaths: {EXPECTED['deaths']}")
    lines.append("")
    lines.append("## Что найдено в локальной базе")
    lines.append("")
    lines.append(f"- Всего записей в site_records.json: {len(rows)}")
    lines.append(f"- Записей, похожих на Hantavirus 2026 / MV Hondius / ANDV: {len(rows_2026)}")
    lines.append(f"- Official-записей: {len(official_rows)}")
    lines.append(f"- Signal-записей: {len(signal_rows)}")
    lines.append("")
    lines.append("## Разбивка по source_tier")
    lines.append("")
    for k, v in by_tier.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Разбивка по status")
    lines.append("")
    for k, v in by_status.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Разбивка по классификации")
    lines.append("")
    for k, v in by_class.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Официальные записи")
    lines.append("")
    for r in official_evidence:
        lines.append(f"### {r['id']}")
        lines.append(f"- title: {r['title']}")
        lines.append(f"- cases: {r['cases']}")
        lines.append(f"- deaths: {r['deaths']}")
        lines.append(f"- source: {r['source']}")
        lines.append(f"- include_in_totals: {r['include_in_totals']}")
        lines.append(f"- url: {r['url']}")
        lines.append("")
    lines.append("## Signal-записи, похожие на случаи")
    lines.append("")
    if not signal_case_like:
        lines.append("Нет signal-записей, похожих на случаи.")
    else:
        for r in signal_case_like:
            lines.append(f"- {r.get('id')} | {r.get('status')} | {r.get('country')} | cases={r.get('cases')} deaths={r.get('deaths')} | {r.get('source_name')}")
    lines.append("")
    lines.append("## Monitoring / route / unknown")
    lines.append("")
    lines.append(f"Таких записей: {len(monitoring_like)}")
    lines.append("Они НЕ должны считаться подтверждёнными заболевшими.")
    lines.append("")
    lines.append("## Вывод")
    lines.append("")
    lines.append("Карта корректна, если:")
    lines.append("")
    lines.append("1. ECDC/WHO/CDC находятся в official.")
    lines.append("2. ArcGIS находится в signal.")
    lines.append("3. Monitoring, unknown, route и suspected не входят в official total.")
    lines.append("4. Главная официальная цифра по Hantavirus 2026 берётся из ECDC: 11 cases, 9 confirmed, 2 probable, 3 deaths.")
    lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")

    csv_lines = [
        "id;tier;status;class;year;country;region;cases;deaths;source;url;comment"
    ]

    for r in rows_2026:
        csv_lines.append(";".join([
            safe(r.get("id")),
            safe(r.get("source_tier")),
            safe(r.get("status")),
            safe(classify(r)),
            safe(r.get("year")),
            safe(r.get("country")),
            safe(r.get("region")),
            safe(r.get("cases")),
            safe(r.get("deaths")),
            safe(r.get("source_name")),
            safe(r.get("source_url")),
            safe(r.get("comment")),
        ]))

    CSV.write_text("\n".join(csv_lines), encoding="utf-8")

    print("OK: аудит готов")
    print(f"Markdown report: {REPORT}")
    print(f"CSV report: {CSV}")
    print("")
    print("Кратко:")
    print(f"2026 records: {len(rows_2026)}")
    print(f"official: {len(official_rows)}")
    print(f"signal: {len(signal_rows)}")
    print("status:", dict(by_status))
    print("classification:", dict(by_class))

if __name__ == "__main__":
    main()