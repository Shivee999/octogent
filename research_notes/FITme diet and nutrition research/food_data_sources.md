# Food Composition Databases and Food Data APIs for an Offline-First iOS Nutrition App (FITme), with Emphasis on Indian Foods

Research date: 2026-10-04. Every claim has an inline source. [unverified] marks claims taken only from secondary or aggregator sources, or that I could not confirm against a primary page.

## Q1. Indian sources: IFCT 2017, INDB (2024), other ICMR-NIN data, Anuvaad, Kaggle datasets

### Takeaway
IFCT 2017 is the authoritative Indian dataset: 528 foods, 151 components, lab-analysed. Its copyright notice explicitly forbids storing or reproducing it "in any electronic format for creating a product" without prior written permission from ICMR-NIN, so bundling it in a commercial app needs a written licence from NIN. INDB (Anuvaad, 2024) is the best recipe-level Indian dataset: 1,014 recipes and 1,095 raw foods. It is described as "open access" and its paper is CC BY, but its ingredient values come mostly from IFCT 2017/2004. Neither the Anuvaad download page nor the repo states a data licence or any permission from NIN. Commercial bundling of INDB values is therefore legally unclear. Kaggle mirrors of INDB that relabel it CC BY-SA 4.0 add risk and remove none.

### Cited Findings
**IFCT 2017 (ICMR-NIN)**
- IFCT 2017 gives nutrient values for 528 key Indian foods and 151 food components: proximates, dietary fibre, water- and fat-soluble vitamins, carotenoids, minerals and trace elements, starch and sugars, fatty acids, amino acids, organic acids, polyphenols, oligosaccharides, phytosterols, saponins and phytate, in 12 tables. — [Zenodo ifct2017 record](https://zenodo.org/records/7088653); [Vikaspedia summary](https://agriculture.vikaspedia.in/viewcontent/health/nutrition/nutritive-value-of-foods/indian-food-composition-tables?lgn=en)
- Each food was composite-sampled from six regions of India to represent the national food supply. — [Vikaspedia summary](https://agriculture.vikaspedia.in/viewcontent/health/nutrition/nutritive-value-of-foods/indian-food-composition-tables?lgn=en)
- Citation: Longvah T., Ananthan R., Bhaskarachary K., Venkaiah K. (2017), Indian Food Composition Tables 2017, NIN-ICMR, Hyderabad. The official PDF is 585 pages and about 12.4 MB. It is encrypted to block text copying ("copy:no"), which I confirmed with pdfinfo on the downloaded file. — [NIN IFCT2017.pdf](https://www.nin.res.in/ebooks/IFCT2017.pdf)
- **Copyright notice, verbatim from the IFCT 2017 PDF front matter:** "Copyright © 2017 by National Institute of Nutrition … The use and dissemination of the data in this book is encouraged. This publication can be reproduced for personal use with full acknowledgment of the source. However, no part of this publication can be stored or reproduced in any electronic format for creating a product without the prior written permission of the National Institute of Nutrition, Hyderabad." Contacts listed: nin@ap.nic.in and ifct2017@gmail.com. — [NIN IFCT2017.pdf](https://www.nin.res.in/ebooks/IFCT2017.pdf)
- Third-party machine-readable copies exist. One example is the `ifct2017` npm/JS package by Subhajit Sahu and Abhishek Sahu (v2.0.10, Sept 2022), listed on Zenodo with licence "Other (Open)". The Zenodo page does not address the copyright of the underlying NIN data. — [Zenodo ifct2017 record](https://zenodo.org/records/7088653)
- The same restrictive notice ("…no part … can be stored or reproduced in any electronic format for creating a product without the prior written permission…") appears in NIN's Dietary Guidelines for Indians 2024. This is NIN's standard copyright stance. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)

**Indian Nutrient Databank (INDB), 2024**
- Developed by Anuvaad Solutions with Prof. Lindsay Jaacks (University of Edinburgh) and funded by the Bill & Melinda Gates Foundation. The methods paper is in *Current Developments in Nutrition* (2024). — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795); [CDN full text](https://cdn.nutrition.org/article/S2475-2991(24)01724-4/fulltext); [Anuvaad on X](https://x.com/anuvadsolutions/status/1808765430556672504)
- Contents: 1,095 raw food items and 1,014 recipes, with more than 40 nutrients (macros, minerals, vitamins, fatty acids). — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- Raw-food sources: IFCT 2017 (528 items) as the primary source, gaps filled from IFCT 2004 (369 items), the UK food composition tables (144 ingredients) and USDA (54 ingredients). — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- Recipes came from two University of Delhi food-preparation manuals (1,124 recipes before removing 258 duplicates) plus 148 recipes from food blogs. — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- The Anuvaad page describes INDB as "open-access", with 1,014 recipes "presented per 100g and per serving size". The download is the Excel file "Anuvaad_INDB_2024.11.xlsx". The page states no licence, no terms of use and nothing on commercial use or IFCT permission. — [Anuvaad INDB page](https://www.anuvaad.org.in/indian-nutrient-databank/)
- The paper says analysis code and files are on GitHub and the article is CC BY. CC BY there covers the article. Whether it extends to the IFCT-derived nutrient values is not stated. — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- The GitHub repo (lindsayjaacks/Indian-Nutrient-Databank-INDB-) contains INDB.xlsx, UK_fct.xlsx, US_fct.xlsx, recipes.xlsx, recipes_servingsize.xlsx, USDA_nrf.xlsx, Units.xlsx and Stata code (INDB.do). Its README says the IFCT 2017 and 2004 data "must be requested from the original source". The fetched page showed no LICENSE file. — [GitHub INDB repo](https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-)

**Kaggle Indian food datasets: provenance and licence risk** (metadata pulled from Kaggle's public API on 2026-10-04)
- "Indian Food Nutritional Values Dataset (2025)" (batthulavinay): licence shown as **CC BY-SA 4.0**, 250+ dishes, 87.5 KB. Its description says it "was sourced from Anuvaad Indian Nutrient Database (INDB), processed, and cleaned". — [Kaggle batthulavinay/indian-food-nutrition](https://www.kaggle.com/datasets/batthulavinay/indian-food-nutrition)
- "Indian Food Nutrition" (syedkhalid076, 2022): licence **"Unknown"**, per-100g values, provenance not stated, described as "not properly cleaned". — [Kaggle syedkhalid076/indian-food-nutrition](https://www.kaggle.com/datasets/syedkhalid076/indian-food-nutrition)
- "Indian Food 101" (nehaprabhavalkar): licence "Data files © Original Authors". It covers 255 dishes with ingredients, diet, region and prep time, and has no nutrient values. — [Kaggle nehaprabhavalkar/indian-food-101](https://www.kaggle.com/datasets/nehaprabhavalkar/indian-food-101)

### Inferences
- **IFCT 2017 cannot be bundled in a commercial app without written NIN permission.** The notice addresses electronic products directly. The path is to email NIN (ifct2017@gmail.com / nin@ap.nic.in) and ask for a written licence. Expect slow or no response; that is an inference, not something I could verify.
- **INDB's legal status for commercial bundling is unclear.** Its recipe values are computed largely from IFCT data. The repo itself won't redistribute IFCT, telling users to request it from NIN. That suggests the authors did not treat IFCT values as freely redistributable, yet Anuvaad's Excel contains IFCT-derived recipe totals. Whether computed recipe aggregates count as "reproducing" IFCT is a legal question these sources do not answer. Recommendation: email Anuvaad and Prof. Jaacks to ask for an explicit data licence and whether NIN cleared redistribution.
- Kaggle relabelling (e.g., CC BY-SA 4.0 on INDB-derived data) is not a valid grant. The uploader cannot license rights they do not hold. Any Kaggle dataset with "Unknown" or missing provenance is a legal and data-quality liability. Avoid it.
- Numbers you calculate yourself from first principles do not copy any database: your own recipes, using CC0 USDA or OGL UK ingredient values. This is the cleanest legal route to Indian dish coverage (see Q2 and Q8).

### Gaps
- I found no public ICMR-NIN licensing or permission page, fee schedule, or record of commercial apps licensing IFCT 2017.
- I found no separate ICMR-NIN *recipe* database. NIN has published recipe-based glycemic-carbohydrate values (DGI 2024 Annexure III), but I found no downloadable NIN recipe database.
- I could not reach the INDB GitHub repo's LICENSE file through the API (access restricted in this environment). The fetched page did not show one [unverified].
- "Anuvaad" here is Anuvaad Solutions (anuvaad.org.in). I found no other open Indian composition datasets with clear licences. Anuvaad also has an "Indian Diet Data" page, which I did not examine.

## Q2. Recipe-level Indian dishes: computing homemade dishes, yield factors, oil variability; household portion measures

### Takeaway
The standard method, used by FAO/INFOODS, EuroFIR and INDB, sums ingredient nutrients and then adjusts for weight change on cooking (yield factor) and nutrient loss (retention factor). INDB applied USDA retention factors but **not** yield factors. That is a stated limitation and matters for dishes reported per 100 g cooked. NIN's Dietary Guidelines for Indians 2024 give an official household-measure reference: a medium katori of 200 ml (also 360, 155 and 115 ml katoris), 15 g tablespoon, 5 g teaspoon. I found no official NIN table of standard roti diameter or weight, or ladle volume.

### Cited Findings
- Yield factor (YF) is the percentage weight change of a food or recipe on cooking. Retention factor (RF) is the percentage of a nutrient preserved after preparation, cooking or reheating. A recipe can be calculated with YF/RF at recipe level ("recipe method") or with YF at recipe level and RF at ingredient level ("mixed method"). YF/RF can come from weighing before and after cooking, from ingredient YFs, or from references such as EuroFIR. — [FAO food composition: recipes and other calculations](https://www.fao.org/fileadmin/templates/food_composition/documents/Presentations/Food_Composition_-_Recipes_and_other_calculations.pdf); [EuroFIR recipe calculation procedures (Vásquez-Caicedo et al. 2007)](https://www.fao.org/uploads/media/vasquez-caicedo_et_al__2007_recipe_rulesD2.2.9_02.pdf)
- FAO/INFOODS food-matching guidance on matching dietary-survey foods to composition-table entries. — [INFOODS Guidelines for Food Matching v1.2](https://www.fao.org/fileadmin/templates/food_composition/documents/upload/INFOODSGuidelinesforFoodMatching_version_1_2.pdf)
- INDB applied USDA nutrient retention factors (Release 6, 2007) and matched 42.62% of recipe ingredients. Vitamin C retention ranged 20–100%; calcium and zinc retention was highest (75–100%). INDB does **not** apply yield factors for cooking weight change, and serving sizes are missing for pickles/preserves and weaning foods. — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795); [GitHub INDB repo](https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-)
- **NIN DGI 2024 Annexure I, "Suggested measuring katori/cups and spoons":** large katori C6 = 360 ml; medium katori C7 = 200 ml; small katori C8 = 155 ml; small katori C9 = 115 ml; tablespoon 15 g; teaspoon 5 g. Of 12 standard cups (C1 = 1500 ml down to C12 = 25 ml), "only 4 cups i.e., C6, C7, C8, C9 were used here as these are most commonly used in households." Weights were measured on a Seca Culina 852 kitchen scale. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
- DGI 2024 states: "Due to substantial variances in home measures such as measuring cups, spoons, or katoris, it is difficult to collect accurate information regarding food intake." Its meal tables use "1 cup/Katori = 200ml". Annexure II gives raw-food weights in household measures (e.g., rice 10 g ≈ 2 teaspoons; 3/4 of a medium 200 ml katori of spinach ≈ 20 g), and its quantities are for raw ingredients. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
- DGI 2024 sample menus list phulka portions by weight (e.g., "Phulka (60g)", "Phulka (100g)") as meal servings, not a per-piece standard. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
- A secondary source says a typical steel katori holds 150–180 ml, and that apps often use 150 g for sabzi or rice. — [search summary of DGI-related sources; unverified]

### Inferences
- In-app recipe builder: store every recipe as raw-ingredient grams plus a cooked total weight, entered by the user or defaulted, to get a per-100 g cooked value. Apply retention factors only if micronutrients matter; for macro and kcal tracking, YF (water gain or loss) is what matters.
- Added fat is the largest error source in Indian home cooking (tadka, frying, ghee on roti). Make "oil used (tsp/tbsp)" an explicit, editable recipe field rather than a hidden constant. A 5 g teaspoon of oil is about 45 kcal (9 kcal/g × 5 g), and 1–3 teaspoons per serving is a plausible range. That kcal figure is arithmetic, not from a source.
- Use the NIN katori volumes (200 ml medium, 155/115 ml small, 360 ml large) as the app's portion presets and cite DGI 2024. Volume-to-weight conversion depends on the food, so store a grams-per-katori value per dish.

### Gaps
- I found no official NIN standard for roti or chapati diameter and weight per piece, or for ladle (karchi) volume. Apps use ad-hoc values [unverified].
- I found no Indian-specific yield or retention factor table. USDA RF Release 6 is the de facto substitute.
- I found no published comparison of how commercial apps (e.g., HealthifyMe) compute Indian recipes.

## Q3. USDA FoodData Central (FDC)

### Takeaway
FDC is CC0 / public domain. Commercial use and offline bundling are allowed with no permission needed; a citation is requested. Foundation Foods and SR Legacy are small enough to bundle (single-digit to tens of MB zipped). Branded Foods (~195–428 MB zipped) is too big to bundle whole and is US-centric. FDC has few Indian dishes but is the best free source for generic ingredients used in recipe calculations.

### Cited Findings
- Licence: FDC data are "in the public domain and they are not copyrighted", released under CC0 1.0 Universal. No permission is needed; attribution is requested as "U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, [year]. fdc.nal.usda.gov." — [FDC API Guide](http://fdc.nal.usda.gov/api-guide/)
- API limits: default 1,000 requests per hour per IP. DEMO_KEY is limited to 30 per hour and 50 per day. Free keys come from api.data.gov. — [FDC API Guide](http://fdc.nal.usda.gov/api-guide/)
- Data types: Foundation Foods, SR Legacy, Survey Foods (FNDDS), Experimental Foods, Branded Foods. — [FDC API Guide](http://fdc.nal.usda.gov/api-guide/)
- Bulk download sizes (download page as of Oct 2026):
  - Foundation Foods, April 2026: JSON 459 KB zipped / 6.5 MB unzipped; CSV 3.7 MB / 32 MB.
  - SR Legacy, April 2018 (final; "will not be updated"): JSON 12.3 MB / 205 MB; CSV 6.7 MB / 54 MB.
  - FNDDS, October 2024: JSON 3.7 MB / 64 MB; CSV 200 MB / 1.6 GB.
  - Branded Foods, April 2026: JSON 195 MB / 3.1 GB; CSV 428 MB / 2.9 GB.
  — [FDC Download Datasets](http://fdc.nal.usda.gov/download-datasets/)
- INDB used USDA data for 54 ingredients missing from IFCT, and USDA retention factors. — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)

### Inferences
- Bundle SR Legacy, about 7,800 foods [unverified count], plus Foundation, after stripping to the needed nutrients (kcal, protein, carbs, fat, fibre, sugar, sodium, plus a few micros) and converting to SQLite or Core Data. The stripped result should be a few MB, which is well within iOS app-size norms. That size is my estimate, not a measured figure.
- A live Branded Foods lookup via the API would send queries off-device, and Branded data mostly covers US products, so it adds little for Indian users.

### Gaps
- I did not verify the current SR Legacy and Foundation food counts, or how many Indian dishes FNDDS contains (e.g., dal, curry, roti). Check by searching the bulk files.

## Q4. Open Food Facts (OFF)

### Takeaway
OFF is free and has an Indian packaged-food catalogue: about 10k products in Sept 2024, with one later snapshot of about 24.7k [unverified]. The database is under ODbL (attribution plus share-alike for derivative databases you publicly use), contents under DbCL, and images under CC BY-SA. An app can use it with prominent attribution. Bundling an OFF subset, or merging OFF into your own food DB, makes that DB a derivative database you must offer under ODbL. The live API is rate-limited (15 product reads per minute per IP) and sends each barcode to OFF's server.

### Cited Findings
- Licences: the database is ODbL 1.0, contents are Database Contents License (DbCL), images are CC BY-SA 3.0. — [OFF Data page](https://world.openfoodfacts.org/data)
- OFF terms: re-users "have to mention the licence and to attribute the authorship to Open Food Facts with a link to https://openfoodfacts.org"; "Derivative works must be shared under the same conditions." — [OFF Terms of use](https://world.openfoodfacts.org/terms-of-use)
- ODbL definitions and obligations:
  - A "Produced Work" is "a work … resulting from using the whole or a Substantial part of the Contents". Publicly using a Produced Work needs a notice that content came from the database (§4.3).
  - Any Derivative Database you Publicly Use must be under ODbL or a compatible licence (§4.4).
  - A Collective Database need not be ODbL as a whole, though ODbL still applies to the included part (§4.5).
  - If you Publicly Use a Derivative Database or a Produced Work from one, you must offer the entire Derivative Database or a file of the alterations in machine-readable form (§4.6).
  — [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)
- Dumps: a MongoDB dump (~0.9 GB compressed / ~9 GB uncompressed), JSONL (gzip), CSV, and Parquet (on Hugging Face), refreshed regularly. OFF asks that "1 API call = 1 real scan by a user" and discourages scraping because exports exist. — [OFF Data page](https://world.openfoodfacts.org/data)
- API rate limits: 15 requests per minute per IP for product reads (`GET /api/*/product`) and 10 requests per minute per IP for search, with a risk of an IP ban if exceeded. A custom User-Agent is required (`AppName/Version (ContactEmail)`). Reads need no authentication. Staging is world.openfoodfacts.net. — [OFF API docs](https://openfoodfacts.github.io/openfoodfacts-server/api/)
- India coverage: about 10,000 Indian products reached by Sept/Oct 2024, 4,000 of them added in 2024. The OFF blog notes Indian labels often print nutrition info in tiny type, which makes crowdsourcing hard. — [OFF blog, India 10K milestone](https://blog.openfoodfacts.org/en/news/open-food-facts-india-database-reaches-10k-product-milestone)
- A search-engine snippet gave "24,674 products" for the India database; I could not confirm it because the OFF facets page returned HTTP 503. — [in.openfoodfacts.org](https://in.openfoodfacts.org/) [unverified]

### Inferences
- Lowest legal friction: call the OFF API live on barcode scan, without bundling, cache results on-device only for that user's own log, and show "Data from Open Food Facts (ODbL)" with a link. The trade-off is privacy, because the barcode and IP go to OFF. That is small, but it should be disclosed in a privacy-first app.
- Offline option: ship a filtered India subset (e.g., products with country=India and complete nutrition) as a **separate** ODbL-licensed file, kept apart from the proprietary or other-licensed DB and published openly (e.g., on GitHub). That keeps it a collective database rather than a merged derivative database. Whether that separation holds is a legal judgement [unverified]; confirm with reuse@openfoodfacts.org.
- Do not ship OFF product images unless you can meet CC BY-SA attribution.

### Gaps
- No verified current India product count, and no measure of nutrition-field completeness for Indian products.

## Q5. Commercial APIs: Nutritionix, FatSecret, Edamam, Spoonacular, Passio.ai

### Takeaway
All five are online-only by design. Every query goes to a third-party server, and most terms restrict caching or building a local copy, so none fits a no-cloud, offline-first app as the core DB. FatSecret's free Basic edition (5,000 calls a day) covers **US data only**; India sits behind the paid, quoted Premier tier. Edamam allows caching only of a few macro fields. Spoonacular requires deleting cached data after one hour. Nutritionix has dropped its free tier and starts at hundreds of dollars a month [partly unverified]. Passio costs $99 a month or more with no free trial, though it offers on-device recognition.

### Cited Findings
**FatSecret Platform API** — [FatSecret API editions](https://platform.fatsecret.com/api-editions)
- Basic: free with self sign-up, 5,000 API calls a day, "US Only" dataset, attribution required, caching supported, UPC barcode scanning, NLP/image recognition as an optional add-on.
- Premier Free: unlimited calls, US only, attribution required, free for verified startups, non-profits and students. Non-US data is available "at discount upon request".
- Premier: unlimited calls, "More than 62 Countries", no attribution, price "Upon request, based on market access".
- Whether India is among the 62+ countries is not stated on the page [unverified].

**Edamam Food Database API** — [Edamam Food DB API](https://developer.edamam.com/food-database-api)
- Enterprise Basic $14/month for 100,000 calls a month (500 Vision calls). Enterprise Core $69/month for 750,000. Enterprise Plus $299/month for 5,000,000. Unlimited is custom.
- Caching is allowed only on eligible plans, and only for "FoodId, Food Label, Protein, Net carbs, Total fat, Kcal" while the subscription is active. Users may not "build a copy of the Edamam data to be reused in any form."
- Attribution with an Edamam badge and link is mandatory on all plans; breach leads to "immediate service suspension".
- Barcode coverage: 700,000+ UPC/EAN/ITN codes. The page says nothing about India.
- A secondary source adds that saved data may be used only in the end user's account, behind a password. — [search summary of Edamam terms; unverified]

**Spoonacular** — [Spoonacular pricing](https://spoonacular.com/food-api/pricing)
- Free plan: $0, "50 points/day then no more calls", backlink required.
- Paid plans: Cook $29, Culinarian $79, Chef $149, Enterprise from $300 a month, no backlink.
- Caching: "You may cache user-requested data … for a maximum of 1 hour. After 1 hour, you must delete your cache." If access ends, "you must delete all data you ever obtained from the spoonacular API."

**Nutritionix**
- Nutritionix says it can no longer maintain a public free-access tier because of misuse; prospective users must contact sales for a limited trial. — [Nutritionix developer site (search snippet; page returned HTTP 402 to fetch)](https://developer.nutritionix.com/admin/access_details) [unverified]
- Plans per search snippets of nutritionix.com/api: Starter $499/month, MVP $999/month, Unicorn from $1,850/month, billed annually. Freemium apps and those with more than 100K MAU need custom pricing. — [Nutritionix API page (search snippet; fetch blocked)](https://www.nutritionix.com/api) [unverified]
- An aggregator blog listing a 200 calls/day free tier conflicts with the above. Treat it as unreliable. — [calorieapi.com blog](https://calorieapi.com/blog/nutritionix-api-pricing) [unverified]

**Passio Nutrition-AI** — [Passio pricing](https://www.passio.ai/pricing)
- Starter $99/month (1M tokens, $25 per 1M refill). Growth $599/month (5M tokens). Pro $2,999/month (100M tokens). Custom for 50,000+ active users.
- No free trial ("Upon purchasing, you will be billed immediately"). One photo analysis uses about 20–30k tokens, so roughly 33–50 photos per $1 of Starter-tier tokens is my arithmetic.
- Cloud recognition sends images to servers, and data "is transitioned to our LLM that could be a third party LLM such as GPT". An on-device recognition mode "keeps the data local to the device". Customers must ensure "no personal data is transferred to Passio".

### Inferences
- For a privacy-first, no-cloud app, commercial APIs work at most as an opt-in online fallback. Caching rules (Edamam, Spoonacular) stop you from turning API results into the offline DB. FatSecret's free tier is US-only and mandates attribution, which makes it weak for Indian users.
- Cost scales with users, which suits a solo founder poorly compared with zero-marginal-cost bundled data.

### Gaps
- I could not verify Indian food coverage for any of these vendors from primary sources.
- I could not fetch Nutritionix's current pricing page or its caching/attribution terms (HTTP 402). FatSecret's full caching terms (duration limits) are in the API terms of use, which I did not read.

## Q6. Indian packaged foods: GS1 India data, FSSAI labelling rules, OCR as an alternative

### Takeaway
Since the FSSAI Labelling and Display Regulations 2020, packaged foods in India must print energy, protein, carbohydrate, total and added sugars, total, saturated and trans fat, cholesterol and sodium per 100 g/ml (or per single-serve pack), plus %RDA per serve. That standard panel makes on-device label OCR a practical, privacy-preserving alternative to a barcode database. GS1 India's DataKart is the national product-data repository, but I found no public, free, or open nutrition API for third-party apps.

### Cited Findings
- FSSAI Labelling and Display Regulations 2020 were notified on 14 Dec 2020. Nutritional information "per 100g or 100ml or per single consumption pack … and per serve percentage (%) contribution to RDA" must include:
  - energy (kcal)
  - protein (g)
  - carbohydrate (g), total sugars (g), added sugars (g)
  - total fat (g), saturated fat (g), trans fat (g), cholesterol (mg)
  - sodium (mg)
  %RDA is based on 2000 kcal, 67 g fat, 22 g saturated fat, 2 g trans fat, 50 g added sugar and 2000 mg sodium. — [FSSAI Labelling & Display Regs compendium (v. VIII, Sept 2025)](https://fssai.gov.in/upload/uploadfiles/files/Comp_Labelling%20Display_Version%20VIII_09_09_2025.pdf); [FSSAI Labelling Guidance Note (Feb 2022)](https://fssai.gov.in/upload/uploadfiles/files/Guidance_Note_Labelling_23_02_2022.pdf)
- DGI 2024 likewise tells consumers that labels give nutrients per 100 g/100 ml or per serve, and that %RDA per serving is now mandatory. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
- GS1 India DataKart is "a national repository of product data" where brand owners upload and share product data. It is integrated with GS1 Cloud. — [GS1 India DataKart](https://www.gs1india.org/services/datakart)
- GS1 India's consumer "Smart Consumer" app shows DataKart data on barcode scan: name, manufacturing date, MRP, net content, contact info and reviews. — [GS1 India Smart Consumer](https://www.gs1india.org/services/smart-consumer); [GS1 India blog](https://www.gs1india.org/blog/smart-consumer-app)
- OFF India contributors report that Indian labels often print nutrition info in tiny type, partly hidden by graphics. That hurts OCR as well as crowdsourcing. — [OFF blog, India 10K milestone](https://blog.openfoodfacts.org/en/news/open-food-facts-india-database-reaches-10k-product-milestone)
- Apple's Vision `VNRecognizeTextRequest` runs on-device, and its supported languages can be queried with `supportedRecognitionLanguages()`. — [Apple docs](https://developer.apple.com/documentation/vision/vnrecognizetextrequest/supportedrecognitionlanguages())

### Inferences
- On-device label OCR is the strongest fit for FITme's privacy model. Use Apple Vision text recognition plus a parser keyed to the fixed FSSAI field list and "per 100 g" header. The user confirms or edits the values, and the result is stored as a personal food. It needs no database licence and no network call.
- Nutrition panels on Indian packs are generally in English, which Vision supports well [unverified]. Hindi OCR support was not confirmed.
- Practical barcode approach: user-scanned barcode → local cache of the user's own past scans → optional OFF lookup → fallback to label OCR. Optionally offer to contribute back to OFF.

### Gaps
- I found no evidence that GS1 India DataKart offers a third-party API with nutrition fields, or its terms and pricing. Ask GS1 India directly.
- I did not confirm whether Hindi or other Indic scripts are supported by `VNRecognizeTextRequest` or by the newer document-recognition APIs as of iOS 26.

## Q7. Other national databases useful for the diaspora: UK CoFID, Australia AUSNUT/AFCD, Canada CNF

### Takeaway
UK CoFID (Open Government Licence v3.0) and Canada's CNF (Open Government Licence – Canada) are permissive. Commercial use and bundling are fine with attribution and no share-alike. Australia's AFCD/AUSNUT are CC BY(-SA) 3.0 AU with share-alike, so bundling them would require releasing your derivative DB under the same licence. CoFID includes a number of UK-consumed South Asian dishes [unverified count], and INDB already used it for 144 ingredients.

### Cited Findings
- UK CoFID: "All content is available under the Open Government Licence v3.0, except where otherwise stated". Last updated 19 March 2021. The main dataset is an Excel file (4.42 MB) with an "old foods" file (634 KB) and a 37-page user guide. — [GOV.UK CoFID](https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid)
- CoFID covers macro- and micronutrient profiles of 3,000+ foods and recipes commonly consumed in the UK. — [search summary; Quadram/PHE sources](https://fnnbri.quadram.ac.uk/data/) [count unverified]
- Older material says reusing M&W data required a Crown copyright licence from OPSI. That is superseded by the OGL statement on the current GOV.UK page. — [FAO-hosted CoF IDS user doc](https://www.fao.org/uploads/media/British_FCDB_cof_user_doc.pdf)
- INDB used the UK McCance & Widdowson database (2021) for 144 ingredients. — [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- Canada CNF 2015 is licensed under the Open Government Licence – Canada. It has 5 relational data files plus 7 support files, in CSV, Excel or Access. A "Canadian Nutrient File, 2026" dataset also appears on the open-data portal. — [Open Canada CNF 2015](https://open.canada.ca/data/en/dataset/089885f9-ed53-44e6-854a-14d21a1ec2e0); [Open Canada CNF 2026](https://open.canada.ca/data/en/dataset/1b6139bd-ed7e-4043-bc28-ff00e10f3109); [Health Canada CNF downloads](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/nutrient-data/canadian-nutrient-file-2015-download-files.html)
- AUSNUT 2011–13 (FSANZ) has 53 nutrients for 5,740 foods and beverages. Sources give its licence as CC BY 3.0 AU, CC BY 2.5 AU (data.gov.au listing) or a CC BY-SA-based licence; these conflict. — [data.gov.au AUSNUT 2011–13](https://data.gov.au/data/dataset/ausnut-2011-13); [FSANZ AUSNUT disclaimer](https://www.foodstandards.gov.au/science-data/monitoringnutrients/ausnut/disclaimer)
- AFCD Data User Licence Agreement: "Creative Commons Attribution-ShareAlike 3.0 Australia". Commercial use is allowed, royalty-free. "You may only distribute a Derivative Work if You apply this Licence Agreement to it." It requires attribution, a Limitation of Data statement and a statement that the work is based on Australian data, and it bars "technological measures" that restrict recipients' rights. — [FSANZ AFCD Data User Licence](https://www.foodstandards.gov.au/science-data/monitoringnutrients/afcd/datauserlicenceagreement)

### Inferences
- For diaspora users, CoFID (OGL) is the most useful extra after USDA: permissive, small (about 4–5 MB of Excel), and it includes UK-consumed Indian takeaway and home dishes.
- CNF is a safe, permissive fill-in. Skip AFCD/AUSNUT unless you accept share-alike, and note that the "no technological measures" clause may clash with App Store DRM [unverified legal interpretation].

### Gaps
- I did not count South Asian dishes in CoFID or CNF. I did not resolve AUSNUT's conflicting licence statements.

## Q8. Practical recommendation: the minimal-cost, legally safe stack for an offline-first app

### Takeaway
Bundle permissively licensed government data (USDA FDC SR Legacy + Foundation under CC0, and UK CoFID under OGL v3, optionally Canada CNF) as the ingredient base. Build the Indian dish catalogue as **your own recipes**, calculated on-device from those ingredients with explicit oil and ghee fields and NIN katori/spoon portion presets. Add on-device FSSAI label OCR for packaged foods, and optionally a live, attributed OFF barcode lookup. Use IFCT 2017 or INDB values only after getting written permission from NIN and from Anuvaad/Jaacks.

### Cited Findings
- USDA FDC is CC0 with citation requested; Foundation + SR Legacy CSV is about 10 MB zipped. — [FDC API Guide](http://fdc.nal.usda.gov/api-guide/); [FDC Download Datasets](http://fdc.nal.usda.gov/download-datasets/)
- UK CoFID is OGL v3.0. — [GOV.UK CoFID](https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid)
- CNF is OGL – Canada. — [Open Canada CNF 2015](https://open.canada.ca/data/en/dataset/089885f9-ed53-44e6-854a-14d21a1ec2e0)
- IFCT 2017 prohibits storing or reproducing it electronically "for creating a product" without NIN's written permission. — [NIN IFCT2017.pdf](https://www.nin.res.in/ebooks/IFCT2017.pdf)
- INDB states no explicit data licence or NIN permission. — [Anuvaad INDB page](https://www.anuvaad.org.in/indian-nutrient-databank/); [PMC11277795](https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795)
- OFF is ODbL, with share-alike for derivative databases and 15 product reads per minute per IP. — [OFF Data page](https://world.openfoodfacts.org/data); [OFF API docs](https://openfoodfacts.github.io/openfoodfacts-server/api/)
- FSSAI makes per-100 g nutrition panels mandatory. — [FSSAI Labelling & Display compendium](https://fssai.gov.in/upload/uploadfiles/files/Comp_Labelling%20Display_Version%20VIII_09_09_2025.pdf)
- NIN household measures are defined in DGI 2024 Annexure I. — [NIN DGI 2024 PDF](https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
- Commercial APIs restrict caching (Edamam, Spoonacular), are US-only on free tiers (FatSecret) or are costly (Nutritionix, Passio). — see Q5 sources.

### Inferences
Proposed stack, in priority order:
1. **Core bundled DB, $0, offline:** USDA SR Legacy + Foundation (CC0), trimmed to the needed nutrients in SQLite. Add CoFID (OGL), and optionally CNF (OGL). Ship an in-app "Data sources and licences" screen with the USDA citation and OGL attribution statements.
2. **Indian dishes, $0:** the founder (ideally with a dietitian) writes 200–500 standard recipes for common Indian dishes in raw-ingredient grams, mapped to USDA/CoFID ingredients. Compute per 100 g cooked using a measured or estimated cooked yield, and set oil or ghee as an adjustable per-serving field. Portions use NIN katori and spoon presets and per-piece weights (roti, idli, dosa) measured by the founder. Since these are your own calculations from CC0/OGL inputs, you own the result and can show "calculated estimate" labels. Calculated values will differ from IFCT's lab-analysed values, especially for Indian-specific ingredients (regional pulses, millets, local vegetables) where USDA/UK coverage is thin. This is a known accuracy trade-off.
3. **Packaged foods:** on-device label OCR (Apple Vision) tuned to the FSSAI panel as the default. It is private and needs no licence.
4. **Optional online barcode lookup:** OFF live API with prominent ODbL attribution and a User-Agent, results stored only in the user's personal log, disclosed in the privacy policy. Avoid merging OFF records into the bundled DB unless you are willing to publish that DB under ODbL.
5. **Upgrade path:** email NIN (ifct2017@gmail.com / nin@ap.nic.in) for written permission to use IFCT 2017, and Anuvaad/Prof. Jaacks for an explicit INDB data licence. If granted, IFCT 2017 would greatly improve Indian ingredient accuracy and INDB would add 1,014 recipes immediately. Keep their responses on file.
6. **Avoid:** Kaggle "Indian food nutrition" CSVs (laundered or unknown provenance), FatSecret Basic (US-only, attribution), Edamam and Spoonacular as an offline source (caching prohibited or limited), Nutritionix and Passio (cost; Passio cloud mode sends images to third-party LLMs).

### Gaps
- No legal opinion was obtained. Whether INDB recipe aggregates infringe NIN's IFCT copyright, and whether a separately stored OFF subset counts as a "Collective Database" under ODbL §4.5, need counsel or direct confirmation from the rights holders.
- I could not confirm the actual Indian-food coverage of USDA, CoFID or CNF, i.e. how many IFCT ingredients have close USDA or UK equivalents. This determines how accurate approach 2 can be.
