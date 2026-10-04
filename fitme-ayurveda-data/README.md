# FITme herb–medicine safety data

When a user scans a medicine, FITme can show which Ayurvedic herbs and products may be risky to take with it. This data **never suggests a herb as an alternative to a medicine.** That was a deliberate choice. Suggesting herbal swaps for prescription drugs could harm users, and it would break India's Drugs and Magic Remedies Act, US FTC/FDA rules and App Store guideline 1.4.1.

## What's inside

| | Count |
|---|---|
| Ayurvedic herbs, spices, formulations, bhasmas and branded products | **113** (60 herbs, 18 spices, 22 formulations, 13 mineral preparations) |
| Herb → drug-class interaction rules | **571**, plus 245 general safety flags (pregnancy, liver, heavy metals, etc.) |
| Medicines the scanner can recognise | **2,626** molecules, plus about 24,500 alternate names, salt forms and US brands |
| Medicines with at least one interaction class | **962** |
| Medicine × herb warnings when expanded | **13,180**: 443 major, 5,879 moderate, 6,858 minor |
| Unique sources cited | **481** (381 PubMed/PMC, the rest NIH, FDA, EMA, CDC, WHO, AYUSH) |

| File | Use |
|---|---|
| `herbs.json` | Herb records: names (English, Hindi, Sanskrit, Latin), products, neutral traditional context, safety flags, interactions with sources |
| `medicines.json` | Molecule → drug classes, plus aliases for scanner matching (paracetamol → acetaminophen, frusemide → furosemide) |
| `herb_drug_warnings.csv` | Every medicine × herb warning, written out in full so you can review in a spreadsheet exactly what each medicine will show |
| `build_report.json` | Counts and the wording-check result |
| `build_ayurveda.py` | Rebuilds the three files above from `research/` |
| `build_medicines.py`, `medicine_rules.py` | Rebuild `research/medicines.csv` from openFDA, NLEM 2022 and the Jan Aushadhi list (about 1.9 GB download on first run) |
| `research/` | The spec, the four herb research batches with notes on gaps and conflicts, and the medicine notes |

## How the app should use it

1. The scanner reads the label's **generic name**. Indian law requires the generic name to be printed larger than the brand (Drugs Rules 1945, Rule 96). Lower-case it and look it up in `medicines.json` by `molecule` or `aliases`.
2. Take that medicine's `classes`. For each herb in `herbs.json`, pick the interactions whose `drug_class` matches. Then apply two rules:
   - If an interaction has `only_molecules`, show it only for those molecules.
   - If it has `major_only_for`, show "major" for those molecules and "moderate" for the rest.
3. Show the results grouped, not as a wall of 35 rows:
   - **Major** warnings, always expanded.
   - **Moderate**, grouped by effect (for example, "May lower blood sugar further: gurmar, karela, methi, jamun…").
   - **Minor**, collapsed under "Lower-evidence interactions".
4. If `classes` is empty, say "No known herb interactions in our database", never "safe".
5. `herb_level_warnings` describe the herb's own toxicity (kuchla, vatsanabh, dhatura) or a dosing rule (isabgol: take 2 h apart from medicines). Show them on the herb's own screen.

Put this banner on every result screen:

> Do not start, stop or change any medicine or herbal product without talking to your doctor or pharmacist. This is general safety information, not medical advice.

## Wording rules the data already follows

- **No disease claims.** Traditional context reads like "Traditionally used in Ayurveda for general vitality".
- **No forbidden words.** No "cure", "treat", "remedy" or "alternative to" anywhere. `build_ayurveda.py` checks for these on every build; the current result is 0 issues.
- **No advice to stop a medicine.** The default advice is "Talk to your doctor or pharmacist before combining."
- **Sources:** every interaction and safety flag cites at least one real source. Classical texts and brand sites are used only for traditional context and ingredient lists, never as evidence for an interaction.

## Before you ship (do these)

1. **Get a lawyer to review the medicine-scanner screens** for India, the US and the EU. This is research, not legal advice.
2. **Email PMBI (Jan Aushadhi) and the NLEM publisher.** Only molecule names were used from them, but both sites say "reproduce only with permission".
3. **Indian brand names (Dolo, Glycomet, Thyronorm) are not included.** No source is legally usable yet: 1mg/PharmEasy forbid scraping, and Kaggle copies are scraped. The government ABDM Drug Registry (launched June 2026, 123,000+ brands) is the route: apply to the National Health Authority for API access and terms.
4. **Check these items against the original source:**
   - the Gazette number for the 2018 generic-name labelling rule (G.S.R. 222(E))
   - the Australian TGA 2026 kalmegh warning (pages didn't load)
   - LiverTox chapter wording (behind a captcha)
5. **Data quality:** 17 herbs are rated "good", 54 "limited" and 42 "poor". Show the evidence level next to every warning so users can see when a warning rests on lab or animal data.

## Credits line for the app

> Medicine data: U.S. FDA (openFDA), Government of India NLEM 2022 and PMBI Jan Aushadhi list. Herb safety data compiled from NIH (NCCIH, LiverTox), EMA, FDA, CDC, WHO, Ministry of AYUSH and peer-reviewed studies; see in-app sources.
