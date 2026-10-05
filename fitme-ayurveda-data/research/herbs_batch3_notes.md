# Batch 3 notes: gaps, conflicts and judgement calls

Output: `herbs_batch3.json`. It has 25 records and 125 interactions: 9 major, 35 moderate and 81 minor. It loads with `json.load`, and every `drug_class` is a key from SPEC.md, including the 4 keys added mid-task:
  - `photosensitizing`: St John's wort
  - `cyp2c19_substrate`: St John's wort (induction) and chitrak (in vitro inhibition)
  - `anticholinergic`: nutmeg at toxic doses
  - `antiparkinson_levodopa`: not used, because no batch-3 herb had a sourced levodopa interaction. Last checked 2026-10.

## How sources were checked
- I pulled every PubMed citation (100 PMIDs) live from NCBI E-utilities. The titles in the JSON come from NCBI esummary, not from memory. I read the abstracts of the studies that each claim relies on.
- Non-PubMed URLs (19) all returned HTTP 200 on 2026-10-04:
  - NCCIH: St John's wort, green tea, Asian ginseng, ephedra, garcinia
  - LiverTox: clove/eugenol, flavocoxid, garcinia, green tea, St John's wort, ginseng
  - EMA HMPC monographs: fennel, St John's wort, ginseng, green tea. I read sections 4.3 to 4.6 of each PDF.
  - FDA 2004 ephedrine-alkaloid rule (govinfo PDF). I confirmed it names *Sida cordifolia*.
  - DailyMed labels: ephedrine (Akovaz) and Xarelto. I confirmed the interaction text in each.
  - FDA tainted-product notice for "Garcinia Cambogia Premium" (sibutramine)
- LiverTox pages on ncbi.nlm.nih.gov/books show a CAPTCHA to scripts. I confirmed the NBK IDs and their summary text through the PubMed index of each LiverTox chapter.
- `traditional_source_type: "API monograph"` is used only where I found the species in Ayurvedic Pharmacopoeia of India Part I, Vols 1 to 5. I checked these through a mirror PDF and did not fetch any AYUSH URL. *Sida cordifolia* (Bala) and *Garcinia indica* (Vrikshamla) were not found in Vols 1 to 5, so both use `classical text`.

## Duplicates and identity problems
- **Musta / mustak**: skipped as a duplicate. Folded into `nagarmotha` (*Cyperus rotundus*). Note that "Nagaramusta" can mean *Cyperus scariosus*, which is traded as a substitute (PMID 26167002).
- **Rasna**: the record uses *Pluchea lanceolata*, the API Rasna. *Alpinia galanga* and *Vanda roxburghii* are also sold as rasna. The data may not apply to those.
- **Vidari kand**: the record uses *Pueraria tuberosa*, the API Vidari. *Ipomoea digitata* is also sold under this name.
- **Pashanbhed**: several unrelated plants are sold under this name (PMID 24948861). This is recorded as an "other" safety flag.
- **Kokum vs Garcinia cambogia**: kept as two separate records. Some texts apply "Vrikshamla" to both species.
- **Ginseng**: covers *Panax ginseng* and *P. quinquefolius* together. It is not ashwagandha ("Indian ginseng"), which is in batch 1.
- **Bala**: the alkaloid content of commercial products is unknown, and the ephedrine content in *Sida* reported in studies is variable and mostly qualitative (PMID 35961325). I found no measured ephedrine levels in Indian Bala products.

## Rule deviations and judgement calls
1. **Bala + MAOI is rated `major` although the evidence is `theoretical`.** I made this exception because a regulator speaks to both halves of it: FDA's 2004 rule names *Sida cordifolia* as an ephedrine-alkaloid source, and the ephedrine label lists MAOIs as augmenting its pressor effect. There are no reports of this interaction for Sida itself. A reviewer may prefer `moderate`.
2. **`traditional_source_type` for non-Ayurvedic herbs.** The schema allows only three values. Ginseng, sea buckthorn (Sowa-Rigpa), St John's wort (European herbal tradition) and green tea use `classical text`. Garcinia cambogia uses `brand literature` because its "traditional" positioning is mostly marketing. If the app needs a separate value for these, add something like `non_ayurvedic_tradition`.
3. **Bleeding-risk classes.** Every herb with an antiplatelet signal also gets `anticoagulant_vka` and `anticoagulant_doac` at `minor`. These are extrapolated by drug class; there are no specific DOAC studies.
4. **Low-blood-sugar classes.** Hypoglycaemic herbs list all three antidiabetic keys so a scan of any antidiabetic matches. Most of this evidence is from animals only. Ginseng and sea buckthorn have small human studies.
5. **Folic acid.** The green tea effect on folic acid absorption sits under `iron_mineral_supplement`, because there is no vitamin key.
6. **Green tea and fexofenadine.** This is an OATP1A2 effect (about 70% lower exposure). No class key fits, so it is mentioned only in the mechanism text of the antihypertensive entry.

## Conflicts between sources
- **Fennel**: the EMA monograph says "None reported" for interactions. A rat study shows fennel lowered ciprofloxacin absorption by about 48%. Kept as `minor` / `preclinical`.
- **Ginseng**: the EMA monograph says "None reported" for interactions. Against this, a randomised trial showed reduced warfarin effect (American ginseng), a volunteer study showed CYP3A induction (midazolam AUC down about 34%), and there are case reports with imatinib, raltegravir and phenelzine. I followed the clinical data.
- **Chitrak**: purified plumbagin strongly inhibits several CYPs in vitro (Ki at or below about 2 µM). But a whole-formulation study of Trimada (chitrak, musta and vidanga) found little CYP inhibition (PMID 33039629). Ratings are kept at minor, except `cyp3a4_substrate_narrow` at moderate because those drugs have a narrow therapeutic margin.
- **Green tea and warfarin**: the only report involved drinking half to one gallon a day, with vitamin K as the proposed cause. Extracts contain little vitamin K. Rated moderate with that caveat.
- **Green tea and tacrolimus**: the single 2026 case was confounded by an orange extract. Rated minor.
- **Khadira and the liver**: the liver injury evidence is for flavocoxid, which combines *A. catechu* catechins with *Scutellaria* baicalin. The responsible component was not established. Rated minor.
- **St John's wort and clopidogrel**: St John's wort increases clopidogrel's effect, the opposite direction to most of its interactions. The evidence is one small open-label trial.

## Gaps (no usable evidence found)
- No herb-drug interaction data of any kind for **devdaru, varun, pashanbhed, rasna, nirgundi, kanchnar** beyond animal pharmacology. Their records are thin and `data_quality: poor`.
- No safety-flag sources were found for **elaichi, nagarmotha, nirgundi, rasna, kantakari, varun, kanchnar**, so their `general_safety` is `[]`. Specific gaps:
  - Pregnancy data for most of these spices and herbs
  - Solanum glycoalkaloid toxicity for kantakari
  - Abortifacient reputation of hing and nutmeg (no reliable source found)
  - Gluten in compounded hing, which is usually cut with wheat flour (no regulatory source found)
- **Kanchnar and thyroid**: Kanchnar guggulu is marketed for thyroid wellbeing, but I found no thyroid data for *Bauhinia variegata* alone. No thyroid interaction was added. Batch 4 should check Kanchnar guggulu.
- **Bael and thyroid**: the data is rodent-only, from the leaf, which is not the fruit commonly eaten.
- **St John's wort**: possible additional entries were not added because no source was verified this session:
  - Antiepileptics (carbamazepine data is mixed)
  - PPIs (omeprazole induction)
  - Calcium-channel blockers
  - Triptans (Henderson 2002 mentions them, but there is no matching key)
- **Green tea**: caffeine interactions with theophylline, clozapine and lithium were not added. The EMA monograph mentions only sedatives and sympathomimetics.
- **Kokum**: all entries are extrapolated from Garcinia cambogia hydroxycitric acid data. There are no kokum-specific safety reports.
- **Sea buckthorn**: NCCIH has no page for it (404). Its evidence is small human studies only.
- **Nutmeg**: a "toxic dose" threshold was left out because it varies between sources.
