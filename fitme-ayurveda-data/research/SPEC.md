# FITme herb-drug safety database: shared spec

Purpose: when a user scans a medicine, FITme shows which Ayurvedic herbs/products may be risky
to combine with it. It NEVER suggests herbs as alternatives or treatments. Worldwide wording:
no disease claims ("treats", "cures", "for diabetes"); traditional uses phrased as
"traditionally used in Ayurveda for general wellbeing of X system".

## Shared drug interaction classes (use these exact keys)
anticoagulant_vka          # warfarin, acenocoumarol
anticoagulant_doac         # apixaban, rivaroxaban, dabigatran, edoxaban
anticoagulant_heparin      # heparin, enoxaparin
antiplatelet               # aspirin (low dose), clopidogrel, prasugrel, ticagrelor
nsaid                      # ibuprofen, diclofenac, naproxen
antidiabetic_insulin
antidiabetic_sulfonylurea  # glimepiride, gliclazide, glibenclamide
antidiabetic_other         # metformin, DPP-4i, SGLT2i, pioglitazone, GLP-1
antihypertensive           # ACEi, ARB, CCB, beta-blockers, alpha-blockers (general BP lowering)
diuretic_loop_thiazide     # furosemide, torsemide, HCTZ, chlorthalidone
potassium_sparing          # spironolactone, eplerenone, amiloride (+ ACEi/ARB hyperkalaemia risk)
cardiac_glycoside          # digoxin
antiarrhythmic             # amiodarone, flecainide, etc.
nitrate_pde5               # nitrates, sildenafil, tadalafil
statin
thyroid_hormone            # levothyroxine
antithyroid                # methimazole, carbimazole, propylthiouracil
immunosuppressant          # cyclosporine, tacrolimus, mycophenolate, azathioprine
corticosteroid
antidepressant_ssri_snri
antidepressant_maoi
antidepressant_tca
sedative_hypnotic          # benzodiazepines, z-drugs, barbiturates
antiepileptic
antipsychotic
lithium
opioid
anticancer                 # chemotherapy, targeted therapy, tamoxifen, etc.
antiretroviral             # HIV drugs
antibiotic_chelating       # fluoroquinolones, tetracyclines (mineral/chelation)
antibiotic_other
antitubercular             # isoniazid, rifampicin (hepatotoxic)
hepatotoxic                # methotrexate, high-dose paracetamol, valproate, etc.
nephrotoxic                # aminoglycosides, NSAIDs at high dose, etc.
hormonal_contraceptive_estrogen  # OCPs, HRT, tamoxifen-like interactions
ppi_antacid
iron_mineral_supplement
laxative_stimulant
theophylline
anaesthesia_surgery        # perioperative bleeding / sedation
cyp3a4_substrate_narrow    # narrow-therapeutic-index CYP3A4 substrates
cyp2c9_substrate
cyp2d6_substrate
cyp1a2_substrate
pgp_substrate              # digoxin, dabigatran, etc.
any_medicine               # general rule (e.g. separate dosing from isabgol/fibre)

## Herb record schema (one JSON object per herb/product)
{
 "id": "ashwagandha",
 "names": {"common_en": "", "hindi": "", "sanskrit": "", "latin": "", "other": []},
 "kind": "herb | formulation | mineral_preparation | food_spice",
 "common_products": ["Ashwagandharishta", "Ashwagandha churna", "KSM-66 capsules"],
 "traditional_context": "one neutral sentence, wellness framing, no disease names",
 "traditional_source_type": "API monograph | classical text | brand literature",
 "general_safety": [
   {"flag": "pregnancy|breastfeeding|liver|kidney|heavy_metals|bleeding|hypoglycaemia|hypotension|thyroid|autoimmune|surgery|children|allergy|other",
    "note": "", "evidence": "regulatory|clinical|case_reports|preclinical|theoretical",
    "sources": [{"title": "", "url": "", "type": "gov|peer_review|other"}]}
 ],
 "interactions": [
   {"drug_class": "<key from list above>",
    "severity": "major|moderate|minor",
    "effect": "plain-English: what may happen (e.g. 'may increase bleeding risk')",
    "mechanism": "e.g. 'antiplatelet activity; CYP2C9 inhibition in vitro'",
    "evidence": "clinical|case_reports|preclinical|theoretical",
    "advice": "e.g. 'Ask your doctor before combining; stop 2 weeks before surgery.'",
    "sources": [{"title": "", "url": "", "type": "gov|peer_review|other"}]}
 ],
 "data_quality": "good|limited|poor",
 "last_checked": "2026-10"
}

Rules:
- Every interaction and safety flag needs at least one real, checkable source URL (PubMed/PMC,
  NIH NCCIH, LiverTox, FDA, EMA HMPC, WHO monographs, AYUSH/API, Cochrane, peer-reviewed reviews).
- Classical texts / brand sites may only support "traditional_context", never interactions.
- Never invent a source, PMID or number. If unsure, omit the item or mark evidence "theoretical"
  and say so in mechanism.
- Severity: major = avoid combination / potentially serious; moderate = monitor, ask doctor;
  minor = small or theoretical effect.
- Advice must never say "stop your medicine" or "use herb instead". Default advice:
  "Talk to your doctor or pharmacist before combining."
