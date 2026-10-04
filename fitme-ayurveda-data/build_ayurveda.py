"""Merge FITme herb-drug safety research into app-ready files.

Inputs (research/):
  herbs_batch1..4.json   herb / formulation records (schema in research/SPEC.md)
  medicines.csv          molecules -> drug_class keys (built by build_medicines.py)
  medicine_aliases.csv   brand / alternate names -> molecules

Outputs (this folder):
  herbs.json                 cleaned herb records, with review fixes applied
  medicines.json             molecule -> classes, for the scanner lookup
  herb_drug_warnings.csv     every medicine x herb warning, expanded for review
  build_report.json          counts and wording-lint results

The app should join at runtime (scanned name -> molecule -> classes -> herb
interactions) using herbs.json + medicines.json; the expanded CSV exists so a
human can review exactly what each medicine will show.
"""
import csv
import glob
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "research")
SEV_RANK = {"major": 3, "moderate": 2, "minor": 1}

# --------------------------------------------------------------- review fixes
# Herbs that are not Ayurvedic but sold alongside it; shown with that label.
NON_AYURVEDIC = {"st_johns_wort", "ginseng", "green_tea_extract", "green_tea", "sea_buckthorn", "garcinia_cambogia"}

# A major rating backed by evidence for specific molecules only: those molecules
# keep "major", the rest of the class gets "moderate".
MAJOR_ONLY_FOR = {
    ("garlic", "antiretroviral"): {"saquinavir"},
    ("shankhpushpi", "antiepileptic"): {"phenytoin", "fosphenytoin"},
    ("daruharidra", "immunosuppressant"): {"cyclosporine", "ciclosporin"},
}
# Interactions that apply to named molecules only, not their whole class.
ONLY_MOLECULES = {
    ("ashwagandharishta", "antibiotic_other"): {"metronidazole", "tinidazole", "secnidazole", "ornidazole"},
    ("dashmularishta", "antibiotic_other"): {"metronidazole", "tinidazole", "secnidazole", "ornidazole"},
    ("arjunarishta", "antibiotic_other"): {"metronidazole", "tinidazole", "secnidazole", "ornidazole"},
    ("kumaryasava", "antibiotic_other"): {"metronidazole", "tinidazole", "secnidazole", "ornidazole"},
}

LEVODOPA_LABEL = {"title": "DailyMed: Carbidopa and levodopa tablets (label)",
                  "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9b17b028-964a-473c-823d-81423535bd66",
                  "type": "gov"}
RESERPINE_LABEL = {"title": "DailyMed: Reserpine tablets (label)",
                   "url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b503fa5e-5726-426d-867c-e8fe59ed3ead",
                   "type": "gov"}
EXTRA_INTERACTIONS = {
    # Researchers recorded these as safety notes because the class key did not exist yet.
    "kapikacchu": [{
        "drug_class": "antiparkinson_levodopa", "severity": "moderate",
        "effect": "Adds extra levodopa, which may cause unwanted movements, low blood pressure or confusion.",
        "mechanism": "Mucuna seeds naturally contain levodopa, in amounts that vary between products.",
        "evidence": "theoretical",
        "advice": "Talk to your doctor or pharmacist before combining.",
        "sources": [{"title": "Levodopa content of Mucuna pruriens products", "url": "https://pubmed.ncbi.nlm.nih.gov/35939305/", "type": "peer_review"}, LEVODOPA_LABEL]}],
    "sarpagandha": [{
        "drug_class": "antiparkinson_levodopa", "severity": "moderate",
        "effect": "May reduce how well levodopa works.",
        "mechanism": "Reserpine in sarpagandha depletes dopamine; the levodopa label advises against reserpine.",
        "evidence": "regulatory",
        "advice": "Talk to your doctor or pharmacist before combining.",
        "sources": [RESERPINE_LABEL, LEVODOPA_LABEL]}],
}

FORBIDDEN = re.compile(r"\b(cures?|curing|heals?|healing|remed(y|ies)|alternative to|instead of|replaces?|treats?|treatment for)\b", re.I)
DISEASE = re.compile(r"\b(diabet\w*|cancer|tumou?r|hypertension|arthritis|asthma|covid|corona\w*|obesity|infertility|"
                     r"impotence|tuberculosis|hepatitis|jaundice|epilep\w*|depression|anxiety disorder|insomnia|piles|"
                     r"ha?emorrhoids|kidney stones?|psoriasis|vitiligo|leucoderma|thyroid disease|parkinson\w*|dementia|alzheimer\w*)\b", re.I)
STOP_MED = re.compile(r"\bstop(ping)? (taking )?(your |any )?(prescribed )?(medicine|medication|drug)s?\b", re.I)


def load_herbs():
    recs = []
    for f in sorted(glob.glob(os.path.join(RES, "herbs_batch*.json"))):
        recs += json.load(open(f, encoding="utf-8"))
    for r in recs:
        if r["id"] in NON_AYURVEDIC:
            r["traditional_source_type"] = "non_ayurvedic"
        for it in r["interactions"]:
            # bakuchi's sun-sensitivity warning was filed under chelating antibiotics.
            if r["id"] == "bakuchi" and it["drug_class"] == "antibiotic_chelating" and "sun" in it["effect"].lower():
                it["drug_class"] = "photosensitizing"
            key = (r["id"], it["drug_class"])
            if key in MAJOR_ONLY_FOR:
                it["major_only_for"] = sorted(MAJOR_ONLY_FOR[key])
            if key in ONLY_MOLECULES:
                it["only_molecules"] = sorted(ONLY_MOLECULES[key])
        have = {it["drug_class"] for it in r["interactions"]}
        for extra in EXTRA_INTERACTIONS.get(r["id"], []):
            if extra["drug_class"] not in have:
                r["interactions"].append(extra)
        # "any_medicine" rows describe the herb's own toxicity or a dosing rule; the app
        # shows them on the herb itself rather than attaching them to every medicine.
        r["herb_level_warnings"] = [it for it in r["interactions"] if it["drug_class"] == "any_medicine"]
        r["interactions"] = [it for it in r["interactions"] if it["drug_class"] != "any_medicine"]
        r["max_severity"] = max([SEV_RANK[i["severity"]] for i in r["interactions"] + r["herb_level_warnings"]] or [0])
    return recs


def lint(recs):
    issues = []
    for r in recs:
        tc = r.get("traditional_context", "")
        if FORBIDDEN.search(tc) or DISEASE.search(tc):
            issues.append({"id": r["id"], "field": "traditional_context", "text": tc})
        for it in r["interactions"] + r["herb_level_warnings"]:
            for fld in ("effect", "advice"):
                t = it.get(fld, "")
                if FORBIDDEN.search(t) or STOP_MED.search(t):
                    issues.append({"id": r["id"], "field": f"{it['drug_class']}.{fld}", "text": t})
            if not it.get("sources"):
                issues.append({"id": r["id"], "field": f"{it['drug_class']}.sources", "text": "missing"})
    return issues


def load_medicines():
    meds = {}
    with open(os.path.join(RES, "medicines.csv"), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            classes = [c for c in (row.get("drug_classes") or "").split("|") if c]
            meds[row["molecule"]] = {
                "molecule": row["molecule"],
                "name": row.get("display_name") or row["molecule"],
                "classes": classes,
                "in_nlem": row.get("in_nlem") == "y",
                "sources": row.get("sources", ""),
                "us_brands": [b for b in (row.get("us_brand_examples") or "").split("|") if b],
            }
    aliases = defaultdict(set)
    path = os.path.join(RES, "medicine_aliases.csv")
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for m in (row.get("molecules") or "").split("|"):
                    if m in meds:
                        aliases[row["alias"].strip().lower()].add(m)
    return meds, aliases


def warnings_for(med, herbs):
    out = []
    classes = set(med["classes"])
    for h in herbs:
        best = None
        for it in h["interactions"]:
            if it["drug_class"] not in classes:
                continue
            only = it.get("only_molecules")
            if only and med["molecule"] not in only:
                continue
            sev = it["severity"]
            if it.get("major_only_for") and med["molecule"] not in it["major_only_for"]:
                sev = "moderate"
            cand = (SEV_RANK[sev], sev, it)
            if best is None or cand[0] > best[0]:
                best = cand
        if best:
            out.append((h, best[1], best[2]))
    out.sort(key=lambda x: (-SEV_RANK[x[1]], x[0]["names"]["common_en"]))
    return out


def main():
    herbs = load_herbs()
    issues = lint(herbs)
    meds, aliases = load_medicines()

    with open(os.path.join(HERE, "herbs.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"count": len(herbs), "spec": "research/SPEC.md",
                            "disclaimer": "Educational safety information only. Not medical advice. "
                                          "Do not start, stop or change any medicine or herbal product "
                                          "without talking to your doctor or pharmacist."},
                   "herbs": herbs}, f, ensure_ascii=False, indent=1)

    classified = {k: v for k, v in meds.items() if v["classes"]}
    by_mol_alias = defaultdict(list)
    for a, ms in aliases.items():
        for m in ms:
            if m in classified and a != m:
                by_mol_alias[m].append(a)
    with open(os.path.join(HERE, "medicines.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"count": len(classified), "note": "Only molecules with at least one interaction class. "
                            "aliases are lower-case brand/alternate names for scanner matching."},
                   "medicines": [dict(v, aliases=sorted(by_mol_alias.get(k, []))[:40]) for k, v in sorted(classified.items())]},
                  f, ensure_ascii=False, separators=(",", ":"))

    rows = 0
    sev_count = Counter()
    meds_with_warning = 0
    with open(os.path.join(HERE, "herb_drug_warnings.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["medicine", "drug_classes", "herb_id", "herb_name", "herb_kind", "severity", "drug_class_matched",
                    "effect", "mechanism", "evidence", "advice", "sources"])
        for m in sorted(classified.values(), key=lambda x: x["molecule"]):
            ws = warnings_for(m, herbs)
            if ws:
                meds_with_warning += 1
            for h, sev, it in ws:
                rows += 1
                sev_count[sev] += 1
                w.writerow([m["molecule"], "|".join(m["classes"]), h["id"], h["names"]["common_en"], h["kind"], sev,
                            it["drug_class"], it["effect"], it.get("mechanism", ""), it.get("evidence", ""),
                            it.get("advice", ""), " ".join(s["url"] for s in it.get("sources", []))])

    report = {
        "herbs": len(herbs),
        "herb_kinds": Counter(h["kind"] for h in herbs),
        "interaction_rules": sum(len(h["interactions"]) for h in herbs),
        "herb_level_warnings": sum(len(h["herb_level_warnings"]) for h in herbs),
        "medicines_total": len(meds),
        "medicines_classified": len(classified),
        "medicines_with_any_warning": meds_with_warning,
        "aliases": len(aliases),
        "expanded_warning_rows": rows,
        "expanded_by_severity": sev_count,
        "lint_issues": issues,
    }
    with open(os.path.join(HERE, "build_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "lint_issues"}, indent=1, default=dict))
    print("lint issues:", len(issues))
    for i in issues[:40]:
        print("  ", i["id"], i["field"], "|", i["text"][:120])


if __name__ == "__main__":
    main()
