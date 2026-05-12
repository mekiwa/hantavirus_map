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
