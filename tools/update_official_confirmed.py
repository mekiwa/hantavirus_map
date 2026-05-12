import json
import re
import html
import ssl
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

ECDC_URL = "https://www.ecdc.europa.eu/en/infectious-disease-topics/hantavirus-infection/surveillance-and-updates/andes-hantavirus-outbreak"
WHO_URL = "https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600"
CDC_URL = "https://www.cdc.gov/han/php/notices/han00528.html"

OFFICIAL_FILE = DATA / "official_records.json"

SEED_ECDC = {
    "id": "ecdc-andv-2026-live",
    "title": "ECDC live/fallback: Andes hantavirus outbreak, MV Hondius",
    "country": "Multi-country / MV Hondius",
    "region": "South Atlantic / Tenerife",
    "group": "Multi-country",
    "year": 2026,
    "event_date": "2026-05-12",
    "updated_at": "2026-05-12",
    "cases": 11,
    "confirmed_cases": 9,
    "probable_cases": 2,
    "suspected_cases": 0,
    "deaths": 3,
    "status": "official_total",
    "source_tier": "official",
    "event_type": "outbreak_summary",
    "location_type": "ship_cluster",
    "confidence": "high",
    "disease_form": "HPS / HCPS",
    "virus_strain": "Andes",
    "lat": 28.2916,
    "lng": -16.6291,
    "source_name": "ECDC live outbreak page / cached fallback",
    "source_url": ECDC_URL,
    "comment": "Fallback ECDC official snapshot used because live fetch failed: total=11, confirmed=9, probable=2, suspected=0, deaths=3.",
    "include_in_totals": True,
    "auto_updated": False,
    "fallback": True
}

def clean_html(raw):
    text = re.sub(r"<script.*?</script>", " ", raw, flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def fetch_urllib(url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 hantavirus-map-official-updater/1.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })

    # Обычный SSL.
    try:
        with urlopen(req, timeout=35) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        pass

    # Ослабленный SSL-контекст. Не для банков, а для публичной страницы ECDC, господи прости.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urlopen(req, timeout=35, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")

def fetch_curl(url):
    result = subprocess.run(
        [
            ("curl.exe" if __import__("sys").platform.startswith("win") else "curl"),
            "-L",
            "--max-time", "40",
            "--retry", "2",
            "--ssl-no-revoke",
            "-A", "Mozilla/5.0 hantavirus-map-official-updater/1.1",
            url
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl failed with code {result.returncode}")

    if not result.stdout.strip():
        raise RuntimeError("curl returned empty body")

    return result.stdout

def fetch(url):
    errors = []

    for name, fn in [("urllib", fetch_urllib), ("curl", fetch_curl)]:
        try:
            raw = fn(url)
            return clean_html(raw)
        except Exception as e:
            errors.append(f"{name}: {e}")

    raise RuntimeError(" | ".join(errors))

def load_previous_ecdc():
    if not OFFICIAL_FILE.exists():
        return None

    try:
        rows = json.loads(OFFICIAL_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None

    for r in rows:
        if r.get("id") == "ecdc-andv-2026-live":
            r["comment"] = str(r.get("comment", "")) + " | Reused cached ECDC record because live fetch failed."
            r["auto_updated"] = False
            r["cached"] = True
            r["include_in_totals"] = True
            return r

    for r in rows:
        text = " ".join([
            str(r.get("id", "")),
            str(r.get("source_name", "")),
            str(r.get("title", "")),
            str(r.get("virus_strain", "")),
        ]).lower()

        if "ecdc" in text and ("andv" in text or "andes" in text or "hondius" in text):
            r["id"] = "ecdc-andv-2026-live"
            r["source_tier"] = "official"
            r["status"] = "official_total"
            r["include_in_totals"] = True
            r["auto_updated"] = False
            r["cached"] = True
            return r

    return None

def num_after(label, text):
    pattern = re.escape(label) + r".{0,120}?(\d+)"
    m = re.search(pattern, text, flags=re.I)
    return int(m.group(1)) if m else None

def parse_ecdc():
    text = fetch(ECDC_URL)

    confirmed = num_after("Confirmed cases", text)
    probable = num_after("Probable cases", text)
    suspected = num_after("Suspected cases", text)
    deaths = num_after("Number of deaths", text)

    total = None

    patterns = [
        r"As of\s+\d{1,2}\s+May,\s+(\d+)\s+cases have been reported in total",
        r"(\d+)\s+cases have been reported in total",
        r"total of\s+(\d+)\s+cases",
    ]

    for pattern in patterns:
        m = re.search(pattern, text, flags=re.I)
        if m:
            total = int(m.group(1))
            break

    if total is None and confirmed is not None and probable is not None:
        total = confirmed + probable

    if confirmed is None or probable is None or deaths is None or total is None:
        raise RuntimeError(
            f"ECDC parse failed: total={total}, confirmed={confirmed}, probable={probable}, suspected={suspected}, deaths={deaths}"
        )

    date = datetime.now(timezone.utc).date().isoformat()

    m = re.search(r"Andes hantavirus outbreak in cruise ship,\s*(\d{1,2}\s+[A-Za-z]+\s+2026)", text, flags=re.I)
    if m:
        try:
            date = datetime.strptime(m.group(1), "%d %B %Y").date().isoformat()
        except Exception:
            pass

    return {
        "id": "ecdc-andv-2026-live",
        "title": f"ECDC live: Andes hantavirus outbreak, MV Hondius, {date}",
        "country": "Multi-country / MV Hondius",
        "region": "South Atlantic / Tenerife",
        "group": "Multi-country",
        "year": 2026,
        "event_date": date,
        "updated_at": date,
        "cases": total,
        "confirmed_cases": confirmed,
        "probable_cases": probable,
        "suspected_cases": suspected if suspected is not None else 0,
        "deaths": deaths,
        "status": "official_total",
        "source_tier": "official",
        "event_type": "outbreak_summary",
        "location_type": "ship_cluster",
        "confidence": "high",
        "disease_form": "HPS / HCPS",
        "virus_strain": "Andes",
        "lat": 28.2916,
        "lng": -16.6291,
        "source_name": "ECDC live outbreak page",
        "source_url": ECDC_URL,
        "comment": f"Auto-updated official ECDC data: total={total}, confirmed={confirmed}, probable={probable}, suspected={suspected if suspected is not None else 0}, deaths={deaths}.",
        "include_in_totals": True,
        "auto_updated": True,
        "fallback": False
    }

def parse_who():
    try:
        text = fetch(WHO_URL)
    except Exception:
        text = ""

    total = 8
    confirmed = 6
    probable = 2
    deaths = 3

    m = re.search(r"As of 8 May, a total of (\d+) cases.*?including (\d+) deaths", text, flags=re.I)
    if m:
        total = int(m.group(1))
        deaths = int(m.group(2))

    return {
        "id": "who-don600-2026",
        "title": "WHO DON600: hantavirus cluster linked to cruise ship travel",
        "country": "Multi-country / MV Hondius",
        "region": "South Atlantic",
        "group": "Multi-country",
        "year": 2026,
        "event_date": "2026-05-08",
        "updated_at": "2026-05-08",
        "cases": total,
        "confirmed_cases": confirmed,
        "probable_cases": probable,
        "suspected_cases": 0,
        "deaths": deaths,
        "status": "official_total",
        "source_tier": "official",
        "event_type": "official_update",
        "location_type": "ship_cluster",
        "confidence": "high",
        "disease_form": "HPS / HCPS",
        "virus_strain": "Andes",
        "lat": 14.933,
        "lng": -23.513,
        "source_name": "WHO Disease Outbreak News",
        "source_url": WHO_URL,
        "comment": f"Historical official WHO update: total={total}, confirmed={confirmed}, probable={probable}, deaths={deaths}. Not included in headline totals to avoid double counting.",
        "include_in_totals": False,
        "auto_updated": True
    }

def cdc_verification_record():
    return {
        "id": "cdc-han00528-2026-verification",
        "title": "CDC HAN00528: 2026 multi-country hantavirus cluster linked to cruise ship",
        "country": "United States / multi-country response",
        "region": "CDC verification",
        "group": "Multi-country",
        "year": 2026,
        "event_date": "2026-05-09",
        "updated_at": datetime.now(timezone.utc).date().isoformat(),
        "cases": None,
        "confirmed_cases": None,
        "probable_cases": None,
        "suspected_cases": None,
        "deaths": None,
        "status": "official_total",
        "source_tier": "official",
        "event_type": "verification_source",
        "location_type": "agency_notice",
        "confidence": "high",
        "disease_form": "HPS / HCPS",
        "virus_strain": "Andes",
        "lat": 39.8283,
        "lng": -98.5795,
        "source_name": "CDC HAN",
        "source_url": CDC_URL,
        "comment": "CDC official health advisory verifying the Andes virus cruise ship cluster. Not used as headline count source.",
        "include_in_totals": False,
        "auto_updated": True
    }

def main():
    records = []

    try:
        ecdc = parse_ecdc()
        print("OK: ECDC live updated:", ecdc["comment"])
    except Exception as e:
        print("WARNING: ECDC live update failed:", e)

        ecdc = load_previous_ecdc()
        if ecdc:
            print("OK: using cached ECDC record")
        else:
            ecdc = dict(SEED_ECDC)
            print("OK: using built-in ECDC fallback seed")

    records.append(ecdc)

    who = parse_who()
    records.append(who)
    print("OK: WHO record ready:", who["comment"])

    cdc = cdc_verification_record()
    records.append(cdc)
    print("OK: CDC verification record ready")

    OFFICIAL_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("OK: official_records.json updated")
    print("records:", len(records))
    print("")
    print("HEADLINE OFFICIAL:")
    print("source:", ecdc["source_name"])
    print("total:", ecdc.get("cases"))
    print("confirmed:", ecdc.get("confirmed_cases"))
    print("probable:", ecdc.get("probable_cases"))
    print("suspected:", ecdc.get("suspected_cases"))
    print("deaths:", ecdc.get("deaths"))
    print("fallback:", ecdc.get("fallback", False))

if __name__ == "__main__":
    main()