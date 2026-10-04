import json

OUT = "/home/user/octogent/fitme-ayurveda-data/research/herbs_batch4.json"
LC = "2026-10"
DEFAULT_ADVICE = "Talk to your doctor or pharmacist before combining."

PM = "https://pubmed.ncbi.nlm.nih.gov/%s/"

S = {
    # Heavy metals / regulatory
    "saper04": ("Saper RB et al. Heavy metal content of ayurvedic herbal medicine products. JAMA 2004", PM % "15598918", "peer_review"),
    "saper08": ("Saper RB et al. Lead, mercury, and arsenic in US- and Indian-manufactured Ayurvedic medicines sold via the Internet. JAMA 2008;300:915-23", PM % "18728265", "peer_review"),
    "mmwr04": ("CDC MMWR. Lead poisoning associated with ayurvedic medications - five states, 2000-2003", "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5326a3.htm", "gov"),
    "mmwr12": ("CDC MMWR. Lead poisoning in pregnant women who used Ayurvedic medications from India - New York City, 2011-2012", "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6133a1.htm", "gov"),
    "mmwr15": ("CDC MMWR. Lead poisoning and anemia associated with use of Ayurvedic medications purchased on the Internet - Wisconsin, 2015 (Mahayogaraj Guggulu sample 4.9% lead)", "https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6432a6.htm", "gov"),
    "fda25": ("FDA. FDA warns about heavy metal poisoning associated with certain unapproved ayurvedic drug products (Dec 2025; products placed on Import Alerts 66-41 and 99-42)", "https://www.fda.gov/drugs/fraudulent-products/fda-warns-about-heavy-metal-poisoning-associated-certain-unapproved-ayurvedic-drug-products", "gov"),
    "arsenic14": ("Chronic arsenic poisoning following ayurvedic medication. J Med Toxicol 2014", PM % "24696169", "peer_review"),
    "rasakarpura25": ("The Ayurvedic remedy Rasa Karpura and a case of inorganic mercury toxicity. Pediatrics 2025", PM % "41052789", "peer_review"),
    "cericola25": ("Cericola G et al. Case report: severe lead poisoning due to exposure to ayurvedic herbal medicine (child). Front Pediatr 2025", PM % "41244251", "peer_review"),
    "kamath12": ("Kamath SU et al. Mercury-based traditional herbo-metallic preparations: a toxicological perspective. Arch Toxicol 2012", PM % "22441626", "peer_review"),
    "jamadagni20": ("Jamadagni S et al. Tissue distribution of mercury and copper after Aarogyavardhini Vati treatment in a rat model. J Ayurveda Integr Med 2020", PM % "32035767", "peer_review"),
    "lavekar10": ("Lavekar GS et al. Mahayograj guggulu: heavy metal estimation and safety studies. Int J Ayurveda Res 2010", PM % "21170206", "peer_review"),
    "mmwr_iron": ("CDC MMWR. Toddler deaths resulting from ingestion of iron supplements - Los Angeles, 1992-1993", "https://www.cdc.gov/mmwr/preview/mmwrhtml/00019593.htm", "gov"),
    "cfr_calamus": ("US eCFR 21 CFR 189.110 - Calamus and its derivatives (prohibited from use in human food)", "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-189/subpart-C/section-189.110", "gov"),
    # Guggul / piperine / trikatu
    "dalvi94": ("Dalvi SS et al. Effect of gugulipid on bioavailability of diltiazem and propranolol. J Assoc Physicians India 1994", PM % "7852226", "peer_review"),
    "brobst04": ("Brobst DE et al. Guggulsterone activates multiple nuclear receptors and induces CYP3A gene expression through the pregnane X receptor. J Pharmacol Exp Ther 2004", PM % "15075359", "peer_review"),
    "mskcc_guggul": ("Memorial Sloan Kettering Cancer Center - About Herbs: Guggul", "https://www.mskcc.org/cancer-care/integrative-medicine/herbs/guggul", "other"),
    "sabarathinam21": ("Sabarathinam S et al. CYP3A4 mediated pharmacokinetics drug interaction potential of Maha-Yogaraj Guggulu and E,Z guggulsterone. Sci Rep 2021", PM % "33436877", "peer_review"),
    "bano91": ("Bano G et al. Effect of piperine on bioavailability and pharmacokinetics of propranolol and theophylline in healthy volunteers. Eur J Clin Pharmacol 1991", PM % "1815977", "peer_review"),
    "pattanaik06": ("Pattanaik S et al. Effect of piperine on the steady-state pharmacokinetics of phenytoin in patients with epilepsy. Phytother Res 2006", PM % "16767797", "peer_review"),
    "bhardwaj02": ("Bhardwaj RK et al. Piperine, a major constituent of black pepper, inhibits human P-glycoprotein and CYP3A4. J Pharmacol Exp Ther 2002", PM % "12130727", "peer_review"),
    "karan99": ("Karan RS et al. Effect of trikatu on the pharmacokinetic profile of rifampicin in rabbits. J Ethnopharmacol 1999", PM % "10363842", "peer_review"),
    "lala04": ("Lala LG et al. Pharmacokinetic and pharmacodynamic studies on interaction of Trikatu with diclofenac sodium. J Ethnopharmacol 2004", PM % "15120451", "peer_review"),
    # Triphala / amla / chyawanprash
    "nontakham22": ("Nontakham J et al. Inhibitory effects of Triphala on CYP isoforms in vitro and its pharmacokinetic interactions with phenacetin and midazolam in rats. Heliyon 2022", PM % "35785236", "peer_review"),
    "ponnusankar11": ("Ponnusankar S et al. Cytochrome P450 inhibitory potential of Triphala - a Rasayana from Ayurveda. J Ethnopharmacol 2011", PM % "20883765", "peer_review"),
    "peterson17": ("Peterson CT et al. Therapeutic uses of Triphala in Ayurvedic medicine. J Altern Complement Med 2017", PM % "28696777", "peer_review"),
    "fatima14": ("Fatima N et al. Pharmacodynamic interaction of Phyllanthus emblica extract with clopidogrel and ecosprin in patients with type II diabetes. Phytomedicine 2014", PM % "24291054", "peer_review"),
    "sharma19cp": ("Sharma R et al. Chyawanprash: a traditional Indian bioactive health supplement. Biomolecules 2019", PM % "31035513", "peer_review"),
    # Arishtas / alcohol
    "niaaa": ("NIAAA (NIH). Harmful interactions: mixing alcohol with medicines", "https://www.niaaa.nih.gov/publications/brochures-and-fact-sheets/harmful-interactions-mixing-alcohol-with-medicines", "gov"),
    "weerasooriya06": ("Weerasooriya W et al. Quantitative parameters of different brands of Asava and Arishta used in ayurvedic medicine. Indian J Pharmacol 2006", "https://www.ijp-online.com/article.asp?issn=0253-7613;year=2006;volume=38;issue=5;spage=365;epage=365;aulast=Weerasooriya", "peer_review"),
    "fernando20": ("Fernando NF et al. Screening for performance enhancing substances and quantification of ethanol in different Arishta manufactured in Sri Lanka. Ceylon Med J 2020", PM % "34825559", "peer_review"),
    "selvan15": ("Selvan PS, Priya ES. Determination of ethanol content in ayurvedic formulations Kumaryasava and Mustakarista by gas chromatography. Indian J Pharm Sci 2015", PM % "25767329", "peer_review"),
    "pandit17": ("Pandit S et al. Evaluation of herb-drug interaction of a polyherbal Ayurvedic formulation (Ridayarishta, made from Arjunarishta and Ashwagandharishta ingredients) through CYP450 inhibition assay. J Ethnopharmacol 2017", PM % "27457692", "peer_review"),
    "varghese15": ("Varghese A et al. In vitro modulatory effects of Terminalia arjuna and its constituents on CYP3A4, CYP2D6 and CYP2C9 in human liver microsomes. Toxicol Rep 2015", PM % "28962416", "peer_review"),
    "shengule18": ("Shengule SA et al. Anti-hyperglycemic and anti-hyperlipidaemic effect of Arjunarishta in high-fat fed animals. J Ayurveda Integr Med 2018", PM % "29249636", "peer_review"),
    # Ashwagandha
    "ods_ashwa": ("NIH Office of Dietary Supplements. Ashwagandha - Health Professional Fact Sheet", "https://ods.od.nih.gov/factsheets/Ashwagandha-HealthProfessional/", "gov"),
    "livertox_ashwa": ("NIH LiverTox: Ashwagandha", "https://www.ncbi.nlm.nih.gov/books/NBK548536/", "gov"),
    "bjornsson20": ("Bjornsson HK et al. Ashwagandha-induced liver injury: a case series from Iceland and the US DILIN. Liver Int 2020", PM % "31991029", "peer_review"),
    "sharma18": ("Sharma AK et al. Efficacy and safety of ashwagandha root extract in subclinical hypothyroid patients: RCT. J Altern Complement Med 2018", PM % "28829155", "peer_review"),
    # Giloy
    "kulkarni22": ("Kulkarni AV et al. Tinospora cordifolia (Giloy)-induced liver injury during the COVID-19 pandemic - multicenter nationwide study from India. Hepatol Commun 2022", PM % "35037744", "peer_review"),
    "nagral21": ("Nagral A et al. Herbal immune booster-induced liver injury in the COVID-19 pandemic - a case series. J Clin Exp Hepatol 2021", PM % "34230786", "peer_review"),
    "pib_giloy": ("Ministry of AYUSH (PIB, 2021). Relating Giloy to liver damage is completely misleading", "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1733260", "gov"),
    "wadood92": ("Wadood N et al. Effect of Tinospora cordifolia on blood glucose and total lipid levels of normal and alloxan-diabetic rabbits. Planta Med 1992", PM % "1529024", "peer_review"),
    # Minerals
    "ods_iron": ("NIH Office of Dietary Supplements. Iron - Health Professional Fact Sheet (interactions with levothyroxine, levodopa, PPIs)", "https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/", "gov"),
    "ods_ca": ("NIH Office of Dietary Supplements. Calcium - Health Professional Fact Sheet (interactions with levothyroxine, lithium, quinolone antibiotics)", "https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/", "gov"),
    "eljaaly21": ("Eljaaly K et al. Multivalent cations interactions with fluoroquinolones or tetracyclines: a cross-sectional study. Saudi J Biol Sci 2021", PM % "34866992", "peer_review"),
    "chavan18": ("Chavan S et al. Pharmaceutical standardization and physicochemical characterization of Shankha Bhasma (incinerated conch shell; calcite CaCO3, ~46% Ca). Mar Drugs 2018", PM % "30445775", "peer_review"),
    "bhargava12": ("Bhargava SC et al. Identification studies of Lauha Bhasma by X-ray diffraction and X-ray fluorescence. Ayu 2012", PM % "23049200", "peer_review"),
    "abhrak_char": ("Nanoparticles of biotite mica as Krishna Vajra Abhraka Bhasma: synthesis and characterization. J Ayurveda Integr Med 2021", PM % "33402266", "peer_review"),
    "gopinath21": ("Gopinath H et al. A study on toxicity and anti-hyperglycemic effects of Abhrak Bhasma in rats. J Ayurveda Integr Med 2021", PM % "34362606", "peer_review"),
    "biswas20": ("Biswas S et al. Physicochemical characterization of Suvarna Bhasma, its toxicity profiling in rat and behavioural assessment in zebrafish. J Ethnopharmacol 2020", PM % "31730889", "peer_review"),
    "punarnavadi": ("Kori VK et al. Evaluation of Punarnavadi Mandura (contains Mandura bhasma, iron oxide) for haematinic activity in rats. Ayu 2021", PM % "37153070", "peer_review"),
    "chandraprabha_np": ("Dongre P et al. Network pharmacology analysis of Chandraprabha Vati (lists 37 ingredients incl. Lauha bhasma, Shilajit, Guggulu, sugar). J Ayurveda Integr Med 2024", PM % "38821011", "peer_review"),
    "gandhak_tox": ("Mundugaru R et al. Chronic toxicity studies of Gandhaka Rasayana - a herbo-mineral preparation. J Ayurveda Integr Med 2021", PM % "34736857", "peer_review"),
    # Brahmi / bacopa
    "brahmivati_rct": ("Sarhyal A et al. Brahmi vati and Aswagandharista in major depressive disorder: RCT (Brahmi vati composition incl. Rasa sindoora and Swarnamakshika). J Ayurveda Integr Med 2024", PM % "39631219", "peer_review"),
    "bacopa_cyp": ("Ramasamy S et al. Inhibition of human cytochrome P450 enzymes by Bacopa monnieri standardized extract and constituents. Molecules 2014", PM % "24566323", "peer_review"),
    "kar02": ("Kar A et al. Relative efficacy of three medicinal plant extracts in the alteration of thyroid hormone concentrations in male mice (Bacopa raised T4). J Ethnopharmacol 2002", PM % "12065164", "peer_review"),
    # Liv.52 / Septilin / Cystone
    "desilva03": ("de Silva HA et al. Liv.52 in alcoholic liver disease: a prospective, controlled trial. J Ethnopharmacol 2003", PM % "12499076", "peer_review"),
    "liv52_review": ("Hepatoprotective effects of Liv.52 in chronic liver disease: preclinical, clinical and safety evidence - a review (discusses the unpublished Fleig 1997 trial). Hepatology Reports (MDPI) 2022", "https://www.mdpi.com/2036-7422/14/3/21", "peer_review"),
    "liv52_dove": ("The effect of Liv.52 DS in metabolic dysfunction-associated fatty liver disease (composition incl. Mandura bhasma). Hepat Med (Dove Press)", "https://www.dovepress.com/the-effect-of-liv52-ds-in-metabolic-dysfunction-associated-fatty-liver-peer-reviewed-fulltext-article-HMER", "peer_review"),
    "ema_licorice": ("EMA/HMPC. Draft European Union herbal monograph on Glycyrrhiza glabra / inflata / uralensis radix (revision 1)", "https://www.ema.europa.eu/en/documents/herbal-monograph/draft-european-union-herbal-monograph-glycyrrhiza-glabra-l-gycyrrhiza-inflata-bat-glycyrrhiza-uralensis-fisch-radix-revision-1_en.pdf", "gov"),
    "nccih_licorice": ("NIH NCCIH. Licorice root: usefulness and safety", "https://www.nccih.nih.gov/health/licorice-root", "gov"),
    "septilin_sd": ("Septilin herbo-mineral formulation in cisplatin-induced toxicity in mice (composition incl. Tinospora, Glycyrrhiza, guggul, Shankha bhasma). Mutat Res Genet Toxicol Environ Mutagen 2022", "https://www.sciencedirect.com/science/article/abs/pii/S138357182200002X", "peer_review"),
    "erickson11": ("Erickson SB et al. Cystone for 1 year did not change urine chemistry or decrease stone burden in cystine stone formers. Urol Res 2011", PM % "21161651", "peer_review"),
    "erickson11b": ("Erickson SB et al. Effect of Cystone on urinary composition and stone formation over a one year period (calcium oxalate stone formers). Phytomedicine 2011", PM % "21419609", "peer_review"),
    # Blood sugar
    "nccih_aloe": ("NIH NCCIH. Aloe vera: usefulness and safety (aloe latex overuse and cardiac glycosides)", "https://www.nccih.nih.gov/health/aloe-vera", "gov"),
    "nccih_diab": ("NIH NCCIH. Diabetes and dietary supplements: what you need to know", "https://www.nccih.nih.gov/health/diabetes-and-dietary-supplements-what-you-need-to-know", "gov"),
    "shane09": ("Shane-McWhorter L. Dietary supplements for diabetes: an evaluation of commonly used products (bitter melon, fenugreek, gymnema; hypoglycaemia with insulin/secretagogues). Diabetes Spectrum 2009", "https://diabetesjournals.org/spectrum/article/22/4/206/2405/Dietary-Supplements-for-Diabetes-An-Evaluation-of", "peer_review"),
    "baskaran90": ("Baskaran K et al. Antidiabetic effect of a leaf extract from Gymnema sylvestre in NIDDM patients (on oral hypoglycaemic drugs). J Ethnopharmacol 1990", PM % "2259217", "peer_review"),
    "shanmuga90": ("Shanmugasundaram ER et al. Gymnema sylvestre leaf extract in IDDM: insulin requirements fell. J Ethnopharmacol 1990", PM % "2259216", "peer_review"),
    "aslam79": ("Aslam M, Stockley IH. Interaction between curry ingredient (karela) and drug (chlorpropamide). Lancet 1979", PM % "85186", "peer_review"),
    "tongia04": ("Tongia A et al. Momordica charantia fruit and its hypoglycemic potentiation of oral hypoglycemic drugs in NIDDM. Indian J Physiol Pharmacol 2004", PM % "15521566", "peer_review"),
    "yin08": ("Yin J et al. Efficacy of berberine in patients with type 2 diabetes mellitus. Metabolism 2008", PM % "18442638", "peer_review"),
    "thikekar22": ("Thikekar AK et al. Effect of herbal formulation (Diabecon) on glimepiride pharmacokinetics and pharmacodynamics in diabetic rats. J Ayurveda Integr Med 2022", PM % "36174302", "peer_review"),
    "rayala24": ("Rayala VVSPK et al. Evaluation of pharmacokinetic herb-drug interaction of Diabecon and losartan (rats). J Chromatogr B 2024", PM % "39126994", "peer_review"),
    "gupta18bgr": ("Gupta BP et al. Preliminary clinical assessment and non-toxicity evaluation of BGR-34 in NIDDM (manufacturer-affiliated authors). J Tradit Complement Med 2018", PM % "30302331", "peer_review"),
    "stohs14": ("Stohs SJ. Safety and efficacy of shilajit (mumie, moomiyo). Phytother Res 2014", PM % "23733436", "peer_review"),
    # Hing / churnas
    "kelly84": ("Kelly KJ et al. Methemoglobinemia in an infant treated with the folk remedy glycerited asafoetida. Pediatrics 1984", PM % "6609339", "peer_review"),
    "mahendra12": ("Mahendra P, Bisht S. Ferula asafoetida: traditional uses and pharmacological activity (anticoagulant/hypotensive in animals; may enhance warfarin). Pharmacogn Rev 2012", PM % "23055640", "peer_review"),
    "makhija12": ("Makhija IK et al. Physico-chemical standardization of Sitopaladi churna. Anc Sci Life 2012", PM % "23284216", "peer_review"),
    "ijapr_talisadi": ("Talisadi churna classical composition incl. sugar 32 parts. Int J Ayurveda Pharma Res", "https://ijapr.in/index.php/ijapr/article/download/1235/979", "other"),
    "avipattikar_rev": ("Critical analysis of formulation and probable mode of action of Avipattikara churna: a comprehensive review (about 50% sugar, 33% trivrit)", "https://www.researchgate.net/publication/359426750_Critical_Analysis_of_Formulation_andProbable_Mode_of_Action_of_Avipattikara_churna_A_Comprehensive_Review", "other"),
    "mahasudarshan": ("Kaur P et al. Validation and quantification of major biomarkers in Mahasudarshan Churna (Swertia chirata ~50% plus ~49 ingredients). BMC Complement Med Ther 2020", PM % "32527318", "peer_review"),
    # Regulatory - Patanjali / Coronil
    "pib_coronil": ("Ministry of AYUSH (PIB, 23 Jun 2020). Statement on claims of Patanjali Ayurved regarding treatment of COVID-19 - asked to stop advertising claims pending examination", "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1633690", "gov"),
    "who_coronil": ("Fact Crescendo (Feb 2021). WHO South-East Asia clarified it has not reviewed or certified any traditional medicine for COVID-19", "https://english.factcrescendo.com/2021/02/24/has-the-who-certified-coronil-as-a-medicinal-treatment-for-covid-19/", "other"),
    "delhihc24": ("LiveLaw (29 Jul 2024). Delhi High Court orders removal of social-media statements promoting Coronil as a COVID-19 cure", "https://www.livelaw.in/high-court/delhi-high-court/delhi-high-court-ramdev-social-media-claims-coronil-covid-allopathy-causing-deaths-264898", "other"),
    "madrashc20": ("The IP Press (Aug 2020). Madras High Court proceedings on use of the 'Coronil' trademark", "https://www.theippress.com/2020/08/20/madras-high-court-stays-single-bench-order-retraining-patanjali-from-using-term-coronil/", "other"),
    "uk_suspend": ("LiveLaw (Apr 2024). Uttarakhand licensing authority suspends licences of 14 Patanjali/Divya Pharmacy products (incl. Madhugrit, Madhunashini Vati Extra Power)", "https://www.livelaw.in/top-stories/after-supreme-court-rap-uttarakhand-authority-suspends-licenses-of-14-patanjali-divya-pharmacy-products-256487", "other"),
    "uk_revoke": ("Business Standard (Jul 2024). Supreme Court asks Uttarakhand to decide on suspension of 14 Patanjali products after suspension order was cancelled on 1 July", "https://www.business-standard.com/companies/news/sc-asks-uttarakhand-govt-to-decide-on-suspension-of-14-patanjali-products-124073100496_1.html", "other"),
    "sc_contempt": ("SCC Online (13 Aug 2024). Supreme Court closes contempt proceedings in the Patanjali misleading-advertisements case (IMA v Union of India)", "https://www.scconline.com/blog/post/2024/08/13/patanjali-misleading-adscase-supreme-court-drops-contempt-of-court-charges-against-baba-ramdev-acharya-balkrishna/", "other"),
    # Brand/composition pages (ingredients only)
    "br_madhugrit": ("Patanjali Ayurved product page - Divya Madhugrit (ingredient list)", "https://www.patanjaliayurved.net/product/ayurvedic-medicine/vati/divya-madhugrit-tablet-60-n/3436", "other"),
    "br_madhunashini": ("Patanjali Ayurved product page - Divya Madhunashini Vati Extra Power (composition)", "https://www.patanjaliayurved.net/product/ayurvedic-medicine/vati/divya-madhunashini-vati-extra-power/95", "other"),
    "br_coronil": ("Patanjali Ayurved product page - Divya Coronil tablet (composition)", "https://www.patanjaliayurved.net/product/ayurvedic-medicine/vati/coronil-tablet-80-tab/3263", "other"),
    "br_diabecon": ("Himalaya Wellness product page - Diabecon", "https://himalayawellness.in/products/diabecon", "other"),
    "br_bgr34": ("AIMIL Pharmaceuticals - BGR-34 composition", "https://www.aimilpharma.life/pages/bgr-34-composition-for-diabetes", "other"),
}


def src(*keys):
    # Brand pages may only support ingredient lists (see notes), never interactions or safety flags.
    out = []
    for k in keys:
        if k.startswith("br_"):
            continue
        t, u, ty = S[k]
        out.append({"title": t, "url": u, "type": ty})
    return out


def ix(dc, sev, effect, mech, ev, srcs, advice=DEFAULT_ADVICE):
    return {"drug_class": dc, "severity": sev, "effect": effect, "mechanism": mech,
            "evidence": ev, "advice": advice, "sources": src(*srcs)}


def flag(f, note, ev, srcs):
    return {"flag": f, "note": note, "evidence": ev, "sources": src(*srcs)}


GLUC_ADVICE = ("Talk to your doctor or pharmacist before combining; check your blood sugar more often "
               "and know the signs of low blood sugar.")


def gluc(mech, ev, srcs, sev_ins="moderate", sev_su="moderate", sev_other="minor",
         effect="may add to the blood-sugar-lowering effect of diabetes medicines and raise the risk of low blood sugar"):
    return [
        ix("antidiabetic_insulin", sev_ins, effect, mech, ev, srcs, GLUC_ADVICE),
        ix("antidiabetic_sulfonylurea", sev_su, effect, mech, ev, srcs, GLUC_ADVICE),
        ix("antidiabetic_other", sev_other, effect.replace("raise the risk of low blood sugar",
           "raise the risk of low blood sugar, especially with other glucose-lowering medicines"), mech, ev, srcs, GLUC_ADVICE),
    ]


def sugar_raise(mech, srcs, sev="minor"):
    eff = "contains a large amount of sugar, which may raise blood sugar and work against diabetes medicines"
    adv = "Talk to your doctor or pharmacist before using regularly; check your blood sugar if you have diabetes."
    return [ix(dc, sev, eff, mech, "theoretical", srcs, adv)
            for dc in ("antidiabetic_insulin", "antidiabetic_sulfonylurea", "antidiabetic_other")]


def alcohol(prefix, srcs_extra=(), strong=True):
    s = ("niaaa",) + tuple(srcs_extra)
    sev_major = "major" if strong else "moderate"
    sev_mod = "moderate" if strong else "minor"
    m = prefix + "self-generated alcohol (ethanol)"
    return [
        ix("antibiotic_other", sev_major,
           "alcohol with metronidazole or tinidazole may cause flushing, vomiting, fast heartbeat and blood-pressure changes",
           m + "; disulfiram-like reaction with nitroimidazole antibiotics", "clinical", s,
           "Avoid alcohol-containing products while taking metronidazole/tinidazole unless your doctor says otherwise; talk to your doctor or pharmacist."),
        ix("sedative_hypnotic", sev_mod, "may increase drowsiness, dizziness and slowed breathing",
           m + "; additive central nervous system depression", "clinical", s),
        ix("opioid", sev_mod, "may increase drowsiness and the risk of slowed breathing or overdose",
           m + "; additive central nervous system depression", "clinical", s),
        ix("antiepileptic", "minor", "may increase drowsiness and dizziness with seizure medicines",
           m + "; additive sedation", "clinical", s),
        ix("antidiabetic_insulin", sev_mod, "alcohol may cause low blood sugar with insulin",
           m + "; alcohol impairs liver glucose output", "clinical", s, GLUC_ADVICE),
        ix("antidiabetic_sulfonylurea", sev_mod, "alcohol may cause low blood sugar or a flushing reaction with some sulfonylureas",
           m + "; alcohol impairs liver glucose output", "clinical", s, GLUC_ADVICE),
    ]


def alcohol_flag(note_extra, srcs):
    return flag("other", "Contains self-generated alcohol from fermentation (arishta/asava). Tested commercial arishtas "
                "contained roughly 5-13% v/v ethanol; levels vary by brand and batch. " + note_extra +
                " People who must avoid alcohol should ask a doctor or pharmacist.", "clinical", ("niaaa",) + tuple(srcs))


def piperine(via, sev="minor", ev="clinical"):
    m = "via ingredient %s (piperine): " % via
    return [
        ix("antiepileptic", sev, "may raise blood levels of phenytoin",
           m + "increased phenytoin AUC and Cmax in patients with epilepsy", ev, ("pattanaik06",)),
        ix("theophylline", sev, "may raise blood levels of theophylline",
           m + "increased oral bioavailability of theophylline in healthy volunteers", ev, ("bano91",)),
        ix("cyp3a4_substrate_narrow", sev, "may raise levels of some medicines broken down by CYP3A4 (e.g. ciclosporin, tacrolimus)",
           m + "CYP3A4 inhibition in human liver microsomes", "preclinical", ("bhardwaj02",)),
        ix("pgp_substrate", sev, "may raise levels of P-glycoprotein substrates such as digoxin",
           m + "P-glycoprotein inhibition in Caco-2 cells", "preclinical", ("bhardwaj02",)),
    ]


def guggul(via="guggulu (Commiphora wightii)", sev="moderate"):
    m = "via ingredient %s: " % via
    return [
        ix("antihypertensive", sev, "may lower the effect of propranolol and diltiazem",
           m + "single-dose study in healthy volunteers showed reduced Cmax and AUC of propranolol and diltiazem", "clinical", ("dalvi94",),
           "Talk to your doctor or pharmacist before combining; your blood pressure or heart rate may need checking."),
        ix("cyp3a4_substrate_narrow", sev, "may change levels of medicines broken down by CYP3A4",
           m + "guggulsterone activates PXR and induces CYP3A in hepatocytes (lab studies)", "preclinical", ("brobst04", "mskcc_guggul")),
        ix("hormonal_contraceptive_estrogen", "minor", "theoretical interference with hormonal medicines",
           m + "guggulsterone activated estrogen and progesterone receptors in vitro (theoretical)", "theoretical", ("brobst04",)),
    ]


def iron(via, sev="moderate", ev="clinical"):
    m = "via ingredient %s (iron oxide): " % via
    sp = "Talk to your doctor or pharmacist before combining; they may advise spacing doses (often at least 4 hours from levothyroxine)."
    return [
        ix("thyroid_hormone", sev, "may reduce absorption of levothyroxine",
           m + "iron binds levothyroxine in the gut", ev, ("ods_iron",), sp),
        ix("antibiotic_chelating", sev, "may reduce absorption of fluoroquinolone and tetracycline antibiotics",
           m + "polyvalent cations chelate these antibiotics", ev, ("eljaaly21",),
           "Talk to your doctor or pharmacist; antibiotic and mineral doses usually need to be taken hours apart."),
        ix("antiparkinson_levodopa", sev, "may reduce absorption and effect of levodopa",
           m + "iron may chelate levodopa in the gut; levodopa labels warn about iron-containing supplements", ev, ("ods_iron",),
           "Talk to your doctor or pharmacist before combining; doses may need to be spaced apart."),
        ix("ppi_antacid", "minor", "acid-reducing medicines may reduce iron absorption from the product",
           m + "gastric acid is needed for non-heme iron absorption", ev, ("ods_iron",)),
    ]


def calcium(via, sev="moderate", ev="clinical"):
    m = "via ingredient %s (calcium carbonate/oxide/sulphate): " % via
    return [
        ix("thyroid_hormone", sev, "may reduce absorption of levothyroxine",
           m + "calcium binds levothyroxine in the gut", ev, ("ods_ca",),
           "Talk to your doctor or pharmacist; levothyroxine is usually taken at least 4 hours apart from calcium."),
        ix("antibiotic_chelating", sev, "may reduce absorption of fluoroquinolone and tetracycline antibiotics",
           m + "calcium chelates these antibiotics", ev, ("ods_ca", "eljaaly21"),
           "Talk to your doctor or pharmacist; take the antibiotic at least 2 hours before or after calcium."),
        ix("lithium", "minor", "may add to the risk of high calcium levels with long-term lithium",
           m + "lithium can cause hypercalcaemia; extra calcium may add to it", "theoretical", ("ods_ca",)),
    ]


HM_SRC = ("saper04", "saper08", "mmwr04", "fda25")


def hm_flag(note, extra=(), ev="regulatory"):
    return flag("heavy_metals", note, ev, HM_SRC + tuple(extra))


def preg_hm(extra=()):
    return flag("pregnancy", "Avoid in pregnancy and breastfeeding unless a doctor advises otherwise: lead poisoning, including "
                "miscarriage, was reported in pregnant women using rasa shastra (metal-containing) Ayurvedic medicines.",
                "case_reports", ("mmwr12",) + tuple(extra))


def child_hm(extra=()):
    return flag("children", "Keep away from children; severe lead and mercury poisoning has been reported in children given "
                "Ayurvedic herbo-mineral remedies.", "case_reports", ("rasakarpura25", "cericola25") + tuple(extra))


def rec(id_, en, hi, sa, other, kind, products, ctx, srctype, safety, inter, dq):
    return {"id": id_, "names": {"common_en": en, "hindi": hi, "sanskrit": sa, "latin": "", "other": other},
            "kind": kind, "common_products": products, "traditional_context": ctx,
            "traditional_source_type": srctype, "general_safety": safety, "interactions": inter,
            "data_quality": dq, "last_checked": LC}


R = []

# 1 Chyawanprash
R.append(rec("chyawanprash", "Chyawanprash", "च्यवनप्राश", "Chyavanaprasha",
    ["ingredients: amla (Phyllanthus emblica) as base", "sugar / jaggery", "honey", "ghee", "sesame oil",
     "about 40-50 herbs incl. pippali (Piper longum), ashwagandha, guduchi, dashmool roots, cardamom, cinnamon"],
    "formulation", ["Dabur Chyawanprash", "Patanjali Chyawanprash", "Baidyanath Chyawanprash", "Sugar-free Chyawanprash variants"],
    "A jam-like amla-based preparation traditionally used in Ayurveda for general wellbeing of the respiratory and immune systems.",
    "classical text",
    [flag("other", "High sugar content: Chyawanprash is a cooked mixture of sugar, honey, ghee and amla, and is generally considered "
          "unsuitable for people who need to limit sugar; sugar-free variants exist. One review notes small studies reporting "
          "no rise in post-meal glucose, so evidence is mixed.", "theoretical", ("sharma19cp",)),
     hm_flag("Classical Chyawanprash is mainly herbal, but some premium variants are sold with added metal bhasmas (check the label); heavy metals have been found in a "
             "share of Ayurvedic products sold in the US. Choose tested products.", ev="regulatory")],
    sugar_raise("sugar, honey and jaggery base (product unstudied for this interaction)", ("sharma19cp",))
    + [ix("antiplatelet", "minor", "may slightly add to bleeding risk with antiplatelet medicines",
          "via ingredient amla: amla extract inhibited platelet aggregation in a small clinical study; amount in Chyawanprash differs",
          "clinical", ("fatima14",)),
       ix("anticoagulant_vka", "minor", "may slightly add to bleeding risk with warfarin",
          "via ingredient amla: antiplatelet effect (theoretical additive effect with anticoagulants)", "theoretical", ("fatima14",))],
    "limited"))

# 2 Triphala
R.append(rec("triphala_churna", "Triphala churna", "त्रिफला चूर्ण", "Triphala",
    ["ingredients: amalaki / amla (Phyllanthus emblica)", "haritaki (Terminalia chebula)", "bibhitaki (Terminalia bellirica)"],
    "formulation", ["Triphala churna", "Triphala tablets", "Triphala guggulu (also contains guggul)"],
    "A three-fruit powder traditionally used in Ayurveda for general wellbeing of the digestive system.",
    "classical text",
    [flag("other", "Has a laxative effect in traditional use and studies; may cause loose stools.", "clinical", ("peterson17",))],
    [ix("cyp3a4_substrate_narrow", "moderate", "may raise levels of medicines broken down by CYP3A4 (e.g. midazolam, tacrolimus)",
        "product studied: Triphala inhibited CYP3A4 in human liver microsomes and increased midazolam exposure in rats", "preclinical",
        ("nontakham22", "ponnusankar11")),
     ix("cyp1a2_substrate", "minor", "may raise levels of CYP1A2 substrates (e.g. theophylline, clozapine)",
        "product studied: Triphala inhibited CYP1A2 in vitro and increased phenacetin exposure in rats", "preclinical", ("nontakham22",)),
     ix("cyp2c9_substrate", "minor", "may raise levels of CYP2C9 substrates (e.g. warfarin, some sulfonylureas)",
        "product studied: CYP2C9 inhibition in human liver microsomes only", "preclinical", ("nontakham22", "ponnusankar11")),
     ix("laxative_stimulant", "minor", "may add to laxative effect and cause diarrhoea",
        "via ingredients haritaki and amla: traditional and studied laxative action", "clinical", ("peterson17",)),
     ix("antiplatelet", "minor", "may slightly add to bleeding risk with antiplatelet medicines",
        "via ingredient amla: antiplatelet effect in a small clinical study", "clinical", ("fatima14",))],
    "limited"))

# 3 Dashmool
R.append(rec("dashmool", "Dashmool (ten roots)", "दशमूल", "Dashamoola",
    ["ingredients: bilva (Aegle marmelos)", "agnimantha (Premna sp.)", "shyonaka (Oroxylum indicum)", "patala (Stereospermum suaveolens)",
     "gambhari (Gmelina arborea)", "shalaparni (Desmodium gangeticum)", "prishniparni (Uraria picta)", "brihati (Solanum indicum)",
     "kantakari (Solanum xanthocarpum)", "gokshura (Tribulus terrestris)"],
    "formulation", ["Dashmool kwath / churna", "Dashmool taila (oil)", "Dashmularishta (alcohol-containing)"],
    "A ten-root combination traditionally used in Ayurveda for general wellbeing of the musculoskeletal and nervous systems.",
    "classical text", [], [], "poor"))

# 4 Trikatu
R.append(rec("trikatu", "Trikatu", "त्रिकटु", "Trikatu",
    ["ingredients: black pepper / maricha (Piper nigrum)", "long pepper / pippali (Piper longum)", "dry ginger / shunthi (Zingiber officinale)",
     "active marker: piperine"],
    "formulation", ["Trikatu churna", "Trikatu capsules"],
    "A three-pungent-spice blend traditionally used in Ayurveda for general wellbeing of the digestive system.",
    "classical text", [],
    [ix("antitubercular", "moderate", "may slow absorption and lower peak levels of rifampicin",
        "product studied: Trikatu reduced rifampicin Cmax in rabbits", "preclinical", ("karan99",),
        "Talk to your doctor or pharmacist before combining with TB medicines."),
     ix("nsaid", "minor", "may lower blood levels of diclofenac",
        "product studied: Trikatu pretreatment decreased diclofenac serum levels in animals", "preclinical", ("lala04",))]
    + piperine("black pepper and long pepper", sev="moderate"),
    "limited"))

# 5 Sitopaladi
R.append(rec("sitopaladi_churna", "Sitopaladi churna", "सितोपलादि चूर्ण", "Sitopaladi churna",
    ["ingredients: sitopala (rock sugar) 16 parts", "vamshalochana (bamboo silica) 8 parts", "pippali (Piper longum) 4 parts",
     "ela / cardamom 2 parts", "tvak / cinnamon 1 part"],
    "formulation", ["Dabur Sitopaladi churna", "Baidyanath Sitopaladi churna", "Patanjali Divya Sitopaladi churna"],
    "A sweet powder traditionally used in Ayurveda for general wellbeing of the respiratory system.",
    "classical text",
    [flag("other", "About half of the powder by weight is sugar (sitopala); people limiting sugar should ask a doctor.", "theoretical", ("makhija12",))],
    sugar_raise("rock sugar is the main ingredient (product unstudied)", ("makhija12",))
    + piperine("pippali (long pepper)", sev="minor")[:2],
    "limited"))

# 6 Talisadi
R.append(rec("talisadi_churna", "Talisadi churna", "तालीसादि चूर्ण", "Talisadi churna",
    ["ingredients: talisa patra (Abies webbiana)", "pippali (Piper longum)", "maricha / black pepper (Piper nigrum)", "shunthi / dry ginger",
     "tvak / cinnamon", "ela / cardamom", "vamshalochana", "sugar (largest share, 32 parts)"],
    "formulation", ["Baidyanath Talisadi churna", "Dabur Talisadi churna", "Talisadi vati"],
    "A spice-and-sugar powder traditionally used in Ayurveda for general wellbeing of the respiratory and digestive systems.",
    "classical text",
    [flag("other", "Sugar is the main ingredient by weight in the classical recipe; people limiting sugar should ask a doctor.", "theoretical", ("ijapr_talisadi",))],
    sugar_raise("sugar is the main ingredient (product unstudied)", ("ijapr_talisadi",))
    + piperine("black pepper and long pepper", sev="minor")[:2],
    "limited"))

# 7 Avipattikar
R.append(rec("avipattikar_churna", "Avipattikar churna", "अविपत्तिकर चूर्ण", "Avipattikara churna",
    ["ingredients: trivrit (Operculina turpethum, about one third)", "sugar (about half)", "trikatu (ginger, black pepper, long pepper)",
     "triphala (amla, haritaki, bibhitaki)", "musta", "vidanga", "ela", "tejpatra", "lavanga (clove)", "vida lavana (salt)"],
    "formulation", ["Baidyanath Avipattikar churna", "Dabur Avipattikar churna", "Patanjali Divya Avipattikar churna", "Avipattikar tablets"],
    "A digestive powder traditionally used in Ayurveda for general wellbeing of the digestive system.",
    "classical text",
    [flag("other", "Roughly half sugar by weight; also contains trivrit, traditionally used as a purgative, so it may cause loose stools.",
          "theoretical", ("avipattikar_rev",))],
    [ix("laxative_stimulant", "minor", "may add to laxative effect and cause diarrhoea",
        "via ingredients trivrit (traditional purgative) and triphala (laxative); product unstudied", "theoretical", ("avipattikar_rev", "peterson17")),
     ix("diuretic_loop_thiazide", "minor", "frequent loose stools could add to potassium loss with water pills",
        "via laxative ingredients; theoretical electrolyte loss", "theoretical", ("peterson17",))]
    + sugar_raise("sugar is about half the formula (product unstudied)", ("avipattikar_rev",)),
    "poor"))

# 8 Hingvashtak
R.append(rec("hingvashtak_churna", "Hingvashtak churna", "हिंग्वाष्टक चूर्ण", "Hingvashtaka churna",
    ["ingredients: hing / asafoetida (Ferula assa-foetida)", "shunthi / dry ginger", "maricha / black pepper", "pippali / long pepper",
     "ajmoda", "jeera (white cumin)", "krishna jeera (black cumin)", "saindhava lavana (rock salt)"],
    "formulation", ["Baidyanath Hingvashtak churna", "Dabur Hingwashtak churna", "Zandu Hingvashtak churna"],
    "A spice-and-salt powder traditionally used in Ayurveda for general wellbeing of the digestive system.",
    "classical text",
    [flag("children", "Not for infants: asafoetida caused methemoglobinaemia (a serious blood oxygen problem) in a 5-week-old infant.",
          "case_reports", ("kelly84", "mahendra12")),
     flag("pregnancy", "Asafoetida has traditional abortifacient use and anti-fertility effects in rats; ask a doctor before use in pregnancy.",
          "preclinical", ("mahendra12",))],
    [ix("anticoagulant_vka", "minor", "may increase the effect of warfarin",
        "via ingredient hing (asafoetida): anticoagulant activity in animals and coumarin constituents; review notes it may enhance warfarin",
        "preclinical", ("mahendra12",)),
     ix("antihypertensive", "minor", "may add to blood-pressure lowering",
        "via ingredient hing: lowered blood pressure in animal studies", "preclinical", ("mahendra12",))]
    + piperine("black pepper and long pepper", sev="minor")[:2],
    "poor"))

# 9 Mahasudarshan
R.append(rec("mahasudarshan_churna", "Mahasudarshan churna", "महासुदर्शन चूर्ण", "Mahasudarshana churna",
    ["ingredients: chirata / kiratatikta (Swertia chirata, about 50%)", "about 49 other herbs incl. guduchi / giloy (Tinospora cordifolia)",
     "kutki (Picrorhiza kurroa)", "triphala", "haridra", "daruharidra", "trikatu", "neem"],
    "formulation", ["Baidyanath Mahasudarshan churna", "Dabur Mahasudarshan kadha / churna", "Mahasudarshan ghan vati"],
    "A bitter multi-herb powder traditionally used in Ayurveda for general wellbeing of the digestive system and seasonal resilience.",
    "classical text",
    [flag("liver", "Contains guduchi (giloy); a multicentre Indian study linked giloy products to liver injury, a finding disputed by the "
          "Ministry of AYUSH. Ask a doctor if you have liver disease.", "case_reports", ("kulkarni22", "pib_giloy"))],
    gluc("via ingredients guduchi (blood glucose lowering in animals) and other bitter herbs; product unstudied", "preclinical",
         ("wadood92", "mahasudarshan"), sev_ins="minor", sev_su="minor", sev_other="minor"),
    "poor"))

# 10 Ashwagandharishta
R.append(rec("ashwagandharishta", "Ashwagandharishta", "अश्वगंधारिष्ट", "Ashvagandharishta",
    ["ingredients: ashwagandha (Withania somnifera, main herb)", "safed musli", "manjistha", "haritaki", "haridra", "daruharidra",
     "yashtimadhu / licorice", "arjuna", "vacha", "chitrak", "dhataki flowers (ferment starter)", "jaggery / honey",
     "class: arishta (self-fermented, alcohol-containing)"],
    "formulation", ["Dabur Ashwagandharishta", "Baidyanath Ashwagandharishta", "Patanjali Divya Ashwagandharishta"],
    "A fermented herbal tonic traditionally used in Ayurveda for general wellbeing of the nervous system.",
    "classical text",
    [alcohol_flag("Ashwagandharishta brands measured 5.2-8.2% (one study) and 5.8-8.4% (another).", ("weerasooriya06", "fernando20")),
     flag("liver", "Contains ashwagandha; NIH LiverTox lists ashwagandha as a probable cause of clinically apparent liver injury.",
          "case_reports", ("livertox_ashwa", "bjornsson20")),
     flag("thyroid", "Ashwagandha raised thyroid hormone levels in a clinical trial; people with thyroid conditions should ask a doctor.",
          "clinical", ("ods_ashwa", "sharma18"))]
    + [],
    alcohol("via ingredient: ", ("weerasooriya06",))
    + [ix("thyroid_hormone", "moderate", "may add to thyroid hormone effects",
          "via ingredient ashwagandha: raised T3/T4 and lowered TSH in a clinical trial", "clinical", ("ods_ashwa", "sharma18"),
          "Talk to your doctor before combining; thyroid levels may need checking."),
       ix("immunosuppressant", "moderate", "may reduce the effect of immune-suppressing medicines",
          "via ingredient ashwagandha: immune-stimulating activity (theoretical interaction noted by NIH ODS)", "theoretical", ("ods_ashwa",)),
       ix("cyp2d6_substrate", "minor", "may raise levels of CYP2D6 substrates",
          "related formulation (Ridayarishta, made from Arjunarishta/Ashwagandharishta ingredients) inhibited CYP2D6 in vitro", "preclinical",
          ("pandit17",)),
       ix("cyp2c19_substrate", "minor", "may raise levels of CYP2C19 substrates (e.g. citalopram, omeprazole) or reduce activation of clopidogrel",
          "related formulation (Ridayarishta) inhibited CYP2C19 in vitro; this product itself unstudied", "preclinical", ("pandit17",))],
    "limited"))

# 11 Dashmularishta
R.append(rec("dashmularishta", "Dashmularishta", "दशमूलारिष्ट", "Dashamoolarishta",
    ["ingredients: dashmool (ten roots)", "chitrak", "lodhra", "guduchi", "amla", "haritaki", "manjistha", "draksha (raisins)",
     "jaggery and honey", "dhataki flowers", "class: arishta (self-fermented, alcohol-containing)"],
    "formulation", ["Dabur Dashmularishta", "Baidyanath Dashmularishta", "Patanjali Divya Dashmularishta"],
    "A fermented root-based tonic traditionally used in Ayurveda for general wellbeing after childbirth and of the musculoskeletal system.",
    "classical text",
    [alcohol_flag("Dashamoolarishta samples tested in Sri Lanka measured about 5.8-8.4% v/v.", ("fernando20",)),
     flag("other", "Made with jaggery and honey; contains sugars.", "theoretical", ("fernando20",))],
    alcohol("via ingredient: ", ("fernando20",)),
    "poor"))

# 12 Arjunarishta
R.append(rec("arjunarishta", "Arjunarishta", "अर्जुनारिष्ट", "Arjunarishta / Parthadyarishta",
    ["ingredients: arjuna bark (Terminalia arjuna)", "draksha (raisins)", "madhuka flowers", "dhataki flowers", "jaggery",
     "class: arishta (self-fermented, alcohol-containing)"],
    "formulation", ["Dabur Arjunarishta", "Baidyanath Arjunarishta", "Patanjali Divya Arjunarishta"],
    "A fermented arjuna-bark tonic traditionally used in Ayurveda for general wellbeing of the heart and circulatory system.",
    "classical text",
    [alcohol_flag("Self-generated ethanol in tested arishtas was about 5-13% v/v.", ("weerasooriya06",))],
    alcohol("via ingredient: ", ("weerasooriya06",))
    + [ix("cyp3a4_substrate_narrow", "moderate", "may raise levels of medicines broken down by CYP3A4",
          "via ingredient arjuna: extracts inhibited CYP3A4, CYP2D6 and CYP2C9 in human liver microsomes", "preclinical", ("varghese15",)),
       ix("cyp2d6_substrate", "minor", "may raise levels of CYP2D6 substrates (e.g. metoprolol)",
          "via ingredient arjuna (in vitro) and a related arishta formulation (CYP2D6 inhibition in vitro)", "preclinical", ("varghese15", "pandit17")),
       ix("cyp2c9_substrate", "minor", "may raise levels of CYP2C9 substrates (e.g. warfarin)",
          "via ingredient arjuna: CYP2C9 inhibition in human liver microsomes", "preclinical", ("varghese15",)),
       ix("cyp2c19_substrate", "minor", "may raise levels of CYP2C19 substrates (e.g. citalopram, omeprazole) or reduce activation of clopidogrel",
          "related formulation (Ridayarishta, made from Arjunarishta/Ashwagandharishta ingredients) inhibited CYP2C19 in vitro", "preclinical", ("pandit17",)),
       ix("antihypertensive", "minor", "may add to blood-pressure lowering",
          "product studied: Arjunarishta lowered systolic blood pressure in high-fat-fed rats", "preclinical", ("shengule18",)),
       ix("antidiabetic_other", "minor", "may add to blood-sugar lowering",
          "product studied: Arjunarishta lowered fasting blood glucose in high-fat-fed rats", "preclinical", ("shengule18",), GLUC_ADVICE)],
    "limited"))

# 13 Kumaryasava
R.append(rec("kumaryasava", "Kumaryasava", "कुमार्यासव", "Kumaryasava",
    ["ingredients: kumari / aloe vera juice (Aloe barbadensis)", "jaggery", "honey", "dhataki flowers", "about 40-50 crude drugs",
     "some classical recipes include iron (loha) preparations - check label", "class: asava (self-fermented, alcohol-containing)"],
    "formulation", ["Baidyanath Kumaryasava", "Dabur Kumaryasava", "Kumaryasava No.1"],
    "A fermented aloe-based tonic traditionally used in Ayurveda for general wellbeing of the digestive and female reproductive systems.",
    "classical text",
    [alcohol_flag("Kumaryasava brands measured only 0.1-1.9% v/v in one gas-chromatography study, lower than other arishtas.", ("selvan15",))],
    alcohol("via ingredient: ", ("selvan15",), strong=False)
    + [ix("antidiabetic_other", "minor", "may affect blood sugar with diabetes medicines",
          "via ingredient aloe: NCCIH cautions that aloe with diabetes drugs can cause unwanted effects", "theoretical", ("nccih_diab",), GLUC_ADVICE),
       ix("cardiac_glycoside", "minor", "theoretical risk of low potassium with digoxin",
          "via ingredient aloe: aloe latex overuse can lower potassium and raise digoxin risk; Kumaryasava uses juice, not latex (theoretical)",
          "theoretical", ("nccih_aloe",))],
    "poor"))

# 14 Kaishore guggulu
R.append(rec("kaishore_guggulu", "Kaishore guggulu", "कैशोर गुग्गुलु", "Kaishora guggulu",
    ["ingredients: guggulu (Commiphora wightii resin)", "triphala (amla, haritaki, bibhitaki)", "guduchi / giloy (Tinospora cordifolia)",
     "trikatu (ginger, black pepper, long pepper)", "vidanga", "danti (Baliospermum montanum)", "trivrit (Operculina turpethum)"],
    "formulation", ["Baidyanath Kaishore guggulu", "Dabur Kaishore guggulu", "Patanjali Divya Kaishore guggulu"],
    "A guggul-based tablet traditionally used in Ayurveda for general wellbeing of the joints and skin.",
    "classical text",
    [flag("liver", "Contains guduchi (giloy); giloy products were linked to liver injury in an Indian multicentre study (disputed by the "
          "Ministry of AYUSH).", "case_reports", ("kulkarni22", "nagral21", "pib_giloy"))],
    guggul()
    + piperine("trikatu (black pepper, long pepper)", sev="minor")[:2]
    + [ix("laxative_stimulant", "minor", "may add to laxative effect",
          "via ingredients triphala, danti and trivrit (laxative/purgative herbs); product unstudied", "theoretical", ("peterson17",))],
    "limited"))

# 15 Yogaraj guggulu
R.append(rec("yogaraj_guggulu", "Yogaraj guggulu", "योगराज गुग्गुलु", "Yogaraja guggulu",
    ["ingredients: guggulu (Commiphora wightii resin)", "triphala", "trikatu", "chitrak (Plumbago zeylanica)", "pippalimool", "ajwain",
     "vidanga", "devdaru", "rasna", "gokshura", "jeera", "musta", "ela", "tvak"],
    "formulation", ["Baidyanath Yogaraj guggulu", "Dabur Yogaraj guggulu", "Patanjali Divya Yograj guggulu"],
    "A guggul-based multi-herb tablet traditionally used in Ayurveda for general wellbeing of the joints and musculoskeletal system.",
    "classical text",
    [hm_flag("Classical Yogaraj guggulu is herbal, but heavy metals have been found in a share of Ayurvedic products, and the related "
             "Mahayogaraj guggulu contains metal bhasmas. Do not confuse the two; choose tested products.")],
    guggul() + piperine("trikatu (black pepper, long pepper)", sev="minor")[:2],
    "limited"))

# 16 Mahayogaraj guggulu
R.append(rec("mahayogaraj_guggulu", "Mahayogaraj guggulu", "महायोगराज गुग्गुलु", "Mahayogaraja guggulu",
    ["ingredients: Yogaraj guggulu herbs plus guggulu", "vanga bhasma (tin)", "rajata bhasma (silver)", "naga bhasma (lead)",
     "loha bhasma (iron)", "abhraka bhasma (mica)", "mandura bhasma (iron oxide)", "rasa sindoor (mercuric sulphide)"],
    "mineral_preparation", ["Baidyanath Mahayogaraj guggulu", "Dabur Mahayograj guggulu", "Sri Sri Ayurveda Mahayogaraj guggulu"],
    "A guggul and metal-bhasma tablet traditionally used in Ayurveda for general wellbeing of the joints and musculoskeletal system.",
    "classical text",
    [hm_flag("Contains lead (naga bhasma) and mercury (rasa sindoor) by design. A Mahayogaraj guggulu sample linked to lead poisoning "
             "contained 4.9% lead (CDC, 2015); a CCRAS study found 25.8 µg/g lead, above the WHO limit.", ("mmwr15", "lavekar10")),
     preg_hm(), child_hm(),
     flag("kidney", "Lead and mercury can damage the kidneys; avoid with kidney disease unless a doctor advises otherwise.", "regulatory",
          ("fda25", "mmwr15"))],
    [ix("cyp3a4_substrate_narrow", "moderate", "may raise levels of medicines broken down by CYP3A4 (e.g. midazolam, tacrolimus, some statins)",
        "product studied: Mahayogaraj guggulu and guggulsterones inhibited CYP3A4 and increased midazolam exposure in rats", "preclinical",
        ("sabarathinam21",))]
    + guggul()[:1]
    + [ix("nephrotoxic", "moderate", "may add to kidney strain with kidney-toxic medicines",
          "via ingredients naga bhasma (lead) and rasa sindoor (mercury): heavy-metal kidney toxicity (theoretical additive effect)",
          "theoretical", ("mmwr15", "kamath12"))],
    "limited"))

# 17 Chandraprabha vati
R.append(rec("chandraprabha_vati", "Chandraprabha vati", "चन्द्रप्रभा वटी", "Chandraprabha vati",
    ["ingredients: shilajit (asphaltum)", "guggulu", "lauha bhasma (iron)", "makshika bhasma (copper-iron pyrite)", "sugar",
     "karpura", "vacha (Acorus calamus)", "musta", "guduchi", "triphala", "trikatu", "salts and kshara (alkalis)"],
    "mineral_preparation", ["Baidyanath Chandraprabha vati", "Dabur Chandraprabha vati", "Patanjali Divya Chandraprabha vati"],
    "A herbo-mineral tablet traditionally used in Ayurveda for general wellbeing of the urinary and reproductive systems.",
    "classical text",
    [hm_flag("Contains mineral bhasmas (iron, copper pyrite) and shilajit; heavy metals were detected in about 40% of rasa shastra "
             "products in a 2008 study. Choose tested products.", ("chandraprabha_np",)),
     flag("other", "Contains vacha (Acorus calamus); calamus is prohibited from use in human food in the US because of beta-asarone.",
          "regulatory", ("cfr_calamus",))],
    guggul()[:2] + iron("lauha bhasma", sev="minor", ev="theoretical")[:3]
    + gluc("via ingredients shilajit and guggulu; product unstudied (theoretical)", "theoretical", ("stohs14", "chandraprabha_np"),
           sev_ins="minor", sev_su="minor", sev_other="minor"),
    "limited"))

# 18 Arogyavardhini vati
R.append(rec("arogyavardhini_vati", "Arogyavardhini vati", "आरोग्यवर्धिनी वटी", "Arogyavardhini rasa / vati",
    ["ingredients: kajjali (purified mercury + sulphur; mercuric sulphide)", "tamra bhasma (copper)", "lauha bhasma (iron)",
     "abhraka bhasma (mica)", "shilajit", "guggulu", "triphala", "chitrak", "kutki (Picrorhiza kurroa, largest herbal share)", "neem leaf juice"],
    "mineral_preparation", ["Baidyanath Arogyavardhini bati", "Dabur Arogyavardhini bati", "Patanjali Divya Arogyavardhini vati"],
    "A herbo-mineral tablet traditionally used in Ayurveda for general wellbeing of the liver and digestive system.",
    "classical text",
    [hm_flag("Contains mercury (about 1.5-2.8% in analyses) and copper by design. In rats, Aarogyavardhini Vati led to mercury "
             "accumulation in the kidney.", ("jamadagni20", "kamath12")),
     preg_hm(), child_hm(),
     flag("kidney", "Mercury from this product accumulated in rat kidneys; avoid with kidney disease unless a doctor advises otherwise.",
          "preclinical", ("jamadagni20",))],
    [ix("nephrotoxic", "moderate", "may add to kidney strain with kidney-toxic medicines",
        "product studied: mercury accumulated in kidneys of treated rats; additive effect with nephrotoxic drugs is theoretical", "preclinical",
        ("jamadagni20", "kamath12"))]
    + guggul()[:1] + iron("lauha bhasma", sev="minor", ev="theoretical")[:3],
    "limited"))

# 19 Punarnavadi mandur
R.append(rec("punarnavadi_mandur", "Punarnavadi mandur", "पुनर्नवादि मण्डूर", "Punarnavadi mandura",
    ["ingredients: mandura bhasma (iron oxide; about 40 parts)", "punarnava (Boerhavia diffusa)", "trivrit", "trikatu", "triphala",
     "vidanga", "devdaru", "chitrak", "kushtha", "haridra", "daruharidra", "danti", "kutki", "musta", "processed in cow's urine (gomutra)"],
    "mineral_preparation", ["Baidyanath Punarnavadi mandur", "Dabur Punarnavadi mandoor", "Patanjali Divya Punarnavadi mandur"],
    "An iron-based herbo-mineral tablet traditionally used in Ayurveda for general wellbeing of the blood.",
    "classical text",
    [flag("children", "Iron-containing products are a classic cause of fatal accidental poisoning in toddlers; store out of reach of children.",
          "case_reports", ("mmwr_iron",)),
     hm_flag("Herbo-mineral (rasa shastra) product; heavy metals have been found in a share of such products. Choose tested products.",
             ("punarnavadi",))],
    iron("mandura bhasma", sev="moderate", ev="clinical"),
    "limited"))

# 20 Swarna bhasma
R.append(rec("swarna_bhasma", "Swarna bhasma (gold calx)", "स्वर्ण भस्म", "Suvarna / Swarna bhasma",
    ["ingredients: processed gold (gold micro- and nano-particles)", "found in 'swarna yukt' formulations, e.g. Swarna vasant malti, "
     "Brihat vata chintamani ras, Garbha chintamani ras (swarna yukt)"],
    "mineral_preparation", ["Baidyanath Swarna bhasma", "Dabur Swarna bhasma", "Swarna yukt (gold-containing) ras/vati products"],
    "A processed gold preparation traditionally used in Ayurveda as a rasayana for general wellbeing.",
    "classical text",
    [hm_flag("Gold bhasma itself showed little toxicity in rat studies, but gold-containing ('swarna yukt') multi-mineral products have been "
             "implicated in lead poisoning (e.g. a 'Swarna Yukt' product in the CDC NYC 2011-2012 cases); many contain mercury or lead too.",
             ("mmwr12", "biswas20")),
     preg_hm(), child_hm()],
    [], "poor"))

# 21 Lauha bhasma
R.append(rec("lauha_bhasma", "Lauha bhasma (iron calx)", "लौह भस्म", "Lauha / Loha bhasma",
    ["ingredients: processed iron (iron oxides, mainly Fe2O3/Fe3O4)", "also in Chandraprabha vati, Arogyavardhini vati, Navayas lauh, Kumaryasava (some recipes)"],
    "mineral_preparation", ["Baidyanath Lauh bhasma", "Dabur Lauh bhasma", "Navayas lauh", "Saptamrit lauh"],
    "A processed iron preparation traditionally used in Ayurveda for general wellbeing of the blood.",
    "classical text",
    [flag("children", "Iron-containing products are a classic cause of fatal accidental poisoning in toddlers; store out of reach of children.",
          "case_reports", ("mmwr_iron",)),
     hm_flag("Characterisation studies show iron oxides with trace contaminants; heavy metals have been found in a share of rasa shastra "
             "products. Choose tested products.", ("bhargava12",))],
    iron("lauha bhasma", sev="moderate", ev="clinical"),
    "limited"))

# 22 Abhrak bhasma
R.append(rec("abhrak_bhasma", "Abhrak bhasma (mica calx)", "अभ्रक भस्म", "Abhraka bhasma",
    ["ingredients: processed biotite mica (silicates of magnesium, aluminium, iron, potassium)", "Krishna vajra abhraka bhasma",
     "Abhrak bhasma sahasraputi / shataputi"],
    "mineral_preparation", ["Baidyanath Abhrak bhasma", "Dabur Abhrak bhasma", "Abhrak bhasma 100 puti / 1000 puti"],
    "A processed mica preparation traditionally used in Ayurveda as a rasayana for general wellbeing of the respiratory system.",
    "classical text",
    [hm_flag("Mineral (rasa shastra) preparation; heavy metals have been found in about 40% of rasa shastra products tested in 2008. "
             "Choose tested products.", ("abhrak_char",))],
    [ix("antibiotic_chelating", "minor", "may reduce absorption of fluoroquinolone and tetracycline antibiotics",
        "via mineral content (Mg, Al, Fe cations) shown in characterisation studies; chelation is theoretical for this product", "theoretical",
        ("abhrak_char", "eljaaly21"), "Talk to your doctor or pharmacist; antibiotic and mineral doses usually need to be taken hours apart.")]
    + gluc("product studied: Abhrak bhasma lowered blood glucose in rats", "preclinical", ("gopinath21",),
           sev_ins="minor", sev_su="minor", sev_other="minor"),
    "poor"))

# 23 Rasa sindoor
R.append(rec("rasa_sindoor", "Rasa sindoor (mercuric sulphide)", "रस सिन्दूर", "Rasasindura",
    ["ingredients: purified mercury (parada) and sulphur (gandhaka), heated by kupipakva method -> red mercuric sulphide (HgS)",
     "found in Brahmi vati, Mahayogaraj guggulu, Vatvidhwansan ras and many 'ras' products"],
    "mineral_preparation", ["Baidyanath Ras sindoor", "Dabur Rasa sindoor", "Products labelled 'ras' or 'rasa'"],
    "A processed mercury-sulphur preparation used in Ayurvedic rasa shastra as a component of herbo-mineral formulations.",
    "classical text",
    [hm_flag("Is a mercury compound by design. Mercury and lead have been detected at levels far above safety limits in rasa shastra "
             "products; a mercury-sulphide Ayurvedic remedy (Rasa Karpura) caused severe mercury poisoning in an infant.",
             ("kamath12", "rasakarpura25")),
     preg_hm(), child_hm(),
     flag("kidney", "Mercury is toxic to the kidneys; avoid with kidney disease.", "case_reports", ("kamath12", "rasakarpura25"))],
    [ix("nephrotoxic", "moderate", "may add to kidney damage risk with kidney-toxic medicines",
        "mercury content (mercuric sulphide); additive kidney toxicity is theoretical", "theoretical", ("kamath12",))],
    "limited"))

# 24 Calcium preparations
R.append(rec("calcium_bhasma_pishti", "Calcium bhasmas and pishtis (coral, pearl, conch, gypsum)", "प्रवाल पिष्टी / मुक्ता पिष्टी / शंख भस्म / गोदन्ती भस्म",
    "Pravala pishti, Mukta pishti, Shankha bhasma, Godanti bhasma",
    ["Praval pishti / praval bhasma (coral; calcium carbonate)", "Mukta pishti / mukta shukti bhasma (pearl; calcium carbonate)",
     "Shankh bhasma (conch shell; calcite, about 46% calcium)", "Godanti bhasma (gypsum; anhydrous calcium sulphate)",
     "Kapardika bhasma (cowrie)", "also in Praval panchamrit, Kamdudha ras, Septilin (shankha bhasma)"],
    "mineral_preparation", ["Baidyanath Praval pishti", "Dabur Shankh bhasma", "Patanjali Divya Mukta pishti", "Godanti bhasma"],
    "Calcium-rich shell and mineral preparations traditionally used in Ayurveda for general wellbeing of the digestive system and bones.",
    "classical text",
    [hm_flag("Mainly calcium salts (a conch-shell bhasma study found lead 0.78 ppm), but heavy metals have been found in a share of rasa "
             "shastra products. Choose tested products.", ("chavan18",))],
    calcium("calcium bhasma/pishti"),
    "limited"))

# 25 Brahmi vati
R.append(rec("brahmi_vati", "Brahmi vati", "ब्राह्मी वटी", "Brahmi vati",
    ["ingredients: brahmi (Bacopa monnieri)", "shankhpushpi (Convolvulus pluricaulis)", "vacha (Acorus calamus)", "jatamansi (Nardostachys jatamansi)",
     "swarna makshika bhasma (copper-iron pyrite)", "rasa sindoor (mercuric sulphide)", "some versions add swarna (gold) or mukta (pearl)"],
    "mineral_preparation", ["Baidyanath Brahmi vati (swarna yukt)", "Dhootapapeshwar Brahmi vati", "KLE Brahmi vati"],
    "A brahmi-based herbo-mineral tablet traditionally used in Ayurveda for general wellbeing of the nervous system and memory.",
    "classical text",
    [hm_flag("Classical Brahmi vati contains rasa sindoor (mercuric sulphide) and swarna makshika bhasma; check the label.",
             ("brahmivati_rct", "kamath12")),
     preg_hm(),
     flag("other", "Contains vacha (Acorus calamus); calamus is prohibited from use in human food in the US because of beta-asarone.",
          "regulatory", ("cfr_calamus",))],
    [ix("cyp3a4_substrate_narrow", "moderate", "may raise levels of medicines broken down by CYP3A4",
        "via ingredient brahmi: Bacopa extract inhibited CYP3A4 (competitive) in vitro", "preclinical", ("bacopa_cyp",)),
     ix("cyp2c9_substrate", "minor", "may raise levels of CYP2C9 substrates", "via ingredient brahmi: CYP2C9 inhibition in vitro", "preclinical", ("bacopa_cyp",)),
     ix("cyp1a2_substrate", "minor", "may raise levels of CYP1A2 substrates", "via ingredient brahmi: CYP1A2 inhibition in vitro", "preclinical", ("bacopa_cyp",)),
     ix("cyp2c19_substrate", "moderate", "may raise levels of CYP2C19 substrates (e.g. citalopram, omeprazole) or reduce activation of clopidogrel",
        "via ingredient brahmi: Bacopa extract inhibited CYP2C19 (non-competitive) in vitro, to under 10% activity at estimated gut concentrations",
        "preclinical", ("bacopa_cyp",)),
     ix("thyroid_hormone", "minor", "may add to thyroid hormone levels",
        "via ingredient brahmi: raised T4 in male mice", "preclinical", ("kar02",)),
     ix("antithyroid", "minor", "may work against antithyroid medicines",
        "via ingredient brahmi: raised T4 in male mice (theoretical)", "preclinical", ("kar02",))],
    "limited"))

# 26 Liv.52
R.append(rec("himalaya_liv52", "Himalaya Liv.52", "लिव 52", "",
    ["ingredients: himsra / caper bush (Capparis spinosa)", "kasani / chicory (Cichorium intybus)", "mandur bhasma (ferric oxide calx, about 33 mg/tablet)",
     "kakamachi / black nightshade (Solanum nigrum)", "arjuna (Terminalia arjuna)", "kasamarda (Cassia occidentalis)",
     "biranjasipha / yarrow (Achillea millefolium)", "jhavuka / tamarisk (Tamarix gallica)"],
    "formulation", ["Liv.52 tablets", "Liv.52 DS tablets", "Liv.52 syrup", "Liv.52 drops"],
    "A branded polyherbal product traditionally used in Ayurveda for general wellbeing of the liver and digestive system.",
    "brand literature",
    [flag("liver", "In a controlled trial in alcoholic liver disease, Liv.52 showed no benefit over placebo; an unpublished trial in alcoholic "
          "cirrhosis reported lower survival with Liv.52. People with liver disease should use it only under medical advice.",
          "clinical", ("desilva03", "liv52_review"))],
    iron("mandur bhasma", sev="minor", ev="theoretical")[:3]
    + [ix("cyp3a4_substrate_narrow", "minor", "theoretical change in levels of medicines broken down by CYP3A4",
          "via ingredient arjuna: CYP3A4 inhibition in human liver microsomes", "preclinical", ("varghese15", "liv52_dove"))],
    "poor"))

# 27 Septilin
R.append(rec("himalaya_septilin", "Himalaya Septilin", "सेप्टिलिन", "",
    ["ingredients: Maharasnadi quath", "guduchi / giloy (Tinospora cordifolia)", "manjistha (Rubia cordifolia)", "amla (Emblica officinalis)",
     "moringa (Moringa pterygosperma)", "yashtimadhu / licorice (Glycyrrhiza glabra)", "guggulu (Balsamodendron mukul)", "shankha bhasma (conch calcium)"],
    "formulation", ["Septilin tablets", "Septilin syrup"],
    "A branded herbo-mineral product traditionally used in Ayurveda for general wellbeing of the immune and respiratory systems.",
    "brand literature",
    [flag("liver", "Contains guduchi (giloy); giloy products were linked to liver injury in an Indian multicentre study (disputed by the "
          "Ministry of AYUSH).", "case_reports", ("kulkarni22", "pib_giloy")),
     flag("other", "Contains licorice; long-term use of glycyrrhizin can raise blood pressure and lower potassium.", "regulatory",
          ("nccih_licorice", "ema_licorice"))],
    [ix("corticosteroid", "minor", "may increase corticosteroid effects and potassium loss",
        "via ingredient licorice (glycyrrhizin): interaction with corticosteroids reported", "case_reports", ("nccih_licorice", "ema_licorice")),
     ix("diuretic_loop_thiazide", "minor", "may add to potassium loss with water pills",
        "via ingredient licorice: EMA monograph advises against use with diuretics because of electrolyte imbalance", "theoretical", ("ema_licorice",)),
     ix("cardiac_glycoside", "minor", "low potassium may increase digoxin side effects",
        "via ingredient licorice: EMA monograph advises against use with cardiac glycosides", "theoretical", ("ema_licorice",))]
    + guggul(sev="minor")[:1]
    + calcium("shankha bhasma", sev="minor", ev="theoretical")[:2]
    + [ix("immunosuppressant", "minor", "theoretical reduction in the effect of immune-suppressing medicines",
          "product studied as an immunomodulatory herbo-mineral formulation (animal data); interaction theoretical", "theoretical", ("septilin_sd",))],
    "poor"))

# 28 Cystone
R.append(rec("himalaya_cystone", "Himalaya Cystone", "सिस्टोन", "",
    ["ingredients: Didymocarpus pedicellata", "pashanbhed (Saxifraga ligulata / Bergenia)", "manjistha (Rubia cordifolia)", "nagarmotha (Cyperus scariosus)",
     "apamarga (Achyranthes aspera)", "gojihva (Onosma bracteatum)", "sahadevi (Vernonia cinerea)", "shilajit", "hajrul yahood bhasma (mineral)"],
    "formulation", ["Cystone tablets", "Cystone syrup"],
    "A branded herbo-mineral product traditionally used in Ayurveda for general wellbeing of the urinary system.",
    "brand literature",
    [flag("kidney", "In small randomised crossover and 1-year open-label studies (calcium oxalate and cystine stone formers), Cystone did not "
          "change urine chemistry or reduce stone burden. People with kidney stones or kidney disease should stay under medical care.",
          "clinical", ("erickson11b", "erickson11"))],
    [], "poor"))

# 29 Diabecon
R.append(rec("himalaya_diabecon", "Himalaya Diabecon", "डायबेकॉन", "",
    ["ingredients: meshashringi / gudmar (Gymnema sylvestre)", "vijaysar / Indian kino (Pterocarpus marsupium)", "shilajit",
     "karela (Momordica charantia)", "guggulu", "yashtimadhu", "gokshura", "bhumyamalaki (DS variant lists more herbs)"],
    "formulation", ["Diabecon tablets", "Diabecon DS tablets"],
    "A branded polyherbal product; recorded here only for blood-sugar interaction risk.",
    "brand literature",
    [flag("hypoglycaemia", "Contains several herbs that lower blood sugar; combining with diabetes medicines may cause low blood sugar.",
          "clinical", ("baskaran90", "shane09", "thikekar22"))],
    gluc("product studied: Diabecon with glimepiride gave additive glucose lowering in diabetic rats (no PK change); "
         "via ingredients gymnema (reduced need for diabetes drugs in clinical studies) and karela (case of interaction with chlorpropamide)",
         "clinical", ("thikekar22", "baskaran90", "shanmuga90", "aslam79", "shane09", "br_diabecon")),
    "limited"))

# 30 Madhunashini vati
R.append(rec("madhunashini_vati", "Madhunashini vati (Patanjali Divya Madhunashini Vati Extra Power)", "मधुनाशिनी वटी", "",
    ["ingredients: giloy (Tinospora cordifolia)", "karela (Momordica charantia)", "gudmar (Gymnema sylvestre)", "jamun seed (Syzygium cumini)",
     "shilajit", "methi (fenugreek)", "neem", "haldi", "ashwagandha", "bael leaf", "kutki", "chirata", "kuchla shuddh (Strychnos nux-vomica)",
     "praval pishti", "vang bhasma (tin)", "lauh bhasma (iron)"],
    "mineral_preparation", ["Patanjali Divya Madhunashini Vati Extra Power", "Madhunashini vati (other makers)"],
    "A branded herbo-mineral product; recorded here only for blood-sugar interaction risk and safety notes.",
    "brand literature",
    [flag("hypoglycaemia", "Contains several herbs that lower blood sugar; combining with diabetes medicines may cause low blood sugar.",
          "clinical", ("shane09", "baskaran90")),
     flag("heavy_metals", "Label lists vang (tin) and lauh (iron) bhasma, praval pishti and purified kuchla (nux vomica, a source of "
          "strychnine). FDA has warned about Ayurvedic products containing heavy metals and strychnine/brucine.", "regulatory",
          ("br_madhunashini", "fda25", "saper08")),
     flag("other", "Regulatory: in April 2024 the Uttarakhand State Licensing Authority suspended manufacturing licences of 14 Patanjali/Divya "
          "Pharmacy products including Madhunashini Vati Extra Power over advertising; the order was cancelled on 1 July 2024 and the "
          "Supreme Court asked the state to decide afresh.", "regulatory", ("uk_suspend", "uk_revoke", "sc_contempt"))],
    gluc("via ingredients gymnema, karela, fenugreek, jamun and giloy (blood-sugar-lowering herbs; gymnema reduced diabetes drug needs "
         "in clinical studies); product itself unstudied", "clinical", ("baskaran90", "aslam79", "shane09", "br_madhunashini")),
    "poor"))

# 31 Madhugrit
R.append(rec("patanjali_madhugrit", "Patanjali Divya Madhugrit", "मधुग्रिट", "",
    ["ingredients: Chandraprabha vati (contains lauha bhasma, shilajit, guggulu)", "shuddh shilajit", "giloy", "indrayan (Citrullus colocynthis)",
     "karela", "chirata", "shatavar", "ashwagandha"],
    "formulation", ["Divya Madhugrit tablets"],
    "A branded herbo-mineral product; recorded here only for blood-sugar interaction risk and regulatory notes.",
    "brand literature",
    [flag("hypoglycaemia", "Contains herbs that lower blood sugar; combining with diabetes medicines may cause low blood sugar.",
          "clinical", ("shane09", "ods_ashwa")),
     flag("other", "Regulatory: Madhugrit was among 14 Patanjali/Divya Pharmacy products whose manufacturing licences the Uttarakhand State "
          "Licensing Authority suspended in April 2024 over advertising; the order was cancelled on 1 July 2024 and the Supreme Court "
          "asked the state to decide afresh. Related Supreme Court contempt proceedings on misleading advertisements closed in Aug 2024.",
          "regulatory", ("uk_suspend", "uk_revoke", "sc_contempt"))],
    gluc("via ingredients karela (case of interaction with chlorpropamide; potentiation of oral hypoglycaemics), giloy (animal data) "
         "and ashwagandha (NIH ODS notes it may lower blood glucose); product unstudied", "clinical",
         ("aslam79", "tongia04", "ods_ashwa", "wadood92", "br_madhugrit")),
    "poor"))

# 32 BGR-34
R.append(rec("bgr_34", "BGR-34", "बीजीआर-34", "",
    ["ingredients: daruharidra (Berberis aristata; berberine)", "vijaysar (Pterocarpus marsupium)", "gudmar (Gymnema sylvestre)",
     "majeeth / manjistha (Rubia cordifolia)", "methi (fenugreek)", "giloy (Tinospora cordifolia)", "shilajit"],
    "formulation", ["AIMIL BGR-34 tablets"],
    "A branded polyherbal product developed with CSIR labs; recorded here only for blood-sugar interaction risk.",
    "brand literature",
    [flag("hypoglycaemia", "Contains berberine-rich daruharidra, gymnema and fenugreek, which lower blood sugar; combining with diabetes "
          "medicines may cause low blood sugar.", "clinical", ("yin08", "shane09", "gupta18bgr"))],
    gluc("via ingredients daruharidra (berberine lowered glucose similarly to metformin in a trial), gymnema and fenugreek; "
         "a manufacturer-affiliated trial also reported glucose lowering", "clinical",
         ("yin08", "baskaran90", "shane09", "gupta18bgr", "br_bgr34")),
    "limited"))

# 33 Coronil
R.append(rec("patanjali_coronil", "Patanjali Divya Coronil", "कोरोनिल", "",
    ["ingredients per tablet: giloy (Tinospora cordifolia) extract 300 mg", "ashwagandha (Withania somnifera) extract 250 mg",
     "tulsi (Ocimum sanctum) extract 50 mg", "sold in a kit with Divya Swasari vati and Anu taila"],
    "formulation", ["Divya Coronil tablets", "Divya Coronil kit"],
    "A branded herbal product; recorded here only for blood-sugar interaction risk and regulatory notes.",
    "brand literature",
    [flag("other", "Regulatory: on 23 June 2020 the Ministry of AYUSH asked Patanjali to stop advertising COVID-19 treatment claims pending "
          "examination; WHO South-East Asia stated in Feb 2021 it had not reviewed or certified any traditional medicine for COVID-19; "
          "in July 2024 the Delhi High Court ordered removal of social-media statements describing Coronil as a COVID-19 cure. "
          "A separate trademark dispute over the name was heard by the Madras High Court in 2020.",
          "regulatory", ("pib_coronil", "who_coronil", "delhihc24", "madrashc20")),
     flag("hypoglycaemia", "Giloy and ashwagandha may lower blood sugar; combining with diabetes medicines may cause low blood sugar.",
          "preclinical", ("ods_ashwa", "wadood92")),
     flag("liver", "Giloy (multicentre Indian case series, disputed by the Ministry of AYUSH) and ashwagandha (NIH LiverTox) have both been "
          "linked to liver injury.", "case_reports", ("kulkarni22", "pib_giloy", "livertox_ashwa"))],
    gluc("via ingredients ashwagandha (NIH ODS notes it may lower blood glucose) and giloy (lowered glucose in animals); product unstudied",
         "preclinical", ("ods_ashwa", "wadood92", "br_coronil"), sev_ins="minor", sev_su="minor", sev_other="minor"),
    "poor"))

# 34 Gandhak rasayan
R.append(rec("gandhak_rasayan", "Gandhak rasayan", "गंधक रसायन", "Gandhaka rasayana",
    ["ingredients: shuddha gandhaka (purified sulphur)", "processed with cow's milk", "chaturjata (cinnamon, cardamom, tejpatra, nagakesara)",
     "guduchi", "triphala", "bhringraj", "ginger juice"],
    "mineral_preparation", ["Baidyanath Gandhak rasayan", "Dabur Gandhak rasayan", "Dhootapapeshwar Gandhak rasayan"],
    "A purified-sulphur preparation traditionally used in Ayurveda for general wellbeing of the skin.",
    "classical text",
    [hm_flag("Sulphur-based rasa shastra product; a 180-day rat study found no toxicity at therapeutic doses, but heavy metals have been "
             "found in a share of rasa shastra products. Choose tested products.", ("gandhak_tox",))],
    [], "poor"))

# basic validation
allowed = set("""anticoagulant_vka anticoagulant_doac anticoagulant_heparin antiplatelet nsaid antidiabetic_insulin antidiabetic_sulfonylurea
antidiabetic_other antihypertensive diuretic_loop_thiazide potassium_sparing cardiac_glycoside antiarrhythmic nitrate_pde5 statin thyroid_hormone
antithyroid immunosuppressant corticosteroid antidepressant_ssri_snri antidepressant_maoi antidepressant_tca sedative_hypnotic antiepileptic
antipsychotic lithium opioid anticancer antiretroviral antibiotic_chelating antibiotic_other antitubercular hepatotoxic nephrotoxic
hormonal_contraceptive_estrogen ppi_antacid iron_mineral_supplement laxative_stimulant theophylline anaesthesia_surgery cyp3a4_substrate_narrow
cyp2c9_substrate cyp2d6_substrate cyp1a2_substrate pgp_substrate any_medicine
antiparkinson_levodopa photosensitizing anticholinergic cyp2c19_substrate""".split())
flags = set("pregnancy breastfeeding liver kidney heavy_metals bleeding hypoglycaemia hypotension thyroid autoimmune surgery children allergy other".split())
ids = set()
for r in R:
    assert r["id"] not in ids, r["id"]; ids.add(r["id"])
    assert r["kind"] in ("formulation", "mineral_preparation")
    seen = set()
    for i in r["interactions"]:
        assert i["drug_class"] in allowed, i["drug_class"]
        assert i["severity"] in ("major", "moderate", "minor")
        assert i["evidence"] in ("clinical", "case_reports", "preclinical", "theoretical")
        assert i["sources"] and all(s["url"].startswith("https://") for s in i["sources"])
        assert i["drug_class"] not in seen, (r["id"], i["drug_class"]); seen.add(i["drug_class"])
    for g in r["general_safety"]:
        assert g["flag"] in flags and g["sources"]
        assert g["evidence"] in ("regulatory", "clinical", "case_reports", "preclinical", "theoretical")

json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(R), "records;", sum(len(r["interactions"]) for r in R), "interactions;",
      sum(1 for r in R for i in r["interactions"] if i["severity"] == "major"), "major;",
      sum(len(r["general_safety"]) for r in R), "safety flags")
