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
