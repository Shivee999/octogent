"""Build fitme_ayurvedic_otc_alternatives.csv: classical Ayurvedic options for minor,
self-care complaints that people usually treat with over-the-counter (OTC) medicines.

Scope is deliberately limited to OTC / minor complaints. Prescription medicines for
serious conditions (diabetes, BP, heart, thyroid, blood thinners, epilepsy, mental
health, cancer, HIV, TB, antibiotics, steroids) are excluded: offering herbal swaps for
them can lead people to stop medicines they need, and advertising cures for many of
those conditions is banned under India's Drugs and Magic Remedies Act.

Every formulation comes from the Ministry of AYUSH "Ayurvedic Standard Treatment
Guidelines" (1st ed., 2017), level-1 (basic clinic) tables. Excluded on purpose even
where the guideline lists them: Rasa / Bhasma (metal-mineral) products, Sanjivani vati
(contains aconite), Sarpagandha (contains reserpine), Shuddha Vishtinduka (strychnine),
Eranda bija (castor seeds), Tankana (borax), Vishagarbha taila (aconite) and Ativisha.
Doses are omitted on purpose: they should come from a qualified Ayurvedic doctor.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STG = "Ministry of AYUSH, Ayurvedic Standard Treatment Guidelines (2017)"
STG_URL = "https://main.ayush.gov.in/ayurvedic-standard-treatment-guidelines/"

# Short cautions, taken from this repo's sourced safety research (herbs.json).
C = {
    "sugar": "About half sugar by weight; count it if you watch blood sugar.",
    "mulethi": "Contains licorice (mulethi): can raise blood pressure and lower potassium. Avoid with BP or heart medicines, water tablets, steroids, and in pregnancy.",
    "piperine": "Contains pepper/long pepper (piperine), which can change blood levels of many prescription medicines. Ask a pharmacist if you take any.",
    "ginger": "Ginger may add to the effect of blood thinners.",
    "laxative": "Laxative. Not for long-term use, children or pregnancy without a doctor's advice.",
    "senna": "Senna-based laxative. Not in pregnancy, breastfeeding or under 12; not for long-term use.",
    "castor": "Strong laxative. Not in pregnancy (can trigger labour) or for children.",
    "alcohol": "Contains natural alcohol (arishta, about 5–13%). Avoid in pregnancy, with liver disease, before driving, and with metronidazole/tinidazole.",
    "ashwagandha": "Ashwagandha: avoid in pregnancy, thyroid or autoimmune conditions, and before surgery; rare liver injury reported.",
    "guggulu": "Guggulu: avoid in pregnancy; may interact with BP and thyroid medicines. Buy from a licensed maker (heavy-metal contamination has been found in some products).",
    "nutmeg": "Nutmeg is toxic in large amounts; keep strictly to the advised dose and away from children.",
    "amla": "Amla may add to the effect of blood thinners and diabetes medicines.",
    "hing": "Contains asafoetida: not for infants or in pregnancy.",
    "vasa": "Vasa (adhatoda) is not for use in pregnancy.",
    "giloy": "Giloy (guduchi): liver injury has been reported; avoid with liver or autoimmune conditions.",
    "turmeric": "Turmeric may add to the effect of blood thinners; not in pregnancy at medicinal doses.",
    "sedative": "May add to drowsiness from sleeping pills, alcohol or antihistamines.",
    "limited": "Little safety research exists; avoid in pregnancy and check with a doctor if you take regular medicines.",
    "external": "For external use only; stop if the skin becomes irritated.",
    "mouth": "Apply in the mouth only; do not swallow large amounts.",
}

RED_FLAGS = {
    "acidity": "chest pain, vomiting blood, black stools, trouble swallowing, weight loss, or symptoms beyond 2 weeks",
    "constipation": "blood in stool, severe belly pain, weight loss, or no improvement in 2 weeks",
    "diarrhoea": "blood in stool, high fever, signs of dehydration, a child or older adult, or lasting more than 2 days (use ORS meanwhile)",
    "cough": "cough beyond 3 weeks, blood in phlegm, breathlessness, chest pain, or high fever",
    "cold": "high fever, breathlessness, ear or face pain, or symptoms beyond 10 days",
    "headache": "sudden severe headache, headache with fever and stiff neck, weakness, vision change, or after a head injury",
    "backache": "numbness, leg weakness, loss of bladder or bowel control, fever, or pain after a fall",
    "joints": "a hot, red or swollen joint, fever, or stiffness lasting all morning",
    "sleep": "trouble sleeping most nights for more than 4 weeks, loud snoring with pauses, or low mood",
    "mouth": "an ulcer lasting more than 3 weeks, a painless white or red patch, or ulcers with fever",
    "gums": "gums that bleed easily without brushing, loose teeth, or swelling of the face",
}

COMPLAINTS = [
    ("Acidity / heartburn after meals", "acidity", "Antacids (aluminium hydroxide, magnesium hydroxide, calcium carbonate, sodium bicarbonate); OTC acid reducers (famotidine, omeprazole 20 mg)", "Amlapitta, Table 3.1", [
        ("Avipattikara churna", "Powder", "internal", ["sugar", "laxative"]),
        ("Yashtimadhu churna", "Powder", "internal", ["mulethi"]),
        ("Amalaki churna", "Powder", "internal", ["amla"]),
        ("Shunthi churna", "Powder", "internal", ["ginger"]),
        ("Hingwashtaka churna", "Powder", "internal", ["hing", "piperine"]),
        ("Shivakshara pachana churna", "Powder", "internal", ["limited"]),
    ]),
    ("Occasional constipation", "constipation", "Bisacodyl, senna (sennosides), lactulose, polyethylene glycol 3350, docusate, psyllium", "Arsha Table 13.2; Parikartika Table 17.1; Mukhapaka Table 36.1", [
        ("Triphala churna", "Powder", "internal", ["laxative"]),
        ("Haritaki churna", "Powder", "internal", ["laxative"]),
        ("Draksha (dried black raisins)", "Dried fruit", "internal", []),
        ("Aragvadha churna", "Powder", "internal", ["laxative"]),
        ("Avipattikara churna", "Powder", "internal", ["sugar", "laxative"]),
        ("Swadishta virechana churna", "Powder", "internal", ["senna", "mulethi"]),
        ("Abhayarishta", "Arishta (liquid)", "internal", ["alcohol", "laxative"]),
        ("Castor oil (eranda taila)", "Oil", "internal", ["castor"]),
    ]),
    ("Loose motions (mild, adults)", "diarrhoea", "Loperamide, bismuth subsalicylate, racecadotril; oral rehydration salts (ORS)", "Atisara, Table 14.2", [
        ("Kutaja ghana vati", "Tablet", "internal", ["limited"]),
        ("Kutaja churna", "Powder", "internal", ["limited"]),
        ("Kutajarishta", "Arishta (liquid)", "internal", ["alcohol"]),
        ("Bilwadi gutika", "Tablet", "internal", ["limited"]),
        ("Bilwamoola churna", "Powder", "internal", ["limited"]),
        ("Dadimashtaka churna", "Powder", "internal", ["sugar"]),
        ("Dadima phala twak churna (pomegranate rind)", "Powder", "internal", ["limited"]),
        ("Musta churna", "Powder", "internal", ["limited"]),
        ("Shunthi churna", "Powder", "internal", ["ginger"]),
    ]),
    ("Cough (short-term)", "cough", "Dextromethorphan, guaifenesin, ambroxol, bromhexine, cough lozenges", "Kasa, Tables 1.2–1.5", [
        ("Sitopaladi churna", "Powder", "internal (with honey)", ["sugar"]),
        ("Yashtimadhu churna", "Powder", "internal (with honey)", ["mulethi"]),
        ("Talishadi churna", "Powder", "internal", ["sugar", "piperine"]),
        ("Vasa swarasa / Vasa churna", "Juice / powder", "internal", ["vasa"]),
        ("Bibhitaki churna with Pippali churna", "Powder", "internal", ["piperine"]),
        ("Bibhitaki kwatha", "Decoction", "internal", ["limited"]),
        ("Kantakaryadi kwatha", "Decoction", "internal", ["limited"]),
        ("Drakshadi leha", "Herbal jam (avaleha)", "internal", ["sugar"]),
        ("Agastya haritaki", "Herbal jam (avaleha)", "internal", ["sugar", "laxative"]),
        ("Trikatu with Vasa (with honey)", "Powder", "internal", ["piperine", "vasa"]),
    ]),
    ("Common cold: runny or blocked nose, sneezing", "cold", "Cetirizine, levocetirizine, chlorphenamine, phenylephrine, pseudoephedrine, xylometazoline nasal spray, cold & flu combinations", "Pratishyaya, Table 37.1", [
        ("Sitopaladi churna", "Powder", "internal", ["sugar"]),
        ("Talishadi churna", "Powder", "internal", ["sugar", "piperine"]),
        ("Trikatu churna", "Powder", "internal", ["piperine"]),
        ("Vyoshadi vati", "Tablet", "internal", ["piperine"]),
        ("Lavangadi vati", "Lozenge tablet", "internal (suck)", ["limited"]),
        ("Gojihvadi kwatha", "Decoction", "internal", ["limited"]),
        ("Dashamoola kwatha", "Decoction", "internal", ["limited"]),
        ("Haridra khanda", "Granules", "internal", ["turmeric", "sugar"]),
        ("Vasavaleha", "Herbal jam (avaleha)", "internal", ["vasa", "sugar"]),
        ("Drakshavaleha", "Herbal jam (avaleha)", "internal", ["sugar"]),
        ("Chitraka haritaki avaleha", "Herbal jam (avaleha)", "internal", ["sugar", "laxative"]),
    ]),
    ("Occasional tension-type headache", "headache", "Paracetamol, ibuprofen, aspirin", "Shiroroga, Table 38.2", [
        ("Pathyadi kwatha", "Decoction", "internal", ["laxative"]),
        ("Cow's ghee nasal drops (Gau ghrita nasya)", "Ghee", "nasal drops", ["limited"]),
    ]),
    ("Occasional lower-back stiffness or ache", "backache", "Ibuprofen, naproxen, diclofenac gel, methyl salicylate rubs", "Katigraha, Table 28.1", [
        ("Yogaraja guggulu", "Tablet", "internal", ["guggulu"]),
        ("Simhanada guggulu", "Tablet", "internal", ["guggulu", "laxative"]),
        ("Rasnasaptakam kashaya", "Decoction", "internal", ["limited"]),
        ("Dashamoola kashaya", "Decoction", "internal", ["limited"]),
        ("Rasna churna", "Powder", "internal", ["limited"]),
        ("Ashwagandha churna with Pippalimoola churna", "Powder", "internal", ["ashwagandha", "piperine"]),
        ("Shunthi churna", "Powder", "internal", ["ginger"]),
        ("Murivenna / Dhanwantharam taila / Nirgundyadi taila / Bala taila", "Oil", "external massage", ["external"]),
    ]),
    ("Occasional joint stiffness (massage oils)", "joints", "Diclofenac gel, methyl salicylate / menthol rubs", "Sandhigata vata, Table 31.1 (local application)", [
        ("Mahanarayana taila", "Oil", "external massage", ["external"]),
        ("Bala taila", "Oil", "external massage", ["external"]),
        ("Sahachara taila", "Oil", "external massage", ["external"]),
        ("Nirgundi taila", "Oil", "external massage", ["external"]),
        ("Dhanvantara taila", "Oil", "external massage", ["external"]),
        ("Kottamchukkadi taila", "Oil", "external massage", ["external"]),
    ]),
    ("Occasional trouble sleeping", "sleep", "Diphenhydramine, doxylamine, melatonin", "Anidra, Table 18.1", [
        ("Ashwagandhadi churna (with milk at bedtime)", "Powder", "internal", ["ashwagandha", "sedative"]),
        ("Tagara churna", "Powder", "internal", ["sedative", "limited"]),
        ("Jatiphala churna (nutmeg)", "Powder", "internal", ["nutmeg", "sedative"]),
        ("Pippalimula churna", "Powder", "internal", ["piperine"]),
        ("Saraswata churna", "Powder", "internal", ["sedative", "limited"]),
    ]),
    ("Mouth ulcers (minor)", "mouth", "Choline salicylate gel, benzocaine gel, antiseptic mouthwash", "Mukhapaka, Table 36.1", [
        ("Honey gargle (kshaudra)", "Liquid", "gargle", []),
        ("Jatipatra (jasmine leaf) paste", "Paste", "apply in mouth", ["mouth"]),
        ("Yashtimadhu churna with Gairika, in honey and ghee", "Powder", "apply in mouth", ["mouth"]),
        ("Darvighana with Gairika", "Powder", "apply in mouth", ["mouth"]),
        ("Samshamani vati (guduchi)", "Tablet", "internal", ["giloy"]),
        ("Swadishta virechana churna", "Powder", "internal (at night)", ["senna", "mulethi"]),
    ]),
    ("Gum care (sore or swollen gums)", "gums", "Chlorhexidine mouthwash, antiseptic gum gels", "Dantaveshta, Table 35.1", [
        ("Panchavalkala kwatha", "Decoction", "gargle", ["mouth"]),
        ("Kshiri vriksha kashaya", "Decoction", "hold in mouth, then spit", ["mouth"]),
        ("Dashana samskara churna", "Powder", "rub on gums", ["mouth"]),
        ("Kalaka churna", "Powder", "rub on gums", ["mouth"]),
        ("Pitaka churna", "Powder", "rub on gums", ["mouth"]),
    ]),
]


def main():
    out = os.path.join(HERE, "fitme_ayurvedic_otc_alternatives.csv")
    rows = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["complaint", "otc_medicines_usually_used", "ayurvedic_option", "form", "how_used",
                    "caution", "see_a_doctor_if", "source"])
        for complaint, key, otc, table, items in COMPLAINTS:
            for name, form, use, cautions in items:
                caution = " ".join(C[c] for c in cautions) or "No specific caution found; avoid in pregnancy unless a doctor advises."
                caution += " Dose: ask a qualified Ayurvedic doctor."
                w.writerow([complaint, otc, name, form, use, caution, RED_FLAGS[key], f"{STG}, {table}. {STG_URL}"])
                rows += 1
    print(out, rows, "rows")


if __name__ == "__main__":
    main()
