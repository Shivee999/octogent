# FITme medicine database: build notes

Built 2026-10-04 by `fitme-ayurveda-data/build_medicines.py`, which reads its rule tables from `medicine_rules.py`.
To rebuild, run `python3 build_medicines.py`. The first run downloads about 1.9 GB into `.cache/`, which is gitignored. Later runs take about 1 minute.

## Files

| File | What it is |
|---|---|
| `medicines.csv` | One row per molecule. Columns: `molecule, display_name, drug_classes` (pipe-separated SPEC.md keys), `fda_epc, sources` (`openfda` / `nlem` / `janaushadhi` / `manual`), `us_brand_examples` (up to 3 NDA/BLA brands from openFDA), `in_nlem` (y/n) |
| `medicine_aliases.csv` | Maps the text a scanner might read to a molecule. It has 201 INN/IP/BAN names (paracetamol → acetaminophen, salbutamol → albuterol, glibenclamide → glyburide…), 38 spelling variants found on the Jan Aushadhi list, 941 salt/ester forms ("metformin hydrochloride") and 23,553 US brand names. Of the brands, 2,535 come from NDA/BLA products and the rest from ANDA or OTC listings, and the `note` column says which. A combination brand maps to all of its molecules, e.g. Janumet → metformin\|sitagliptin |
| `medicine_class_evidence.csv` | Every molecule→class assignment (1,693 rows) with its basis: the FDA EPC/MoA string, the FDA table and category, or the manual note |
| `medicines_build_stats.json` | Counts, dropped rows, unmatched Jan Aushadhi strings and unmapped EPCs, for the next curation pass |

`any_medicine` is not written on any row. It is a general rule (e.g. "take isabgol 2 h apart from any medicine"), so the app should apply it to every scanned medicine.

## Counts

| | |
|---|---|
| Molecules in `medicines.csv` | **2,626** |
| …with ≥1 drug_class | **962 (36.6 %)** |
| …with ≥2 classes | 236 |
| …with an FDA EPC | 1,440 |
| …with US brand examples | 1,312 |
| From openFDA | 2,437. Built from 97,984 NDC products (export 2026-10-02) + 72,388 label records (export 2026-10-02) |
| In NLEM 2022 (`in_nlem=y`) | 362 molecules from the 384 NLEM entries; **214 classified** |
| In Jan Aushadhi list | 780 molecules from 2,044 of the 2,439 PMBI products; **450 classified**. The other 395 products are sutures, devices, diapers, nutraceuticals and similar |
| Not in openFDA at all (India sources only) | 189 molecules, **66 classified** |
| Dropped (no class, not a scannable medicine) | 539 in total: 291 that appear only in "unapproved drug other" listings (mostly plant extracts), 231 vaccine antigens, allergen extracts, radiodiagnostics and cosmetic peptides, and 17 openFDA name fragments such as "3500 mw)". All are listed in the stats JSON |

The 962 classified molecules split by class as follows:

| Class | Molecules | Class | Molecules | Class | Molecules |
|---|---:|---|---:|---|---:|
| anticancer | 194 | sedative_hypnotic | 32 | antiplatelet | 9 |
| antibiotic_other | 78 | antidiabetic_other | 31 | nitrate_pde5 | 9 |
| antihypertensive | 73 | corticosteroid | 30 | diuretic_loop_thiazide | 9 |
| cyp3a4_substrate_narrow | 59 | antiepileptic | 28 | statin | 7 |
| anticholinergic | 55 | antipsychotic | 28 | antidiabetic_insulin | 7 |
| cyp2d6_substrate | 53 | nsaid | 25 | anticoagulant_heparin | 6 |
| nephrotoxic | 44 | potassium_sparing | 25 | theophylline | 5 |
| photosensitizing | 42 | antiretroviral | 24 | laxative_stimulant | 5 |
| immunosuppressant | 38 | hormonal_contraceptive_estrogen | 23 | antidepressant_maoi | 5 |
| iron_mineral_supplement | 35 | anaesthesia_surgery | 22 | anticoagulant_doac | 4 |
| hepatotoxic | 34 | ppi_antacid | 19 | antidiabetic_sulfonylurea | 4 |
| antibiotic_chelating | 19 | cyp2c19_substrate | 18 | antithyroid | 3 |
| cyp2c9_substrate | 18 | opioid | 18 | thyroid_hormone | 3 |
| antidepressant_ssri_snri | 16 | antiparkinson_levodopa | 15 | anticoagulant_vka | 2 |
| antitubercular | 14 | pgp_substrate | 13 | lithium | 2 |
| antiarrhythmic | 12 | cyp1a2_substrate | 11 | cardiac_glycoside | 1 |
| antidepressant_tca | 11 | | | | |

Most of the 1,664 unclassified rows are OTC topical actives (sunscreens, antiseptics, skin protectants), vitamins, contrast agents, biologics and drugs whose class has no spec key (see "Unmapped" below). An unclassified row still lets the scanner recognise the medicine. The app should show "no known herb-class interactions in our database", not "safe".

## How classes are assigned (in order)

1. **FDA EPC → key** (`EPC_MAP`, 189 EPC strings). openFDA attaches EPCs to the product. A product's EPCs are credited to an ingredient only when the product has a single ingredient. 32 ingredients that are only sold in combinations got their EPCs by elimination: from a combination product in which every other ingredient's EPCs are known, they take the EPCs those partners do not explain. Examples are sacubitril (Neprilysin Inhibitor), clavulanate and sulbactam (beta Lactamase Inhibitor).
2. **FDA MoA → key** (`MOA_MAP`; HIV protease inhibitors).
3. **FDA interaction tables** (only substrates FDA names):
   - *FDA "Healthcare professionals – examples of drugs that interact with CYP enzymes and transporter systems"* (content current as of 05/29/2026). Its "sensitive" and "moderate sensitive" substrate columns supply 3A, 2C9, 2C19, 2D6 and 1A2, and its transporter column supplies P-gp. CYP3A substrates go to `cyp3a4_substrate_narrow`.
   - *FDA "Drug Development and Drug Interactions: Table of Substrates, Inhibitors and Inducers"* (index-substrate tables, as of 06/05/2023).
   - *FDA's 2006 version of the same table*. Its Table 7 lists **CYP3A substrates with narrow therapeutic range**: alfentanil, cyclosporine, dihydroergotamine, ergotamine, fentanyl, pimozide, quinidine, sirolimus and tacrolimus. Its Table 8 lists NTI substrates: theophylline and tizanidine for 1A2, warfarin and phenytoin for 2C9, thioridazine for 2D6. Its Table 11 lists P-gp substrates. The current FDA pages no longer carry an NTI list. The fda.gov original (ucm093664) is offline, so the copy used is FDA's page as captured 2011-01-03 and hosted at courses.washington.edu.
   - *FDA Table of Pharmacogenetic Associations* (as of 09/10/2026). It supplies the CYP2C19, CYP2C9 and CYP2D6 rows from all three sections. This is where **clopidogrel and citalopram** come from (FDA names them for CYP2C19), along with pantoprazole and escitalopram. The section number is kept in the evidence file. Section 3 means "pharmacokinetic effect only".
4. **Manual overrides** (`OVERRIDES`, 638 entries). They cover three things:
   - drugs with no usable EPC, plus India-only molecules;
   - FDA boxed or labelled warnings, mapped to `hepatotoxic` / `nephrotoxic`;
   - removals where an EPC misfires. Examples: loperamide is not `opioid`, colchicine and griseofulvin are not `anticancer`, botulinum toxins are not `anaesthesia_surgery`, and ovine digoxin Fab is not `cardiac_glycoside`.
5. **Derived keys:**
   - `antibiotic_chelating` ⇒ `photosensitizing`. Tetracyclines and quinolones are both spec examples.
   - `antidepressant_tca` ⇒ `anticholinergic`. This is in the spec's own description of the key.

### Judgement calls (uncertain fits, flagged here and in the evidence notes)

- **NSAIDs ⇒ also `nephrotoxic`.** The spec lists "NSAIDs at high dose" under nephrotoxic. Ophthalmic-only NSAIDs (bromfenac, nepafenac) are excluded. Aspirin keeps the key even though it is mostly used at low dose.
- **ACE inhibitors, ARBs and aliskiren ⇒ also `potassium_sparing`.** This follows the spec comment "(+ ACEi/ARB hyperkalaemia risk)".
- **Thiazide and thiazide-like diuretics ⇒ also `antihypertensive`.** Loop diuretics do not get it.
- **α-blockers ⇒ `antihypertensive`.** This includes uroselective tamsulosin and silodosin, because the spec says "alpha-blockers". Ophthalmic β-blockers such as timolol also keep `antihypertensive`.
- **Parenteral factor Xa and thrombin inhibitors ⇒ `anticoagulant_heparin`.** This covers fondaparinux, argatroban and bivalirudin. Oral agents go to `anticoagulant_doac`.
- **MAO-B inhibitors ⇒ `antiparkinson_levodopa`.** Rasagiline and safinamide follow this rule. Selegiline also keeps `antidepressant_maoi` because its patch is an MAOI antidepressant. Rasagiline additionally has `antidepressant_maoi` from its FDA EPC "Monoamine Oxidase Inhibitor".
- **FDA EPC "Serotonin Reuptake Inhibitor" puts trazodone and nefazodone under `antidepressant_ssri_snri`.**
- **The `anticholinergic` set is limited.** It covers the FDA "Anticholinergic", "Cholinergic Muscarinic Antagonist" and "Antihistamine" EPCs, TCAs, a manual list of first-generation (sedating) antihistamines, antimuscarinic antispasmodics and bladder drugs, and cyclobenzaprine and orphenadrine. Strongly anticholinergic antipsychotics (clozapine, olanzapine) and paroxetine were *not* added.
- **`photosensitizing` covers the spec examples plus a few others.** The extras are retinoids, psoralens, photodynamic agents, voriconazole, vemurafenib, pirfenidone and griseofulvin, which all carry a labelled photosensitivity warning.
- **`cyp3a4_substrate_narrow` includes FDA "moderate sensitive" substrates**, such as atorvastatin, alprazolam, rivaroxaban and colchicine, as well as sensitive and NTI ones. Use the evidence file if the app wants only sensitive/NTI.
- **India-specific fits:**
  - nicorandil → `nitrate_pde5`: its label contraindicates PDE5 inhibitors;
  - doxofylline, acebrophylline and etofylline → `theophylline`;
  - saroglitazar → `antidiabetic_other`;
  - levosulpiride → `antipsychotic`: it is a D2 antagonist, but in India it is mostly used as a prokinetic;
  - ormeloxifene, dydrogesterone, allylestrenol and cyproterone → `hormonal_contraceptive_estrogen`;
  - diacerein, agomelatine and nimesulide → `hepatotoxic`, following EMA restrictions;
  - riociguat → `nitrate_pde5`.
- **Molecule-level, not route-level.** For example, minoxidil and tretinoin get their classes whatever the dosage form. openFDA routes were not carried into the CSV.

## Unmapped important classes

These classes have no spec key, so nothing was mapped. Consider them for SPEC v2:

- **CYP / P-gp inhibitors and inducers.** Examples are azole antifungals (16 unmapped molecules), clarithromycin and rifampin as an inducer. The spec only models the drug as a substrate.
- **Thrombolytics and haemostatics.** Streptokinase, tenecteplase and alteplase carry real bleeding risk, but there is no key for them. Tranexamic acid and etamsylate are in the same position.
- **Serotonergic drugs outside SSRI/SNRI/MAOI/TCA.** These include triptans, ondansetron, linezolid, dextromethorphan, mirtazapine and bupropion. Bupropion also lowers the seizure threshold.
- **CNS stimulants**: methylphenidate, amphetamines, modafinil.
- **Other lipid drugs**: fibrates, ezetimibe, bile-acid sequestrants. Sequestrants bind other drugs, so `any_medicine` covers them.
- **QT-prolonging drugs** in general: domperidone, hydroxychloroquine and chloroquine, macrolides, ondansetron.
- **Androgens and anabolic steroids, GnRH analogues, bisphosphonates and antimalarials.** Bisphosphonates also chelate minerals.
- **Non-HIV antivirals, antifungals, anthelmintics, local anaesthetics** (lidocaine is mapped only as an antiarrhythmic) **and most muscle relaxants.**
- **Vaccines, immunoglobulins and most biologics.** IL-17/IL-23 antagonists, for example, are not mapped to `immunosuppressant`. Only TNF, JAK, IL-6R, S1P, T-cell co-stimulation, calcineurin, mTOR and antimetabolite agents are.
- **Other CYPs and transporters**: CYP2C8, CYP2B6, BCRP and OATP substrates have no keys.

## India coverage

- **NLEM 2022** comes from the MoHFW PDF hosted by CDSCO (`nlem2022.pdf`). The build parses its alphabetical list of 384 entries. Combination entries such as "Abacavir (A) + Lamivudine (B)" are split into their molecules. Devices, blood components and dialysis fluids are skipped. Vaccines are kept as single named rows. INN/IP names are mapped to the US names (frusemide → furosemide, rifampicin → rifampin, phenobarbitone → phenobarbital…).
- **Jan Aushadhi (PMBJP)**: the full product table, 2,439 rows, comes from PMBI's official product-list page (`pmbi.co.in/ProductList.aspx`, the table behind its "Export to PDF" button). Product names are split into ingredients and matched against the molecule vocabulary. Every molecule that is not US-listed was read off this list or NLEM. Examples are aceclofenac, nimesulide, teneligliptin, voglibose, vildagliptin, gliclazide, remogliflozin, imeglimin, saroglitazar, cilnidipine, nicorandil, acenocoumarol, etizolam, doxofylline, ormeloxifene and levosulpiride. Each one got its class through `OVERRIDES` with a note. The 123 India-only molecules with no spec class are listed in the stats JSON, e.g. domperidone, serratiopeptidase, thiocolchicoside and trimetazidine.
- **Spelling.** The PMBI list contains misspellings ("Glimipride", "Flecanide", "Nimesulid"…). They are mapped as `spelling_variant` aliases, which also helps with OCR noise.

## Indian brand names: finding

**This build has no lawful, openly licensed bulk source of Indian brand names, so it contains none.** What was checked:

| Candidate | Result |
|---|---|
| **ABDM Drug Registry**: MoHFW / National Health Authority, built with CDSCO and NRCeS, launched 29 Jun 2026 ([PIB release 2278991](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2278991)): "123,000+ branded drugs, 10,000+ generic drugs, 29,000+ substances", "provides open APIs", portal `drugregistry.abdm.gov.in` | **This is the most promising route, but it could not be verified or used.** The portal and sandbox return HTTP 403 from outside India (CloudFront geo-block), so I could read neither the terms of use nor the API registration rules nor any redistribution licence. The data is coded in SNOMED CT. NRCeS gives SNOMED CT free to users in India, but an app distributed worldwide may need a separate SNOMED licence. **Next step:** apply to NHA/ABDM for API access and get written terms covering use in a commercial consumer app before ingesting anything. |
| CDSCO lists (approved new drugs, etc.) | These carry generic names only. The CDSCO copyright policy says: "may not be reproduced partially or fully, without due permission". |
| NPPA price notifications / Pharma Sahi Daam app | These are scattered PDFs that name brands only for price-fixed formulations, so there is no complete list. The app has no bulk export, and I found no data licence. |
| Kaggle/GitHub "A-Z Medicine Dataset of India", "Extensive A-Z Medicines Dataset", "India Medicines and Drug Info", junioralive/Indian-Medicine-Dataset | **Excluded and not downloaded.** They are scraped from 1mg and other e-pharmacies whose terms forbid scraping. The MIT, CC BY-SA or CC BY-NC-SA labels that uploaders attach do not cure that provenance, and CC BY-NC-SA is non-commercial anyway. |
| International Drug Dictionary (Mendeley, CC BY 4.0; 44 countries' official sources) | India is not included. |

**Fallback: read the generic name.** Indian law requires the generic name on the label:

- **Drugs Rules, 1945, Rule 96(1)(i)** (text via [IndianKanoon](https://indiankanoon.org/doc/47913260/)) requires the label to show the name of the drug. "The proper name of the drug shall be printed or written in a more conspicuous manner than the trade name, if any, which shall be shown immediately after or under the proper name." The proper name is the Schedule F / pharmacopoeial name (e.g. "Paracetamol Tablets I.P."), or the WHO INN for other drugs.
- **The Drugs and Cosmetics (First Amendment) Rules, 2018** tightened this. The proper name of a single drug, or of a fixed-dose combination, must now be printed in the same font, at least **two font sizes larger than the brand name**. This was voluntary from 13 Sep 2018 and mandatory from **1 Apr 2019**. Vitamin combinations and FDCs of more than three drugs are exempt from the font-size rule. **Uncertain:** the notification number (G.S.R. 222(E), 13 Mar 2018) and the exemption wording come from secondary sources (Mondaq, Pharmabiz, CDSCO artwork-guidance reports). I did not retrieve the Gazette itself, so check it on egazette.gov.in before citing it in-app.
- **What this means for the scanner:** on Indian packs it should look for the largest drug-name text and match it through `medicine_aliases.csv`. That file holds the IP/INN spellings (paracetamol, salbutamol, glibenclamide, frusemide, rifampicin, adrenaline, lignocaine…). For FDCs with more than three drugs the generic names are still on the label, just not necessarily larger, so the app should OCR the composition block too.

## Licences of every source used

| Source | Licence / terms | Use here |
|---|---|---|
| openFDA drug NDC and drug label bulk downloads (`download.open.fda.gov`) | Public domain / CC0 1.0. openFDA: "Unless otherwise noted, the content, data, documentation, code, and related materials on openFDA is public domain and made available with a Creative Commons CC0 1.0 Universal dedication." | Molecules, EPC/MoA, brand names, salt forms |
| FDA DDI substrate tables, FDA HCP CYP/transporter table, FDA Table of Pharmacogenetic Associations, FDA 2006 DDI table | US federal government works, public domain (17 U.S.C. §105). The 2006 table is FDA's own page; the courses.washington.edu file is only a copy of it | CYP/P-gp substrate keys |
| NLEM 2022 (MoHFW; PDF on cdsco.gov.in) | Government of India publication. The CDSCO site policy says no reproduction without permission, and the source must be acknowledged | Used only for facts: molecule names and the `in_nlem` flag. The list's text and structure are not redistributed. Credit "National List of Essential Medicines 2022, MoHFW". If the app reproduces the list itself, ask CDSCO/MoHFW first |
| PMBJP / PMBI Jan Aushadhi product list (`pmbi.co.in`) | PMBI copyright page: "Material featured on this Portal may be reproduced free of charge after taking proper permission by sending a mail to us… the source must be prominently acknowledged." | Used only to extract molecule names, which are facts. Prices, product codes and the list are not redistributed. **Before shipping, email PMBI for permission** and credit "PMBJP product list, PMBI" |
| Drugs and Cosmetics Rules 1945 (Rule 96) and amendments | Statute / subordinate legislation | Cited only |
| `medicine_rules.py` (EPC map, overrides, synonyms) | Written for this project. It contains pharmacology facts and short labelled notes | Classification |

These were considered and **not used** because their licence does not allow commercial redistribution, or because the data was scraped:

- WHO Model List of Essential Medicines: CC BY-NC-SA 3.0 IGO, non-commercial.
- WHO ATC/DDD: commercial use needs permission.
- DrugBank: non-commercial licence.
- RxNorm: free, but some of its sources need a UMLS licence.
- The Kaggle and GitHub Indian medicine datasets in the brand table above.

None of this is legal advice. Have counsel confirm the NLEM/PMBI fact-extraction position and the ABDM terms.

## Validation

- The CSV loads with `csv.DictReader`. The columns match exactly, and every `drug_classes` token is one of the 50 keys in SPEC.md, which now include `antiparkinson_levodopa`, `photosensitizing`, `anticholinergic` and `cyp2c19_substrate`. Molecule keys are unique and lower-case, `sources` uses only the four allowed values, and no row has more than 3 brands. `build_medicines.py` refuses to run if `medicine_rules.py` has duplicate dict keys or unknown spec keys.
- **Spot check: 69 well-known drugs plus 6 negative checks, 0 failures.** All of the following are correct:
  - warfarin → anticoagulant_vka + cyp2c9_substrate;
  - levothyroxine → thyroid_hormone;
  - digoxin → cardiac_glycoside + pgp_substrate;
  - cyclosporine and tacrolimus → immunosuppressant + cyp3a4_substrate_narrow (+ nephrotoxic);
  - metformin → antidiabetic_other;
  - glimepiride → antidiabetic_sulfonylurea + cyp2c9_substrate;
  - insulin glargine → antidiabetic_insulin;
  - atorvastatin and simvastatin → statin;
  - sertraline → antidepressant_ssri_snri;
  - citalopram → antidepressant_ssri_snri + cyp2c19_substrate;
  - carbamazepine, valproate and phenytoin → antiepileptic;
  - clopidogrel → antiplatelet + cyp2c19_substrate;
  - aspirin, ibuprofen, acetaminophen;
  - amlodipine, telmisartan, furosemide, hydrochlorothiazide (incl. photosensitizing) and spironolactone;
  - apixaban, dabigatran, enoxaparin and amiodarone;
  - sildenafil, methimazole, carbimazole, prednisolone, lithium and tramadol;
  - tamoxifen, isoniazid, rifampin, ciprofloxacin, doxycycline and amoxicillin;
  - omeprazole, ferrous sulfate, bisacodyl, theophylline and propofol;
  - ethinyl estradiol, alprazolam, zolpidem, olanzapine, phenelzine and amitriptyline (incl. anticholinergic);
  - methotrexate, dolutegravir and gentamicin;
  - levodopa, carbidopa and pramipexole → antiparkinson_levodopa;
  - oxybutynin, benztropine, diphenhydramine and trihexyphenidyl → anticholinergic;
  - isotretinoin and methoxsalen → photosensitizing;
  - India-only aceclofenac, nimesulide, teneligliptin, voglibose, gliclazide and acenocoumarol.

  The negative checks confirm that loperamide is not opioid, cetirizine and fexofenadine are not anticholinergic, colchicine and clascoterone are not anticancer, and dexamethasone is not immunosuppressant. The expected classes are standard pharmacology. A pharmacist should still review `medicine_class_evidence.csv` before launch.
