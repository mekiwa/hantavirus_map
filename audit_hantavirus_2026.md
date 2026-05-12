# Аудит карты Hantavirus 2026

## Официальный эталон для проверки

- ECDC дата: 2026-05-12
- Всего случаев: 11
- Confirmed: 9
- Probable: 2
- Suspected: 0
- Deaths: 3

## Что найдено в локальной базе

- Всего записей в site_records.json: 108
- Записей, похожих на Hantavirus 2026 / MV Hondius / ANDV: 108
- Official-записей: 2
- Signal-записей: 106

## Разбивка по source_tier

- official: 2
- signal: 106

## Разбивка по status

- official_total: 2
- confirmed: 8
- suspected: 7
- deceased: 3
- monitoring: 84
- unknown: 4

## Разбивка по классификации

- OFFICIAL_AGGREGATE: 2
- SIGNAL_CASE_NEEDS_OFFICIAL_MATCH: 11
- SIGNAL_NOT_CONFIRMED_CASE: 95

## Официальные записи

### ecdc-andv-2026
- title: ECDC: Andes hantavirus outbreak, MV Hondius
- cases: 11
- deaths: 3
- source: ECDC
- include_in_totals: True
- url: https://www.ecdc.europa.eu/en/infectious-disease-topics/hantavirus-infection/surveillance-and-updates/andes-hantavirus-outbreak

### who-don600-2026
- title: WHO DON600: hantavirus cluster linked to cruise ship travel
- cases: 8
- deaths: 3
- source: WHO Disease Outbreak News
- include_in_totals: False
- url: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600

## Signal-записи, похожие на случаи

- arcgis-signal-7 | confirmed | ZURICH | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.bag.admin.ch/en/newnsb/p--A7yPSfxdBqR0N9kZMC
- arcgis-signal-999 | suspected | ZURICH | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.cbc.ca/news/health/hondius-ship-hantavirus-andes-strain-9.7189281
- arcgis-signal-3 | confirmed | JOHANNESBURG | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599
- arcgis-signal-1 | deceased | MV HONDIUS | cases=1 deaths=1 | ArcGIS independent dashboard; listed source: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600
- arcgis-signal-2 | deceased | JOHANNESBURG | cases=1 deaths=1 | ArcGIS independent dashboard; listed source: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599
- arcgis-signal-9 | suspected | NETHERLANDS | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.cnn.com/2026/05/07/world/hantavirus-ship-tenerife-outbreak-intl
- arcgis-signal-6 | confirmed | NETHERLANDS | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: ArcGIS independent dashboard
- arcgis-signal-5 | confirmed | NETHERLANDS | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.cnn.com/2026/05/07/world/hantavirus-ship-tenerife-outbreak-intl
- arcgis-signal-4 | deceased | MV HONDIUS | cases=1 deaths=1 | ArcGIS independent dashboard; listed source: https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599
- arcgis-signal-11 | suspected | SINGAPORE | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.channelnewsasia.com/singapore/hantavirus-mv-hondius-ncid-test-virus-isolated-cda-6106671
- arcgis-signal-13 | suspected | FRANCE | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.ctvnews.ca/canada/article/people-on-hantavirus-ship-ate-every-meal-side-by-side-even-after-first-death-passenger-says-live-updates-here/#:~:text=A%20French%20citizen%20with%20%E2%80%9Cbenign,said%20in%20a%20statement%20Thursday.
- arcgis-signal-26 | suspected | ALICANTE, SPAIN | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.forbes.com/sites/maryroeloffs/2026/05/08/another-hantavirus-case-suspected-in-spanish-woman-authorities-say-latest-updates/
- arcgis-signal-31 | confirmed | TRISTAN DA CUNHA | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.gov.uk/government/news/ukhsa-update-on-the-hantavirus-cruise-ship-outbreak#full-publication-update-history
- arcgis-signal-35 | suspected | TRISTAN DA CUNHA | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: ArcGIS independent dashboard
- arcgis-signal-36 | confirmed | FRANCE | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.tagesschau.de/ausland/europa/hantavirus-schiff-102.html
- arcgis-signal-48 | confirmed | UNITED STATES | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://www.tagesschau.de/ausland/europa/hantavirus-schiff-102.html
- arcgis-signal-49 | suspected | NEBRASKA, USA | cases=1 deaths=0 | ArcGIS independent dashboard; listed source:   https://abcnews.com/International/live-updates/hantavirus-live-updates-mv-hondius-canary-islands/?id=132746955&entryId=132836441
- arcgis-signal-111 | confirmed | SPAIN | cases=1 deaths=0 | ArcGIS independent dashboard; listed source: https://elpais.com/sociedad/2026-05-11/ultima-hora-del-brote-de-hantavirus-en-directo.html

## Monitoring / route / unknown

Таких записей: 88
Они НЕ должны считаться подтверждёнными заболевшими.

## Вывод

Карта корректна, если:

1. ECDC/WHO/CDC находятся в official.
2. ArcGIS находится в signal.
3. Monitoring, unknown, route и suspected не входят в official total.
4. Главная официальная цифра по Hantavirus 2026 берётся из ECDC: 11 cases, 9 confirmed, 2 probable, 3 deaths.
