from pathlib import Path
import json

ROOT = Path(r"D:\projects\hantavirus_map")
(ROOT / "data").mkdir(parents=True, exist_ok=True)
(ROOT / "tools").mkdir(parents=True, exist_ok=True)

def w(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")

def wj(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

official = [
  {
    "id":"ecdc-andv-2026",
    "title":"ECDC: Andes hantavirus outbreak, MV Hondius",
    "country":"Multi-country / MV Hondius",
    "region":"South Atlantic / Tenerife",
    "group":"Multi-country",
    "year":2026,
    "event_date":"2026-05-12",
    "updated_at":"2026-05-12",
    "cases":11,
    "deaths":3,
    "status":"official_total",
    "source_tier":"official",
    "event_type":"outbreak_summary",
    "location_type":"ship_cluster",
    "confidence":"high",
    "disease_form":"HPS / HCPS",
    "virus_strain":"Andes",
    "lat":28.2916,
    "lng":-16.6291,
    "source_name":"ECDC",
    "source_url":"https://www.ecdc.europa.eu/en/infectious-disease-topics/hantavirus-infection/surveillance-and-updates/andes-hantavirus-outbreak",
    "comment":"Официальная сводка ECDC. Используется как основной источник по вспышке.",
    "include_in_totals":True
  },
  {
    "id":"who-don600-2026",
    "title":"WHO DON600: hantavirus cluster linked to cruise ship travel",
    "country":"Multi-country / MV Hondius",
    "region":"South Atlantic",
    "group":"Multi-country",
    "year":2026,
    "event_date":"2026-05-08",
    "updated_at":"2026-05-08",
    "cases":8,
    "deaths":3,
    "status":"official_total",
    "source_tier":"official",
    "event_type":"official_update",
    "location_type":"ship_cluster",
    "confidence":"high",
    "disease_form":"HPS / HCPS",
    "virus_strain":"Andes",
    "lat":14.933,
    "lng":-23.513,
    "source_name":"WHO Disease Outbreak News",
    "source_url":"https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600",
    "comment":"Историческая официальная сводка WHO. Не считается в главном total, чтобы не было двойного счета.",
    "include_in_totals":False
  },
  {
    "id":"ecdc-eueea-2023",
    "title":"ECDC: EU/EEA hantavirus infection annual report 2023",
    "country":"EU/EEA",
    "region":"Europe",
    "group":"Europe",
    "year":2023,
    "event_date":"2023-12-31",
    "updated_at":"2025-03-07",
    "cases":1885,
    "deaths":3,
    "status":"official_total",
    "source_tier":"official",
    "event_type":"annual_stats",
    "location_type":"regional_centroid",
    "confidence":"high",
    "disease_form":"Mostly HFRS",
    "virus_strain":"Mostly Puumala",
    "lat":54.526,
    "lng":15.255,
    "source_name":"ECDC",
    "source_url":"https://www.ecdc.europa.eu/en/publications-data/hantavirus-infection-annual-epidemiological-report-2023",
    "comment":"Годовая статистика EU/EEA.",
    "include_in_totals":True
  },
  {
    "id":"cdc-usa-1993-2023",
    "title":"CDC: United States hantavirus cases, 1993-2023",
    "country":"United States",
    "region":"USA",
    "group":"USA",
    "year":2023,
    "event_date":"2023-12-31",
    "updated_at":"2026-04-23",
    "cases":890,
    "deaths":None,
    "status":"official_total",
    "source_tier":"official",
    "event_type":"annual_stats",
    "location_type":"country_centroid",
    "confidence":"high",
    "disease_form":"HPS and non-pulmonary hantavirus infection",
    "virus_strain":"Mixed / not specified",
    "lat":39.8283,
    "lng":-98.5795,
    "source_name":"CDC",
    "source_url":"https://www.cdc.gov/hantavirus/data-research/cases/index.html",
    "comment":"Накопительная статистика CDC по США.",
    "include_in_totals":True
  },
  {
    "id":"rospotrebnadzor-kostroma-2022",
    "title":"Роспотребнадзор: Костромская область, ГЛПС, 2022",
    "country":"Россия",
    "region":"Костромская область",
    "group":"Russia",
    "year":2022,
    "event_date":"2022-12-31",
    "updated_at":"2023-04-17",
    "cases":64,
    "deaths":None,
    "status":"official_total",
    "source_tier":"official",
    "event_type":"annual_stats",
    "location_type":"regional_centroid",
    "confidence":"high",
    "disease_form":"ГЛПС / HFRS",
    "virus_strain":"unknown",
    "lat":57.8029,
    "lng":40.9907,
    "source_name":"Роспотребнадзор, Костромская область",
    "source_url":"https://44.rospotrebnadzor.ru/osnovnye_napravlenij/profilaktika_infekci/5800/",
    "comment":"Официальная региональная статистика.",
    "include_in_totals":True
  }
]

w("index.html", """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Hantavirus Map</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <div>
    <h1>Онлайн-карта хантавируса</h1>
    <p>Официальные источники отдельно, ArcGIS и похожие трекеры отдельно как signal</p>
  </div>
  <b>v2</b>
</header>

<main>
  <aside>
    <h2>Фильтры</h2>

    <label>Регион
      <select id="groupFilter">
        <option value="all">Весь мир</option>
        <option value="Europe">Европа</option>
        <option value="Russia">Россия</option>
        <option value="USA">США</option>
        <option value="Multi-country">Мульти-страна</option>
      </select>
    </label>

    <label>Источник
      <select id="tierFilter">
        <option value="all">Все</option>
        <option value="official">Официальные</option>
        <option value="signal">Сигнальные / ArcGIS</option>
      </select>
    </label>

    <label>Статус
      <select id="statusFilter">
        <option value="all">Все</option>
        <option value="official_total">Официальная сводка</option>
        <option value="confirmed">Confirmed</option>
        <option value="probable">Probable</option>
        <option value="suspected">Suspected</option>
        <option value="deceased">Deceased</option>
        <option value="monitoring">Monitoring</option>
        <option value="unknown">Unknown</option>
      </select>
    </label>

    <label>Год
      <select id="yearFilter">
        <option value="all">Все годы</option>
      </select>
    </label>

    <label>Поиск
      <input id="searchInput" placeholder="страна, регион, источник">
    </label>

    <div class="stats">
      <div><span id="recordsCount">0</span><small>записей</small></div>
      <div><span id="officialCount">0</span><small>official</small></div>
      <div><span id="signalCount">0</span><small>signal</small></div>
      <div><span id="deathCount">0</span><small>смертей official</small></div>
    </div>

    <button id="resetBtn">Сбросить</button>

    <section>
      <h3>Важно</h3>
      <p><b>Signal</b> не считается официальной статистикой. Monitoring и suspected не складываются с confirmed, потому что мы не совсем безумцы.</p>
    </section>
  </aside>

  <div id="map"></div>
</main>

<section class="tableBox">
  <h2>Данные</h2>
  <table>
    <thead>
      <tr>
        <th>Год</th><th>Tier</th><th>Статус</th><th>Страна / регион</th><th>Случаи</th><th>Смерти</th><th>Источник</th>
      </tr>
    </thead>
    <tbody id="dataTable"></tbody>
  </table>
</section>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="app.js"></script>
</body>
</html>
""")

w("style.css", """
body{margin:0;background:#0b1120;color:#e5e7eb;font-family:Arial,sans-serif}
header{display:flex;justify-content:space-between;align-items:center;padding:18px 24px;background:#111827;border-bottom:1px solid #334155}
header h1{margin:0 0 6px;font-size:26px}
header p{margin:0;color:#9ca3af}
main{display:grid;grid-template-columns:360px 1fr;min-height:720px}
aside{background:#111827;padding:18px;border-right:1px solid #334155}
label{display:block;margin:12px 0;color:#9ca3af}
select,input,button{width:100%;box-sizing:border-box;margin-top:6px;padding:11px;border-radius:10px;border:1px solid #334155;background:#1f2937;color:#e5e7eb}
button{background:#2563eb;border:0;font-weight:bold;cursor:pointer}
#map{min-height:720px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.stats div{background:#1f2937;border:1px solid #334155;border-radius:12px;padding:12px;text-align:center}
.stats span{display:block;font-size:24px;font-weight:bold}
.stats small{color:#9ca3af}
section{background:#1f2937;border:1px solid #334155;border-radius:12px;padding:12px;margin-top:14px}
section p{color:#9ca3af;line-height:1.45}
.tableBox{margin:0;padding:22px;border-radius:0;border-left:0;border-right:0}
table{width:100%;border-collapse:collapse;background:#111827}
th,td{padding:11px;border-bottom:1px solid #334155;text-align:left;vertical-align:top}
th{color:#fff}
td{color:#cbd5e1}
a{color:#93c5fd}
.badge{display:inline-block;padding:3px 8px;border-radius:999px;background:#334155}
.official{background:#1d4ed8}
.signal{background:#c2410c}
@media(max-width:900px){main{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid #334155}}
""")

w("app.js", """
let map, layer, allRecords=[];

const statusNames={
  official_total:"Официальная сводка",
  confirmed:"Confirmed",
  probable:"Probable",
  suspected:"Suspected",
  deceased:"Deceased",
  monitoring:"Monitoring",
  unknown:"Unknown"
};

function color(r){
  if(r.source_tier==="official") return "#3b82f6";
  if(r.status==="confirmed") return "#ef4444";
  if(r.status==="deceased") return "#7f1d1d";
  if(r.status==="probable") return "#f97316";
  if(r.status==="suspected") return "#eab308";
  if(r.status==="monitoring") return "#6b7280";
  return "#8b5cf6";
}

function val(x){return x===null||x===undefined||x===""?"—":x}

function popup(r){
  let warn = r.source_tier==="signal"
    ? "<p><b>Signal:</b> не считать официальной статистикой без проверки через WHO/ECDC/CDC/минздрав.</p>"
    : "";
  return `
    <b>${r.title}</b>
    <p><b>Tier:</b> ${r.source_tier}</p>
    <p><b>Статус:</b> ${statusNames[r.status]||r.status}</p>
    <p><b>Место:</b> ${r.country}, ${r.region}</p>
    <p><b>Случаи:</b> ${val(r.cases)} | <b>Смерти:</b> ${val(r.deaths)}</p>
    <p><b>Вирус:</b> ${val(r.virus_strain)}</p>
    <p>${val(r.comment)}</p>
    ${warn}
    <p><a target="_blank" href="${r.source_url}">${r.source_name}</a></p>
  `;
}

function init(){
  map=L.map("map").setView([35,20],2);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:18,attribution:"&copy; OpenStreetMap"}).addTo(map);
  layer=L.layerGroup().addTo(map);
}

function filters(){
  return {
    group:document.getElementById("groupFilter").value,
    tier:document.getElementById("tierFilter").value,
    status:document.getElementById("statusFilter").value,
    year:document.getElementById("yearFilter").value,
    q:document.getElementById("searchInput").value.toLowerCase().trim()
  };
}

function match(r,f){
  if(f.group!=="all" && r.group!==f.group) return false;
  if(f.tier!=="all" && r.source_tier!==f.tier) return false;
  if(f.status!=="all" && r.status!==f.status) return false;
  if(f.year!=="all" && String(r.year)!==f.year) return false;
  if(f.q){
    let s=[r.title,r.country,r.region,r.source_name,r.comment,r.status,r.source_tier].join(" ").toLowerCase();
    if(!s.includes(f.q)) return false;
  }
  return true;
}

function render(){
  let f=filters();
  let rows=allRecords.filter(r=>match(r,f));
  layer.clearLayers();

  let bounds=[];
  for(let r of rows){
    if(typeof r.lat!=="number" || typeof r.lng!=="number") continue;
    let m=L.circleMarker([r.lat,r.lng],{
      radius:r.source_tier==="signal"?7:12,
      color:color(r),
      fillColor:color(r),
      fillOpacity:r.source_tier==="signal"?0.45:0.75,
      weight:r.source_tier==="signal"?1:2
    }).bindPopup(popup(r));
    layer.addLayer(m);
    bounds.push([r.lat,r.lng]);
  }
  if(bounds.length) map.fitBounds(bounds,{padding:[35,35],maxZoom:5});

  document.getElementById("recordsCount").textContent=rows.length;
  document.getElementById("officialCount").textContent=rows.filter(r=>r.source_tier==="official").length;
  document.getElementById("signalCount").textContent=rows.filter(r=>r.source_tier==="signal").length;
  document.getElementById("deathCount").textContent=rows.filter(r=>r.source_tier==="official"&&r.include_in_totals!==false).reduce((a,r)=>a+(Number(r.deaths)||0),0);

  let body=document.getElementById("dataTable");
  body.innerHTML="";
  for(let r of rows){
    body.innerHTML += `<tr>
      <td>${r.year}</td>
      <td><span class="badge ${r.source_tier}">${r.source_tier}</span></td>
      <td>${statusNames[r.status]||r.status}</td>
      <td><b>${r.country}</b><br>${r.region}</td>
      <td>${val(r.cases)}</td>
      <td>${val(r.deaths)}</td>
      <td><a target="_blank" href="${r.source_url}">${r.source_name}</a></td>
    </tr>`;
  }
}

async function load(){
  let res=await fetch("data/site_records.json?x="+Date.now());
  allRecords=await res.json();

  let years=[...new Set(allRecords.map(r=>String(r.year)))].sort((a,b)=>Number(b)-Number(a));
  let yf=document.getElementById("yearFilter");
  for(let y of years) yf.innerHTML += `<option value="${y}">${y}</option>`;

  for(let id of ["groupFilter","tierFilter","statusFilter","yearFilter"]) document.getElementById(id).onchange=render;
  document.getElementById("searchInput").oninput=render;
  document.getElementById("resetBtn").onclick=()=>{
    groupFilter.value="all";tierFilter.value="all";statusFilter.value="all";yearFilter.value="all";searchInput.value="";render();
  };
  render();
}

init();
load().catch(e=>alert("Ошибка загрузки: "+e.message));
""")

w("tools/update_arcgis_signal.py", """
import json, math
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "arcgis_signal_records.json"
URL = "https://services1.arcgis.com/wb4Og4gH5mvzQAIV/arcgis/rest/services/Tracking_Hantavirus_2026/FeatureServer/1/query"

def pick(a,*names):
    low={str(k).lower():k for k in a}
    for n in names:
        k=low.get(n.lower())
        if k and a.get(k) not in (None,""):
            return a[k]
    return None

def to_ll(x,y,wkid):
    if x is None or y is None:
        return None,None
    x=float(x); y=float(y)
    if abs(x)<=180 and abs(y)<=90:
        return y,x
    origin=20037508.342789244
    lng=(x/origin)*180
    lat=(y/origin)*180
    lat=180/math.pi*(2*math.atan(math.exp(lat*math.pi/180))-math.pi/2)
    return lat,lng

def status(v,death):
    t=str(v or "").upper()
    d=str(death or "").upper()
    if "DECEASE" in t or "DEAD" in t or "DIED" in t or d not in ("","NONE","NO","N/A","NULL"):
        return "deceased"
    if "CONFIRM" in t: return "confirmed"
    if "PROBABLE" in t: return "probable"
    if "SUSPECT" in t: return "suspected"
    if "MONITOR" in t or "CONTACT" in t: return "monitoring"
    return "unknown"

def main():
    params=urlencode({"where":"1=1","outFields":"*","returnGeometry":"true","f":"json","resultRecordCount":"2000"})
    try:
        req=Request(URL+"?"+params,headers={"User-Agent":"hantavirus-map"})
        data=json.loads(urlopen(req,timeout=25).read().decode("utf-8"))
        wkid=(data.get("spatialReference") or {}).get("latestWkid") or (data.get("spatialReference") or {}).get("wkid")
        records=[]
        for i,f in enumerate(data.get("features",[]),1):
            a=f.get("attributes") or {}
            g=f.get("geometry") or {}
            cid=pick(a,"CASE_","CASE","OBJECTID","FID") or i
            st=status(pick(a,"STATUS"),pick(a,"DEATH"))
            lat,lng=to_ll(g.get("x"),g.get("y"),wkid)
            loc=pick(a,"LASTLOCATION","LOCATION") or "Unknown / multi-country"
            src=pick(a,"SOURCE") or "ArcGIS independent dashboard"
            det=pick(a,"DETAILS") or ""
            records.append({
                "id":f"arcgis-signal-{cid}",
                "title":f"ArcGIS signal #{cid}: {st}",
                "country":str(loc),
                "region":"ArcGIS independent tracker",
                "group":"Multi-country",
                "year":2026,
                "event_date":"2026-05-01",
                "updated_at":datetime.now(timezone.utc).date().isoformat(),
                "cases":1 if st in ("confirmed","probable","suspected","deceased") else 0,
                "deaths":1 if st=="deceased" else 0,
                "status":st,
                "source_tier":"signal",
                "event_type":"individual_case",
                "location_type":"reported_location",
                "confidence":"low" if st in ("suspected","monitoring","unknown") else "medium",
                "disease_form":"HPS / HCPS",
                "virus_strain":"Andes",
                "lat":lat,
                "lng":lng,
                "source_name":"ArcGIS independent dashboard; listed source: "+str(src),
                "source_url":"https://www.arcgis.com/apps/dashboards/5c68442d2afc42d7ba2696e4cd393729",
                "comment":str(det) or "Imported from ArcGIS. Treat as signal, not official statistics.",
                "include_in_totals":False
            })
        OUT.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        print("OK: ArcGIS imported:",len(records))
    except Exception as e:
        if not OUT.exists():
            OUT.write_text("[]",encoding="utf-8")
        print("WARNING: ArcGIS update failed:",e)

if __name__=="__main__":
    main()
""")

w("tools/build_site_data.py", """
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/"data"/"official_records.json",ROOT/"data"/"arcgis_signal_records.json"]
out=ROOT/"data"/"site_records.json"

records=[]
seen=set()
for p in files:
    if not p.exists():
        continue
    for r in json.loads(p.read_text(encoding="utf-8")):
        if r.get("id") in seen:
            continue
        seen.add(r.get("id"))
        records.append(r)

records.sort(key=lambda r:(int(r.get("year") or 0),str(r.get("updated_at") or "")),reverse=True)
out.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK: site records:",len(records))
""")

w("tools/validate_data.py", """
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"data"/"site_records.json"
need=["id","title","country","region","group","year","cases","deaths","status","source_tier","lat","lng","source_name","source_url","comment"]
rows=json.loads(p.read_text(encoding="utf-8"))
ids=set()
for i,r in enumerate(rows,1):
    for k in need:
        if k not in r:
            raise SystemExit(f"ERROR row {i}: missing {k}")
    if r["id"] in ids:
        raise SystemExit(f"ERROR duplicate id: {r['id']}")
    ids.add(r["id"])
print("OK: validated",len(rows))
""")

w("run_local.bat", """
@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

echo [1/4] Updating ArcGIS signal...
%PY% tools\\update_arcgis_signal.py

echo [2/4] Building data...
%PY% tools\\build_site_data.py

echo [3/4] Validating...
%PY% tools\\validate_data.py
if errorlevel 1 (
  pause
  exit /b 1
)

echo [4/4] Starting server...
start "" "http://127.0.0.1:8000"
%PY% -m http.server 8000
pause
""")

w("run_no_update.bat", """
@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)

%PY% tools\\build_site_data.py
%PY% tools\\validate_data.py
start "" "http://127.0.0.1:8000"
%PY% -m http.server 8000
pause
""")

wj("data/official_records.json", official)
wj("data/arcgis_signal_records.json", [])
wj("data/site_records.json", official)

print("OK: project repaired")
print(r"Path: D:\projects\hantavirus_map")