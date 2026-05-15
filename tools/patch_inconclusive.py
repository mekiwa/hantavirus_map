from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "tools" / "update_official_confirmed.py"

text = p.read_text(encoding="utf-8")

# 1. Добавляем парсинг inconclusive cases
text = text.replace(
'''    suspected = num_after("Suspected cases", text)
    deaths = num_after("Number of deaths", text)''',
'''    suspected = num_after("Suspected cases", text)
    inconclusive = num_after("Inconclusive cases", text)
    deaths = num_after("Number of deaths", text)'''
)

# 2. Если total не найден, считаем confirmed + probable + inconclusive
text = text.replace(
'''    if total is None and confirmed is not None and probable is not None:
        total = confirmed + probable''',
'''    if total is None and confirmed is not None and probable is not None:
        total = confirmed + probable + (inconclusive or 0)'''
)

# 3. Проверка ошибки должна учитывать inconclusive в сообщении
text = text.replace(
'''            f"ECDC parse failed: total={total}, confirmed={confirmed}, probable={probable}, suspected={suspected}, deaths={deaths}"''',
'''            f"ECDC parse failed: total={total}, confirmed={confirmed}, probable={probable}, inconclusive={inconclusive}, suspected={suspected}, deaths={deaths}"'''
)

# 4. Добавляем поле inconclusive_cases в ECDC record
text = text.replace(
'''        "suspected_cases": suspected if suspected is not None else 0,
        "deaths": deaths,''',
'''        "suspected_cases": suspected if suspected is not None else 0,
        "inconclusive_cases": inconclusive if inconclusive is not None else 0,
        "deaths": deaths,'''
)

# 5. Комментарий ECDC должен показывать inconclusive
text = text.replace(
'''        "comment": f"Auto-updated official ECDC data: total={total}, confirmed={confirmed}, probable={probable}, suspected={suspected if suspected is not None else 0}, deaths={deaths}.",''',
'''        "comment": f"Auto-updated official ECDC data: total={total}, confirmed={confirmed}, probable={probable}, inconclusive={inconclusive if inconclusive is not None else 0}, suspected={suspected if suspected is not None else 0}, deaths={deaths}.",'''
)

# 6. WHO и CDC тоже пусть имеют поле inconclusive_cases
text = text.replace(
'''        "suspected_cases": 0,
        "deaths": deaths,''',
'''        "suspected_cases": 0,
        "inconclusive_cases": 0,
        "deaths": deaths,'''
)

text = text.replace(
'''        "suspected_cases": None,
        "deaths": None,''',
'''        "suspected_cases": None,
        "inconclusive_cases": None,
        "deaths": None,'''
)

# 7. Печать headline
text = text.replace(
'''    print("suspected:", ecdc.get("suspected_cases"))
    print("deaths:", ecdc.get("deaths"))''',
'''    print("suspected:", ecdc.get("suspected_cases"))
    print("inconclusive:", ecdc.get("inconclusive_cases"))
    print("deaths:", ecdc.get("deaths"))'''
)

p.write_text(text, encoding="utf-8")
print("OK: update_official_confirmed.py patched for inconclusive cases")