import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "hantavirus_events.json"

def ask(prompt, default=None):
    value = input(f"{prompt}" + (f" [{default}]" if default is not None else "") + ": ").strip()
    return value if value else default

def ask_int(prompt, allow_empty=True):
    value = input(f"{prompt}: ").strip()
    if allow_empty and not value:
        return None
    return int(value)

def ask_float(prompt):
    return float(input(f"{prompt}: ").strip().replace(",", "."))

def main():
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    print("Добавление новой записи. Да, руками через форму в консоли, зато без ковыряния JSON.")

    record = {
        "id": ask("id, например who-something-2026"),
        "title": ask("Название записи"),
        "country": ask("Страна / зона"),
        "region": ask("Регион"),
        "group": ask("Группа: Europe / Russia / USA / Americas / Multi-country"),
        "year": ask_int("Год", allow_empty=False),
        "event_date": ask("Дата события YYYY-MM-DD"),
        "updated_at": ask("Дата обновления YYYY-MM-DD"),
        "cases": ask_int("Случаи, пусто если нет данных"),
        "deaths": ask_int("Смерти, пусто если нет данных"),
        "type": ask("Тип: annual_stats / outbreak / risk_zone"),
        "lat": ask_float("Широта lat"),
        "lng": ask_float("Долгота lng"),
        "source_name": ask("Название источника"),
        "source_url": ask("Ссылка на источник"),
        "comment": ask("Комментарий", "")
    }

    records.append(record)
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Запись добавлена.")
    print("Теперь проверь данные командой: python tools\\validate_data.py")

if __name__ == "__main__":
    main()