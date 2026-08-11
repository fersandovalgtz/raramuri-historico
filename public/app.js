
let entries=[]; let direction='ALL';
const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ſ/g,'s').toLowerCase();
async function init(){entries=await fetch('data/entries.json').then(r=>r.json()); document.getElementById('count').textContent=entries.length; render();}
function setDir(d,b){direction=d;document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('active'));b.classList.add('active');render()}
function render(){const q=norm(document.getElementById('q').value.trim()); let rows=entries.filter(e=>(direction==='ALL'||e.direction===direction)&&(!q||norm([e.headword_raw,e.gloss_de_raw,e.translation_es_editorial].join(' ')).includes(q))); document.getElementById('shown').textContent=rows.length; const box=document.getElementById('results'); if(!rows.length){box.innerHTML='<div class="empty">No hay coincidencias en el corpus inicial.</div>';return;} box.innerHTML=rows.slice(0,80).map(e=>`<article class="card"><div><div class="head">${esc(e.headword_raw)}</div><div class="gloss"><strong>Alemán:</strong> ${esc(e.gloss_de_raw)}</div><div class="es"><strong>Español editorial:</strong> ${esc(e.translation_es_editorial)}</div><span class="flag">OCR sin cotejo final</span></div><div class="meta">${e.direction}<br>Steffel 1809 · p. ${e.printed_page}<br>${e.record_id}</div></article>`).join('')}
function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
document.addEventListener('DOMContentLoaded',()=>{document.getElementById('q').addEventListener('input',render);init()});
