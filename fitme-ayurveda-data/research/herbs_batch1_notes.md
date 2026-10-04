# Batch 1 notes: gaps, conflicts, weak data

File: `herbs_batch1.json`. It has 27 records and 182 interaction rows. 7 rows are major and 175 are moderate or minor. Last checked 2026-10.

## How it was built
- Every PubMed title in the JSON was pulled automatically from NCBI E-utilities by PMID. None were typed by hand, and the build fails if any PMID does not resolve.
- I checked the government URLs directly:
  - NCCIH pages returned HTTP 200.
  - LiverTox NBK IDs were resolved through the NCBI Books esummary.
  - EMA monograph PDFs were downloaded and their sections 4.3 to 4.6 were read.
  - The Federal Register document was confirmed through its API.
  - The PIB press release was found through web search.
- LiverTox chapter text is behind a reCAPTCHA, so I could not read it in this run. LiverTox sources are cited only for general statements that have a chapter for that herb (for example, "rare cases of liver injury" or "not linked to liver injury"). No LiverTox likelihood scores are quoted.
- Diabetes-medicine effects appear as one row each for `antidiabetic_insulin`, `antidiabetic_sulfonylurea` and `antidiabetic_other`, so the app can match any of them. This means the 182 rows overcount the distinct herb–mechanism pairs.
- The spec allows "regulatory" as evidence only for safety flags. Interactions that rest on an EMA monograph statement are therefore labelled "clinical", and the EMA wording is given in `mechanism`. The one exception is psyllium with opioids, which is labelled "theoretical" because EMA gives it only as a precaution.
- New keys from the spec update: `cyp2c19_substrate` is used for brahmi (in vitro) and giloy (in vitro). No Batch 1 herb has documented photosensitizing, anticholinergic or levodopa interactions, so those keys are not used.

## Conflicts between sources
- **Turmeric:** The EMA monograph says "none reported" for interactions. Published case reports describe a raised INR with a vitamin K antagonist and raised tacrolimus levels with nephrotoxicity. A separate monitored transplant patient showed no tacrolimus change at culinary doses. One trial found that a curcumin+piperine product did not change midazolam, flurbiprofen or paracetamol levels (PMID 22725836). On liver injury, one Italian group calls turmeric hepatotoxicity "a baseless accusation" (PMID 34776989), while DILIN, LiverTox and NCCIH treat it as real. The JSON follows the regulators.
- **Ginger:** The EMA monograph says "none known". A phenprocoumon case report describes an INR of 10, while a controlled warfarin study in healthy volunteers found no effect. Platelet data are inconsistent. The warfarin row is kept at moderate.
- **Giloy:** Indian hepatology case series (35037744, 34230786) link giloy to autoimmune-like liver injury. The Ministry of Ayush (PIB, 2021) calls the link misleading and suggests the plant was misidentified (Tinospora crispa). Both sides are cited in the liver flag.
- **Garlic + warfarin:** EMA and NCCIH advise caution, but a trial of aged garlic extract found no extra bleeding risk. The row is kept at moderate.
- **Psyllium + levothyroxine:** EMA requires medical supervision, but a small human study (PMID 9737361) found no significant malabsorption. The row is set to minor.
- **Cinnamon + letrozole/nicotine (CYP2A6):** NCCIH raises a theoretical concern, but a 2026 clinical PK study (PMID 41622703) found no interaction. The row is minor.
- **Ashwagandha CYP:** In vitro testing (PMID 40023576) found no reversible CYP inhibition, so no CYP rows were added. NCCIH lists several pharmacodynamic interactions, and these are included.
- **Ginger in pregnancy:** NCCIH says it "may be safe". EMA says avoid it as a precaution. Both are cited.

## Herbs with poor or limited data
- **Poor:** shatavari, jamun, punarnava, safed musli, shilajit. All interaction rows for these are preclinical or theoretical and are minor or moderate. Shilajit has no herb-specific drug-interaction studies; its rows only reflect heavy-metal contamination risk.
- **Limited (mostly in vitro or animal data):** guggul, giloy, tulsi, brahmi, arjuna, neem, amla, karela, gurmar, shankhpushpi, gokshura, kalonji. Some notes:
  - Arjuna's CYP3A4/2C9/2D6 inhibition is strong in human liver microsomes but has not been tested in people. It is rated moderate.
  - Kalonji's CYP2D6/3A4 effect was seen in only 4 volunteers.
- **Shankhpushpi + phenytoin (major):** The case reports and rat study used a multi-ingredient syrup sold as "Shankhapushpi", not pure *Convolvulus pluricaulis*. The authors advised against combining it with phenytoin, so severity is kept at major.

## Gaps and items deliberately left out
- **Turmeric/curcumin with sulfasalazine and rosuvastatin (BCRP):** The spec has no key for BCRP substrates. The sulfasalazine evidence is folded into `pgp_substrate`. Consider adding a `bcrp_substrate` key.
- **CYP2A6 (cinnamon) and CYP2E1 (garlic, PMID 12235448):** The spec has no keys for these. Only the cinnamon–letrozole row was kept, under `anticancer`.
- **Guggul:** Antiplatelet or anticoagulant claims are common online, but I found no PubMed source that clearly supports them, so they are omitted.
- **Licorice + digoxin:** No specific case report was found. The major rating rests on the EMA monograph ("not to be used concomitantly with cardiac glycosides") and the well-documented hypokalaemia. The FDA "Black Licorice: Trick or Treat?" consumer page now returns 404 and is not cited.
- **Amla (vitamin C) increasing iron absorption, and fenugreek or karela fibre affecting drug absorption:** These are plausible, but no adequate source was found, so they are omitted.
- **Garlic + ritonavir (GI toxicity case, Can J Hosp Pharm 1998):** Not indexed in PubMed and not cited. The garlic `antiretroviral` row rests on the EMA monograph and the saquinavir PK study.
- **Ayurvedic Pharmacopoeia of India / AYUSH monographs:** No accessible online text was found. `traditional_source_type` is set to "classical text" for all herbs, and `traditional_context` sentences are general wellness framings without citations.
- **Isabgol Sanskrit name** ("Snigdhajiraka"): This is from secondary literature and was not verified against the API.
- **Name confusion:**
  - "Brahmi" is also used for *Centella asiatica*.
  - "Shankhpushpi" is also used for *Evolvulus alsinoides* and *Clitoria ternatea*.
  - For aloe, inner-leaf gel and the anthranoid latex carry very different risks. The laxative and potassium rows apply mainly to latex and whole-leaf products.
- **Heavy metals:** The Saper JAMA 2004 and 2008 studies are cited for shilajit. They cover Ayurvedic products in general, especially rasa shastra products, not shilajit specifically. A shilajit-specific metals analysis (PMID 34800280) is also cited.
