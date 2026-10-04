"""Build FITme's medicine database: molecule -> herb-interaction drug_class keys (research/SPEC.md).

Sources (see research/medicines_notes.md for licences):
  - openFDA drug NDC + drug label bulk downloads (public domain, CC0): molecules, FDA Established
    Pharmacologic Classes (EPC) / MoA, US brand names.
  - FDA "Drug Development and Drug Interactions" substrate tables (US government work): CYP/P-gp keys.
  - India NLEM 2022 (MoHFW/CDSCO PDF) and the PMBJP Jan Aushadhi product list (PMBI's own
    "Export" of its product table): Indian generic molecules.
  - medicine_rules.py: hand-written EPC map, overrides, INN<->USAN synonyms.

Usage:
  python3 build_medicines.py [--cache DIR] [--no-labels]

Downloads everything into the cache dir (default .cache/, gitignored) on first run; the label
dataset (~1.8 GB zipped) is streamed with ijson and reduced to a small JSONL of openfda fields.
Writes research/medicines.csv, research/medicine_aliases.csv, research/medicine_class_evidence.csv
and research/medicines_build_stats.json.
"""
import argparse
import csv
import html
import http.cookiejar
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict

import medicine_rules as R

try:
    import ijson
except ImportError:  # streaming parser; falls back to json.load per file (needs ~3 GB RAM)
    ijson = None

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "research")

OPENFDA_MANIFEST = "https://api.fda.gov/download.json"
NLEM_URL = "https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadConsumer/nlem2022.pdf"
PMBI_URL = "https://www.pmbi.co.in/ProductList.aspx"
UA = "Mozilla/5.0 (FITme medicine research; contact via app store listing)"

SPEC_KEYS = [
    "anticoagulant_vka", "anticoagulant_doac", "anticoagulant_heparin", "antiplatelet", "nsaid",
    "antidiabetic_insulin", "antidiabetic_sulfonylurea", "antidiabetic_other", "antihypertensive",
    "diuretic_loop_thiazide", "potassium_sparing", "cardiac_glycoside", "antiarrhythmic",
    "nitrate_pde5", "statin", "thyroid_hormone", "antithyroid", "immunosuppressant", "corticosteroid",
    "antidepressant_ssri_snri", "antidepressant_maoi", "antidepressant_tca", "sedative_hypnotic",
    "antiepileptic", "antipsychotic", "lithium", "opioid", "anticancer", "antiretroviral",
    "antibiotic_chelating", "antibiotic_other", "antitubercular", "hepatotoxic", "nephrotoxic",
    "hormonal_contraceptive_estrogen", "ppi_antacid", "iron_mineral_supplement", "laxative_stimulant",
    "theophylline", "anaesthesia_surgery", "cyp3a4_substrate_narrow", "cyp2c9_substrate",
    "cyp2d6_substrate", "cyp1a2_substrate", "pgp_substrate", "any_medicine",
]

# NDC marketing categories that are not finished medicines a person takes.
SKIP_CATEGORIES = {
    "UNAPPROVED HOMEOPATHIC", "BULK INGREDIENT", "DRUG FOR FURTHER PROCESSING",
    "BULK INGREDIENT FOR HUMAN PRESCRIPTION COMPOUNDING", "EXPORT ONLY",
}
SKIP_PRODUCT_TYPES = {"NON-STANDARDIZED ALLERGENIC", "STANDARDIZED ALLERGENIC",
                      "ANIMAL DRUG FOR FURTHER PROCESSING", "LICENSED VACCINE BULK INTERMEDIATE"}


# ---------------------------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------------------------
def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print("downloading", url, file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest + ".part", "wb") as f:
        shutil.copyfileobj(r, f)
    os.replace(dest + ".part", dest)
    return dest


def openfda_partitions(cache, name):
    manifest = json.load(open(fetch(OPENFDA_MANIFEST, os.path.join(cache, "download.json"))))
    entry = manifest["results"]["drug"][name]
    sub = "" if name == "ndc" else name
    paths = [fetch(p["file"], os.path.join(cache, sub, os.path.basename(p["file"])))
             for p in entry["partitions"]]
    return paths, entry.get("export_date")


def iter_results(zip_path):
    z = zipfile.ZipFile(zip_path)
    with z.open(z.namelist()[0]) as fh:
        if ijson:
            yield from ijson.items(fh, "results.item")
        else:
            yield from json.load(fh)["results"]


# ---------------------------------------------------------------------------------------------
# Name normalisation
# ---------------------------------------------------------------------------------------------
_BIOSIMILAR_SUFFIX = re.compile(r"-[a-z]{4}$")


NAME_MAP = {**R.SYNONYMS, **R.SPELLING_VARIANTS}


def _clean(name):
    s = name.lower().replace("\u00a0", " ").replace("\u2019", "'")
    # British/Indian spellings -> US spellings used by openFDA
    s = s.replace("aluminium", "aluminum").replace("sulph", "sulf")
    s = re.sub(r"\s*\*+\s*$", "", s)
    s = re.sub(r"\((?:[a-c])\)", " ", s)  # NLEM "(A)" "(B)" component markers
    s = s.replace(",", " ")
    return re.sub(r"\s+", " ", s).strip()


def _strip_salts(s):
    toks = s.split()
    while len(toks) > 1 and toks[-1] in R.SALT_TOKENS:
        cand = toks[:-1]
        if all(t in R.ION_BASES or t in R.SALT_TOKENS for t in cand):
            break
        toks = cand
    return " ".join(toks)


def normalize(name):
    """Raw ingredient name -> list of canonical molecule keys (a synonym may expand to several)."""
    s = _clean(name)
    if not s:
        return []
    for cand in (s, _strip_salts(s)):
        if cand in NAME_MAP:
            return NAME_MAP[cand].split("|")
    s = _BIOSIMILAR_SUFFIX.sub("", s) if " " not in s and len(s) > 9 else s
    s = _strip_salts(s)
    return NAME_MAP.get(s, s).split("|")


# ---------------------------------------------------------------------------------------------
# openFDA aggregation
# ---------------------------------------------------------------------------------------------
GENERIC_BRAND_WORDS = set("""
pain relief reliever relieving extra strength regular maximum children's childrens children infant
infants adult adults junior tablets tablet caplets caplet capsules capsule gelcaps softgels liquid
oral suspension solution cream ointment gel lotion spray drops injection usp ip bp mg mcg ml er xr sr
dr cd la hcl hydrochloride sodium potassium fever reducer allergy cold flu cough sinus headache
night day time nighttime daytime formula plus original brand care health mart up and good sense
equate basic leader kirkland signature rite aid cvs walgreens topcare quality choice sunmark
harris teeter members mark premier value smart sense pharmacy chewable chewables dissolve fast
""".split())


def brand_ok(brand, molecules, raw_names, generic):
    b = brand.lower().strip()
    if not b or len(b) < 3 or b == (generic or "").lower().strip():
        return False
    for m in list(molecules) + list(raw_names):
        for tok in re.split(r"[\s,/-]+", m.lower()):
            if len(tok) > 4 and tok in b:
                return False
    words = re.findall(r"[a-z']+", b)
    return bool(words) and not all(w in GENERIC_BRAND_WORDS for w in words)


class Agg:
    def __init__(self):
        self.epc = defaultdict(Counter)          # molecule -> EPC counts (single-ingredient products)
        self.moa = defaultdict(Counter)
        self.brands = defaultdict(Counter)       # molecule -> (brand, approved_flag) counts
        self.raw = defaultdict(set)              # molecule -> raw salt/ester names seen
        self.products = Counter()
        self.combo_epcs = []                     # (ingredients tuple, epc set) for inference
        self.brand_index = defaultdict(lambda: {"sets": set(), "n": 0})

    def add(self, ingredients_raw, epcs, moas, brand, generic, approved, source):
        mols = []
        for raw in ingredients_raw:
            for m in normalize(raw):
                if m and m not in mols:
                    mols.append(m)
                    self.raw[m].add(raw.strip().lower())
        if not mols:
            return
        for m in mols:
            self.products[m] += 1
        if len(mols) == 1:
            m = mols[0]
            for e in epcs:
                self.epc[m][e] += 1
            for e in moas:
                self.moa[m][e] += 1
        elif epcs:
            self.combo_epcs.append((tuple(mols), frozenset(epcs)))
        if brand and brand_ok(brand, mols, ingredients_raw, generic):
            disp = brand.strip()
            disp = disp.title() if disp.isupper() else disp
            if len(mols) == 1:
                self.brands[mols[0]][(disp, approved)] += 1
            bi = self.brand_index[disp.lower()]
            bi["sets"].add(tuple(sorted(mols)))
            bi["n"] += 1
            bi.setdefault("display", Counter())[disp] += 1


def _split_classes(pharm_class):
    epc = [p[:-6] for p in pharm_class if p.endswith(" [EPC]")]
    moa = [p[:-6] for p in pharm_class if p.endswith(" [MoA]")]
    return epc, moa


def load_ndc(agg, cache):
    paths, date = openfda_partitions(cache, "ndc")
    n = 0
    for p in paths:
        for x in iter_results(p):
            if x.get("marketing_category") in SKIP_CATEGORIES or x.get("product_type") in SKIP_PRODUCT_TYPES:
                continue
            ings = [a["name"] for a in x.get("active_ingredients") or [] if a.get("name")]
            if not ings:
                continue
            epc, moa = _split_classes(x.get("pharm_class") or [])
            approved = (x.get("marketing_category") or "").startswith(("NDA", "BLA"))
            agg.add(ings, epc, moa, x.get("brand_name"), x.get("generic_name"), approved, "ndc")
            n += 1
    return n, date


def load_labels(agg, cache, known):
    """Stream the label dataset once into a compact JSONL, then aggregate from it."""
    paths, date = openfda_partitions(cache, "label")
    compact = os.path.join(cache, "label_openfda.jsonl")
    if not os.path.exists(compact):
        with open(compact + ".part", "w") as out:
            for p in paths:
                for r in iter_results(p):
                    o = r.get("openfda") or {}
                    keep = {k: o[k] for k in ("generic_name", "brand_name", "substance_name",
                                              "pharm_class_epc", "pharm_class_moa", "route",
                                              "product_type", "application_number") if k in o}
                    if keep:
                        out.write(json.dumps(keep) + "\n")
        os.replace(compact + ".part", compact)
    n = 0
    for line in open(compact):
        r = json.loads(line)
        subs = r.get("substance_name") or []
        if not subs:
            continue
        app = (r.get("application_number") or [""])[0]
        mols = {m for s in subs for m in normalize(s)}
        # New molecules only from approved applications (keeps homeopathic labels out).
        if not app.startswith(("NDA", "ANDA", "BLA")) and not mols <= known:
            continue
        epc = [e[:-6] for e in r.get("pharm_class_epc") or []]
        moa = [e[:-6] for e in r.get("pharm_class_moa") or []]
        agg.add(subs, epc, moa, (r.get("brand_name") or [None])[0], (r.get("generic_name") or [None])[0],
                app.startswith(("NDA", "BLA")), "label")
        n += 1
    return n, date


def infer_combo_epcs(agg):
    """Two-or-more-ingredient products: if exactly one ingredient has no single-ingredient EPC,
    give it the combo EPCs that none of the other ingredients explain (e.g. sacubitril)."""
    inferred = defaultdict(Counter)
    for mols, epcs in agg.combo_epcs:
        unknown = [m for m in mols if not agg.epc.get(m)]
        if len(unknown) != 1:
            continue
        explained = set()
        for m in mols:
            explained |= set(agg.epc.get(m, {}))
        for e in epcs - explained:
            inferred[unknown[0]][e] += 1
    for m, c in inferred.items():
        agg.epc[m].update(c)
    return {m: sorted(c) for m, c in inferred.items()}


# ---------------------------------------------------------------------------------------------
# FDA DDI substrate table
# ---------------------------------------------------------------------------------------------
CYP_KEYS = {"3A": "cyp3a4_substrate_narrow", "2C9": "cyp2c9_substrate", "2D6": "cyp2d6_substrate",
            "1A2": "cyp1a2_substrate"}


def _fda_name(cell):
    s = html.unescape(re.sub(r"<[^>]+>", "", cell)).strip().lower()
    s = re.sub(r"[\d,\s]+$", "", s).strip()  # footnote numbers ("warfarin19", "ritonavir 14, 15")
    return R.FDA_NAME_FIX.get(s, s)


def load_fda_ddi(cache):
    path = fetch(R.FDA_HCP_URL, os.path.join(cache, "fda", "hcp_table.html"))
    t = open(path, encoding="utf-8", errors="replace").read()
    table = re.search(r"(?s)<table.*?</table>", t).group(0)
    rows = re.findall(r"(?s)<tr.*?</tr>", table)
    header = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
              for c in re.findall(r"(?s)<t[hd][^>]*>(.*?)</t[hd]>", rows[0])]
    col = {h: i for i, h in enumerate(header)}
    out = []
    for r in rows[1:]:
        cells = re.findall(r"(?s)<t[hd][^>]*>(.*?)</t[hd]>", r)
        if len(cells) != len(header):
            continue
        name = _fda_name(cells[0])
        if " and " in name or "(" in name:
            continue
        for head, tier in (("CYP SENS SUB", "sensitive"), ("CYP Mod SENS SUB", "moderate sensitive")):
            txt = html.unescape(re.sub(r"<[^>]+>", " ", cells[col[head]]))
            for enz, key in CYP_KEYS.items():
                if re.search(r"\b" + enz + r"\b", txt):
                    out.append((name, key, f"{enz} {tier} substrate (FDA HCP table)", R.FDA_HCP_URL))
        trn = html.unescape(re.sub(r"<[^>]+>", " ", cells[col["TRNSP SUB"]]))
        if "P-gp" in trn:
            out.append((name, "pgp_substrate", "P-gp substrate (FDA HCP table)", R.FDA_HCP_URL))
    as_of = re.search(r"current as of:.*?(\d\d/\d\d/\d{4})", t, re.S)
    return out + list(R.FDA_LEGACY_SUBSTRATES), as_of.group(1) if as_of else None


# ---------------------------------------------------------------------------------------------
# India: NLEM 2022 and Jan Aushadhi
# ---------------------------------------------------------------------------------------------
def load_nlem(cache):
    pdf = fetch(NLEM_URL, os.path.join(cache, "india", "nlem2022.pdf"))
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext (poppler-utils) is required to read the NLEM PDF")
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    start = txt.index("Alphabetical List of Medicines in NLEM 2022\n\n1.")
    end = txt.index("Medicines Added Therapeutic category wise", start)
    block = txt[start:end].replace("Insulin (S\noluble)", "Insulin (Soluble)")
    block = re.sub(r"Nevir\s*\napine", "Nevirapine", block)
    entries = []
    for line in block.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.+?)\s*$", line)
        if m:
            entries.append(re.sub(r"\s+", " ", m.group(2)))
    return entries


def nlem_components(entry):
    """'Abacavir (A) + Lamivudine (B)' -> ['abacavir', 'lamivudine'] (canonical keys)."""
    e = entry.lower().strip()
    if e in R.NLEM_NON_MOLECULES:
        return []
    if "vaccine" in e or "immunoglobulin" in e or "antiserum" in e or "antitoxin" in e:
        return [re.sub(r"\s*\+\s*", "+", e)]
    e = re.sub(r"^co-trimoxazole \[(.*)\]$", r"\1", e)
    out = []
    for part in re.split(r"\s*\+\s*|\s{2,}", e):
        part = re.sub(r"\((?:[a-c])\)", "", part).strip(" *")
        cp = _clean(part)
        if cp in NAME_MAP or cp.split(" (")[0] in NAME_MAP:
            key = cp if cp in NAME_MAP else cp.split(" (")[0]
            out += NAME_MAP[key].split("|")
            continue
        part = re.sub(r"\s*\(.*?\)\s*", " ", part).strip()
        out += normalize(part)
    return [o for o in out if o]


def load_janaushadhi(cache):
    """PMBI's product table (the same data its 'Export to PDF' button produces)."""
    tsv = os.path.join(cache, "india", "pmbi_products.tsv")
    if not os.path.exists(tsv):
        cj = http.cookiejar.CookieJar()
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        op.addheaders = [("User-Agent", UA)]

        def hidden(t):
            return {m.group(1): html.unescape(m.group(2)) for m in
                    re.finditer(r'<input type="hidden" name="([^"]+)" id="[^"]+" value="([^"]*)"', t)}
        page = op.open(PMBI_URL, timeout=120).read().decode("utf-8", "replace")
        form = hidden(page)
        form.update({"ctl00$Bppi_body$ddlProduct": "", "ctl00$Bppi_body$txtSearch": "",
                     "ctl00$Bppi_body$btnSearch": "Search"})
        page = op.open(PMBI_URL, urllib.parse.urlencode(form).encode(), timeout=300).read().decode("utf-8", "replace")
        os.makedirs(os.path.dirname(tsv), exist_ok=True)
        with open(tsv, "w", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            for row in re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", page):
                cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ")).strip()
                         for c in re.findall(r"(?s)<t[dh][^>]*>(.*?)</t[dh]>", row)]
                if cells:
                    w.writerow(cells)
    rows = list(csv.reader(open(tsv), delimiter="\t"))
    return [{"code": r[1], "name": r[2]} for r in rows[1:] if len(r) >= 3]


JA_FORM_WORDS = set("""
tablet tablets tab tabs capsule capsules cap caps capulses injection injections inj syrup suspension
oral solution drops drop eye ear nasal gel cream ointment lotion spray powder granules sachet sachets
infusion inhaler respules respule rotacaps rotacap transdermal patch patches vaginal pessary pessaries
suppository suppositories dispersible chewable effervescent film coated film-coated uncoated
gastro-resistant gastro resistant enteric delayed prolonged extended modified sustained controlled
release released immediate orally disintegrating mouth dissolving strips strip sublingual buccal
paediatric pediatric adult dry reconstitution for use ip bp usp i.p. b.p. u.s.p. nf ph.eur equivalent
eq. eq to as each contains containing per base sr er xr cr dr md od mr sterile vial vials ampoule
ampoules bottle pfs prefilled pre-filled syringe pen cartridge kit combi pack lozenges lozenge
liquid elixir emulsion mouthwash gargle toothpaste shampoo soap facewash face wash dusting topical
solution. tablets. caps. w/w w/v v/v v/w mg mcg gm g ml kg iu units unit lakh million billion cfu
spores au i.u. mmol meq % w v plain sugar free sugar-free flavoured flavour orange mint strawberry
mixed fruit with without in of the a an to new hcl bulk cutaneous dermal concentrate diluent
preservative preservatives benzalkonium chloride sodium methylparaben propylparaben ophthalmic otic
nebuliser nebulizer nebulisation inhalation aerosol metered dose mdi dpi intrauterine device double
single strength forte junior kid kids cold elastic
""".split())


def ja_chunks(name):
    s = name.lower().replace("\u00a0", " ")
    s = re.sub(r"\b\d+(\.\d+)?\s*(mg|mcg|µg|gm|g|ml|iu|i\.u\.|%|lakh|million|billion|cfu|au|units?|meq|mmol)\b", " ", s)
    s = re.sub(r"\b(w/w|w/v|v/v|v/w)\b", " ", s)
    s = re.sub(r"\d+(\.\d+)?", " ", s)
    parts = re.split(r",|\+|&|\(|\)|\[|\]|;|\band\b|\bwith\b|/| - ", s)
    out = []
    for p in parts:
        words = [w for w in re.findall(r"[a-z][a-z0-9'.-]*", p) if w.strip(".") not in JA_FORM_WORDS and w not in JA_FORM_WORDS]
        words = [w.strip(".-") for w in words if w.strip(".-")]
        if words:
            out.append(words)
    return out


def match_ja(name, vocab):
    found, unmatched = [], []
    for words in ja_chunks(name):
        hit = None
        for n in range(min(len(words), 5), 0, -1):
            for i in range(len(words) - n + 1):
                cand = " ".join(words[i:i + n])
                keys = normalize(cand)
                if keys and all(k in vocab for k in keys):
                    hit = keys
                    break
            if hit:
                break
        if hit:
            found += [k for k in hit if k not in found]
        else:
            unmatched.append(" ".join(words))
    return found, unmatched


# ---------------------------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------------------------
def classify(mol, epcs, moas, ddi, evidence):
    keys = []

    def add(k, basis, src):
        if k not in SPEC_KEYS:
            raise ValueError(f"unknown spec key {k} for {mol}")
        if k not in keys:
            keys.append(k)
        evidence.append((mol, k, basis, src))

    for e in epcs:
        for k in R.EPC_MAP.get(e, []):
            add(k, f"FDA EPC: {e}", "openFDA")
    for e in moas:
        for k in R.MOA_MAP.get(e, []):
            add(k, f"FDA MoA: {e}", "openFDA")
    for k, basis, src in ddi.get(mol, []):
        add(k, basis, src)
    ov = R.OVERRIDES.get(mol, {})
    for k in ov.get("add", []):
        add(k, "manual" + (": " + ov["note"] if ov.get("note") else ""), "medicine_rules.OVERRIDES")
    for k in ov.get("remove", []):
        if k in keys:
            keys.remove(k)
            evidence[:] = [e for e in evidence if not (e[0] == mol and e[1] == k)]
    return [k for k in SPEC_KEYS if k in keys]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", default=os.path.join(HERE, ".cache"))
    ap.add_argument("--no-labels", action="store_true", help="skip the 1.8 GB openFDA label dataset")
    args = ap.parse_args()
    cache = args.cache
    stats = {}

    agg = Agg()
    stats["ndc_products_used"], stats["ndc_export_date"] = load_ndc(agg, cache)
    if not args.no_labels:
        stats["label_records_used"], stats["label_export_date"] = load_labels(agg, cache, set(agg.products))
    stats["combo_inferred_epc"] = infer_combo_epcs(agg)

    ddi_rows, stats["fda_hcp_table_as_of"] = load_fda_ddi(cache)
    ddi = defaultdict(list)
    for name, key, basis, src in ddi_rows:
        for m in normalize(name):
            if (key, basis, src) not in ddi[m]:
                ddi[m].append((key, basis, src))

    # India
    nlem_entries = load_nlem(cache)
    nlem = {}
    for e in nlem_entries:
        for m in nlem_components(e):
            nlem.setdefault(m, e)
    stats["nlem_entries"] = len(nlem_entries)
    stats["nlem_molecules"] = len(nlem)

    vocab = (set(agg.products) | set(nlem) | set(R.OVERRIDES) | set(R.INDIA_MOLECULES)
             | {v for s in NAME_MAP.values() for v in s.split("|")})
    ja_products = load_janaushadhi(cache)
    ja = defaultdict(list)
    ja_unmatched = Counter()
    ja_matched_products = 0
    for p in ja_products:
        found, unmatched = match_ja(p["name"], vocab)
        if found:
            ja_matched_products += 1
        for m in found:
            ja[m].append(p["name"])
        for u in unmatched:
            ja_unmatched[u] += 1
    stats["janaushadhi_products"] = len(ja_products)
    stats["janaushadhi_products_with_molecule"] = ja_matched_products
    stats["janaushadhi_molecules"] = len(ja)

    # Indian names seen in source text, for display names / aliases
    reverse_syn = defaultdict(list)
    for alias, target in NAME_MAP.items():
        for t in target.split("|"):
            if alias != t:
                reverse_syn[t].append(alias)
    india_text = " ".join(nlem_entries).lower() + " " + " ".join(p["name"] for p in ja_products).lower()

    molecules = sorted(set(agg.products) | set(nlem) | set(ja) | {m for m, o in R.OVERRIDES.items() if o.get("add") and (m in nlem or m in ja)})
    evidence = []
    rows = []
    for m in molecules:
        epcs = [e for e, _ in agg.epc.get(m, Counter()).most_common()]
        moas = [e for e, _ in agg.moa.get(m, Counter()).most_common()]
        keys = classify(m, epcs, moas, ddi, evidence)
        srcs = []
        if m in agg.products:
            srcs.append("openfda")
        if m in nlem:
            srcs.append("nlem")
        if m in ja:
            srcs.append("janaushadhi")
        if any(e[0] == m and e[3] == "medicine_rules.OVERRIDES" for e in evidence) and keys:
            srcs.append("manual")
        brands = sorted(agg.brands.get(m, Counter()).items(), key=lambda kv: (-kv[0][1], -kv[1], kv[0][0]))
        seen, us_brands = set(), []
        for (b, _approved), _n in brands:
            if b.lower() not in seen:
                seen.add(b.lower())
                us_brands.append(b)
            if len(us_brands) == 3:
                break
        india_alias = next((a for a in reverse_syn.get(m, []) if re.search(r"\b" + re.escape(a) + r"\b", india_text)), None)
        disp = m[:1].upper() + m[1:]
        if india_alias and india_alias != m:
            disp += f" ({india_alias})"
        rows.append({
            "molecule": m,
            "display_name": disp,
            "drug_classes": "|".join(keys),
            "fda_epc": "|".join(epcs),
            "sources": "|".join(srcs),
            "us_brand_examples": "|".join(us_brands),
            "in_nlem": "y" if m in nlem else "n",
        })

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "medicines.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    mol_set = set(molecules)
    with open(os.path.join(OUT, "medicine_class_evidence.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["molecule", "drug_class", "basis", "source"])
        w.writerows(sorted(set(e for e in evidence if e[0] in mol_set)))

    alias_rows = []
    for table, kind in ((R.SYNONYMS, "inn_ip_or_alternate_name"), (R.SPELLING_VARIANTS, "spelling_variant")):
        for alias, target in sorted(table.items()):
            targets = [t for t in target.split("|") if t in mol_set]
            if targets and alias not in targets:
                alias_rows.append([alias, kind, "|".join(targets), "manual", ""])
    for m in molecules:
        for raw in sorted(agg.raw.get(m, ())):
            r = re.sub(r"\s+", " ", raw)
            if r != m:
                alias_rows.append([r, "salt_or_ester_form", m, "openfda", ""])
    for b, info in sorted(agg.brand_index.items()):
        mols = sorted({x for s in info["sets"] for x in s})
        note = "brand covers several formulations" if len(info["sets"]) > 1 else ""
        alias_rows.append([info["display"].most_common(1)[0][0], "us_brand", "|".join(mols), "openfda", note])
    with open(os.path.join(OUT, "medicine_aliases.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["alias", "alias_type", "molecules", "source", "note"])
        w.writerows(alias_rows)

    cls_counter = Counter(k for r in rows for k in r["drug_classes"].split("|") if k)
    stats.update({
        "molecules": len(rows),
        "classified": sum(1 for r in rows if r["drug_classes"]),
        "with_fda_epc": sum(1 for r in rows if r["fda_epc"]),
        "by_source": Counter(s for r in rows for s in r["sources"].split("|")),
        "in_nlem": sum(1 for r in rows if r["in_nlem"] == "y"),
        "india_only": sum(1 for r in rows if "openfda" not in r["sources"]),
        "india_only_classified": sum(1 for r in rows if "openfda" not in r["sources"] and r["drug_classes"]),
        "class_counts": dict(cls_counter.most_common()),
        "unused_spec_keys": [k for k in SPEC_KEYS if k not in cls_counter],
        "aliases": Counter(a[1] for a in alias_rows),
        "nlem_unclassified": [m for m in nlem if not next(r for r in rows if r["molecule"] == m)["drug_classes"]],
        "ja_unmatched_top": ja_unmatched.most_common(400),
        "unmapped_epc_top": Counter(e for r in rows if not r["drug_classes"] for e in r["fda_epc"].split("|") if e).most_common(80),
    })
    with open(os.path.join(OUT, "medicines_build_stats.json"), "w") as f:
        json.dump(stats, f, indent=1, default=dict)
    print(json.dumps({k: stats[k] for k in ("molecules", "classified", "with_fda_epc", "in_nlem",
                                            "india_only", "india_only_classified", "by_source", "aliases")},
                     default=dict, indent=1))


if __name__ == "__main__":
    main()
