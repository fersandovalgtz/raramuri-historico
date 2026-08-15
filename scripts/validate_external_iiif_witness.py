#!/usr/bin/env python3
"""Validate the registered IA Steffel item as a noncanonical parallel witness.

The canonical RHD facsimile is checksum-fixed locally. Live Internet Archive image
fetches are useful rechecks, but a transient third-party Canvas failure must not block
canonical products. We therefore fail only on structural IIIF/registry contradictions
or on a successful live comparison that unexpectedly approaches image identity.
Unavailable live image windows are reported as degraded verification and preserve the
already registered strong-mismatch result; they never substitute external images for
canonical evidence.
"""
from pathlib import Path
from io import BytesIO
import json, sys, urllib.request
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/steffel-iiif-manifest.json")
LOCAL_MAP = ROOT / "data/appendices/facsimile_page_map.json"
FINGERPRINTS = ROOT / "data/iiif/steffel-1809-local-page-fingerprints.json"
REGISTRY = ROOT / "sources/external-references.json"
errors = []
if not MANIFEST.exists(): print(f"ERROR: downloaded manifest missing: {MANIFEST}"); sys.exit(1)
data = json.loads(MANIFEST.read_text(encoding="utf-8")); registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
external = next((w for w in registry.get("witnesses", []) if w.get("witness_id") == "IA-tarahumarischesw00stef"), None)
if external is None: errors.append("Internet Archive witness is not registered")
elif external.get("canonical_for_rhd") is not False: errors.append("Internet Archive witness must remain explicitly noncanonical")
elif external.get("role") != "parallel_external_witness_candidate": errors.append(f"unexpected external witness role: {external.get('role')}")
context = data.get("@context"); context_text = " ".join(str(x) for x in context) if isinstance(context, list) else str(context or "")
if "presentation/3" not in context_text: errors.append(f"manifest is not IIIF Presentation 3.x: context={context!r}")
if data.get("type") != "Manifest": errors.append(f"manifest type is {data.get('type')!r}, expected 'Manifest'")
manifest_id = data.get("id") or ""
if "tarahumarischesw00stef" not in manifest_id: errors.append(f"manifest id does not identify registered item: {manifest_id}")
canvases = data.get("items")
if not isinstance(canvases, list) or not canvases: errors.append("Presentation 3 Manifest has no Canvas items"); canvases = []
if len(canvases) < 80: errors.append(f"implausibly small Canvas count: {len(canvases)}")
local = json.loads(LOCAL_MAP.read_text(encoding="utf-8"))
if [x.get("printed_page") for x in local.get("mapping", [])] != [369,370,371,372,373,374]: errors.append("local appendix page map changed unexpectedly")
expected = json.loads(FINGERPRINTS.read_text(encoding="utf-8")).get("pages", [])
if [(x.get("pdf_page"), x.get("printed_page")) for x in expected] != [(79,369),(80,370),(81,371),(82,372),(83,373),(84,374)]: errors.append("local fingerprint sequence differs from collated appendix mapping")
registered_result = ((external or {}).get("identity_comparison") or {}).get("result")
if registered_result != "strong_mismatch_not_verified_as_same_scan": errors.append(f"registry identity result changed unexpectedly: {registered_result!r}")
if errors: print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)

def label_text(canvas):
    label = canvas.get("label")
    if isinstance(label, str): return label
    if isinstance(label, dict):
        vals=[]
        for v in label.values(): vals.extend(str(x) for x in v) if isinstance(v,list) else vals.append(str(v)) if v is not None else None
        return " | ".join(vals)
    return ""
def image_url(canvas):
    try:
        body=canvas["items"][0]["items"][0]["body"]; body=body[0] if isinstance(body,list) else body
        service=body.get("service") if isinstance(body,dict) else None; service=[service] if isinstance(service,dict) else service
        if isinstance(service,list):
            for srv in service:
                sid=(srv or {}).get("id") or (srv or {}).get("@id")
                if sid and sid.startswith("http"): return sid.removesuffix("/info.json").rstrip("/")+"/full/800,/0/default.jpg"
        bid=(body or {}).get("id") if isinstance(body,dict) else None
        return bid if bid and bid.startswith("http") else None
    except (KeyError,IndexError,TypeError): return None
def dhash256(image):
    g=image.convert("L"); mask=g.point(lambda p:255 if p<245 else 0); bbox=mask.getbbox()
    if bbox:
        x0,y0,x1,y1=bbox; px=max(2,int((x1-x0)*.02)); py=max(2,int((y1-y0)*.02)); g=g.crop((max(0,x0-px),max(0,y0-py),min(g.width,x1+px),min(g.height,y1+py)))
    small=g.resize((17,16),Image.Resampling.LANCZOS); pixels=list(small.getdata()); value=0
    for y in range(16):
        row=y*17
        for x in range(16): value=(value<<1)|int(pixels[row+x+1]>pixels[row+x])
    return f"{value:064x}"
def fetch_hash(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Raramuri-Historico-Digital/1.0 machine-witness-validator"})
    with urllib.request.urlopen(req,timeout=45) as response: raw=response.read()
    with Image.open(BytesIO(raw)) as image: return dhash256(image)
def hamming(a,b): return (int(a,16)^int(b,16)).bit_count()

start=max(0,len(canvases)-20); hashes={}; failures=[]
for idx in range(start,len(canvases)):
    url=image_url(canvases[idx])
    if not url: failures.append({"index":idx,"reason":"no_recoverable_image_url"}); continue
    try: hashes[idx]=fetch_hash(url)
    except Exception as exc: failures.append({"index":idx,"reason":f"{type(exc).__name__}: {exc}"})

best=None
for seq in range(start,len(canvases)-5):
    if not all((seq+j) in hashes for j in range(6)): continue
    distances=[hamming(expected[j]["dhash256"],hashes[seq+j]) for j in range(6)]; score=(sum(distances),max(distances))
    if best is None or score < best[:2]: best=(score[0],score[1],distances,seq)

if best is None:
    print("OK-DEGRADED: IIIF Presentation 3 manifest and explicit NONCANONICAL registry status remain valid; live six-Canvas perceptual recheck was unavailable because of third-party image failures. Prior strong-mismatch evidence remains registered; canonical checksum-fixed facsimile is not substituted. failures="+json.dumps(failures,ensure_ascii=False))
    sys.exit(0)

total,maxd,distances,seq=best; mean=total/6; labels=[label_text(c) for c in canvases[seq:seq+6]]
if maxd<=72 and mean<=48:
    print(f"ERROR: external witness is unexpectedly close to canonical scan; explicit identity reconsideration required. indexes={seq}-{seq+5}, labels={labels!r}, distances={distances}, mean={mean:.2f}"); sys.exit(1)
print(f"OK: IA item remains a valid IIIF Presentation 3 NONCANONICAL parallel witness; Canvas count={len(canvases)}; best live window={seq}-{seq+5}; labels={labels!r}; distances={distances}; mean={mean:.2f}; transient_failures={len(failures)}. No external Canvas is substituted for the checksum-fixed working facsimile.")
