import json, re, time, urllib.request

OUT = "/home/user/octogent/fitme-ayurveda-data/research/herbs_batch1.json"
SPEC = "/home/user/octogent/fitme-ayurveda-data/research/SPEC.md"
ADV = "Talk to your doctor or pharmacist before combining."

# ---------------- government / regulatory sources (URLs checked) ----------------
EMA = "https://www.ema.europa.eu/en/documents/herbal-monograph/"
GOV = {
 "nccih_ash": ("NCCIH fact sheet: Ashwagandha", "https://www.nccih.nih.gov/health/ashwagandha"),
 "nccih_tur": ("NCCIH fact sheet: Turmeric", "https://www.nccih.nih.gov/health/turmeric"),
 "nccih_gin": ("NCCIH fact sheet: Ginger", "https://www.nccih.nih.gov/health/ginger"),
 "nccih_gar": ("NCCIH fact sheet: Garlic", "https://www.nccih.nih.gov/health/garlic"),
 "nccih_fen": ("NCCIH fact sheet: Fenugreek", "https://www.nccih.nih.gov/health/fenugreek"),
 "nccih_lic": ("NCCIH fact sheet: Licorice Root", "https://www.nccih.nih.gov/health/licorice-root"),
 "nccih_alo": ("NCCIH fact sheet: Aloe Vera", "https://www.nccih.nih.gov/health/aloe-vera"),
 "nccih_cin": ("NCCIH fact sheet: Cinnamon", "https://www.nccih.nih.gov/health/cinnamon"),
 "lt_ash": ("LiverTox (NIH): Ashwagandha", "https://www.ncbi.nlm.nih.gov/books/NBK548536/"),
 "lt_tur": ("LiverTox (NIH): Turmeric", "https://www.ncbi.nlm.nih.gov/books/NBK548561/"),
 "lt_sen": ("LiverTox (NIH): Senna", "https://www.ncbi.nlm.nih.gov/books/NBK547922/"),
 "lt_alo": ("LiverTox (NIH): Aloe Vera", "https://www.ncbi.nlm.nih.gov/books/NBK548634/"),
 "lt_fen": ("LiverTox (NIH): Fenugreek", "https://www.ncbi.nlm.nih.gov/books/NBK548826/"),
 "lt_lic": ("LiverTox (NIH): Licorice", "https://www.ncbi.nlm.nih.gov/books/NBK590484/"),
 "lt_cin": ("LiverTox (NIH): Cinnamon", "https://www.ncbi.nlm.nih.gov/books/NBK623885/"),
 "lt_tin": ("LiverTox (NIH): Tinospora", "https://www.ncbi.nlm.nih.gov/books/NBK608429/"),
 "lt_gin": ("LiverTox (NIH): Ginger", "https://www.ncbi.nlm.nih.gov/books/NBK600585/"),
 "lt_gym": ("LiverTox (NIH): Gymnema", "https://www.ncbi.nlm.nih.gov/books/NBK610217/"),
 "lt_tri": ("LiverTox (NIH): Tribulus", "https://www.ncbi.nlm.nih.gov/books/NBK583201/"),
 "lt_bac": ("LiverTox (NIH): Bacopa monnieri", "https://www.ncbi.nlm.nih.gov/books/NBK603563/"),
 "lt_bit": ("LiverTox (NIH): Bitter Melon", "https://www.ncbi.nlm.nih.gov/books/NBK590483/"),
 "lt_nig": ("LiverTox (NIH): Black Cumin Seed", "https://www.ncbi.nlm.nih.gov/books/NBK591552/"),
 "lt_hds": ("LiverTox (NIH): Herbal and Dietary Supplements (overview)", "https://www.ncbi.nlm.nih.gov/books/NBK548441/"),
 "ema_lic": ("EMA/HMPC European Union herbal monograph on Glycyrrhiza glabra / inflata / uralensis, radix (Revision 1)",
             EMA + "final-european-union-herbal-monograph-glycyrrhiza-glabra-l-glycyrrhiza-inflata-bat-glycyrrhiza-uralensis-fisch-radix-revision-1_en.pdf"),
 "ema_sen": ("EMA/HMPC European Union herbal monograph on Senna alexandrina Mill., folium (Revision 1)",
             EMA + "final-european-union-herbal-monograph-senna-alexandrina-mill-cassia-senna-l-cassia-angustifolia-vahl-folium-revision-1_en.pdf"),
 "ema_alo": ("EMA/HMPC European Union herbal monograph on Aloe barbadensis Mill. and Aloe (various species), folii succus siccatus",
             EMA + "final-european-union-herbal-monograph-aloe-barbadensis-mill-and-aloe-various-species-mainly-aloe-ferox-mill-and-its-hybrids-folii-succus-siccatus_en.pdf"),
 "ema_psy": ("EMA/HMPC Community herbal monograph on Plantago ovata Forssk., seminis tegumentum (ispaghula husk)",
             EMA + "final-community-herbal-monograph-plantago-ovata-forssk-seminis-tegumentum_en.pdf"),
 "ema_tur": ("EMA/HMPC European Union herbal monograph on Curcuma longa L., rhizoma (Revision 1)",
             EMA + "final-european-union-herbal-monograph-curcuma-longa-l-rhizoma-revision-1_en.pdf"),
 "ema_gar": ("EMA/HMPC European Union herbal monograph on Allium sativum L., bulbus",
             EMA + "final-european-union-herbal-monograph-allium-sativum-l-bulbus_en.pdf"),
 "ema_gin": ("EMA/HMPC European Union herbal monograph on Zingiber officinale Roscoe, rhizoma (Revision 1)",
             EMA + "final-european-union-herbal-monograph-zingiber-officinale-roscoe-rhizoma-revision-1_en.pdf"),
 "ema_fen": ("EMA/HMPC European Union herbal monograph on Trigonella foenum-graecum L., semen (Revision 1)",
             EMA + "european-union-herbal-monograph-trigonella-foenum-graecum-l-semen-revision-1_en.pdf"),
 "ema_cin": ("EMA/HMPC Community herbal monograph on Cinnamomum verum J.S. Presl, cortex",
             EMA + "community-herbal-monograph-cinnamomum-verum-js-presl-cortex_en.pdf"),
 "fda_aloe": ("FDA final rule: Status of Certain Additional Over-the-Counter Drug Category II and III Active Ingredients (aloe and cascara sagrada laxatives), Federal Register, 9 May 2002",
              "https://www.federalregister.gov/documents/2002/05/09/02-11510/status-of-certain-additional-over-the-counter-drug-category-ii-and-iii-active-ingredients"),
 "pib_giloy": ("Ministry of Ayush (PIB press release, 2021): Relating Giloy to Liver Damage is completely Misleading",
               "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1733260"),
}

def G(k):
    t, u = GOV[k]
    return {"title": t, "url": u, "type": "gov"}

def P(pmid):
    return {"pmid": str(pmid)}

def I(cls, sev, effect, mech, ev, src, advice=ADV):
    return {"drug_class": cls, "severity": sev, "effect": effect, "mechanism": mech,
            "evidence": ev, "advice": advice, "sources": src}

def DM(sev, effect, mech, ev, src, advice=None, classes=("antidiabetic_insulin", "antidiabetic_sulfonylurea", "antidiabetic_other")):
    adv = advice or (ADV + " If you combine them, check your blood sugar more often and know the signs of low blood sugar.")
    return [I(c, sev, effect, mech, ev, src, adv) for c in classes]

def F(flag, note, ev, src):
    return {"flag": flag, "note": note, "evidence": ev, "sources": src}

BLEED_ADV = ADV + " Watch for unusual bruising or bleeding. Tell your surgeon or dentist you take it; it is commonly advised to stop it about 2 weeks before planned surgery."
SURG_ADV = "Tell your surgeon, anaesthetist and dentist that you take it. It is commonly advised to stop the herb about 2 weeks before planned surgery; ask your doctor."
SEP_ADV = "Take other medicines at least 30-60 minutes before or after isabgol/psyllium, with plenty of water. " + ADV

R = []

# ======================= 1. ASHWAGANDHA =======================
R.append({
 "id": "ashwagandha",
 "names": {"common_en": "Ashwagandha", "hindi": "Ashwagandha (अश्वगंधा)", "sanskrit": "Ashvagandha (अश्वगन्धा)",
           "latin": "Withania somnifera (L.) Dunal", "other": ["Indian ginseng", "Winter cherry"]},
 "kind": "herb",
 "common_products": ["Ashwagandha churna (root powder)", "Ashwagandharishta", "Ashwagandha capsules/tablets (e.g. KSM-66, Sensoril extracts)", "Ashwagandha gummies", "Ashwagandhadi lehya"],
 "traditional_context": "Traditionally used in Ayurveda as a rasayana for general vitality and the wellbeing of the nervous system.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "NCCIH advises avoiding ashwagandha during pregnancy and not using it while breastfeeding.", "regulatory", [G("nccih_ash")]),
   F("liver", "Rare but sometimes severe liver injury (usually cholestatic, appearing within weeks to months) has been reported with ashwagandha supplements in several countries.", "case_reports", [G("lt_ash"), P(31991029), P(37756041)]),
   F("thyroid", "May raise thyroid hormone levels; cases of thyrotoxicosis and painless thyroiditis have been reported. NCCIH advises against use in people with thyroid disorders.", "clinical", [G("nccih_ash"), P(28829155), P(35475098)]),
   F("autoimmune", "NCCIH advises against use in people with autoimmune conditions (immune-stimulating activity).", "regulatory", [G("nccih_ash")]),
   F("surgery", "NCCIH advises against use by people about to have surgery (possible additive sedation with anaesthesia).", "regulatory", [G("nccih_ash")]),
   F("other", "Short-term use (up to about 3 months) appears reasonably safe; long-term safety is not established.", "regulatory", [G("nccih_ash")]),
 ],
 "interactions": [
   I("thyroid_hormone", "moderate", "May raise thyroid hormone levels and add to the effect of levothyroxine, so thyroid levels may move out of range.",
     "Increases serum T3/T4 in a randomised trial; case reports of thyrotoxicosis.", "clinical",
     [G("nccih_ash"), P(28829155), P(35475098)], ADV + " If you combine them, your doctor may want to re-check thyroid blood tests."),
   I("antithyroid", "moderate", "May push thyroid hormone levels up and work against antithyroid medicines.",
     "Thyroid-stimulating effect (raised T3/T4 in trial; thyrotoxicosis case reports).", "case_reports",
     [G("nccih_ash"), P(35475098), P(38559552)]),
   I("immunosuppressant", "moderate", "May work against medicines that dampen the immune system.",
     "Immune-stimulating activity; NCCIH lists immunosuppressants among possible interactions.", "theoretical",
     [G("nccih_ash")]),
   I("sedative_hypnotic", "moderate", "May add to drowsiness from sleeping pills or sedatives.",
     "GABA-mimetic / sedative activity in preclinical studies; NCCIH lists sedatives among possible interactions.", "preclinical",
     [G("nccih_ash"), P(37335157)]),
   I("antiepileptic", "moderate", "May change how well anti-seizure medicines work or add to drowsiness.",
     "NCCIH lists anticonvulsants among possible interactions; GABA-ergic activity shown in animals.", "theoretical",
     [G("nccih_ash"), P(24117067)]),
   *DM("moderate", "May lower blood sugar further when taken with diabetes medicines.",
       "Glucose-lowering effect seen in animal studies and small clinical studies; NCCIH lists diabetes medicines among possible interactions.", "clinical",
       [G("nccih_ash"), P(31975514)]),
   I("antihypertensive", "moderate", "May lower blood pressure further when taken with blood-pressure medicines.",
     "NCCIH lists blood-pressure medicines among possible interactions; mechanism not well defined.", "theoretical",
     [G("nccih_ash")], ADV + " Watch for dizziness or light-headedness."),
   I("hepatotoxic", "moderate", "May add to the risk of liver injury when taken with medicines that can harm the liver.",
     "Ashwagandha itself is a rare cause of drug-induced liver injury; additive risk is theoretical.", "theoretical",
     [G("lt_ash"), P(31991029)]),
   I("antidepressant_ssri_snri", "minor", "Side effects such as stomach upset, muscle pain or diarrhoea were reported when combined with some antidepressants.",
     "Reported in a retrospective pharmacovigilance chart review (sertraline, escitalopram, paroxetine); mechanism unclear.", "case_reports",
     [P(37829299)]),
   I("anaesthesia_surgery", "moderate", "May add to sedation from anaesthesia.",
     "NCCIH advises against use before surgery; sedative activity.", "theoretical",
     [G("nccih_ash")], SURG_ADV),
 ],
 "data_quality": "good",
 "_notes": "In vitro testing of root and leaf extracts found no meaningful CYP inhibition (PMID 40023576), so no CYP-based interactions are listed.",
})

# ======================= 2. TURMERIC =======================
R.append({
 "id": "turmeric",
 "names": {"common_en": "Turmeric (incl. curcumin supplements)", "hindi": "Haldi (हल्दी)", "sanskrit": "Haridra (हरिद्रा)",
           "latin": "Curcuma longa L.", "other": ["Curcumin", "Indian saffron"]},
 "kind": "food_spice",
 "common_products": ["Haldi powder (culinary)", "Curcumin capsules (often with piperine/black pepper)", "Bioavailable curcumin formulations (e.g. Meriva, BCM-95, Theracurmin)", "Haridrakhand", "Turmeric latte / golden milk mixes"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of the skin, digestion and joints.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("liver", "Liver injury (often hepatocellular, sometimes autoimmune-like) has been reported with turmeric/curcumin supplements, especially highly bioavailable or piperine-enhanced products; amounts used in food are not a concern.", "case_reports",
     [G("nccih_tur"), G("lt_tur"), P(36252717), P(32656820)]),
   F("pregnancy", "Supplement doses may be unsafe in pregnancy; EMA does not recommend medicinal use in pregnancy or breastfeeding.", "regulatory", [G("nccih_tur"), G("ema_tur")]),
   F("other", "EMA advises against medicinal use with bile-duct obstruction, gallstones or liver disease (stimulates bile flow / gallbladder contraction).", "regulatory", [G("ema_tur"), P(10102956)]),
   F("bleeding", "Curcumin has antiplatelet and anticoagulant effects in laboratory studies.", "preclinical", [P(29052850)]),
   F("heavy_metals", "Loose turmeric powder has been found adulterated with lead chromate in South Asia and linked to lead exposure, including in the US.", "case_reports", [P(31550596), P(28358991)]),
   F("other", "High-dose turmeric has been linked to iron-deficiency anaemia in a case report (curcumin binds iron).", "case_reports", [P(30899609)]),
 ],
 "interactions": [
   I("anticoagulant_vka", "moderate", "May increase the effect of warfarin-type blood thinners and raise the risk of bleeding (raised INR reported).",
     "Antiplatelet/anticoagulant activity of curcumin; a probable case of raised INR with a vitamin K antagonist (fluindione).", "case_reports",
     [P(25230280), P(29052850)], BLEED_ADV + " Your INR may need to be checked more often."),
   I("anticoagulant_doac", "moderate", "May add to the bleeding risk of newer blood thinners.",
     "Curcumin antiplatelet/anticoagulant activity in lab studies; additive effect is theoretical.", "theoretical",
     [P(29052850)], BLEED_ADV),
   I("antiplatelet", "moderate", "May add to the effect of antiplatelet medicines and increase bleeding risk.",
     "Curcumin inhibits platelet aggregation in lab studies; in rats it changed clopidogrel levels without changing platelet effect.", "preclinical",
     [P(29052850), P(23807811)], BLEED_ADV),
   I("nsaid", "minor", "May add to bleeding risk, including stomach bleeding, with NSAID painkillers.",
     "Additive antiplatelet effect; theoretical.", "theoretical", [P(29052850)]),
   I("immunosuppressant", "moderate", "May raise tacrolimus blood levels (kidney harm reported in one case), although another monitored patient showed no change.",
     "Probable CYP3A4/P-gp inhibition by curcumin; raised tacrolimus levels in rats and one case report; a second case found no effect at culinary doses.", "case_reports",
     [P(28104136), P(22123127), P(37586787)], ADV + " If you take tacrolimus or cyclosporine, levels may need extra monitoring."),
   I("anticancer", "moderate", "Curcumin lowered blood levels of tamoxifen and its active form endoxifen, which might reduce its effect.",
     "Clinical PK study in breast-cancer patients: endoxifen AUC fell 7.7% with curcumin and 12.4% with curcumin + piperine.", "clinical",
     [P(30909366)], ADV + " Tell your cancer team about any curcumin supplement."),
   I("antidiabetic_sulfonylurea", "moderate", "May add to the glucose-lowering effect of glibenclamide (glyburide).",
     "Small clinical study: curcumin altered glyburide levels and lowered glucose further (no hypoglycaemia observed).", "clinical",
     [P(25044423)], ADV + " If you combine them, check your blood sugar more often."),
   I("antihypertensive", "minor", "Curcumin reduced absorption of the beta-blocker talinolol in volunteers, which could reduce its effect.",
     "Clinical PK study: talinolol AUC fell about one third after 6 days of curcumin (transporter-mediated).", "clinical",
     [P(17468862)]),
   I("pgp_substrate", "minor", "May change blood levels of medicines that are moved by P-gp/BCRP transporters.",
     "Curcumin altered talinolol (P-gp) and sulfasalazine (BCRP) exposure in human studies.", "clinical",
     [P(17468862), P(22300367)]),
   I("hepatotoxic", "moderate", "May add to the risk of liver injury with other medicines that can affect the liver.",
     "Turmeric/curcumin is itself linked to rare liver injury; additive risk theoretical.", "theoretical",
     [G("lt_tur"), P(36252717)]),
   I("iron_mineral_supplement", "minor", "High doses may reduce iron absorption.",
     "Curcumin is an iron chelator; iron-deficiency anaemia reported with high-dose turmeric.", "case_reports",
     [P(30899609), P(16545682)], "Ask your doctor or pharmacist; consider taking iron at a different time of day from turmeric supplements."),
   I("anaesthesia_surgery", "minor", "May add to bleeding risk around surgery.",
     "Antiplatelet activity; theoretical.", "theoretical", [P(29052850)], SURG_ADV),
 ],
 "data_quality": "good",
 "_notes": "EMA monograph lists no interactions, unlike case reports. A curcumin+piperine product did not change midazolam/flurbiprofen/paracetamol levels (PMID 22725836).",
})

# ======================= 3. GUGGUL =======================
R.append({
 "id": "guggul",
 "names": {"common_en": "Guggul", "hindi": "Guggul (गुग्गुल)", "sanskrit": "Guggulu (गुग्गुलु)",
           "latin": "Commiphora wightii (Arn.) Bhandari (syn. Commiphora mukul)", "other": ["Indian bdellium", "Gugulipid / guggulsterone"]},
 "kind": "herb",
 "common_products": ["Shuddha guggulu", "Yogaraj guggulu", "Kaishore guggulu", "Triphala guggulu", "Gugulipid / guggul extract capsules"],
 "traditional_context": "Traditionally used in Ayurveda, usually as purified resin in guggulu formulations, for the general wellbeing of joints and metabolism.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("allergy", "Skin rash (hypersensitivity) was noticeably more common with guggulipid than placebo in a randomised trial.", "clinical", [P(12915429)]),
   F("thyroid", "Guggulsterone stimulated thyroid function in rats; relevance in people is uncertain.", "preclinical", [P(6739577)]),
   F("pregnancy", "Guggulsterone binds steroid hormone receptors (oestrogen, progesterone and others); use in pregnancy is not supported by safety data.", "preclinical", [P(15602004)]),
   F("liver", "Acute liver failure has been reported with a multi-ingredient 'fat burner' that contained guggul (cause not attributable to guggul alone).", "case_reports", [P(21499580)]),
 ],
 "interactions": [
   I("antihypertensive", "moderate", "May reduce absorption and effect of propranolol and diltiazem.",
     "Single 1 g dose of gugulipid significantly reduced Cmax and AUC of propranolol and diltiazem in healthy volunteers.", "clinical",
     [P(7852226)], ADV + " If you combine them, have your blood pressure and heart rate checked."),
   I("antiarrhythmic", "moderate", "May reduce blood levels of diltiazem and beta-blockers used for heart rhythm.",
     "Reduced bioavailability of diltiazem and propranolol in healthy volunteers.", "clinical", [P(7852226)]),
   I("cyp3a4_substrate_narrow", "moderate", "May lower blood levels of medicines broken down by CYP3A4, making them less effective.",
     "Guggulsterone activates the pregnane X receptor and induces CYP3A in lab studies; not confirmed in people.", "preclinical",
     [P(15075359)]),
   I("thyroid_hormone", "minor", "May change thyroid function tests or levothyroxine needs.",
     "Thyroid-stimulating action of Z-guggulsterone in rats.", "preclinical", [P(6739577)]),
   I("antithyroid", "minor", "May work against antithyroid medicines.",
     "Thyroid-stimulating action of guggulsterone in rats; theoretical.", "preclinical", [P(6739577)]),
   I("hormonal_contraceptive_estrogen", "minor", "May interfere with hormone-based medicines.",
     "Guggulsterone binds oestrogen, progesterone and other steroid receptors in vitro; clinical relevance unknown.", "preclinical",
     [P(15602004)]),
 ],
 "data_quality": "limited",
})

# ======================= 4. GILOY =======================
R.append({
 "id": "giloy",
 "names": {"common_en": "Giloy / Heart-leaved moonseed", "hindi": "Giloy (गिलोय)", "sanskrit": "Guduchi (गुडूची), Amrita",
           "latin": "Tinospora cordifolia (Willd.) Miers", "other": ["Guduchi", "Gulvel"]},
 "kind": "herb",
 "common_products": ["Giloy juice", "Giloy ghanvati / tablets", "Guduchi satva", "Giloy-tulsi immunity drops", "Samshamani vati"],
 "traditional_context": "Traditionally used in Ayurveda as a rasayana for general vitality and the wellbeing of the body's natural defences.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("liver", "Multicentre case series from India (especially during COVID-19 'immunity booster' use) linked giloy to liver injury, often autoimmune-like. The Ministry of Ayush disputes the link, citing possible plant misidentification.", "case_reports",
     [G("lt_tin"), P(35037744), P(34230786), G("pib_giloy")]),
   F("autoimmune", "May unmask or trigger autoimmune-like hepatitis; caution in people with autoimmune conditions.", "case_reports", [P(35068778), P(35037744)]),
   F("hypoglycaemia", "Glucose-lowering activity in animal studies.", "preclinical", [P(21665451)]),
 ],
 "interactions": [
   I("hepatotoxic", "moderate", "May add to the risk of liver injury with medicines that can affect the liver.",
     "Giloy linked to autoimmune-like liver injury in case series; additive risk theoretical.", "case_reports",
     [P(35037744), G("lt_tin")], ADV + " Report tiredness, dark urine or yellow eyes promptly."),
   I("immunosuppressant", "moderate", "May work against medicines that dampen the immune system.",
     "Immune-stimulating activity; associated with autoimmune-like hepatitis. Interaction itself is theoretical.", "theoretical",
     [P(35068778), P(24105360)]),
   I("antidiabetic_sulfonylurea", "moderate", "May raise glibenclamide levels and lower blood sugar further.",
     "In rats, 14-day giloy extract increased glibenclamide bioavailability and reduced clearance; CYP2C9 inhibition in vitro.", "preclinical",
     [P(29413979)], ADV + " If you combine them, check your blood sugar more often."),
   *DM("minor", "May lower blood sugar further with diabetes medicines.", "Hypoglycaemic activity of giloy alkaloids in animals.", "preclinical",
       [P(21665451)], classes=("antidiabetic_insulin", "antidiabetic_other")),
   I("cyp3a4_substrate_narrow", "minor", "May slightly raise levels of medicines broken down by CYP3A4.",
     "Mild CYP3A4 inhibition by stem extract in vitro (stronger for its protoberberine alkaloid fraction); not shown in people.", "preclinical",
     [P(24105360), P(27721546)]),
   I("cyp2c9_substrate", "minor", "May slightly raise levels of medicines broken down by CYP2C9.",
     "CYP2C9 inhibition in human liver microsomes at high concentrations; not shown in people.", "preclinical",
     [P(27721546), P(29413979)]),
   I("cyp2c19_substrate", "minor", "May slightly raise levels of medicines broken down by CYP2C19.",
     "CYP2C19 inhibited by giloy extract in rat and human liver microsomes (weaker than CYP2C9/CYP2D6); not shown in people.", "preclinical",
     [P(29413979)]),
 ],
 "data_quality": "limited",
})

# ======================= 5. TULSI =======================
R.append({
 "id": "tulsi",
 "names": {"common_en": "Holy basil", "hindi": "Tulsi (तुलसी)", "sanskrit": "Tulasi (तुलसी)",
           "latin": "Ocimum tenuiflorum L. (syn. Ocimum sanctum L.)", "other": ["Holy basil", "Krishna tulsi", "Rama tulsi"]},
 "kind": "herb",
 "common_products": ["Tulsi tea", "Tulsi drops", "Tulsi capsules", "Tulsi leaves (fresh)"],
 "traditional_context": "Traditionally used in Ayurveda and Indian households for the general wellbeing of the respiratory system and stress resilience.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "Antifertility effects have been reported in animal studies; safety in pregnancy is not established.", "preclinical", [P(4344433), P(28400848)]),
   F("hypoglycaemia", "Lowered fasting and post-meal blood glucose in a small randomised trial.", "clinical", [P(8880292)]),
   F("bleeding", "Tulsi fixed oil prolonged clotting time in animals.", "preclinical", [P(11694358)]),
 ],
 "interactions": [
   *DM("minor", "May lower blood sugar further with diabetes medicines.", "Glucose-lowering effect in a small randomised placebo-controlled trial.", "clinical", [P(8880292), P(28400848)]),
   I("anticoagulant_vka", "minor", "May add to the effect of blood thinners.", "Prolonged blood clotting time in animals; clinical relevance unknown.", "preclinical",
     [P(11694358)], BLEED_ADV),
   I("antiplatelet", "minor", "May add to the effect of antiplatelet medicines.", "Prolonged clotting time in animals; theoretical.", "preclinical",
     [P(11694358)], BLEED_ADV),
   I("sedative_hypnotic", "minor", "May add to drowsiness from sedatives.", "Tulsi fixed oil prolonged pentobarbitone sleeping time in animals.", "preclinical",
     [P(11694358)]),
   I("antihypertensive", "minor", "May lower blood pressure further.", "Tulsi fixed oil lowered blood pressure in animals.", "preclinical", [P(11694358)]),
 ],
 "data_quality": "limited",
})

# ======================= 6. BRAHMI =======================
R.append({
 "id": "brahmi",
 "names": {"common_en": "Brahmi / Water hyssop", "hindi": "Brahmi (ब्राह्मी)", "sanskrit": "Brahmi (ब्राह्मी)",
           "latin": "Bacopa monnieri (L.) Wettst.", "other": ["Bacopa", "Jalnim"]},
 "kind": "herb",
 "common_products": ["Brahmi churna", "Brahmi vati", "Brahmi ghrita", "Bacopa extract capsules (e.g. Bacognize, CDRI-08)", "Brahmi oil (topical)"],
 "traditional_context": "Traditionally used in Ayurveda as a medhya rasayana for the general wellbeing of memory and the nervous system.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("other", "Stomach upset (nausea, cramps, loose stools) is the most common side effect in trials.", "clinical", [P(20590480)]),
   F("thyroid", "Raised T4 levels in mice, suggesting a thyroid-stimulating effect.", "preclinical", [P(12065164)]),
   F("liver", "Not linked to clinically apparent liver injury in LiverTox.", "regulatory", [G("lt_bac")]),
 ],
 "interactions": [
   I("cyp3a4_substrate_narrow", "moderate", "May raise blood levels of medicines broken down by CYP3A4.",
     "Bacopa extract inhibited CYP3A4 (and CYP2C9, CYP2C19, CYP1A2) in vitro; estimated gut concentrations could be relevant. Not tested in people.", "preclinical",
     [P(24566323)]),
   I("cyp2c9_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2C9 (e.g. some blood thinners and diabetes tablets).",
     "Non-competitive CYP2C9 inhibition in vitro; not tested in people.", "preclinical", [P(24566323)]),
   I("cyp2c19_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2C19 (e.g. omeprazole, citalopram) and could reduce activation of clopidogrel.",
     "CYP2C19 was the most strongly inhibited enzyme in vitro (IC50 ~24 µg/mL, non-competitive); not tested in people.", "preclinical", [P(24566323)]),
   I("cyp1a2_substrate", "minor", "May raise blood levels of medicines broken down by CYP1A2.", "CYP1A2 inhibition in vitro.", "preclinical", [P(24566323)]),
   I("thyroid_hormone", "minor", "May change thyroid hormone levels.", "Raised T4 in mice.", "preclinical", [P(12065164)]),
   I("antidepressant_maoi", "minor", "A serious cardiac event was reported in a patient combining Bacopa with moclobemide.",
     "Single report in a pharmacovigilance chart review; causality and mechanism uncertain.", "case_reports", [P(37829299)]),
 ],
 "data_quality": "limited",
 "_notes": "Name confusion: Centella asiatica (mandukaparni/gotu kola) is also sold as 'brahmi' in some regions.",
})

# ======================= 7. SHATAVARI =======================
R.append({
 "id": "shatavari",
 "names": {"common_en": "Shatavari / Wild asparagus", "hindi": "Shatavari (शतावरी)", "sanskrit": "Shatavari (शतावरी)",
           "latin": "Asparagus racemosus Willd.", "other": ["Satavar"]},
 "kind": "herb",
 "common_products": ["Shatavari churna", "Shatavari granules / kalpa", "Shatavari capsules", "Shatavari ghrita"],
 "traditional_context": "Traditionally used in Ayurveda as a rasayana for the general wellbeing of the female reproductive system.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "Used traditionally around childbirth and as a galactagogue, but there is little safety data for pregnancy or breastfeeding.", "theoretical", [P(23012383)]),
   F("hypoglycaemia", "Stimulated insulin secretion and lowered glucose in animal and cell studies.", "preclinical", [P(17210753), P(21899804)]),
 ],
 "interactions": [
   *DM("minor", "May lower blood sugar further with diabetes medicines.", "Insulin-secretory and glucose-lowering effects in animal and cell studies.", "preclinical",
       [P(17210753), P(21899804)]),
   I("diuretic_loop_thiazide", "minor", "May add to the fluid-losing effect of diuretics.", "Diuretic activity of root extract in rats; theoretical in people.", "preclinical",
     [P(20931905)]),
 ],
 "data_quality": "poor",
 "_notes": "Aqueous extract did not inhibit CYP3A4 in vitro (PMIDs 24105360, 26006029).",
})

# ======================= 8. ARJUNA =======================
R.append({
 "id": "arjuna",
 "names": {"common_en": "Arjuna", "hindi": "Arjun (अर्जुन)", "sanskrit": "Arjuna (अर्जुन)",
           "latin": "Terminalia arjuna (Roxb. ex DC.) Wight & Arn.", "other": ["Arjun bark"]},
 "kind": "herb",
 "common_products": ["Arjuna bark powder (churna)", "Arjunarishta", "Arjuna ksheerapaka (milk decoction)", "Arjuna capsules/tablets"],
 "traditional_context": "Traditionally used in Ayurveda, as bark decoctions, for the general wellbeing of the heart and circulation.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("bleeding", "Bark extract inhibited platelet activation in vitro.", "preclinical", [P(19437336)]),
   F("other", "Clinical safety data are short-term and limited.", "clinical", [P(24600529), P(25014508)]),
 ],
 "interactions": [
   I("cyp3a4_substrate_narrow", "moderate", "May raise blood levels of medicines broken down by CYP3A4.",
     "Bark extracts strongly inhibited CYP3A4 in human liver microsomes (IC50 < 50 µg/mL); not tested in people.", "preclinical", [P(28962416)]),
   I("cyp2c9_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2C9, such as warfarin.",
     "CYP2C9 inhibition in human liver microsomes; not tested in people.", "preclinical", [P(28962416)]),
   I("cyp2d6_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2D6, such as many beta-blockers and antidepressants.",
     "CYP2D6 inhibition in human liver microsomes; not tested in people.", "preclinical", [P(28962416)]),
   I("antiplatelet", "moderate", "May add to the effect of antiplatelet medicines.", "Inhibited platelet aggregation and activation in vitro.", "preclinical",
     [P(19437336)], BLEED_ADV),
   I("anticoagulant_vka", "moderate", "May add to the effect of warfarin and raise bleeding risk.",
     "Theoretical: antiplatelet activity plus CYP2C9 inhibition in vitro.", "theoretical", [P(19437336), P(28962416)], BLEED_ADV),
   I("antihypertensive", "minor", "May add to the effect of heart and blood-pressure medicines.",
     "Used alongside anti-anginal drugs in small trials; additive effects are theoretical.", "theoretical", [P(12086380), P(24600529)]),
 ],
 "data_quality": "limited",
})

# ======================= 9. NEEM =======================
R.append({
 "id": "neem",
 "names": {"common_en": "Neem", "hindi": "Neem (नीम)", "sanskrit": "Nimba (निम्ब)",
           "latin": "Azadirachta indica A.Juss.", "other": ["Margosa", "Indian lilac"]},
 "kind": "herb",
 "common_products": ["Neem leaf capsules/tablets", "Neem leaf juice", "Nimbadi churna", "Neem oil (topical; poisonous if swallowed)", "Neem toothpaste/datun"],
 "traditional_context": "Traditionally used in Ayurveda, mostly as leaf preparations, for the general wellbeing of the skin.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("children", "Swallowing neem (margosa) oil has caused serious poisoning in infants and young children, including a Reye-like illness with brain swelling, liver damage and deaths. Neem oil must never be given by mouth to children.", "case_reports",
     [P(6110100), P(7330956), P(18250509)]),
   F("pregnancy", "Antifertility and contraceptive effects in animals; avoid in pregnancy or when trying to conceive.", "preclinical", [P(34092456)]),
   F("hypoglycaemia", "Leaf extract lowered blood glucose in animal studies.", "preclinical", [P(10919098)]),
 ],
 "interactions": [
   *DM("moderate", "May lower blood sugar further with diabetes medicines.", "Hypoglycaemic effect of leaf extract in normal and diabetic animals; human data limited.", "preclinical",
       [P(10919098), P(26716795)]),
   I("immunosuppressant", "minor", "May work against medicines that dampen the immune system.", "Immune-stimulating activity of neem preparations in animals; theoretical.", "preclinical",
     [P(1452404), P(3302545)]),
 ],
 "data_quality": "limited",
})

# ======================= 10. AMLA =======================
R.append({
 "id": "amla",
 "names": {"common_en": "Indian gooseberry", "hindi": "Amla (आंवला)", "sanskrit": "Amalaki (आमलकी)",
           "latin": "Phyllanthus emblica L. (syn. Emblica officinalis Gaertn.)", "other": ["Amalaki", "Emblic"]},
 "kind": "food_spice",
 "common_products": ["Amla juice", "Amla churna", "Amla murabba / candy", "Chyawanprash (main ingredient)", "Triphala (one of three fruits)", "Amla extract capsules (e.g. Capros)"],
 "traditional_context": "Traditionally used in Ayurveda as a rasayana for general vitality and the wellbeing of digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("bleeding", "A standardised amla extract reduced platelet aggregation and prolonged bleeding time in clinical studies.", "clinical", [P(24291054), P(25756303)]),
   F("hypoglycaemia", "Amla powder lowered blood glucose in a small human study.", "clinical", [P(21495900)]),
 ],
 "interactions": [
   I("antiplatelet", "moderate", "May add to the effect of aspirin or clopidogrel and increase bleeding risk.",
     "In a crossover study in diabetic patients, amla extract inhibited platelet aggregation and prolonged bleeding time alone and combined with clopidogrel or aspirin.", "clinical",
     [P(24291054)], BLEED_ADV),
   I("anticoagulant_vka", "moderate", "May add to the bleeding risk of warfarin-type blood thinners.",
     "Antiplatelet activity shown clinically; combination with anticoagulants not studied.", "theoretical", [P(24291054), P(25756303)], BLEED_ADV),
   I("anticoagulant_doac", "minor", "May add to the bleeding risk of newer blood thinners.", "Antiplatelet activity; theoretical additive effect.", "theoretical",
     [P(24291054)], BLEED_ADV),
   *DM("minor", "May lower blood sugar slightly with diabetes medicines.", "Glucose-lowering effect in a small human study.", "clinical", [P(21495900)]),
   I("antihypertensive", "minor", "May lower blood pressure slightly when added to blood-pressure medicines.", "Add-on randomised trial showed modest blood-pressure lowering.", "clinical",
     [P(33570228)]),
 ],
 "data_quality": "limited",
})

# ======================= 11. GINGER =======================
R.append({
 "id": "ginger",
 "names": {"common_en": "Ginger", "hindi": "Adrak (अदरक); dried: Saunth (सोंठ)", "sanskrit": "Shunthi (शुण्ठी); fresh: Ardraka (आर्द्रक)",
           "latin": "Zingiber officinale Roscoe", "other": ["Sonth", "Dry ginger"]},
 "kind": "food_spice",
 "common_products": ["Fresh ginger / adrak", "Saunth powder", "Ginger capsules", "Ginger tea", "Trikatu (with black pepper and pippali)", "Adrak ras / ginger juice"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "Supplements may be safe in pregnancy (NCCIH), but EMA prefers avoiding medicinal use in pregnancy as a precaution and does not recommend use while breastfeeding.", "regulatory", [G("nccih_gin"), G("ema_gin")]),
   F("bleeding", "Effects on platelets are inconsistent across studies; an over-anticoagulation case with phenprocoumon has been reported.", "case_reports", [P(14742762), P(16883626)]),
   F("liver", "Not linked to clinically apparent liver injury on its own (LiverTox).", "regulatory", [G("lt_gin")]),
 ],
 "interactions": [
   I("anticoagulant_vka", "moderate", "May raise INR and bleeding risk with coumarin blood thinners in some people.",
     "Case report of INR up to 10 with phenprocoumon; a controlled study in healthy volunteers found no effect on warfarin INR or kinetics.", "case_reports",
     [P(14742762), P(15801937)], BLEED_ADV + " Your INR may need to be checked if you start or stop ginger supplements."),
   I("anticoagulant_doac", "minor", "May add to bleeding risk with newer blood thinners.", "Possible antiplatelet effect; theoretical.", "theoretical",
     [P(16883626)], BLEED_ADV),
   I("antiplatelet", "moderate", "May add to the effect of antiplatelet medicines.",
     "Ginger inhibited platelet aggregation and had a synergistic antiplatelet effect with nifedipine in humans; other studies inconsistent.", "clinical",
     [P(16883626)], BLEED_ADV),
   I("nsaid", "minor", "May add to bleeding risk with NSAID painkillers.", "Additive antiplatelet effect; theoretical.", "theoretical", [P(16883626)]),
   I("antihypertensive", "minor", "With nifedipine, ginger increased the anti-clotting effect on platelets.",
     "Synergistic antiplatelet effect of ginger plus nifedipine in hypertensive patients and volunteers.", "clinical", [P(16883626)]),
   I("anticancer", "moderate", "Ginger was linked to raised crizotinib levels and liver injury in a cancer patient.",
     "Probable CYP3A4 inhibition; single case report.", "case_reports", [P(30701569)], ADV + " Tell your cancer team about ginger supplements."),
   I("immunosuppressant", "minor", "May raise tacrolimus levels (shown in rats); a monitored patient showed no change at culinary doses.",
     "Ginger juice increased tacrolimus AUC in rats; human case negative.", "preclinical", [P(22123127), P(37586787)]),
   I("anaesthesia_surgery", "minor", "May add to bleeding risk around surgery.", "Possible antiplatelet effect; theoretical.", "theoretical", [P(16883626)], SURG_ADV),
 ],
 "data_quality": "good",
 "_notes": "EMA monograph states 'none known' for interactions, unlike the case reports.",
})

# ======================= 12. GARLIC =======================
R.append({
 "id": "garlic",
 "names": {"common_en": "Garlic", "hindi": "Lahsun (लहसुन)", "sanskrit": "Lashuna (लशुन)",
           "latin": "Allium sativum L.", "other": ["Rasona"]},
 "kind": "food_spice",
 "common_products": ["Garlic (culinary)", "Garlic pearls / garlic oil capsules", "Aged garlic extract", "Lashunadi vati"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of digestion and circulation.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("bleeding", "Garlic supplements may increase bleeding risk; spontaneous bleeding and post-operative bleeding have been reported.", "case_reports",
     [G("nccih_gar"), G("ema_gar"), P(2352608), P(7809259)]),
   F("surgery", "EMA advises avoiding garlic preparations 7 days before surgery because of post-operative bleeding risk.", "regulatory", [G("ema_gar")]),
   F("pregnancy", "Supplement amounts may not be safe in pregnancy or breastfeeding; food amounts are fine.", "regulatory", [G("nccih_gar"), G("ema_gar")]),
 ],
 "interactions": [
   I("antiretroviral", "major", "Can sharply lower blood levels of some HIV medicines (saquinavir), risking treatment failure and resistance.",
     "Garlic supplements cut saquinavir AUC by about half in volunteers (likely CYP3A4/P-gp induction); EMA contraindicates use with saquinavir/ritonavir.", "clinical",
     [G("ema_gar"), P(11740713)], "Avoid garlic supplements with HIV protease inhibitors unless your HIV doctor agrees. " + ADV),
   I("anticoagulant_vka", "moderate", "May add to the effect of warfarin and raise bleeding risk.",
     "Antiplatelet effect; EMA and NCCIH advise caution. A trial of aged garlic extract with warfarin found no increased bleeding.", "clinical",
     [G("ema_gar"), G("nccih_gar"), P(16484565)], BLEED_ADV),
   I("anticoagulant_doac", "moderate", "May add to bleeding risk with newer blood thinners.", "EMA advises caution with oral anticoagulants (antiplatelet effect).", "theoretical",
     [G("ema_gar")], BLEED_ADV),
   I("anticoagulant_heparin", "moderate", "May add to bleeding risk with heparin injections.", "Antiplatelet effect; theoretical additive bleeding.", "theoretical",
     [G("nccih_gar"), P(22300597)], BLEED_ADV),
   I("antiplatelet", "moderate", "May add to the effect of aspirin or clopidogrel and increase bleeding risk.",
     "Garlic inhibits platelet function; EMA advises caution with antiplatelet therapy.", "case_reports",
     [G("ema_gar"), G("nccih_gar"), P(2352608)], BLEED_ADV),
   I("nsaid", "minor", "May add to bleeding risk with NSAID painkillers.", "Additive antiplatelet effect; theoretical.", "theoretical", [G("nccih_gar")]),
   I("anaesthesia_surgery", "moderate", "May increase bleeding during and after surgery.", "Antiplatelet effect; EMA advises stopping 7 days before surgery.", "case_reports",
     [G("ema_gar"), P(7809259)], "Tell your surgeon and dentist. EMA advises stopping garlic supplements at least 7 days before surgery."),
   I("antitubercular", "moderate", "May lower blood levels of isoniazid.", "Garlic extract reduced isoniazid bioavailability in rabbits; not studied in people.", "preclinical",
     [P(16699292)]),
   I("anticancer", "minor", "May change docetaxel clearance in some people.",
     "Clinical PK study found no significant change overall, but possible reduced clearance in CYP3A5*1A carriers.", "clinical", [P(16899612)]),
   *DM("minor", "May lower blood sugar slightly with diabetes medicines.", "Garlic supplements may modestly reduce blood glucose (NCCIH).", "clinical", [G("nccih_gar")]),
   I("antihypertensive", "minor", "May lower blood pressure slightly with blood-pressure medicines.", "Small blood-pressure-lowering effect (NCCIH).", "clinical", [G("nccih_gar")]),
 ],
 "data_quality": "good",
})

# ======================= 13. FENUGREEK =======================
R.append({
 "id": "fenugreek",
 "names": {"common_en": "Fenugreek", "hindi": "Methi (मेथी)", "sanskrit": "Methika (मेथिका)",
           "latin": "Trigonella foenum-graecum L.", "other": ["Methi dana"]},
 "kind": "food_spice",
 "common_products": ["Methi seeds / powder", "Fenugreek capsules", "Methi water", "Lactation teas and supplements"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of digestion and metabolism.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "Not safe in pregnancy in amounts above food use; linked to birth defects in animals and people. EMA does not recommend it in pregnancy, breastfeeding, or women who may become pregnant without contraception.", "regulatory",
     [G("nccih_fen"), G("ema_fen")]),
   F("hypoglycaemia", "Large doses may cause a harmful drop in blood sugar; EMA advises closer glucose monitoring in people on diabetes treatment.", "regulatory", [G("nccih_fen"), G("ema_fen")]),
   F("allergy", "EMA contraindicates use with allergy to peanut, soya or other legumes (cross-reactivity).", "regulatory", [G("ema_fen"), P(28283164)]),
   F("thyroid", "Reduced T3 production in mice and rats.", "preclinical", [P(10527654)]),
 ],
 "interactions": [
   *DM("moderate", "May lower blood sugar further and cause low blood sugar with diabetes medicines.",
       "Glucose-lowering effect in meta-analyses of clinical trials; EMA advises close glycaemic monitoring.", "clinical",
       [G("ema_fen"), G("nccih_fen"), P(24438170)]),
   I("anticoagulant_vka", "moderate", "May increase the effect of warfarin (raised INR reported).",
     "Case report of raised INR with a boldo-fenugreek combination; mechanism unclear (coumarin-like constituents proposed).", "case_reports",
     [P(11310527)], BLEED_ADV + " Your INR may need checking."),
   I("hepatotoxic", "minor", "May add to liver stress from medicines that can harm the liver.",
     "Case of worsened ribociclib liver toxicity with a fenugreek supplement; causality uncertain.", "case_reports", [P(40388649), G("lt_fen")]),
   I("thyroid_hormone", "minor", "May change thyroid hormone levels.", "Inhibited T3 production in rodents.", "preclinical", [P(10527654)]),
   I("nitrate_pde5", "minor", "May lower sildenafil levels.", "Fenugreek reduced sildenafil Cmax and AUC in dogs; not studied in people.", "preclinical", [P(24719213)]),
 ],
 "data_quality": "good",
})

# ======================= 14. KARELA =======================
R.append({
 "id": "karela",
 "names": {"common_en": "Bitter melon / Bitter gourd", "hindi": "Karela (करेला)", "sanskrit": "Karavellaka (कारवेल्लक)",
           "latin": "Momordica charantia L.", "other": ["Bitter gourd", "Balsam pear"]},
 "kind": "food_spice",
 "common_products": ["Karela juice", "Karela-jamun juice", "Karela powder / capsules", "Karela (cooked vegetable)"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of metabolism.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Can lower blood sugar; hypoglycaemic coma and convulsions have been reported in children given bitter melon tea.", "case_reports", [P(12625217), G("lt_bit")]),
   F("pregnancy", "Seeds and fruit contain abortifacient proteins in animal studies; avoid in pregnancy.", "preclinical", [P(12625217), P(15182917)]),
   F("other", "Seeds contain vicine; people with G6PD deficiency may be at risk of haemolytic anaemia (favism-like).", "case_reports", [P(12625217)]),
 ],
 "interactions": [
   I("antidiabetic_sulfonylurea", "moderate", "May lower blood sugar further with sulfonylureas.",
     "Case of improved/excess glucose control when karela curry was eaten with chlorpropamide; additive hypoglycaemic effect.", "case_reports",
     [P(85186), P(12625217)], ADV + " If you combine them, check your blood sugar more often and know the signs of low blood sugar."),
   *DM("moderate", "May lower blood sugar further with diabetes medicines.", "Glucose-lowering effect seen in trials (modest; evidence quality low).", "clinical",
       [P(21211558), P(22895968)], classes=("antidiabetic_insulin", "antidiabetic_other")),
 ],
 "data_quality": "limited",
})

# ======================= 15. JAMUN =======================
R.append({
 "id": "jamun",
 "names": {"common_en": "Jamun / Java plum", "hindi": "Jamun (जामुन)", "sanskrit": "Jambu (जम्बू)",
           "latin": "Syzygium cumini (L.) Skeels", "other": ["Jambolan", "Black plum"]},
 "kind": "food_spice",
 "common_products": ["Jamun seed powder (guthli churna)", "Jamun juice / vinegar", "Karela-jamun juice", "Jamun fruit"],
 "traditional_context": "Traditionally used in Ayurveda, especially seed powder, for the general wellbeing of metabolism and digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Seed and fruit extracts lower blood glucose in animal studies; human data are limited.", "preclinical", [P(9687076), P(23642956)]),
 ],
 "interactions": [
   *DM("moderate", "May lower blood sugar further with diabetes medicines.", "Hypoglycaemic activity of seed extract in animals; clinical data limited and older.", "preclinical",
       [P(9687076), P(23642956), P(18380393)]),
 ],
 "data_quality": "poor",
})

# ======================= 16. GURMAR =======================
R.append({
 "id": "gurmar",
 "names": {"common_en": "Gymnema", "hindi": "Gudmar (गुड़मार)", "sanskrit": "Meshashringi (मेषशृङ्गी)",
           "latin": "Gymnema sylvestre (Retz.) R.Br. ex Sm.", "other": ["Gurmar", "Sugar destroyer"]},
 "kind": "herb",
 "common_products": ["Gurmar churna", "Gymnema capsules/tablets", "Gurmar in polyherbal sugar-balance products (e.g. Madhunashini vati)"],
 "traditional_context": "Traditionally used in Ayurveda for the general wellbeing of metabolism; the leaf briefly dulls sweet taste.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Lowers blood glucose; insulin requirements fell in people on insulin in an early study.", "clinical", [P(2259216), P(2259217)]),
   F("liver", "Rare cases of liver injury have been reported.", "case_reports", [G("lt_gym"), P(20856101)]),
 ],
 "interactions": [
   *DM("moderate", "May lower blood sugar further; insulin or tablet doses may need adjusting.",
       "Glucose-lowering effect in clinical studies; reduced insulin requirements reported.", "clinical", [P(2259216), P(2259217)]),
   I("cyp2c9_substrate", "moderate", "May change blood levels of medicines broken down by CYP2C9 (e.g. tolbutamide, warfarin).",
     "Ethanolic extract altered tolbutamide (CYP2C9 probe) kinetics in rats; organic extracts inhibited CYP2C9 in vitro, aqueous extract did not.", "preclinical",
     [P(29042257), P(27761064)]),
   I("cyp1a2_substrate", "moderate", "May raise blood levels of medicines broken down by CYP1A2.",
     "Increased phenacetin (CYP1A2 probe) exposure about 1.3-1.4-fold in rats; CYP1A2 inhibition in vitro.", "preclinical",
     [P(29042257), P(27761064)]),
   I("hepatotoxic", "minor", "May add to the risk of liver injury.", "Rare reports of Gymnema-associated hepatitis; additive risk theoretical.", "case_reports",
     [G("lt_gym"), P(20856101)]),
 ],
 "data_quality": "limited",
})

# ======================= 17. MULETHI =======================
LIC_K = "Glycyrrhizin causes potassium loss and salt/water retention (pseudo-aldosteronism)."
R.append({
 "id": "mulethi",
 "names": {"common_en": "Liquorice / Licorice root", "hindi": "Mulethi (मुलेठी)", "sanskrit": "Yashtimadhu (यष्टिमधु)",
           "latin": "Glycyrrhiza glabra L.", "other": ["Jethimadh", "Licorice"]},
 "kind": "herb",
 "common_products": ["Mulethi powder / sticks", "Yashtimadhu churna", "Licorice tea", "Cough lozenges and syrups", "DGL (deglycyrrhizinated licorice) tablets"],
 "traditional_context": "Traditionally used in Ayurveda for the general wellbeing of the throat, voice and digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypotension", "Regular intake of glycyrrhizin-containing licorice can raise blood pressure, lower potassium, cause fluid retention and heart-rhythm problems (pseudo-aldosteronism). EMA advises against use with high blood pressure, kidney, liver or heart disease, or low potassium.", "regulatory",
     [G("ema_lic"), P(34604277), P(36843745)]),
   F("pregnancy", "EMA does not recommend use in pregnancy or breastfeeding; heavy licorice intake in pregnancy has been linked to earlier delivery.", "regulatory", [G("ema_lic"), G("nccih_lic"), P(12396997)]),
   F("other", "Deglycyrrhizinated licorice (DGL) lacks most glycyrrhizin and is less likely to cause these effects.", "regulatory", [G("nccih_lic")]),
 ],
 "interactions": [
   I("diuretic_loop_thiazide", "major", "Can cause dangerously low potassium when combined with water tablets.",
     LIC_K + " EMA: not to be used with diuretics.", "clinical", [G("ema_lic"), P(1563455)],
     "Avoid this combination unless your doctor agrees. " + ADV),
   I("cardiac_glycoside", "major", "Low potassium from licorice can make digoxin toxic (dangerous heart rhythms).",
     LIC_K + " EMA: not to be used with cardiac glycosides.", "clinical", [G("ema_lic")],
     "Avoid this combination unless your doctor agrees. " + ADV),
   I("antiarrhythmic", "major", "Low potassium can trigger dangerous heart rhythms (torsades de pointes) with rhythm medicines.",
     LIC_K + " Torsades de pointes reported with licorice-induced hypokalaemia; EMA warns against use with medicines that aggravate electrolyte imbalance.", "case_reports",
     [G("ema_lic"), P(36843745)], "Avoid this combination unless your doctor agrees. " + ADV),
   I("corticosteroid", "major", "Adds to potassium loss and fluid retention, and may increase steroid effects.",
     "Glycyrrhizin inhibits 11β-HSD2 and raises prednisolone levels; EMA: not to be used with corticosteroids.", "clinical",
     [G("ema_lic"), G("nccih_lic"), P(1752235)], "Avoid this combination unless your doctor agrees. " + ADV),
   I("laxative_stimulant", "major", "Combined potassium loss can become dangerous.", LIC_K + " EMA: not to be used with stimulant laxatives.", "clinical",
     [G("ema_lic"), G("ema_sen")], "Avoid this combination unless your doctor agrees. " + ADV),
   I("antihypertensive", "moderate", "May raise blood pressure and work against blood-pressure medicines.", "Mineralocorticoid-like effect; EMA states it may counteract antihypertensives.", "clinical",
     [G("ema_lic")], ADV + " Have your blood pressure checked."),
   I("cyp3a4_substrate_narrow", "moderate", "May lower blood levels of medicines broken down by CYP3A4.",
     "Glycyrrhizin 300 mg/day for 14 days modestly induced CYP3A (midazolam AUC down ~23%); EMA advises caution.", "clinical",
     [G("ema_lic"), P(20393696)]),
   I("hormonal_contraceptive_estrogen", "moderate", "Women on the pill may be more sensitive to licorice side effects (high blood pressure, low potassium, swelling).",
     "In a dose-ranging study, a volunteer taking oral contraceptives developed hypertension, hypokalaemia and oedema on high-dose licorice.", "clinical",
     [P(8072387)]),
   I("anticoagulant_vka", "moderate", "May lower warfarin levels and weaken its effect.",
     "Licorice (Glycyrrhiza uralensis) activated PXR and increased warfarin metabolism in rats; not confirmed in people.", "preclinical", [P(16267138)],
     ADV + " Your INR may need checking."),
   I("potassium_sparing", "minor", "Licorice's potassium-lowering effect can confuse blood-test results and blood-pressure control in people on these medicines.",
     "Mineralocorticoid-like action opposes spironolactone/eplerenone; theoretical.", "theoretical", [P(34604277)]),
 ],
 "data_quality": "good",
})

# ======================= 18. SENNA =======================
SEN_SRC = [G("ema_sen")]
R.append({
 "id": "senna",
 "names": {"common_en": "Senna", "hindi": "Sanay / Sonamukhi (सनाय / सोनामुखी)", "sanskrit": "Svarnapatri (स्वर्णपत्री)",
           "latin": "Senna alexandrina Mill. (syn. Cassia angustifolia Vahl)", "other": ["Indian senna", "Tinnevelly senna"]},
 "kind": "herb",
 "common_products": ["Senna leaf powder / tea", "Senna tablets (sennosides)", "Panchsakar churna", "Many 'detox' and 'slimming' teas", "Pet saffa / laxative churnas"],
 "traditional_context": "Traditionally used in Ayurveda and Unani for short-term support of bowel regularity.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "EMA contraindicates senna in pregnancy and breastfeeding (genotoxicity concerns with anthranoids; metabolites pass into milk).", "regulatory", SEN_SRC),
   F("children", "EMA contraindicates use in children under 12.", "regulatory", SEN_SRC),
   F("kidney", "Long-term use can cause potassium and fluid loss; people with kidney problems should be aware of electrolyte imbalance.", "regulatory", SEN_SRC),
   F("liver", "Rare liver injury has been reported, mostly with long-term high-dose use.", "case_reports", [G("lt_sen"), P(15956233)]),
   F("other", "Not for long-term use: prolonged use can cause laxative dependence and bowel dysfunction.", "regulatory", SEN_SRC),
 ],
 "interactions": [
   I("cardiac_glycoside", "moderate", "Potassium loss from prolonged use can make digoxin more toxic.", "Hypokalaemia from long-term laxative use potentiates cardiac glycosides (EMA).", "clinical", SEN_SRC),
   I("antiarrhythmic", "moderate", "Potassium loss can increase the risk of heart-rhythm problems with rhythm medicines.", "Hypokalaemia interacts with antiarrhythmics and QT-prolonging drugs (EMA).", "clinical", SEN_SRC),
   I("diuretic_loop_thiazide", "moderate", "Adds to potassium loss.", "EMA: concomitant diuretics may enhance potassium loss.", "clinical", SEN_SRC),
   I("corticosteroid", "moderate", "Adds to potassium loss.", "EMA: concomitant corticosteroids may enhance potassium loss.", "clinical", SEN_SRC),
 ],
 "data_quality": "good",
})

# ======================= 19. ALOE VERA (oral) =======================
R.append({
 "id": "aloe_vera_oral",
 "names": {"common_en": "Aloe vera (taken by mouth)", "hindi": "Ghritkumari / Gwarpatha (घृतकुमारी / ग्वारपाठा)", "sanskrit": "Kumari (कुमारी)",
           "latin": "Aloe vera (L.) Burm.f. (syn. Aloe barbadensis Mill.)", "other": ["Aloe juice", "Aloe latex"]},
 "kind": "herb",
 "common_products": ["Aloe vera juice", "Aloe-amla juice", "Kumaryasava", "Aloe latex / 'aloe bitters' laxatives", "Aloe vera capsules"],
 "traditional_context": "Traditionally used in Ayurveda, as Kumari preparations, for the general wellbeing of digestion and skin.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("pregnancy", "Oral aloe (gel, latex or whole leaf) may be unsafe in pregnancy and breastfeeding; EMA contraindicates aloe latex laxatives in pregnancy, breastfeeding and children under 12.", "regulatory",
     [G("nccih_alo"), G("ema_alo")]),
   F("other", "In 2002 the FDA removed aloe from US over-the-counter laxatives because safety data were lacking; non-decolorised whole-leaf extract caused intestinal tumours in rats (NTP).", "regulatory",
     [G("fda_aloe"), P(22968693)]),
   F("liver", "Rare cases of hepatitis have been reported with oral aloe products.", "case_reports", [G("lt_alo"), P(17726067)]),
   F("hypoglycaemia", "Oral aloe may lower blood glucose.", "clinical", [G("nccih_alo")]),
   F("kidney", "Long-term laxative use of aloe latex can cause potassium and fluid loss.", "regulatory", [G("ema_alo")]),
 ],
 "interactions": [
   I("cardiac_glycoside", "moderate", "Potassium loss from aloe latex laxatives can make digoxin more toxic.", "Hypokalaemia from laxative use potentiates cardiac glycosides (EMA).", "clinical", [G("ema_alo")]),
   I("antiarrhythmic", "moderate", "Potassium loss can increase the risk of heart-rhythm problems.", "Hypokalaemia interacts with antiarrhythmics and QT-prolonging drugs (EMA).", "clinical", [G("ema_alo")]),
   I("diuretic_loop_thiazide", "moderate", "Adds to potassium loss.", "EMA: diuretics may enhance potassium loss with aloe laxatives.", "clinical", [G("ema_alo")]),
   I("corticosteroid", "moderate", "Adds to potassium loss.", "EMA: corticosteroids may enhance potassium loss with aloe laxatives.", "clinical", [G("ema_alo")]),
   *DM("moderate", "May lower blood sugar further with diabetes medicines.", "Oral aloe may reduce blood glucose and HbA1c (NCCIH).", "clinical", [G("nccih_alo")]),
   I("anaesthesia_surgery", "moderate", "May add to bleeding during surgery.", "Case of excess intraoperative bleeding attributed to aloe plus sevoflurane (both inhibit platelet thromboxane).", "case_reports",
     [P(15292490)], SURG_ADV),
   I("thyroid_hormone", "minor", "May lower thyroid hormone levels.", "Leaf extract reduced T3 and T4 in mice.", "preclinical", [P(12065164)]),
 ],
 "data_quality": "good",
 "_notes": "Inner-leaf gel and latex (aloin-containing) differ greatly; laxative/potassium warnings apply mainly to latex or whole-leaf products.",
})

# ======================= 20. ISABGOL =======================
PSY = [G("ema_psy")]
R.append({
 "id": "isabgol",
 "names": {"common_en": "Psyllium husk / Ispaghula", "hindi": "Isabgol (ईसबगोल)", "sanskrit": "Snigdhajiraka (स्निग्धजीरक)",
           "latin": "Plantago ovata Forssk.", "other": ["Ispaghula", "Psyllium"]},
 "kind": "herb",
 "common_products": ["Isabgol husk (e.g. Sat Isabgol)", "Psyllium powder drinks (e.g. Metamucil)", "Fibre supplements", "Isabgol-containing laxative granules"],
 "traditional_context": "Traditionally used in Ayurveda and Unani as a dietary fibre for the general wellbeing of bowel regularity.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("other", "Must be taken with plenty of water; taken with too little fluid it can block the throat, oesophagus or bowel. EMA contraindicates it with swallowing difficulty or bowel narrowing/obstruction.", "regulatory",
     PSY + [P(6488929)]),
   F("allergy", "Serious allergic reactions, including anaphylaxis, have been reported (higher risk in people sensitised by handling the powder).", "case_reports", PSY + [P(14700444)]),
   F("hypoglycaemia", "Lowers post-meal blood glucose; EMA says people with diabetes should use it under medical supervision as treatment may need adjustment.", "regulatory", PSY + [P(26561625)]),
 ],
 "interactions": [
   I("any_medicine", "moderate", "Can delay or reduce absorption of other medicines taken at the same time.",
     "Bulk-forming fibre binds/slows absorption of co-administered drugs (EMA).", "clinical", PSY, SEP_ADV),
   I("lithium", "moderate", "May lower lithium blood levels.", "Reduced lithium absorption; case report of falling lithium levels; EMA lists lithium.", "case_reports",
     PSY + [P(1968148)], SEP_ADV + " Lithium levels may need checking."),
   I("cardiac_glycoside", "moderate", "May reduce digoxin absorption.", "Delayed enteral absorption (EMA).", "clinical", PSY, SEP_ADV),
   I("anticoagulant_vka", "moderate", "May change warfarin absorption and INR control.", "Delayed absorption of coumarin derivatives (EMA).", "clinical", PSY, SEP_ADV + " Keep your intake steady and check INR if you start or stop."),
   I("antiepileptic", "moderate", "May reduce carbamazepine absorption.", "Delayed enteral absorption of carbamazepine (EMA).", "clinical", PSY, SEP_ADV),
   I("iron_mineral_supplement", "moderate", "May reduce absorption of minerals and vitamin B12.", "Delayed absorption of minerals and vitamins (EMA).", "clinical", PSY, SEP_ADV),
   I("thyroid_hormone", "minor", "May affect levothyroxine absorption.",
     "EMA advises medical supervision; a small human study found only a non-significant reduction in absorption.", "clinical", PSY + [P(9737361)], SEP_ADV),
   *DM("moderate", "May lower post-meal blood sugar; diabetes treatment may need adjusting.", "Soluble fibre slows carbohydrate absorption; EMA advises medical supervision.", "clinical",
       PSY + [P(26561625)], advice=SEP_ADV + " Check your blood sugar more often when starting."),
   I("opioid", "moderate", "Higher risk of bowel blockage with medicines that slow the gut.", "EMA: use with peristalsis-inhibiting medicines (e.g. opioids) only under medical supervision.", "theoretical",
     PSY, ADV + " Drink plenty of fluid."),
 ],
 "data_quality": "good",
})

# ======================= 21. SHANKHPUSHPI =======================
R.append({
 "id": "shankhpushpi",
 "names": {"common_en": "Shankhpushpi", "hindi": "Shankhpushpi (शंखपुष्पी)", "sanskrit": "Shankhapushpi (शङ्खपुष्पी)",
           "latin": "Convolvulus pluricaulis Choisy (syn. Convolvulus prostratus Forssk.)", "other": ["Evolvulus alsinoides and Clitoria ternatea are also sold under this name"]},
 "kind": "herb",
 "common_products": ["Shankhpushpi syrup", "Shankhpushpi churna", "Memory/brain tonics with brahmi and shankhpushpi"],
 "traditional_context": "Traditionally used in Ayurveda as a medhya herb for the general wellbeing of memory and calm.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("thyroid", "Root extract lowered T3 in mice (including mice given levothyroxine).", "preclinical", [P(11280709)]),
   F("other", "Several different plants are sold as shankhpushpi; product identity varies.", "theoretical", [P(25182446)]),
 ],
 "interactions": [
   I("antiepileptic", "major", "Has been linked to loss of seizure control with phenytoin.",
     "Two patients on phenytoin taking a Shankhapushpi preparation had lower phenytoin levels and seizures; in rats, repeated dosing lowered phenytoin levels and its anti-seizure effect. Authors advised against the combination.", "case_reports",
     [P(1548901), P(1484013)], "Avoid this combination unless your neurologist agrees. " + ADV),
   I("thyroid_hormone", "minor", "May reduce the effect of levothyroxine.", "Inhibited T3 production (5'-deiodinase) in levothyroxine-treated mice.", "preclinical", [P(11280709)]),
 ],
 "data_quality": "limited",
 "_notes": "The phenytoin study used a multi-ingredient syrup called Shankhapushpi; the effect may not be from Convolvulus alone.",
})

# ======================= 22. PUNARNAVA =======================
R.append({
 "id": "punarnava",
 "names": {"common_en": "Punarnava / Spreading hogweed", "hindi": "Punarnava (पुनर्नवा)", "sanskrit": "Punarnava (पुनर्नवा)",
           "latin": "Boerhavia diffusa L.", "other": ["Red hogweed", "Gadahpurna"]},
 "kind": "herb",
 "common_products": ["Punarnava churna", "Punarnavadi mandur", "Punarnavasava", "Punarnava capsules"],
 "traditional_context": "Traditionally used in Ayurveda for the general wellbeing of the urinary system and fluid balance.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Leaf extract lowered blood glucose in diabetic rats.", "preclinical", [P(15036478)]),
   F("other", "Few human safety data; traditionally regarded as diuretic.", "preclinical", [P(26844923)]),
 ],
 "interactions": [
   I("diuretic_loop_thiazide", "minor", "May add to the effect of water tablets.", "Traditional diuretic use and diuretic activity reported in animal studies; theoretical in people.", "theoretical",
     [P(26844923), P(1178789)]),
   I("lithium", "minor", "Diuretic herbs may change lithium levels.", "Theoretical: altered fluid/sodium balance can affect lithium clearance.", "theoretical", [P(26844923)],
     ADV + " Lithium levels may need checking."),
   *DM("minor", "May lower blood sugar further with diabetes medicines.", "Hypoglycaemic effect in diabetic rats.", "preclinical", [P(15036478), P(15671692)]),
 ],
 "data_quality": "poor",
})

# ======================= 23. GOKSHURA =======================
R.append({
 "id": "gokshura",
 "names": {"common_en": "Puncture vine / Tribulus", "hindi": "Gokhru (गोखरू)", "sanskrit": "Gokshura (गोक्षुर)",
           "latin": "Tribulus terrestris L.", "other": ["Tribulus", "Caltrop"]},
 "kind": "herb",
 "common_products": ["Gokshura churna", "Gokshuradi guggulu", "Tribulus capsules (sports/libido supplements)"],
 "traditional_context": "Traditionally used in Ayurveda for the general wellbeing of the urinary and male reproductive systems.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("kidney", "Severe kidney injury (with raised liver enzymes and neurotoxicity) has been reported after drinking Tribulus water.", "case_reports", [P(20667992), P(38328764)]),
   F("liver", "Rare cholestatic liver injury reported, often with kidney injury.", "case_reports", [G("lt_tri"), P(38328764)]),
   F("other", "Gynaecomastia reported in a young man using a Tribulus product.", "case_reports", [P(15454201)]),
 ],
 "interactions": [
   I("nephrotoxic", "moderate", "May add to kidney stress from medicines that can harm the kidneys.", "Tribulus-associated kidney injury case reports; additive risk theoretical.", "case_reports",
     [P(20667992), P(38328764)]),
   I("hepatotoxic", "minor", "May add to the risk of liver injury.", "Rare Tribulus-associated liver injury; theoretical additive risk.", "case_reports", [G("lt_tri")]),
   I("antihypertensive", "minor", "May lower blood pressure further.", "ACE-inhibiting and blood-pressure-lowering effect in hypertensive rats.", "preclinical", [P(14519445)]),
   *DM("minor", "May lower blood sugar slightly with diabetes medicines.", "Lowered fasting glucose in a small randomised trial in women with diabetes.", "clinical", [P(27255456)]),
   I("lithium", "minor", "Diuretic herbs may change lithium levels.", "Theoretical: traditional diuretic use may alter lithium clearance.", "theoretical", [G("lt_tri")],
     ADV + " Lithium levels may need checking."),
   I("antidepressant_ssri_snri", "minor", "Isolated side effects (itching, breast milk secretion) were reported with citalopram/escitalopram.", "Pharmacovigilance chart review; mechanism unclear.", "case_reports",
     [P(37829299)]),
 ],
 "data_quality": "limited",
})

# ======================= 24. SAFED MUSLI =======================
R.append({
 "id": "safed_musli",
 "names": {"common_en": "Safed musli", "hindi": "Safed musli (सफ़ेद मूसली)", "sanskrit": "Shveta musali (श्वेत मुसली)",
           "latin": "Chlorophytum borivilianum Santapau & R.R.Fern.", "other": ["White musli"]},
 "kind": "herb",
 "common_products": ["Safed musli powder", "Safed musli capsules", "Musli pak", "Vitality/men's wellness blends"],
 "traditional_context": "Traditionally used in Ayurveda as a vajikarana rasayana for general vitality and the wellbeing of the male reproductive system.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Root extract lowered blood glucose in diabetic rats.", "preclinical", [P(25249786)]),
   F("other", "Very few human safety data.", "preclinical", [P(24045177)]),
 ],
 "interactions": [
   *DM("minor", "May lower blood sugar further with diabetes medicines.", "Glucose-lowering effect in diabetic rats; no human data.", "preclinical", [P(25249786)]),
 ],
 "data_quality": "poor",
})

# ======================= 25. SHILAJIT =======================
R.append({
 "id": "shilajit",
 "names": {"common_en": "Shilajit / Mineral pitch", "hindi": "Shilajit (शिलाजीत)", "sanskrit": "Shilajatu (शिलाजतु)",
           "latin": "Asphaltum punjabianum (mineral exudate, not a plant)", "other": ["Mumie", "Mumijo", "Moomiyo"]},
 "kind": "mineral_preparation",
 "common_products": ["Shilajit resin", "Shilajit capsules/tablets", "Shuddha shilajit", "Shilajit in men's vitality products"],
 "traditional_context": "Traditionally used in Ayurveda, after purification (shodhana), as a rasayana for general vitality.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("heavy_metals", "Raw or poorly purified shilajit can contain toxic metals; Ayurvedic products bought online have repeatedly tested positive for lead, mercury or arsenic.", "clinical",
     [P(34800280), P(18728265), P(15598918)]),
   F("other", "Human safety data are limited; it can raise testosterone levels.", "clinical", [P(23733436), P(26395129)]),
 ],
 "interactions": [
   I("nephrotoxic", "minor", "Contaminated products could add to kidney stress.", "Theoretical: heavy-metal contamination of some products.", "theoretical", [P(34800280), P(18728265)],
     ADV + " Choose only tested, purified products."),
   I("hepatotoxic", "minor", "Contaminated products could add to liver stress.", "Theoretical: heavy-metal contamination of some products.", "theoretical", [P(34800280), P(15598918)],
     ADV + " Choose only tested, purified products."),
 ],
 "data_quality": "poor",
})

# ======================= 26. KALONJI =======================
R.append({
 "id": "kalonji",
 "names": {"common_en": "Black seed / Black cumin", "hindi": "Kalonji (कलौंजी)", "sanskrit": "Upakunchika (उपकुञ्चिका), Krishna jiraka",
           "latin": "Nigella sativa L.", "other": ["Black seed oil", "Nigella", "Habbatus sauda"]},
 "kind": "food_spice",
 "common_products": ["Kalonji seeds (culinary)", "Black seed oil", "Black seed capsules", "Kalonji honey blends"],
 "traditional_context": "Traditionally used in Ayurveda, Unani and Indian cooking for the general wellbeing of digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("hypoglycaemia", "Lowered blood glucose in people with type 2 diabetes in clinical trials.", "clinical", [P(21675032), P(25706772)]),
   F("hypotension", "Modestly lowers blood pressure in trials.", "clinical", [P(27512971)]),
   F("kidney", "Acute kidney failure was reported in a person taking large amounts of black seed.", "case_reports", [P(23464648)]),
   F("bleeding", "Severe low platelets were reported in a patient taking black seed oil with evening primrose oil.", "case_reports", [P(32637272)]),
   F("liver", "Not linked to clinically apparent liver injury in LiverTox.", "regulatory", [G("lt_nig")]),
 ],
 "interactions": [
   *DM("moderate", "May lower blood sugar further with diabetes medicines.", "Glucose-lowering effect in clinical trials.", "clinical", [P(21675032), P(25706772)]),
   I("antihypertensive", "minor", "May lower blood pressure further.", "Blood-pressure-lowering effect in meta-analysis of trials.", "clinical", [P(27512971)]),
   I("cyp2d6_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2D6.", "Black seed inhibited CYP2D6 (dextromethorphan O-demethylation) in vitro and in 4 healthy volunteers.", "clinical",
     [P(20201775)]),
   I("cyp3a4_substrate_narrow", "moderate", "May raise blood levels of medicines broken down by CYP3A4.", "Black seed inhibited CYP3A4 (dextromethorphan N-demethylation) in vitro and in a small volunteer study.", "clinical",
     [P(20201775)]),
   I("immunosuppressant", "moderate", "May lower cyclosporine levels and weaken its effect.", "Nigella sativa reduced cyclosporine Cmax by ~36% and AUC by ~56% in rabbits.", "preclinical",
     [P(23957013)], ADV + " Cyclosporine levels may need extra monitoring."),
   I("anticoagulant_vka", "moderate", "May raise warfarin levels.", "Thymoquinone competitively inhibited warfarin 7-hydroxylation (CYP2C9) in vitro; modelling suggested risk above ~1 g/day of seed or oil.", "preclinical",
     [P(35921950)], BLEED_ADV),
   I("cyp2c9_substrate", "moderate", "May raise blood levels of medicines broken down by CYP2C9.", "Thymoquinone inhibited CYP2C9 in vitro.", "preclinical", [P(35921950)]),
   I("nitrate_pde5", "minor", "May lower sildenafil levels.", "Reduced sildenafil AUC and Cmax in dogs.", "preclinical", [P(24719213)]),
   I("nephrotoxic", "minor", "May add to kidney stress.", "Single case of acute kidney failure; theoretical additive risk.", "case_reports", [P(23464648)]),
 ],
 "data_quality": "limited",
})

# ======================= 27. CINNAMON =======================
R.append({
 "id": "cinnamon",
 "names": {"common_en": "Cinnamon (Ceylon and cassia)", "hindi": "Dalchini (दालचीनी)", "sanskrit": "Tvak (त्वक्)",
           "latin": "Cinnamomum verum J.Presl (Ceylon); Cinnamomum cassia (L.) J.Presl (cassia)", "other": ["Cassia", "Ceylon cinnamon"]},
 "kind": "food_spice",
 "common_products": ["Dalchini sticks / powder (culinary)", "Cinnamon capsules", "Cinnamon tea", "Sitopaladi churna (contains tvak)"],
 "traditional_context": "Traditionally used in Ayurveda and Indian cooking for the general wellbeing of digestion.",
 "traditional_source_type": "classical text",
 "general_safety": [
   F("liver", "Cassia cinnamon contains coumarin, which can harm the liver in sensitive people with prolonged high intake; Ceylon cinnamon contains far less.", "regulatory",
     [G("nccih_cin"), G("lt_cin"), P(20024932)]),
   F("pregnancy", "Food amounts are likely safe, but larger amounts (supplements) are considered unsafe in pregnancy; EMA does not recommend medicinal use in pregnancy or breastfeeding.", "regulatory",
     [G("nccih_cin"), G("ema_cin")]),
   F("allergy", "EMA contraindicates use with allergy to cinnamon or Peru balsam.", "regulatory", [G("ema_cin")]),
   F("hypoglycaemia", "Cinnamon supplements may modestly lower fasting glucose.", "clinical", [P(24019277)]),
 ],
 "interactions": [
   I("hepatotoxic", "moderate", "Cassia cinnamon supplements may add to liver stress with medicines that can harm the liver.", "Coumarin hepatotoxicity in sensitive individuals; additive risk theoretical.", "theoretical",
     [G("nccih_cin"), P(20024932), P(27378929)], ADV + " If you take supplements, Ceylon cinnamon contains much less coumarin."),
   *DM("minor", "May lower blood sugar slightly with diabetes medicines.", "Modest fasting-glucose lowering in meta-analysis.", "clinical", [P(24019277)]),
   I("anticancer", "minor", "Possible interaction with letrozole was predicted, but a clinical study found none.",
     "Cinnamaldehyde inactivates CYP2A6 in vitro (NCCIH notes theoretical concern); a 2026 clinical study of Ceylon cinnamon found no change in letrozole or nicotine levels.", "clinical",
     [G("nccih_cin"), P(26851241), P(41622703)]),
 ],
 "data_quality": "good",
})

# ---------------- resolve PubMed titles from NCBI (never typed by hand) ----------------
def collect(rec):
    for blk in rec["general_safety"] + rec["interactions"]:
        for s in blk["sources"]:
            if "pmid" in s:
                yield s["pmid"]

pmids = sorted({p for r in R for p in collect(r)}, key=int)
titles = {}
def fetch(ids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids)
    for i in range(8):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=40))
            if "result" in d:
                return d["result"]
        except Exception:
            pass
        time.sleep(2 + i)
    raise SystemExit("esummary failed")
for i in range(0, len(pmids), 40):
    res = fetch(pmids[i:i+40])
    for p in pmids[i:i+40]:
        x = res.get(p)
        if not x or not x.get("title") or "error" in x:
            raise SystemExit("PMID not found: " + p)
        titles[p] = "%s %s (%s)" % (x["title"].rstrip(), x.get("source", ""), x.get("pubdate", "")[:4])
    time.sleep(1.2)

for r in R:
    for blk in r["general_safety"] + r["interactions"]:
        new = []
        for s in blk["sources"]:
            if "pmid" in s:
                new.append({"title": titles[s["pmid"]], "url": "https://pubmed.ncbi.nlm.nih.gov/%s/" % s["pmid"], "type": "peer_review"})
            else:
                new.append(s)
        blk["sources"] = new

# ---------------- validate against spec ----------------
spec = open(SPEC).read()
block = spec.split("## Shared drug interaction classes")[1].split("## Herb record schema")[0]
keys = set(re.findall(r"^([a-z0-9_]+)\s", block, re.M))
FLAGS = set("pregnancy breastfeeding liver kidney heavy_metals bleeding hypoglycaemia hypotension thyroid autoimmune surgery children allergy other".split())
bad = []
for r in R:
    r.pop("_notes", None)
    r["last_checked"] = "2026-10"
    for it in r["interactions"]:
        if it["drug_class"] not in keys: bad.append((r["id"], "class", it["drug_class"]))
        if it["severity"] not in ("major", "moderate", "minor"): bad.append((r["id"], "sev", it["severity"]))
        if it["evidence"] not in ("clinical", "case_reports", "preclinical", "theoretical"): bad.append((r["id"], "ev", it["evidence"]))
        if it["evidence"] in ("preclinical", "theoretical") and it["severity"] == "major": bad.append((r["id"], "major-theory", it["drug_class"]))
        if not it["sources"]: bad.append((r["id"], "nosrc", it["drug_class"]))
        if re.search(r"stop (taking )?your (medicine|medication)|instead", it["advice"], re.I): bad.append((r["id"], "advice", it["advice"]))
    for f in r["general_safety"]:
        if f["flag"] not in FLAGS: bad.append((r["id"], "flag", f["flag"]))
        if not f["sources"]: bad.append((r["id"], "nosrc-flag", f["flag"]))
    if re.search(r"diabet|cancer|hypertens|arthrit|asthma|infect|disease|cure|treat", r["traditional_context"], re.I):
        bad.append((r["id"], "tc", r["traditional_context"]))
    dup = [it["drug_class"] for it in r["interactions"]]
    if len(dup) != len(set(dup)): bad.append((r["id"], "dup", [d for d in dup if dup.count(d) > 1]))
if bad:
    for b in bad: print("BAD", b)
    raise SystemExit(1)

json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
n = sum(len(r["interactions"]) for r in R)
maj = [(r["id"], i["drug_class"]) for r in R for i in r["interactions"] if i["severity"] == "major"]
print("herbs", len(R), "interactions", n, "major", len(maj), maj)
print("pmids", len(pmids))
