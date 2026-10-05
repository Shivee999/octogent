# Evidence-based nutrition science for FITme's diet/macro targets (India focus)

Research date: 2026-10-04. Verification legend: claims marked **[verified]** were checked in this session against the primary document (the ICMR-NIN *Dietary Guidelines for Indians 2024* PDF and the Misra et al. 2025 obesity paper were downloaded and text-searched). **[unverified]** marks numbers or URLs recalled from well-known literature that I did not re-open this session. The report writer should treat those as "probably right, check before shipping in-app copy".

---

## 1. BMR/TDEE equations, activity multipliers, South Asian accuracy, adaptive TDEE

### Takeaway
Use Mifflin-St Jeor (MSJ) as the default RMR equation. It is the most accurate general equation, coming within ±10% of measured RMR in about 80% of non-obese adults. It was built mostly on white subjects, so for Indians treat it as a starting guess. Then switch to an adaptive TDEE (intake minus trend-weight change × tissue energy density) once you have about 2–3 weeks of logs. Metabolic adaptation is real but usually small, roughly 50–100 kcal/day beyond what lost mass explains. The Biggest Loser data are an extreme outlier.

### Cited Findings
**Equations (exact forms)**
- Mifflin-St Jeor (1990): men RMR = 10×W(kg) + 6.25×H(cm) − 5×age + 5; women = 10×W + 6.25×H − 5×age − 161. Derived from 498 healthy adults, 19–78 y. — [Mifflin et al., Am J Clin Nutr 1990;51:241–7](https://pubmed.ncbi.nlm.nih.gov/2305711/) [verified formula is standard; PMID not re-opened]
- A systematic review of RMR equations in healthy non-obese and obese adults found MSJ the most reliable. It predicted RMR within 10% of measured in more non-obese and obese people than any other equation, about 82% non-obese and about 75% obese. Most validation subjects were white. — [Frankenfield, Roth-Yousey & Compher, J Am Diet Assoc 2005;105:775–89](https://pubmed.ncbi.nlm.nih.gov/15883556/) [unverified exact percentages]
- A later bias/accuracy study confirmed MSJ (and Livingston) as the most accurate in healthy people, with similar accuracy rates (82% vs 79%). Accuracy is lower in obese than non-obese people. — [Clinical Nutrition 2013, "Bias and accuracy of RMR equations in non-obese and obese adults"](https://www.sciencedirect.com/science/article/abs/pii/S0261561413001003)
- MSJ "was not tested on racial groups other than Caucasian and so may not be accurate for these groups." — summary from the Academy of Nutrition and Dietetics evidence analysis, [ANDEAL RMR guide](https://www.andeal.org/template.cfm?template=guide_summary&key=621) (paraphrased via search snippet; page not fully read).
- Harris-Benedict, Roza & Shizgal 1984 revision: men = 88.362 + 13.397W + 4.799H − 5.677A; women = 447.593 + 9.247W + 3.098H − 4.330A. It tends to overestimate RMR in modern populations. — [Revised Harris–Benedict equation, PMC9967803](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9967803/) (coefficients [unverified] against that page)
- Katch-McArdle: RMR = 370 + 21.6 × lean body mass (kg). It needs a body-fat % input, so its accuracy depends on the BF estimate. Smart-scale BIA error is large. [unverified; standard textbook form, no primary URL found]
- In athletes, a systematic review/meta-analysis found that general equations, including MSJ and Harris-Benedict, underestimate RMR. Fat-free-mass-based equations perform better. — [Accuracy of RMR prediction equations in athletes, Sports Med 2023, PMC10687135](https://pmc.ncbi.nlm.nih.gov/articles/PMC10687135/)
- In a non-Western group (Emirati young women), MSJ was again the most accurate across BMI categories. — [PMC12481887](https://pmc.ncbi.nlm.nih.gov/articles/PMC12481887/)

**Activity multipliers**
- The common app multipliers come from convention, not one validated source: sedentary 1.2, light 1.375, moderate 1.55, very 1.725, extra 1.9 [unverified origin; widely used].
- FAO/WHO/UNU 2004 PAL bands: sedentary/light 1.40–1.69, active/moderate 1.70–1.99, vigorous 2.00–2.40. The ICMR-NIN 2020 requirements use these PAL categories for the Indian reference man (65 kg) and woman (55 kg). [unverified]
- ICMR-NIN 2020 reference energy requirements: sedentary man ~2110 kcal, moderate ~2710, heavy ~3470. Sedentary woman ~1660, moderate ~2130, heavy ~2720. [unverified]. The DGI 2024 sample adult menus include a ~1660 kcal day and a ~2100 kcal day. — [ICMR-NIN DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified that 1660/2100 kcal menus appear]

**Adaptive TDEE (MacroFactor-style)**
- MacroFactor states its expenditure estimate is "a deterministic calculation based on your calorie intake and change in trend weight": Calories in − Change in stored energy = Calories out. It does not publish the energy density or smoothing constants. It notes that partial-day logging (e.g., skipping dinner) biases the estimate. — [MacroFactor help: Expenditure](https://help.macrofactorapp.com/en/articles/20-expenditure) [verified]
- 7700 kcal/kg (3500 kcal/lb) is the classic rule. Hall's Forbes-based analysis shows the energy per kg lost varies with initial body fat and with the fat/lean mix being lost. The 7700 rule overestimates long-term weight loss because it ignores dynamic changes in expenditure. — [Hall, Int J Obes 2008;32:573–6](https://www.researchgate.net/publication/5991461_What_is_the_Required_Energy_Deficit_per_unit_Weight_Loss)
- Hall's model uses tissue energy densities of about 9,400 kcal/kg for fat (≈39.5 MJ/kg) and about 1,800 kcal/kg for lean tissue (≈7.6 MJ/kg). [unverified exact constants; from Hall 2008 and later Hall models]
- The dynamic model gives a rule of thumb: each sustained 10 kcal/day change in intake gives about 0.45 kg (1 lb) eventual weight change in an average adult. About half is reached in roughly 1 year and about 95% in roughly 3 years. — [Hall et al., Lancet 2011, "Quantification of the effect of energy imbalance on bodyweight"](https://pubmed.ncbi.nlm.nih.gov/21872751/) [unverified PMID]
- Weight-trend smoothing: the classic method is an exponentially weighted moving average with 10% smoothing, trend_t = trend_{t−1} + 0.1 × (W_t − trend_{t−1}). — [John Walker, *The Hacker's Diet*](https://www.fourmilab.ch/hackdiet/) [unverified exact page]

**Metabolic adaptation**
- Six years after "The Biggest Loser", contestants' RMR was about 500–700 kcal/day below that predicted for their body composition. — [Fothergill et al., Obesity 2016](https://pubmed.ncbi.nlm.nih.gov/27136388/) [unverified PMID and number]
- Pure calorie counting with the 7700 rule overpredicts weight loss over time. — [Hall 2008](https://www.researchgate.net/publication/5991461_What_is_the_Required_Energy_Deficit_per_unit_Weight_Loss); [LighterLife model test, J Nutr Sci](https://www.cambridge.org/core/journals/journal-of-nutritional-science/article/testing-a-proposed-mathematical-model-of-weight-loss-in-women-enrolled-on-a-commercial-weightloss-programme-the-lighterlife-study/16D465BDCCCFA52B617B3CC35F1BBADE)

### Inferences
- **Recommended algorithm:**
  - Day 0: TDEE₀ = MSJ × activity factor. Indian users may need a −5% "India prior" [no Indian validation found; see Gaps].
  - After ≥14 days with ≥80% of days fully logged:
    - TDEE_obs = mean(intake over window) − (trend_end − trend_start) × ρ / days.
    - ρ is about 7700 kcal/kg by default. Optionally ρ = 7700 for fat loss and a lower value (~5000–6000) for lean gain [inference].
  - Blend the estimates: TDEE_new = TDEE_old + k × (TDEE_obs − TDEE_old), with k ≈ 0.1–0.25 per week.
  - Cap weekly changes at about ±100–150 kcal so noise and missed logs don't make it jump around [design inference].
- Exclude days the user flags as incomplete. Water swings from high-sodium or high-carb Indian meals, and menstrual cycles, are why the EWMA trend matters.
- MacroFactor keeps its constants private, so FITme should document its own and keep them easy to change.

### Gaps
- I found no published validation of MSJ against indirect calorimetry in Asian Indians in this session. The claim that South Asians have lower RMR at the same weight and height is commonly made, but I did not verify it here [unverified].
- MacroFactor's exact ρ and smoothing parameters are not public.

---

## 2. Safe rate of weight loss/gain; calorie floors

### Takeaway
Default fat-loss rate is about 0.5% of body weight per week, with a hard ceiling around 1%/week, which roughly matches 0.5–1 kg/week. Indian guidance specifically says 0.5 kg/week is safe and reduction diets should not fall below 1000 kcal/day. Deficits over 40% of TDEE undermine muscle retention. For gain, use about 0.25–0.5%/week.

### Cited Findings
- ICMR-NIN 2024: "Weight reduction should be gradual. Weight reduction diets should not be less than 1000 Kcal/day and should provide all nutrients. A reduction of half a kilogram body weight per week is considered to be safe. Approaches of rapid weight loss and use of anti-obesity drugs should be avoided." — [ICMR-NIN DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- ICMR-NIN 2024: about 15% energy from protein matters during a 500–750 kcal/day deficit to preserve muscle. "The protective effect of higher-protein diets on muscle mass is compromised if the energy deficit is more than 40% of daily energy needs… advisable not to go beyond 40% energy deficit." — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- India Obesity Commission (Misra et al. 2025): "A daily calorie deficit of roughly 500 kcal is advised"; "A weight loss rate of 0.5–1 kg per week is widely accepted as a safe and effective approach", which needs a 500–1000 kcal/day deficit. Large caloric reductions risk nutrient deficiency, lean-mass loss and regain. — [Misra et al., Diabetes Metab Syndr 2025;19:102989](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) [verified]
- In elite athletes, losing about 0.7% of body weight per week preserved or increased lean mass and strength better than about 1.4%/week. — [Garthe et al., IJSNEM 2011](https://pubmed.ncbi.nlm.nih.gov/21558571/) [unverified PMID/details]
- US NHLBI (1998) and later practice set low-calorie diets for women at about 1000–1200 kcal/day and for men at about 1200–1600 kcal/day. Very-low-calorie diets (<800 kcal) are reserved for medical supervision. [unverified; NHLBI Clinical Guidelines 1998, no URL checked]

### Inferences
- **Defaults:**
  - Loss rate: 0.5%/week, user-selectable 0.25–1.0%.
  - Block or warn above 1%/week, and above 0.5%/week if BMI < 23 (Asian normal range).
  - Deficit: never more than 40% of TDEE (ICMR-NIN).
  - Floors: absolute 1000 kcal/day (ICMR-NIN); soft floor 1200 kcal for women and 1500 kcal for men [inference]. Also never below estimated BMR without a "consult a doctor" acknowledgement [design inference].
  - Gain: 0.25%/week for trained users, 0.5% for novices [inference; no primary source checked].

### Gaps
- I did not retrieve RCT evidence on lean-mass gain rates; the gain defaults are expert convention.

---

## 3. Protein targets, distribution, plant protein quality, Indian vegetarian sources

### Takeaway
ICMR-NIN 2020 sets protein EAR at 0.66 g/kg and RDA at 0.83 g/kg (about 54 g/day for 65 kg). For resistance trainees, about 1.6 g/kg is the evidence-based point beyond which extra protein adds no muscle; 2.2 g/kg is the upper 95% CI. During a cut, higher intake (up to ~2.2 g/kg, or 2.3–3.1 g/kg of fat-free mass for lean athletes) helps preserve muscle. ICMR-NIN cites the same ~1.6 g/kg plateau but discourages protein powders. Indian vegetarian protein quality improves with cereal:pulse at about 3:1 plus dairy.

### Cited Findings
- ICMR-NIN: "The estimated average requirement (EAR) for protein intake is 0.66g of protein per kg/day… RDA… is 0.83g protein/kg/day for healthy men and women… EAR of 43g protein/day or RDA of 54g/day for a person weighing 65kg, regardless of physical activity or gender." — [DGI 2024 (citing ICMR-NIN 2020 NRV)](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- ICMR-NIN on supplements: "Consuming high level of protein, especially in the form of protein supplement powders is not advisable." They note that supplementation gives only small gains and that "protein intake levels greater than ~1.6g/kg/day do not contribute any further to RET-induced gains in muscle mass". Most athletes can meet needs from food. — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- Morton et al. 2018 (49 RCTs, 1,863 participants): protein supplementation increased RT-induced gains in fat-free mass and strength. Gains plateaued at a total intake of 1.62 g/kg/day (95% CI upper bound ≈2.2 g/kg). Age reduced the effect and training experience increased it. — [Morton et al., Br J Sports Med 2018](https://pubmed.ncbi.nlm.nih.gov/28698222/); [PDF](http://breathe-edu-downloads.s3.amazonaws.com/Morton-2018.pdf)
- ISSN position stand: 1.4–2.0 g/kg/day for most exercising people. Intakes above 3.0 g/kg may help body composition in resistance-trained people during a cut. Spread intake as 0.25 g/kg (20–40 g) per meal every 3–4 h. — [Jäger et al., JISSN 2017;14:20](https://jissn.biomedcentral.com/articles/10.1186/s12970-017-0177-8) [unverified exact wording]
- Distribution: for maximal anabolism, eat ≥0.4 g/kg per meal across ≥4 meals to reach ≥1.6 g/kg/day, with an upper target of 0.55 g/kg/meal (≈2.2 g/kg/day). — [Schoenfeld & Aragon, JISSN 2018](https://jissn.biomedcentral.com/articles/10.1186/s12970-018-0215-1) [unverified exact URL]
- During caloric restriction in lean resistance-trained athletes: 2.3–3.1 g/kg of fat-free mass. — [Helms et al., IJSNEM 2014](https://pubmed.ncbi.nlm.nih.gov/24092765/) [unverified PMID]
- Protein quality: ICMR-NIN states that "Appropriate combination of cereals: pulses in a ratio of 3:1 or by substituting 30g of recommended level of pulses with 80g meat per day would improve quality of protein". Its Table 8.2 shows the My Plate vegetarian and non-vegetarian diets meet all essential amino acids. — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- My Plate 2000 kcal vegetarian protein sources: cereals 250 g raw → ~25 g protein; pulses 85 g → ~20 g; milk/curd 300 ml → ~10 g; vegetables 400 g → ~10 g; nuts/seeds 35 g → ~6 g. Total ~72 g, which is 15% of energy. — [DGI 2024 Table 1.2a](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]

### Inferences
- **Defaults:**
  - General users: max(0.83 g/kg, 15% energy). Use 1.0–1.2 g/kg as a "healthy active" default [inference].
  - Users logging resistance training: 1.6 g/kg (range 1.6–2.2).
  - Fat loss: 1.8–2.2 g/kg.
  - Obese users: base targets on goal or adjusted weight, e.g. weight at BMI 23–25, or ~1.2–1.5 g/kg of actual weight [inference]. Otherwise targets get unrealistic.
  - Distribution nudge: 4 meals × ~0.4 g/kg.
- A 70 kg Indian vegetarian lifter needs about 112 g/day at 1.6 g/kg. That is hard on a typical Indian diet. Useful food suggestions: paneer (~18 g/100 g), soy chunks (~52 g/100 g dry), curd/hung curd, milk, dals (~22–24 g/100 g raw), chana/rajma, tofu, eggs for eggetarians, peanuts, sattu, whey [values unverified; take from IFCT 2017].
- Respect the ICMR-NIN stance: present powders as optional, not required.

### Gaps
- DIAAS/PDCAAS for specific dal+rice mixes: I found no primary figure in this session. Do not show a DIAAS number in-app without a source [unverified]. IFCT 2017 (Indian Food Composition Tables) should be the nutrient database source; not checked here.

---

## 4. Carb/fat/fibre defaults; Indian dietary patterns; ICMR-NIN 2024 DGI and 2020 NRV; My Plate

### Takeaway
ICMR-NIN 2024 recommends 50–55% energy from carbohydrate, 10–15% from protein and 20–30% from fat. Cereals should supply at most 45% of energy and pulses/eggs/flesh foods about 14–15%. Actual Indian intake is cereal-heavy (50–70% of energy from cereals) and protein-light (6–9% from pulses, meat and fish). The DGI attribute 56.4% of India's disease burden to unhealthy diets.

### Cited Findings
- "A balanced diet should provide not more than 45% calories (energy) from cereals and millets… and up to 15% calories from pulses, beans and meat… this will ensure 50%–55% of total calories from carbohydrates, 10%–15% from proteins and 20%–30% from dietary fats." — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- "As per the data, cereals contribute to 50% to 70% of total energy per day. Pulses, meat, poultry and fish together contribute to 6% to 9% of the total energy per day as against the recommended intake level of 14%." — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- "Estimates show that 56.4% of total disease burden in India is due to unhealthy diets… prevent up to 80% of type 2 diabetes." — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- **My Plate for the Day, 2000 kcal vegetarian (raw g/day → % energy):**

  | Food group | Raw amount | % energy |
  |---|---|---|
  | Cereals incl. millets | 250 g | 42% |
  | Pulses | 85 g | 14% |
  | Milk/curd | 300 ml | 11% |
  | Vegetables + GLV | 400 g | 9% |
  | Fruits | 100 g | 3% |
  | Nuts & seeds | 35 g | 9% |
  | Fats & oils | 27 g | 12% |

  Totals: ~72 g protein (15% energy), ~66 g fat (30%), carbohydrate 55%. "Vegetables, fruits, green leafy vegetables, tubers and roots" make up about half the plate. At least half the cereals should be whole grains or millets, with millets at 30–40% of cereals. Sugar is limited to 25–30 g/day (<5% energy). Salt is <5 g/day (2 g sodium). — [DGI 2024 Table 1.2a, Guidelines 11 & 15](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- Fibre: the DGI pregnancy section advises "around 25 g/1000 Kcal" of fibre-rich foods [verified wording in context]. ICMR-NIN 2020 suggests about 30 g fibre per 2000 kcal [unverified]. EFSA sets an adequate fibre intake of 25 g/day for adults [unverified].
- Misra et al. 2025: "Carbohydrate consumption in Asian Indians is high"; increasing protein may also correct poor protein nutrition in India. Intermittent fasting causes weight loss, but "its advantage over long-term vs. calorie-restrictive diets is doubtful". — [Misra et al. 2025](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) [verified]
- ICMR-INDIAB nationally representative data: carbohydrate is about 62% of energy and protein about 12%. The ICMR-INDIAB-17 analysis suggested that lowering carbohydrate to ~50–56% and raising protein to ~15–20% of energy is associated with diabetes remission or prevention. — [Anjana et al., Diabetes Care 2024](https://diabetesjournals.org/care) [unverified: numbers and exact URL]. Related: [I-STARCH-1 macronutrient intake study, medRxiv 2025](https://www.medrxiv.org/content/10.1101/2025.11.04.25339356.full.pdf) (not read in full).
- An IJMR review compares the DGI 2024 with other countries' guidelines. — [IJMR](https://ijmr.org.in/dietary-guidelines-across-different-countries-comparisons-to-dietary-guidelines-for-indians-2024/)

### Inferences
- **Default macro split for general users:** carbohydrate 50%, protein 15–20% (or the g/kg target), fat 25–30%.
  - Fit-focused users: set protein in g/kg, set fat at 20–30% of kcal (and at least 0.6 g/kg [inference]), and give carbohydrate the remainder.
  - Add a "Cereal share" insight that compares the user's cereal kcal against the 45% cap. It is a distinctive India-specific nudge.
- Fibre target: 14 g/1000 kcal (IOM style) or 25–30 g/day [inference that both fit Indian guidance].

### Gaps
- The full ICMR-NIN 2020 NRV table (EAR/RDA for every nutrient) was not opened. The NIN short report should be checked: https://www.nin.res.in/RDA_short_Report_2020.html [unverified URL].

---

## 5. Asian/Indian BMI and waist cutoffs; diabetes risk; app implications

### Takeaway
For Indian users, show Asian cutoffs.
- **BMI:** normal 18.5–22.9, overweight 23–24.9, obesity ≥25.
- **Waist:** ≥90 cm in men or ≥80 cm in women, or waist-to-height ratio >0.5.

The 2025 India Obesity Commission redefined obesity in two stages: BMI >23 alone is Stage 1, and Stage 2 adds abdominal adiposity plus functional limits or comorbidity.

### Cited Findings
- Misra et al. 2025 (India Obesity Commission Delphi):
  - Stage 1 obesity is BMI >23 kg/m² without effects on organ function or daily activity.
  - Stage 2 needs BMI >23 (mandatory), plus WC or W-HtR, plus at least one functional limitation or obesity-related comorbidity.
  - BMI grades: normal 18.5–22.99; Grade I 23–24.9; Grade II 25–27.5; Grade III 27.6–32.4; Grade IV ≥32.5.
  - WC cutoffs ≥90 cm in men and ≥80 cm in women; W-HtR cutoff >0.5. W-HtR is preferred over waist-to-hip ratio.
  - Body-fat cutoffs >25.5% for men and >38% for women.
  - Pharmacotherapy can be considered at BMI ≥27.5.
  — [Misra et al., Diabetes Metab Syndr Clin Res Rev 2025;19:102989](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) [verified]
- 2009 Indian consensus: overweight BMI 23–24.9, obesity ≥25; abdominal obesity WC ≥90 cm in men and ≥80 cm in women. — [Misra et al., JAPI 2009 consensus](https://www.academia.edu/22340953/Consensus_Statement_for_Diagnosis_of_Obesity_Abdominal_Obesity_and_the_Metabolic_Syndrome_for_Asian_Indians_and_Recommendations_for_Physical_Activity_Medical_and_Surgical_Management)
- WHO expert consultation (2004): Asian public-health action points at BMI 23 (increased risk) and 27.5 (high risk). — [WHO Expert Consultation, Lancet 2004;363:157–63](https://pubmed.ncbi.nlm.nih.gov/14726171/) [unverified PMID]
- The DGI 2024 report NFHS-5 adult overweight/obesity using WHO Asian cut-offs: men 22.9% and women 24.0% in 2021. Chronic energy deficiency (CED) is 16.2% in men and 18.7% in women, so India has a dual burden. Among adolescents (CNNS), 10.4% have prediabetes. — [DGI 2024 Tables I–II](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]

### Inferences
- If the user's region or ethnicity is Indian/South Asian, default to Asian BMI bands and capture waist circumference. Show W-HtR as the main central-adiposity metric because it needs no sex-specific cutoff.
- Suggested goal weight: no lower than BMI 18.5. Default suggestion is the upper end of BMI 22.9 for users above it [inference].
- Because of the dual burden, the app must also handle underweight users (BMI <18.5): disable deficit goals and offer a gain goal.

### Gaps
- None material.

---

## 6. Glycemic index/load of Indian staples; is showing GI useful?

### Takeaway
GI is real but depends heavily on context: variety, processing, fermentation, cooling, and what it is eaten with. In Indian RCTs, swapping white rice for brown rice, or adding legumes, cut 24 h glycemic response by about 20–23%. Showing raw GI numbers per food is low-value and error-prone. Meal-level nudges are more defensible: add dal or protein, choose whole grain or millet, keep cereal portions moderate.

### Cited Findings
- Overweight Asian Indians, crossover RCT using continuous glucose monitoring: 5-day average IAUC was 19.8% lower with brown rice than white rice (P=0.004), and 22.9% lower with brown rice plus legumes (P=0.02). — [Mohan et al., brown vs white rice in overweight Asian Indians](https://www.researchgate.net/publication/259845530_Effect_of_Brown_Rice_White_Rice_and_Brown_Rice_with_Legumes_on_Blood_Glucose_and_Insulin_Responses_in_Overweight_Asian_Indians_A_Randomized_Controlled_Trial)
- A high-fiber rice diet lowered 24 h glycemic response on CGM in Asian Indians. — [Anjana et al., Diabetes Technol Ther 2019](https://pubmed.ncbi.nlm.nih.gov/30844309/)
- A brown-for-white rice substitution RCT on diabetes risk factors in India was published in the British Journal of Nutrition. — [BJN](https://www.cambridge.org/core/journals/british-journal-of-nutrition/article/substituting-brown-rice-for-white-rice-on-diabetes-risk-factors-in-india-a-randomised-controlled-trial/A0778FC028F6F25D0E6A73787EECECC4)
- Rice processing changes rapidly available glucose; idli fermentation is discussed. — [PMC6683079](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6683079/)
- Commonly quoted values (secondary sources only, low reliability): white rice ~73–79, chapati ~62–66, rice idli up to ~85, rice dosa ~76, upma ~71. Fermentation, fat, protein and cooling lower glycemic response. — [InDiabetes chart](https://www.indiabetes.in/glycemic-index-chart-for-indian-foods) (secondary; values [unverified]). The authoritative source is the international GI tables: [Atkinson et al., AJCN 2021](https://pubmed.ncbi.nlm.nih.gov/34258626/) [unverified PMID].

### Inferences
- Do not show GI as a precise per-food number from the AI estimator. If shown at all, use Low/Medium/High bands taken only from Atkinson 2021 tables. Prefer glycemic load per serving, since it reflects portion size.
- Nudges with stronger evidence for Indian users: add dal or legumes to rice, replace part of the rice with brown rice or millets, eat vegetables first, and cap cereal share.

### Gaps
- I did not retrieve a verified primary Indian-food GI table in this session.

---

## 7. Hydration targets

### Takeaway
EFSA total water adequate intakes (AI) are 2.5 L/day for men and 2.0 L/day for women. About 70–80% of that should come from drinks, which means roughly 2.0 L and 1.6 L of fluid. The IOM values are higher: 3.7 L and 2.7 L total water. ICMR-NIN advises about 2 L/day for adults and more than 2 L in pregnancy. Indian heat and sweat losses justify adding about 0.5–1 L on hot or workout days.

### Cited Findings
- EFSA: AI total water 2.0 L/day for women (P95 3.1 L) and 2.5 L/day for men (P95 4.0 L). 70–80% comes from beverages and 20–30% from food. Pregnancy adds 300 mL/day and lactation about 700 mL/day. — [EFSA Scientific Opinion on DRVs for water, EFSA J 2010;8(3):1459](https://www.efsa.europa.eu/en/efsajournal/pub/1459); [PDF mirror](https://www.sennutricion.org/media/Docs_Consenso/Scientific_Opinion_Dietary_Reference_Values_for_water-EFSA_2010.pdf)
- IOM/NASEM 2005: AI total water 3.7 L/day for men and 2.7 L/day for women (about 3.0 L and 2.2 L as beverages). — [NASEM DRI for Water, Potassium, Sodium, Chloride, Sulfate (2005)](https://nap.nationalacademies.org/catalog/10925) [unverified exact URL]
- ICMR-NIN DGI 2024: "Adequate water (two litres/day) should be consumed". In pregnancy, "plenty of fluids (over 2 litres per day)". — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]

### Inferences
- **Default fluid target:**
  - Men: 2.5 L. Women: 2.0 L. Alternative: ~35 mL/kg, clamped to 1.5–3.5 L [inference].
  - +0.5 L per hour of exercise [inference; ACSM-style individualised replacement].
  - +0.5 L on hot days, using weather or location if permission is given [inference].
  - Pregnancy +0.3 L; lactation +0.7 L (EFSA).
- Guardrail: no target above about 4 L without context, and warn against drinking excessive volumes quickly (hyponatraemia). Users with heart failure or kidney disease on fluid restriction need a "follow your doctor's limit" option.

### Gaps
- No India-specific climate adjustment formula was found from an official body.

---

## 8. Micronutrients commonly deficient in India

### Takeaway
Anaemia affects 57% of women and 25% of men (NFHS-5). Among adolescents (CNNS), about 31% are B12-deficient, about 36% folate-deficient, about 24% vitamin D deficient and about 32% zinc-deficient. Vegetarian diets raise the B12 risk. The app should track iron, B12, calcium and vitamin D for flagged users and give food-first tips, not supplement doses.

### Cited Findings
- NFHS-5 (2019–21) anaemia: women 15–49 y 57.0%; men 15–49 y 25.0%; children 6–59 months >67%. — [Factly summary of NFHS-5](https://factly.in/data-nfhs-5-findings-reveal-increase-in-anaemia-prevalence-in-children-women-across-most-states/); [PIB Anaemia Mukt Bharat](https://www.pib.gov.in/PressReleasePage.aspx?PRID=1795421)
- CNNS 2016–18, as reproduced in DGI 2024 Table I. — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]

  | Deficiency | 1–4 y | 5–9 y | 10–19 y |
  |---|---|---|---|
  | B12 | 13.8% | 17.2% | 30.9% |
  | Vitamin D (25-OH-D) | 13.7% | 18.2% | 23.9% |
  | Zinc | 19.0% | 16.8% | 31.7% |
  | Vitamin A | 17.5% | 21.5% | 15.6% |

- CNNS B12 deficiency (serum B12 <203 pg/mL): 13.8% at 1–4 y, 17.3% at 5–9 y, 31.0% at 10–19 y. Folate deficiency (erythrocyte folate <151 ng/mL): 22.8%, 27.6% and 35.6% respectively. Predominantly plant-based or cereal-based diets were linked to deficiency. — [Shalini et al., Nutrients 2023;15:3026](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10346745/) [verified]
- ICMR-NIN notes that vegetarian diets make B12 and long-chain n-3 PUFA a challenge. B12 can come from curd, eggs and flesh foods, and milk has small amounts. Sunlight exposure is needed for vitamin D. — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified wording]
- ICMR-NIN 2020 RDAs [unverified]: iron 19 mg/day for men and 29 mg/day for women; calcium 1000 mg/day; vitamin D 600 IU (15 µg); B12 2.2 µg/day; folate 300 µg (men) and 220 µg (women).

### Inferences
- Micronutrient insights for vegetarians: a B12 food-source counter (dairy, curd, eggs, fortified foods) plus "consider testing B12" after long-term vegan or vegetarian logging.
- Iron: pair iron sources with vitamin C, and keep tea or coffee away from meals (well-established, not verified here).
- Women of reproductive age: iron focus.
- Never give dosing advice. Route to a doctor for supplementation.

### Gaps
- NFHS-5 primary report PDF not opened (summaries used). Adult (non-adolescent) vitamin D and B12 national prevalence: no nationally representative source found.

---

## 9. Special populations and guardrails

### Takeaway
Calorie tracking is linked to eating-disorder (ED) symptoms in vulnerable users: 73% of an ED sample said MyFitnessPal contributed to their ED. Minors, pregnancy, insulin- or sulfonylurea-treated diabetes, chronic kidney disease (CKD), and ED history all need gating or modified targets with "consult a doctor" prompts.

### Cited Findings
- **Eating disorders.** Of 105 people with EDs, 75% used MyFitnessPal and 73% said it contributed to their ED. About 30–35% felt it contributed "largely". — [Levinson, Fewell & Brosof, Eating Behaviors 2017;27:14–16](https://www.sciencedirect.com/science/article/abs/pii/S1471015317301484)
- Men using MFP showed associations with ED symptoms and psychosocial impairment. — [Eating Behaviors 2018](https://www.sciencedirect.com/science/article/abs/pii/S147101531830326X)
- A 2025 systematic review covers associations between fitness/diet tracking technology and disordered eating. — [PMC12547374](https://pmc.ncbi.nlm.nih.gov/articles/PMC12547374/)
- A qualitative study on diet apps and ED behaviours. — [BJPsych Open](https://www.cambridge.org/core/journals/bjpsych-open/article/effects-of-diet-and-fitness-apps-on-eating-disorder-behaviours-qualitative-study/2D1EE739D97AB3EFC6573835E4C527BD)
- A qualitative analysis of online forums on MFP use in EDs. — [McCaig et al., IJED 2020](https://onlinelibrary.wiley.com/doi/10.1002/eat.23205)
- **Minors.** The AAP advises against dieting, weight talk and calorie counting for adolescents. Focus on healthy family behaviours. — [Golden et al., Pediatrics 2016;138:e20161649](https://publications.aap.org/pediatrics/article/138/3/e20161649) [unverified URL]
- **Pregnancy.** ICMR-NIN adds 350 kcal/day for normal pregnancy weight gain, or 450 kcal if undernourished. Fluids >2 L. Overweight pregnant women should avoid added sugar and cut refined cereal and oil, not diet. — [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) [verified]
- **CKD.** KDOQI 2020: for metabolically stable CKD stages 3–5 not on dialysis and without diabetes, 0.55–0.6 g/kg/day protein (or 0.28–0.43 g/kg with keto-analogues). With diabetes, 0.6–0.8 g/kg. — [KDOQI Clinical Practice Guideline for Nutrition in CKD 2020, AJKD](https://www.ajkd.org/article/S0272-6386(20)30726-5/fulltext) [unverified exact numbers/URL]. High-protein defaults (1.6–2.2 g/kg) are contraindicated.
- **Diabetes on insulin or sulfonylureas.** Calorie restriction or fasting raises hypoglycaemia risk, and medicines need adjusting under clinician supervision. — [ADA Standards of Care](https://diabetesjournals.org/care/issue) [unverified specific section]

### Inferences
**Onboarding screen:**
- Age <18: no deficit targets, no calorie numbers by default; show food-group or My Plate guidance.
- Pregnant or breastfeeding: disable deficits and add +350 kcal (2nd/3rd trimester per ICMR) or a lactation add-on. Prompt to see an OB.
- ED history (current or past): hide numbers ("no-numbers mode"), disable deficit goals, remove streak pressure and "over budget" red colours. Show crisis resources, e.g. India's Tele-MANAS 14416 [unverified number].
- Diabetes on insulin or sulfonylurea: a warning before any deficit or intermittent fasting, plus a doctor prompt.
- CKD, liver disease or gout: cap protein at 0.8 g/kg and show a doctor prompt.

**Ongoing detection, which triggers a soft check-in rather than blocking:**
- BMI <18.5, or a goal weight below BMI 18.5.
- Logged intake <1000 kcal for ≥3 days.
- Weekly loss >1%.
- Repeated "compensatory exercise" patterns [design inference].

**Wording:** neutral, no "good/bad foods", no "cheat meals".

### Gaps
- No RCT evidence was found on which specific app guardrails reduce harm. The guardrail list above is expert and design inference.

---

## 10. Intermittent fasting

### Takeaway
Intermittent fasting (IF) gives about the same weight loss as continuous calorie restriction. In a 2025 BMJ network meta-analysis of 99 RCTs, only alternate-day fasting beat continuous restriction, and only modestly (−1.29 kg). Time-restricted eating did not. IF is fine as an optional scheduling feature, not a superior method. Gate it for people with diabetes on medication, pregnancy, minors and ED history.

### Cited Findings
- BMJ 2025 network meta-analysis (99 RCTs, 6,582 adults):
  - All IF strategies and continuous energy restriction reduced weight vs unrestricted intake.
  - Only alternate-day fasting beat continuous restriction: mean difference −1.29 kg (95% CI −1.99 to −0.59).
  - Time-restricted eating and whole-day fasting did not outperform continuous restriction.
  — [Semnani-Azad et al., BMJ 2025](https://www.researchgate.net/publication/392802015_Intermittent_fasting_strategies_and_their_effects_on_body_weight_and_other_cardiometabolic_risk_factors_systematic_review_and_network_meta-analysis_of_randomised_clinical_trials); [Science Media Centre expert reaction](https://www.sciencemediacentre.org/expert-reaction-to-study-comparing-evidence-on-intermittent-fasting-and-traditional-calorie-reduction-diets-for-weight-loss/) (author names [unverified])
- India Obesity Commission: IF "has been shown to cause weight loss but its advantage over long-term vs. calorie-restrictive diets is doubtful". — [Misra et al. 2025](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) [verified]
- Meta-analysis of IF effects on appetite. — [PMC10255792](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10255792/) (not read in full)

### Inferences
- An IF eating-window feature fits culturally: religious fasts (Navratri, Ramadan, Ekadashi) are common in India. Frame it as a scheduling or adherence tool within the same calorie target.
- Add hypoglycaemia warnings for medicated diabetics.

### Gaps
- No India-specific IF RCTs retrieved.

---

## 11. Summary of recommended app defaults (synthesis)

### Takeaway
A defensible default rule set exists from the sources above. It is tabulated below.

### Cited Findings

| Parameter | Default | Source |
|---|---|---|
| RMR | Mifflin-St Jeor | [Frankenfield 2005](https://pubmed.ncbi.nlm.nih.gov/15883556/) |
| TDEE | RMR × activity factor, then adaptive after 14 days | [MacroFactor](https://help.macrofactorapp.com/en/articles/20-expenditure), [Hall 2008](https://www.researchgate.net/publication/5991461_What_is_the_Required_Energy_Deficit_per_unit_Weight_Loss) |
| Loss rate | 0.5%/week (max 1%); ICMR-NIN says 0.5 kg/week | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Max deficit | 40% of TDEE | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Calorie floor | ≥1000 kcal absolute | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Protein (general) | ≥0.83 g/kg | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Protein (resistance training) | 1.6 g/kg (to 2.2) | [Morton 2018](https://pubmed.ncbi.nlm.nih.gov/28698222/) |
| Macro split (general) | C 50–55 / P 10–15 (≥15 in deficit) / F 20–30% | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Added sugar | <25–30 g (<5% energy) | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| Salt | <5 g/day | [DGI 2024](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf) |
| BMI bands | 18.5 / 23 / 25 | [Misra 2025](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) |
| Waist | ≥90 cm men, ≥80 cm women; W-HtR >0.5 | [Misra 2025](https://www.cmcendovellore.org/pub/2025/revised-definition-of-obesity-in-asian-indians-living-in-india.pdf) |
| Water | 2.5 L men, 2.0 L women total water | [EFSA 2010](https://www.efsa.europa.eu/en/efsajournal/pub/1459) |

### Inferences
- The main India-specific differentiators FITme can encode:
  - Asian BMI and waist bands.
  - A cereal-share cap of 45% of energy.
  - A protein-gap nudge, since actual intake is 6–9% of energy from pulses, meat and fish.
  - A B12 watch for vegetarians.
  - An anaemia-aware iron insight for women.
  - Fasting-festival awareness.

### Gaps
- Items marked [unverified] above (ICMR 2020 RDAs, PAL tables, KDOQI numbers, several PMIDs) should be confirmed against the primary documents before they appear in user-facing copy.
