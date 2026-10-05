# Batch 2 notes: gaps, conflicts and judgement calls

File: `herbs_batch2.json`: 27 records, 117 interactions (7 major, 52 moderate, 58 minor). Checked with `python3 json.load`, and the `drug_class` keys, flag and evidence enums and source URLs were checked against SPEC.md. Last checked: 2026-10.

## How sources were verified
- I got PubMed titles from NCBI E-utilities (esummary) by PMID, so titles are exact. I read the abstracts of the key studies through efetch before citing them.
- NCBI Bookshelf pages (LiverTox, LactMed, StatPearls) block automated page fetches with a reCAPTCHA. I confirmed their content through the PubMed abstract records for those Bookshelf entries.
- I downloaded and text-searched the EMA HMPC PDFs (asarone statement; Andrographis assessment report and public statement). I read the DailyMed labels (Renese-R for reserpine; Sinemet for levodopa) through the DailyMed SPL API. NCCIH pages for goldenseal and boswellia, and eCFR 21 CFR 189.110, returned HTTP 200 and I read them.
- **TGA Andrographis pages could not be fetched** (HTTP 503 or connection reset). The URLs came from a web search. The details (more than 300 hypersensitivity/anaphylaxis reports, a fatal case in 2024, and removal from permissible ingredients for new listed medicines effective about 17 Sept 2026) come from search-result summaries and secondary news coverage. Re-verify on tga.gov.au before release.
- `traditional_source_type: "API monograph"` was checked by text-searching a combined Ayurvedic Pharmacopoeia of India Part I PDF (archive.org copy). Kalmegh, vacha and manjistha were not found in that copy, so they are labelled "classical text". Ajwain (Yavani) appeared only as a botanical-name match, not a "consists of" monograph line. The API Vatsanabha monograph names *Aconitum chasmanthum*, not *A. ferox*; this is noted in `names.other`.

## Missing drug_class keys (spec gaps)
1. **Antiparkinson / dopaminergic drugs (levodopa-carbidopa, dopamine agonists, MAO-B inhibitors)** have no key. This is the most important gap for **kapikacchu** (Mucuna contains levodopa, so effects add to levodopa medicines) and **sarpagandha** (reserpine blunts levodopa; the label says to avoid it). I put both under `general_safety` "other" flags. Suggest adding `antiparkinson_dopaminergic`.
2. **Photosensitising drugs** have no key. For **bakuchi** (psoralens), I mapped this to `antibiotic_chelating` (tetracyclines and fluoroquinolones are common photosensitisers). Other photosensitisers (methoxsalen, isotretinoin, amiodarone, thiazides) are not covered.
3. **Anticholinergic drugs** (antihistamines, oxybutynin, trihexyphenidyl) have no key. For **dhatura**, only TCAs, antipsychotics and opioids were mapped.
4. **CYP2C19 substrates** have no key. Haritaki raised omeprazole exposure in rats, so I mapped it to `ppi_antacid`.

## Judgement calls
- **`any_medicine` = major for kuchla, vatsanabh and dhatura.** This is not a pharmacological interaction. These plants are toxic at small overdoses and poisoning has been documented with traditional preparations (evidence: case_reports). The product may prefer to show this as a standalone "toxic herb" banner instead of attaching it to every scanned medicine.
- **Kapikacchu + MAOI = major with evidence "theoretical".** No Mucuna + MAOI study exists. Severity follows the FDA levodopa label, which contraindicates non-selective MAOIs, together with human data showing Mucuna delivers active levodopa (Katzenschlager 2004). Most other Mucuna rows extrapolate from the levodopa label and are graded minor or moderate.
- **Sarpagandha rows rely on the reserpine label** (Renese-R, DailyMed). Reserpine content of crude root and Ayurvedic products varies and is usually unlabelled.
- **Piperine data cover isolated piperine (about 20 mg/day).** For pippali, the evidence is extrapolated through piperine. Culinary pepper is unlikely to matter; advice text says this.
- **Berberine + cyclosporine = major.** This rests on a clinical study in transplant recipients (narrow-therapeutic-index drug).

## Conflicts in the evidence
- **Piperine and CYP3A4/P-gp:** inhibits them in vitro and in human PK studies (fexofenadine, carbamazepine, nevirapine), but also activates PXR and induces CYP3A4/MDR1 in human cells (Wang 2013). The net long-term effect is uncertain.
- **Trikatu + diclofenac:** in rabbits, Trikatu *decreased* diclofenac levels. This is the opposite of the usual piperine "enhancer" effect.
- **Andrographis + warfarin:** andrographolide increased warfarin exposure in rats (Zhang 2018). The Kan Jang combination showed no PK or PT effect in rats (EMA assessment report). Andrographis + theophylline also gave mixed results (clearance up with andrographolide, down with the extract at high theophylline doses).
- **Moringa:** inhibits CYP3A4/1A2/2D6 in vitro, but leaf powder did not change nevirapine PK in HIV patients. LactMed says moringa "may stimulate blood clotting" without a clear mechanism.
- **Saffron:** antiplatelet in vitro, but no change in PT, PTT or coagulation factors at 200–400 mg/day in volunteers. Grades are therefore kept minor.
- **Haritaki/Triphala:** Triphala weakly inhibits CYP3A4/2D6 in vitro, while chebulinic acid *induces* CYP1A2/2C/2D/2E1 in rats. The direction of any effect is unknown.
- **Reserpine and depression:** the label contraindicates reserpine in people with a history of depression. A 2023 systematic review (Strawbridge) found the reserpine–depression association inconsistent. The antidepressant interaction rows were downgraded to minor/theoretical.
- **Berberine + metformin:** the pharmacodynamic effect is additive glucose lowering. The pharmacokinetic effect goes the other way: goldenseal reduced metformin AUC by about 20% at low metformin doses in people, and berberine lowered plasma metformin but raised its kidney-tissue concentration in rats (OCT1/2 and MATE1 inhibition). The net clinical effect is uncertain.
- **Kalmegh kidney injury:** reported only with intravenous andrographolide preparations in China. Relevance to oral kalmegh is unclear.

## Herbs with little or no usable interaction evidence
- **Bhringraj (Eclipta prostrata)** and **manjistha (Rubia cordifolia):** no human or animal interaction data were found. Interactions and safety flags are left empty rather than invented; data_quality is "poor". Possible leads: Eclipta's traditional haemostatic use and coumestans (wedelolactone); Rubia's anthraquinones. Note that the related *Rubia tinctorum* (madder) was withdrawn in Germany over lucidin genotoxicity. That was not verified for *R. cordifolia* and is not included.
- **Vasaka:** only the pregnancy flag (vasicine is uterotonic/abortifacient in animals). No drug interaction data were found.
- **Lodhra, ashoka, chirata, kutki, bibhitaki, jatamansi, ajwain:** interactions rest on animal or in vitro pharmacology or reviews and are graded minor (chirata + sulfonylurea is moderate because swerchirin was tested on top of tolbutamide). Ashoka products are often adulterated or substituted.
- **Vacha:** only a sedative interaction (old animal data). The main concern is beta-asarone genotoxicity (EMA limit; banned as a food additive in the US).
- **Pregnancy flags** were left out where no source said anything specific: jatamansi, kutki, chirata, lodhra, bhringraj, manjistha, haritaki. This means "no data", not "safe".

## Wording
- Traditional-context lines use "general wellbeing of …" phrasing and name no diseases. Some source titles and study-population descriptions in `mechanism` (e.g. "patients with epilepsy", "HIV patients") name conditions. They describe the study, not a claim. Scrub them if the UI shows mechanism text to users.
- Advice never says to stop a medicine or use the herb instead. For kuchla, vatsanabh and dhatura, it says to use them only under a qualified practitioner with a purified, labelled product.
