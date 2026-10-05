# Batch 4 notes: gaps, conflicts and judgement calls

Output: `herbs_batch4.json`. It has 34 records (22 `formulation`, 12 `mineral_preparation`), 149 interactions (3 major, 52 moderate, 94 minor) and 59 general-safety flags. It loads with `json.load`, and every `drug_class` is a key from SPEC.md, including the keys added in the spec update. Data quality: 19 records are `limited` and 15 are `poor`. Last checked 2026-10.

## How sources were checked
- **PubMed:** I resolved every PubMed citation (56 PMIDs) live through NCBI E-utilities and read the abstract behind each claim. Three IDs were wrong in my first draft and are now fixed:
  - Saper 2008 is PMID 18728265. PMID 19155449 is a later JAMA letter.
  - Bano 1991 is PMID 1815977.
  - The Cystone trials are PMIDs 21161651 and 21419609. PMID 21359878 is a manufacturer letter commenting on them.
- **Other URLs (32):** 21 returned HTTP 200 on 2026-10-04. The other 11 return 403 to scripts (CDC MMWR x4, NIH ODS x3, diabetesjournals.org, MDPI, ScienceDirect, ResearchGate). I confirmed their content through WebFetch (CDC MMWR 2004/2012/2015) or through search-engine extracts (ODS ashwagandha/iron/calcium, the CDC 1993 iron MMWR, Diabetes Spectrum, the MDPI Liv.52 review, the Septilin ScienceDirect abstract, the Avipattikar review).
- **Dropped:** two sources I could not use. The FDA 2008 consumer page "Use Caution With Ayurvedic Products" now returns 404. The Health Canada 2008 warning could not be reached through the proxy.
- **FDA import alerts:** the page for Import Alert 66-41 itself does not mention Ayurveda. I cite the alerts only through FDA's Dec 2025 warning, which says that Ayurvedic products were placed on Import Alerts 66-41 and 99-42.

## Brand sites
These pages were used only to check ingredient lists in `names.other` and `common_products`. The build script removes every brand URL from `sources` arrays, so no interaction or safety flag relies on brand literature:
- Patanjali: Madhugrit, Madhunashini Vati Extra Power, Coronil
- Himalaya: Diabecon, Septilin, Cystone
- AIMIL: BGR-34

The Liv.52 ingredients (including Mandur bhasma) come from a peer-reviewed Dove Press paper. Classical formulations use ingredient lists from Ayurvedic formulary tradition. They are not verified against each brand's label, and composition varies by maker.

## Spec update (new keys)
- `antiparkinson_levodopa`: added to every iron-containing product. The full set at `moderate` is on Punarnavadi mandur and Lauha bhasma. Chandraprabha, Arogyavardhini and Liv.52 have it at `minor` / `theoretical`. Source: ODS iron (levodopa labels warn about iron).
- `cyp2c19_substrate`: added to three records:
  - Brahmi vati at `moderate` / `preclinical`. Bacopa inhibited CYP2C19 to under 10% activity at estimated gut concentrations (PMID 24566323).
  - Ashwagandharishta and Arjunarishta at `minor`, based on the related Ridayarishta formulation (PMID 27457692).
- `photosensitizing` and `anticholinergic`: not used. No product in this batch has sourced evidence for them.

## Judgement calls
1. **Three `major` ratings.** Alcohol-containing arishtas with metronidazole or tinidazole are rated `major` because the drug labels and NIAAA advise avoiding alcohol. A 15-30 ml dose of a 6-8% arishta holds only about 1-2.5 g of ethanol, so a reviewer may prefer `moderate`. Kumaryasava is rated `moderate` because the one GC study measured only 0.1-1.9% ethanol.
2. **Evidence level.** I applied "use the ingredient's evidence level" as instructed. For example, a gymnema clinical study gives `clinical` for Diabecon. Where the ingredient's share is small or unknown, I lowered the severity instead. `theoretical` is used only when neither the product nor the ingredient has data for that interaction.
3. **Diabetes classes.** Blood-sugar effects are entered under all three keys (`antidiabetic_insulin`, `antidiabetic_sulfonylurea`, `antidiabetic_other`), so a scan of any diabetes drug matches. This follows batch 3.
4. **Sugar content.** The schema has no "sugar" flag. Sugar is recorded as an `other` safety flag plus `minor` / `theoretical` "may raise blood sugar" interactions. This applies to Chyawanprash, Sitopaladi, Talisadi and Avipattikar. Dashmularishta has a flag only.
5. **Branded diabetes/COVID products.** For Diabecon, Madhunashini, Madhugrit, BGR-34 and Coronil, interactions are limited to the three antidiabetic keys, as instructed. Safety flags also include:
   - hypoglycaemia
   - regulatory notes
   - liver flags for Coronil (giloy and ashwagandha)
   - a heavy-metal/strychnine flag for Madhunashini (its label lists vang and lauh bhasma and kuchla)

   I kept these because they are safety facts, not marketing. `traditional_context` for these products deliberately says only "recorded here only for ... risk". No efficacy wording is repeated, and the BGR-34 trial is cited only as evidence that it lowers glucose.
6. **Calcium preparations.** Praval/mukta pishti and shankh/godanti bhasma are one record, `calcium_bhasma_pishti`. All names are in `names.other`. Split it if the app needs a separate ID per product.
7. **Records with no interactions.** Dashmool, Swarna bhasma, Cystone and Gandhak rasayan have empty `interactions` because I found no sourced evidence. Dashmool also has no safety flags.
8. **Heavy-metal flag on herbal products.** The flag is also on herbal-only products that are sometimes sold with metals or confused with metal versions: Chyawanprash premium variants, and Yogaraj vs Mahayogaraj guggulu. A reviewer may drop these.
9. **Guggul CYP3A4 direction.** Guggulsterone induces CYP3A through PXR (PMID 15075359). Mahayogaraj guggulu inhibited CYP3A4 in rats (PMID 33436877). The effect text therefore says "may change levels".

## Conflicts between sources
- **Giloy and the liver:** a multicentre Indian study (PMID 35037744) and a case series (PMID 34230786) link giloy to liver injury. The Ministry of AYUSH (PIB, Jul 2021) called this misleading and suggested *Tinospora crispa* misidentification. Both sides are cited in each giloy liver flag.
- **Mahayogaraj guggulu:** a CCRAS rat study found it "generally well tolerated" despite 25.8 µg/g lead, which is above the WHO limit (PMID 21170206). CDC (2015) linked a sample with 4.9% lead to lead poisoning and anaemia.
- **Arogyavardhini:** the rat study concluded there was "no biologically significant" toxicity, yet mercury accumulated in the kidney (PMID 32035767).
- **Swarna bhasma:** rat toxicity studies show low toxicity (PMID 31730889). Gold-containing ("Swarna Yukt") multi-metal products were among those linked to lead poisoning in pregnant women (CDC 2012).
- **Alcohol content:** most arishtas measured 5-13% v/v (PMID 34825559 and Indian J Pharmacol 2006). Kumaryasava measured 0.1-1.9% (PMID 25767329).
- **Chyawanprash and sugar:** the review (PMID 31035513) says it is generally avoided in diabetes because of its sugar, but also cites reports of lower post-meal glucose.
- **Liv.52:** a controlled trial found no benefit in alcoholic liver disease (PMID 12499076). Higher mortality in Child C cirrhosis comes from the Fleig 1997 trial, which was never published. I cite it only through the MDPI review, so it is unverified at source.
- **Diabecon:** in rats, glimepiride showed no pharmacokinetic change but an additive glucose-lowering effect (PMID 36174302). A losartan PK change was non-significant (PMID 39126994), so it was not recorded as an interaction.
- **Arjuna:** in-vitro CYP inhibition (PMID 28962416) conflicts with a ResearchGate "compatibility" study that claims no interaction with cardiovascular drugs. That study is not peer-review indexed and is not cited.
- **Cystone:** two negative trials (Erickson 2011). A manufacturer letter disputes them (PMID 21359878, not cited).
- **BGR-34:** the only clinical trial has manufacturer-affiliated authors (PMID 30302331).

## Regulatory actions found (Patanjali / Coronil)
- **Ministry of AYUSH, 23 Jun 2020** (PIB primary): Patanjali was asked to stop advertising COVID-19 claims pending examination.
- **WHO South-East Asia, Feb 2021:** said it had not reviewed or certified any traditional medicine for COVID-19. Cited through a fact-check site; the primary WHO post was not fetched.
- **Delhi High Court, 29 Jul 2024:** ordered removal of posts calling Coronil a COVID-19 "cure". Cited through LiveLaw.
- **Madras High Court, 2020:** "Coronil" trademark dispute. Cited through The IP Press.
- **Uttarakhand State Licensing Authority, 15 Apr 2024:** suspended the licences of 14 products, including Madhugrit and Madhunashini Vati Extra Power. The order was cancelled on 1 Jul 2024. Cited through LiveLaw and Business Standard.
- **Supreme Court (IMA v Union of India):** contempt proceedings closed on 13 Aug 2024. Cited through SCC Online.

Gaps here:
- No court order was fetched from a court website. All court items come from legal or news reporting, typed `other`.
- Coronil was not on the Uttarakhand list (the Swasari products were).
- I found no regulatory action against BGR-34 or Diabecon.

## Remaining gaps
- No human interaction study exists for any classical formulation as a whole. Most interactions are extrapolated from ingredients: piperine, guggul, ashwagandha, licorice, iron, calcium and alcohol.
- I found no brand-level heavy-metal test data for most products. The flags rely on class-level surveys (Saper 2004/2008) and case reports.
- Kumaryasava: whether it contains loha/tamra bhasma could not be verified. It is marked "check label".
- Talisadi and Avipattikar compositions rely on non-indexed sources (IJAPR PDF, ResearchGate review), typed `other`.
- Mahasudarshan's main herb (*Swertia chirata*) has no good PubMed hypoglycaemia data. The glucose entry relies on giloy animal data and is `minor`.
- `traditional_source_type` is `classical text` for classical products and `brand literature` for branded ones. I did not check the API (Ayurvedic Pharmacopoeia) formulary volumes for this batch.
- Hindi names are common spellings, and Sanskrit names are left blank for branded products. Neither was checked against a standard.
