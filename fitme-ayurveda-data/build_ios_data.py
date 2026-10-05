"""Write the bundled JSON files the FITme iOS app loads (fitme-ios/Resources/).

  AyurvedaOTC.json   classical Ayurvedic options for 15 minor complaints (English + Hindi)
  HerbSafety.json    113 herbs/products with safety flags and drug-class interactions
  Medicines.json     2,626 medicines -> drug classes + aliases for scanner matching

Run after build_ayurveda.py and build_otc_alternatives.py.
"""
import json
import os
import re

from hindi_names import COMPLAINTS_HI, HERBS_HI, OPTIONS_HI

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "fitme-ios", "Resources")
DISCLAIMER = ("General safety information, not medical advice. Do not start, stop or change any "
              "medicine or herbal product without talking to your doctor or pharmacist.")

CLASS_LABELS = {
    "anticoagulant_vka": "Blood thinner (warfarin-type)", "anticoagulant_doac": "Blood thinner (newer oral)",
    "anticoagulant_heparin": "Blood thinner (heparin)", "antiplatelet": "Antiplatelet", "nsaid": "Painkiller (NSAID)",
    "antidiabetic_insulin": "Insulin", "antidiabetic_sulfonylurea": "Diabetes medicine (sulfonylurea)",
    "antidiabetic_other": "Diabetes medicine", "antihypertensive": "Blood pressure medicine",
    "diuretic_loop_thiazide": "Water tablet (diuretic)", "potassium_sparing": "Potassium-raising medicine",
    "cardiac_glycoside": "Digoxin", "antiarrhythmic": "Heart rhythm medicine", "nitrate_pde5": "Nitrate / PDE5 inhibitor",
    "statin": "Statin", "thyroid_hormone": "Thyroid hormone", "antithyroid": "Antithyroid medicine",
    "immunosuppressant": "Immunosuppressant", "corticosteroid": "Steroid",
    "antidepressant_ssri_snri": "Antidepressant (SSRI/SNRI)", "antidepressant_maoi": "Antidepressant (MAOI)",
    "antidepressant_tca": "Antidepressant (tricyclic)", "sedative_hypnotic": "Sedative / sleeping pill",
    "antiepileptic": "Anti-seizure medicine", "antipsychotic": "Antipsychotic", "lithium": "Lithium", "opioid": "Opioid",
    "anticancer": "Cancer medicine", "antiretroviral": "HIV medicine", "antibiotic_chelating": "Antibiotic (binds minerals)",
    "antibiotic_other": "Antibiotic", "antitubercular": "TB medicine", "hepatotoxic": "Medicine that can strain the liver",
    "nephrotoxic": "Medicine that can strain the kidneys", "hormonal_contraceptive_estrogen": "Hormonal contraceptive / oestrogen",
    "ppi_antacid": "Acid reducer", "iron_mineral_supplement": "Iron / mineral", "laxative_stimulant": "Stimulant laxative",
    "theophylline": "Theophylline", "anaesthesia_surgery": "Anaesthesia / surgery",
    "cyp3a4_substrate_narrow": "Processed by CYP3A4 (narrow margin)", "cyp2c9_substrate": "Processed by CYP2C9",
    "cyp2d6_substrate": "Processed by CYP2D6", "cyp1a2_substrate": "Processed by CYP1A2",
    "cyp2c19_substrate": "Processed by CYP2C19", "pgp_substrate": "Moved by P-gp transporter",
    "antiparkinson_levodopa": "Parkinson's medicine (levodopa)", "photosensitizing": "Causes sun sensitivity",
    "anticholinergic": "Anticholinergic",
}
DEVANAGARI = re.compile(r"[ऀ-ॿ][ऀ-ॿ\s]*[ऀ-ॿ]|[ऀ-ॿ]")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def hindi_of(text):
    """Pull the Devanagari part out of strings like 'Ashwagandha (अश्वगंधा)'."""
    m = DEVANAGARI.findall(text or "")
    return " / ".join(x.strip() for x in m) if m else None


def write(name, obj):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{name}: {os.path.getsize(path) / 1024:.0f} KB")


def otc():
    src = json.load(open(os.path.join(HERE, "fitme_ayurvedic_otc_alternatives.json"), encoding="utf-8"))
    complaints = []
    for c in src["complaints"]:
        cid = slug(c["complaint"])
        complaints.append({
            "id": cid, "title": c["complaint"], "titleHi": COMPLAINTS_HI.get(c["complaint"]),
            "otcMedicinesUsuallyUsed": c["otcMedicinesUsuallyUsed"], "seeADoctorIf": c["seeADoctorIf"],
            "source": c["source"],
            "options": [{"id": f"{cid}--{slug(o['name'])}", "name": o["name"], "nameHi": OPTIONS_HI.get(o["name"]),
                         "form": o["form"], "howUsed": o["howUsed"], "caution": o["caution"]} for o in c["options"]],
        })
    missing = [o["name"] for c in complaints for o in c["options"] if not o["nameHi"]]
    assert not missing, f"missing Hindi names: {missing}"
    write("AyurvedaOTC.json", {"version": "1.0.0", "disclaimer": src["disclaimer"], "complaints": complaints})


def herbs():
    src = json.load(open(os.path.join(HERE, "herbs.json"), encoding="utf-8"))["herbs"]
    out = []
    for h in src:
        n = h["names"]
        out.append({
            "id": h["id"], "name": n.get("common_en") or h["id"], "nameHi": hindi_of(n.get("hindi")) or HERBS_HI.get(h["id"]),
            "sanskrit": n.get("sanskrit") or None, "latin": n.get("latin") or None,
            "otherNames": n.get("other") or [], "kind": h["kind"], "dataQuality": h["data_quality"],
            "traditionalContext": h.get("traditional_context") or None,
            "isAyurvedic": h.get("traditional_source_type") != "non_ayurvedic",
            "commonProducts": h.get("common_products") or [],
            "safetyFlags": [{"flag": s["flag"], "note": s["note"], "evidence": s["evidence"],
                             "sources": [x["url"] for x in s.get("sources", [])]} for s in h["general_safety"]],
            "interactions": [{"drugClass": i["drug_class"], "severity": i["severity"], "effect": i["effect"],
                              "mechanism": i.get("mechanism") or None, "evidence": i.get("evidence") or None,
                              "advice": i.get("advice") or None, "sources": [x["url"] for x in i.get("sources", [])],
                              "onlyMolecules": i.get("only_molecules"), "majorOnlyFor": i.get("major_only_for")}
                             for i in h["interactions"]],
            "herbWarnings": [{"severity": i["severity"], "effect": i["effect"],
                              "sources": [x["url"] for x in i.get("sources", [])]} for i in h["herb_level_warnings"]],
        })
    write("HerbSafety.json", {"version": "1.0.0", "disclaimer": DISCLAIMER, "drugClassLabels": CLASS_LABELS, "herbs": out})


def medicines():
    src = json.load(open(os.path.join(HERE, "medicines.json"), encoding="utf-8"))["medicines"]
    out = [{"id": m["molecule"], "name": m["name"], "classes": m["classes"],
            "aliases": m["aliases"][:30], "inNLEM": m["in_nlem"]} for m in src]
    write("Medicines.json", {"version": "1.0.0", "medicines": out})


if __name__ == "__main__":
    otc()
    herbs()
    medicines()
