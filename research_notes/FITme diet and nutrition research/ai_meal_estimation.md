# AI Meal Calorie/Macro Estimation: Accuracy, On-Device iOS Options, and Indian Food

Research date: 2026-10-04. Context: FITme is a privacy-first, fully on-device iOS fitness app that already estimates meal macros from text descriptions. Figures marked [unverified] came only from a search snippet or a secondary source I could not open, or their definitions are unclear.

## 1. Published accuracy of LLM/vision-model calorie estimation (photos and text), commercial apps, and the human baseline

### Takeaway
On mixed real-world meals, general LLMs looking at a photo alone are typically off by about 25-35% on energy. Most of that error comes from portion size: the models consistently underestimate medium and large portions. Accuracy improves a lot (to about 14% MAPE) when the user supplies ingredients or quantities. Commercial photo apps underestimate by roughly 250-345 kcal per meal, mostly because they miss fat. Humans are also poor at this: dietitians eyeballing portions are off by about 40-48%, so "as good as a dietitian looking at a photo" is a low bar.

### Cited Findings
**LLMs on photos**
- O'Hara et al. (Nutrients, 2025) tested ChatGPT-4 on 114 photos (38 meals x 3 portion sizes) from Ireland's National Adult Nutrition Survey. Food identification had 93.0% precision, 84.6% recall and an F1 of 88.6%. The mean absolute percentage difference in portion weight was 27.8% ± 18.5%, and 76.3% of meals were underestimated. Small portions were fine (408 g actual vs 431 g estimated), but medium (581 g vs 426 g) and large (798 g vs 530 g) were significantly underestimated. Mean energy difference was only +0.1%, because over- and underestimates cancelled out (rs = 0.73). Sugar was off by -32%, fibre by -20% and potassium by -50%. Agreement with 7 dietitians, measured as ICC, was 0.56 for energy, 0.67 for protein and 0.31 for carbohydrate. — [PMC11858203](https://pmc.ncbi.nlm.nih.gov/articles/PMC11858203/)
- Rodríguez-Jiménez et al. (Nutrients, Nov 2025) tested ChatGPT-5 on 195 dishes (Allrecipes 96, SNAPMe 74, dietitian-weighed home meals 25) with increasing amounts of context:
  - Image only: energy MAE 123 kcal, MAPE 30.5%
  - Image + non-visual descriptors (fat type, sweetener, meat type): 92 kcal, 24.4%
  - Image + detailed ingredients with quantities: 53 kcal, 13.9%
  - Ingredients only, no image: 66.5 kcal, 18.1%

  The authors conclude that the image still adds value on top of a text ingredient list. — [PMC12655113](https://pmc.ncbi.nlm.nih.gov/articles/PMC12655113/)
- A pilot study of ChatGPT-4o on simple, moderate and complex meals found initial errors of up to 54.4% for energy and 76.5% for fat, especially in complex meals and those with visually obscured fat. Giving the model additional information raised energy R² from 0.591 to 0.941. — [ScienceDirect, J. Food Composition & Analysis S088915752501659X](https://www.sciencedirect.com/science/article/pii/S088915752501659X) (figures from abstract snippet; full text returned 403) [unverified detail]
- A Taiwan validation study (Diabot-GPT-4o) used 714 food images from 3-day weighed food records (57 young adults). Using images alone, a customised GPT-4o recognised 74% of food items vs 59% for stock GPT-4o. GPT-4o configurations reportedly landed at ±10-15% for portion, ±10-20% for energy and ±10-22% for fat. Reported error sources were portion size, obscured food, poor prompts, and omissions or intrusions. — [PubMed 41138916](https://pubmed.ncbi.nlm.nih.gov/41138916/); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0002916525006173) (abstract snippet only) [unverified detail]
- A comparison of three LLMs on food images found that ChatGPT and Claude had similar error: MAPE of 36.3% and 37.3% for weight and about 35.8% for energy. Gemini was much worse, with MAPE of 64.2-109.9% across nutrients. — [ScienceDirect S2475299125030185 (Current Developments in Nutrition)](https://www.sciencedirect.com/science/article/pii/S2475299125030185) (abstract snippet; full text 403; model versions not confirmed) [unverified detail]
- Chatbots vs professional nutritionists on nutrition labels of ready-to-eat meal boxes: dietitians gave the estimates closest to labelled values for calories, protein, fat, saturated fat, carbohydrate and sodium. All AI models consistently underestimated sodium, with CVs of 20-70%. — [PMC12526241](https://pmc.ncbi.nlm.nih.gov/articles/PMC12526241/)
- An earlier systematic analysis of multimodal ChatGPT for dietary assessment also exists. — [arXiv 2312.08592](https://arxiv.org/pdf/2312.08592) (not opened; no numbers extracted)

**LLMs on text descriptions** (the format FITme uses today)
- NutriBench (Hua, Dhaliwal et al., 2024) contains 11,857 meal descriptions built from real-world global dietary intake data, with human-verified carb, protein, fat and calorie labels, split into 15 subsets by complexity. Across 7 LLMs, GPT-4o with chain-of-thought scored best at 66.82% accuracy for carb estimation, answering 99.16% of queries. The authors report that LLMs beat professional nutritionists on accuracy and speed for carb estimation. NutriBench v2 (2025) covers 24 countries. — [arXiv 2407.12843](https://arxiv.org/pdf/2407.12843v2); [project page](https://mehak126.github.io/nutribench.html). The accuracy metric appears to be "within a fixed gram tolerance of the true carbs". I did not confirm the exact tolerance [unverified].
- Hoang et al., "AI dietitian: Unveiling the accuracy of ChatGPT's nutritional estimations" (Nutrition, 2023) is a text-based evaluation. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0899900723003532) (numbers not retrieved)

**Purpose-built vision models** (non-LLM)
- Nutrition5k (Google, CVPR 2021) has about 5k real cafeteria dishes, weighed item by item, with nutrition values from USDA FNDDS. Errors by approach:
  - Single RGB image, predicting absolute calories directly: 26.1% calorie MAE
  - Calories per gram only (portion given): 9.5%
  - RGB plus depth channel: 18.8%
  - Depth-derived volume as an input to mass regression: mass error falls from 18.7% to 13.7%
  - End-to-end pipeline: 16.5% calorie MAE

  The 9.5% vs 26.1% gap shows that portion estimation nearly triples the error. — [arXiv 2103.03375](https://arxiv.org/pdf/2103.03375)

**Commercial apps**
- NIDDK/NIH (Hengist & Charles) presented at NUTRITION 2026 (an abstract, not yet a peer-reviewed paper). They tested MyFitnessPal, Lose It!, Cal AI and Appediet on 102 metabolic-kitchen meals weighed to 0.1 g, with a follow-up of more than 200 meals. All four apps underestimated energy by about 250-345 kcal per meal and fat by about 30 g per meal. Lose It! and Cal AI underestimated carbs by about 14 g. Ketogenic (high-fat) meals were the hardest. — [ScienceDaily, Jul 2026](https://www.sciencedaily.com/releases/2026/07/260726015237.htm); [Medscape](https://www.medscape.com/viewarticle/photo-based-meal-apps-underestimate-calories-and-fat-2026a1000qo9)
- SnapCalorie uses the phone's depth sensor plus human reviewers and claims about 15% mean calorie error, "under 20%". This is a company claim, not independently validated. — [TechCrunch 2023](https://techcrunch.com/2023/06/26/snapcalorie-computer-vision-health-app-raises-3m/); [SnapCalorie blog](https://www.snapcalorie.com/blog/snapcalorie-revolutionizing-nutrition-tracking-with-ai.html)
- A "2026 meta-analysis" reports pooled MAPE of 13.9% for Cal AI, 16.5% for Foodvisor and 9.1% for MyFitnessPal manual or barcode entry. It is hosted on a non-journal site and I could not verify its authorship or methods, so treat it as **[unverified]**. It also conflicts with the NIH finding of large systematic underestimation. — [clinicalnutritionreport.com](https://clinicalnutritionreport.com/research/ai-calorie-tracker-accuracy-meta-analysis-2026/)

**Human baseline**
- In the Nutrition5k survey, non-nutritionists had an average mass estimation error of 53% and nutritionists 41%. The model beat both. — [arXiv 2103.03375](https://arxiv.org/pdf/2103.03375)
- 38 nutritionists, dietitians and researchers estimating portions from digital images were off by 47.6 ± 21.2% for food on a plate and 44.3 ± 16.6% in a bowl. Only 23.7% (plate) and 32.3% (bowl) of estimates were within 10% of true weight. — [PMC6115988](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6115988/)
- A crowdsourcing study of laypeople estimating calories from food photos also exists. — [PMC6246963](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6246963/) (numbers not extracted)

### Inferences
- A realistic accuracy target for FITme's text estimator on everyday mixed meals is about 15-30% energy error per meal without quantities, and about 15% or better when the user gives quantities. Errors are biased low (portion and fat underestimation), not random, so they will not average out across a day for a user in a deficit.
- Text with explicit quantities (FITme's current input) is arguably a better starting point than a bare photo. In the ChatGPT-5 study, ingredients-only text (18% MAPE) beat image-only (30.5%). Photos help most as an addition, not a replacement.
- No published study evaluates Apple's ~3B on-device model for nutrition estimation. All the numbers above come from frontier cloud models or purpose-trained CNNs, so expect a small on-device model to do worse at recalling nutrition numbers (see section 3).

### Gaps
- No peer-reviewed independent accuracy studies were found for Cal AI, Foodvisor, SnapCalorie or MyFitnessPal Meal Scan individually, apart from the NIH abstract (not yet a full paper).
- I could not open full text for the 3-LLM comparison, the GPT-4o complex-meals study or the Diabot study (403 or cookie walls), so their exact figures and model versions are unconfirmed.
- I found no study evaluating Apple Foundation Models (on-device) on food or nutrition.

## 2. Main error sources: portion/volume, hidden oil/ghee/sugar, mixed dishes, depth estimation

### Takeaway
Portion size is the biggest error source: it roughly triples error compared with per-gram estimation. The second is invisible energy (cooking fat, sugar, sauces), which drives systematic underestimation. Both are worse for Indian food: curries, dals and gravies are amorphous, and oil or ghee is dissolved in the dish rather than visible. Depth sensing (LiDAR or TrueDepth) helps with volume but not with hidden fat.

### Cited Findings
- Portion: Nutrition5k error rose from 9.5% (calories per gram) to 26.1% (absolute calories) once the model also had to estimate portion. A depth-derived volume prior cut mass error from 18.7% to 13.7%. — [arXiv 2103.03375](https://arxiv.org/pdf/2103.03375)
- Portion: ChatGPT-4 underestimated the weight of medium and large meals, with large plates estimated at 530 g vs 798 g actual. — [PMC11858203](https://pmc.ncbi.nlm.nih.gov/articles/PMC11858203/)
- Amorphous foods are harder for humans too. With computer-based portion aids, error was 8.3% for solid foods, -10% for amorphous foods and 19% for liquids. — search-result summary of [Lucassen et al. 2021, J Hum Nutr Diet / PMC9291996](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9291996/) [unverified attribution of exact figures]
- Hidden fat: all four commercial apps underestimated fat by about 30 g per meal (about 270 kcal) and failed most on high-fat keto meals. — [ScienceDaily/NIH](https://www.sciencedaily.com/releases/2026/07/260726015237.htm)
- Hidden fat: GPT-4o fat error reached 76.5% in meals with visually obscured fat. — [ScienceDirect S088915752501659X](https://www.sciencedirect.com/science/article/pii/S088915752501659X) [unverified detail]
- Telling the model the fat type, sweetener type and meat type cut ChatGPT-5 energy MAPE from 30.5% to 24.4%. — [PMC12655113](https://pmc.ncbi.nlm.nih.gov/articles/PMC12655113/)
- Depth limits: depth sensors struggle with dense or layered dishes, hidden calories and sauce-heavy dishes, where volume does not convert cleanly to calories. — [Macaron SnapCalorie review](https://macaron.im/blog/snapcalorie-review-2026) (secondary blog) [unverified]
- Academic depth work includes DPF-Nutrition (depth prediction from monocular images) and RGB-D transformers. — [arXiv 2310.11702](https://arxiv.org/pdf/2310.11702); [arXiv 2406.01938](https://arxiv.org/pdf/2406.01938)
- Indian-specific: portions of Indian dishes are often non-standard and served mixed, and models trained on homogeneous datasets generalise poorly to them. — summary of [Performance Evaluation of 3 LLMs, ResearchGate](https://www.researchgate.net/publication/395491050_Performance_evaluation_of_Three_Large_Language_Models_for_Nutritional_Content_Estimation_from_Food_Images) and related literature [unverified attribution]
- Adding dish names as text to an image CNN on Nutrition5k improved calorie MAE only marginally, from 84.76 to 83.70 kcal (-1.25%). Naming the dish does not fix the portion problem. — [arXiv 2511.11705](https://arxiv.org/abs/2511.11705)

### Inferences
- For Indian meals, the single most useful clarifying question is about cooking fat: amount of oil or ghee (none, light, normal, restaurant-heavy) and whether it is home or restaurant food. The next most useful is portion in household units (katori, roti count, ladle, cup). Both target the two largest documented error sources.
- A depth-based volume pipeline means substantial custom ML work for a solo founder, and it still cannot see ghee dissolved in a dal. Asking about fat probably beats LiDAR on cost and benefit for Indian food.
- Direction of error matters for a fitness app. Systematic underestimation makes users think they are in a deficit when they are not. A deliberate correction, such as defaulting to "typical home cooking oil" rather than zero, is defensible.

### Gaps
- I found no peer-reviewed study that quantifies oil or ghee underestimation by AI specifically for Indian dishes, or how much cooking fat varies between home and restaurant Indian food.

## 3. On-device options on iOS (as of Oct 2026)

### Takeaway
Apple's Foundation Models framework is the natural fit. It is free, offline, and adds no app size, and it offers guided generation (typed structured output) and tool calling. Under iOS 26 it was text-only with a roughly 4K-token context window. iOS 27 (WWDC26) adds image input to the on-device model and Vision-backed OCR and barcode tools. The model is about 3B parameters and Apple says explicitly that it is not a world-knowledge engine, so it should identify foods and quantities and call a local nutrition database, not recall calorie numbers itself. It only runs on Apple Intelligence devices (iPhone 15 Pro and newer), so FITme needs a fallback for older phones.

### Cited Findings
**Apple Foundation Models framework**
- Model: about 3B parameters, compressed to 2 bits per weight with quantization-aware training (4-bit embeddings, 8-bit KV cache). The on-device model has a ViTDet-L vision backbone (300M parameters) that Apple says compares favourably with Qwen-2.5-VL-3B. It supports 15 languages and was pre-trained for contexts up to 65K tokens. Apple's Python toolkit trains rank-32 LoRA adapters, which must be retrained with each base-model update. The model is "not designed to be a chatbot for general world knowledge". — [Apple ML Research, 2025 update](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)
- Framework (WWDC25):
  - Guided generation with the `@Generable` macro on Swift structs and enums uses constrained decoding, so outputs always parse.
  - With tool calling, the model decides when to call app-defined `Tool` implementations, and the framework handles parallel and serial calls.
  - Available from iOS 26.

  — [WWDC25 "Meet the Foundation Models framework"](https://developer.apple.com/videos/play/wwdc2025/286/)
- iOS 26 on-device context budget is 4K tokens; Private Cloud Compute (PCC) offers 32K. — [blakecrosley.com explainer](https://blakecrosley.com/blog/apple-foundation-models-framework) (secondary source)
- WWDC26 ("What's new in the Foundation Models framework", iOS 27):
  - Image input: pass an `Attachment(UIImage)` alongside text. Any size or aspect ratio is accepted, and larger images cost more tokens and latency.
  - New system tools: `BarcodeReaderTool` and `OCRTool`, both backed by the Vision framework, plus a Spotlight search tool for fully local RAG.
  - `model.contextSize` and `tokenCount(for:)` APIs (iOS 26.4+). The session's example prints `contextSize` as 8192.
  - On-device model "rebuilt from the ground up" with better tool calling.
  - `DynamicProfile` API for switching instructions and tools mid-session.
  - New `PrivateCloudComputeLanguageModel` with reasoning levels; free under 2M first-time downloads, requires an entitlement.
  - `LanguageModel` protocol with open-source `CoreAILanguageModel` and `MLXLanguageModel` conformances.
  - New Evaluations framework for measuring feature quality.

  — [WWDC26 session 241](https://developer.apple.com/videos/play/wwdc2026/241/); see also [WWDC26 "What's new in image understanding"](https://developer.apple.com/videos/play/wwdc2026/237/)
- The 8192 value comes from a code example and may vary by device or OS. Check it at runtime with `contextSize` [unverified as a guaranteed spec].
- Device and storage requirements:
  - iPhone 16 models or later, iPhone 15 Pro and 15 Pro Max
  - iPad with M1 or later, iPad mini (A17 Pro), Mac with M1 or later
  - Up to 8 GB of free storage, or 12-14 GB on the newest devices (current page references iOS 27)

  — [Apple Support 121115](https://support.apple.com/en-us/121115)
- Languages: English is supported, including the English (India) locale. Hindi is not among the supported Apple Intelligence languages. — [iClarified](https://www.iclarified.com/102432/siri-ai-compatibility-supported-devices-languages-and-availability); [Apple Support 121115](https://support.apple.com/en-us/121115). Apple's current page lists "English" without regional variants, so English (India) comes from the secondary source.
- Privacy caveat: PCC models run on Apple servers. Apple says prompts are not stored and that independent researchers can verify this. — [WWDC26 session 241](https://developer.apple.com/videos/play/wwdc2026/241/). Even so, using PCC would technically break a "100% on-device / no cloud" promise.

**Other on-device routes**
- MLX / open models: Gemma 3 4B vision-language model compressed to about 2.1 GB on Apple Silicon. A mobile-optimised version has about 23% lower memory and about 2.2 GB text-only runtime. — [arXiv 2601.19139](https://arxiv.org/html/2601.19139)
- Gemma 3 1B at 4-bit is about 300 MB in an iPhone MLX app. — [LLMVoice App Store listing](https://apps.apple.com/us/app/llmvoice/id6753925010)
- MLX Swift supports Qwen2-VL-class models on Metal. — [SwiftLM GitHub](https://github.com/SharpAI/SwiftLM)
- Core ML / Create ML image classifiers: on the Khana Indian dataset, standard backbones reach 80-87% top-1 accuracy. EfficientNet-V2-S has about 20M parameters (roughly 40-80 MB at fp16/fp32 before further quantisation). — [arXiv 2509.06006](https://arxiv.org/pdf/2509.06006). The size in MB is my estimate from parameter count, not a source figure.

### Inferences
- Recommended stack for FITme (iOS 27+, Apple Intelligence devices):
  1. Use Foundation Models with a `@Generable` schema such as `[FoodItem{name, matchedDbId, quantity, unit, cookingFat, confidence}]`.
  2. Give the model a `lookupFood` tool backed by a bundled local database (INDB/IFCT; see section 5).
  3. On iOS 27, accept a photo via `Attachment`.

  This stays fully on-device, adds no model weight to the app, and keeps calorie numbers coming from vetted data.
- The 4K-8K context limit rules out stuffing the whole food database into the prompt. Tool calling or local retrieval is required, which matches the grounding pattern anyway.
- For devices without Apple Intelligence, which are probably a large share of FITme's Indian users on older or non-Pro iPhones, options are: (a) a deterministic text parser plus database search, (b) a small bundled Core ML classifier for photos, or (c) an optional download of a roughly 0.3-2 GB MLX model. Option (c) costs significant storage and battery, so it is probably not worth it for a solo founder.
- Hindi and Hinglish input ("2 roti aur dal") may be handled poorly by the Apple model, since Hindi is unsupported. A local synonym table that maps Hinglish and regional dish names to database IDs is cheap and high-value. That last point is an inference, not tested.

### Gaps
- I found no published benchmark of the iOS 27 on-device model's image understanding on food, and no official per-device statement of its context size.
- The WWDC26 session I read did not specify whether image input works offline on every Apple Intelligence device or has extra hardware limits. Verify in the [Foundation Models documentation](https://developer.apple.com/videos/play/wwdc2026/241/) before building on it.
- Frameworks change at each WWDC. These notes reflect WWDC26 (June 2026) material, and iOS 27 point releases may have changed details.

## 4. Indian food image datasets and models

### Takeaway
Several Indian food datasets exist, but the largest and most recent (Khana, 131K images, 80 classes, 86.7% top-1) is licensed CC BY-NC-ND, which blocks commercial use. Most others are small (10-50 classes) with unclear licences. Classification at 80-90% is achievable, but these datasets carry no portion or nutrition labels, so they help only with identifying the dish.

### Cited Findings
- **Khana** (Prabhu, arXiv Sep 2025):
  - About 131K images, 80 classes, 500x500 px, scraped from search engines and from Swiggy/Zomato menus, with automated labelling and deduplication.
  - Licence: CC BY-NC-ND 4.0.
  - Baselines (top-1 / top-5): ResNet-152 81.00% / 95.37%; EfficientNet-V2-S 80.47% / 95.52%; ViT-B-16 85.34% / 97.15%; ConvNeXt-S 86.72% / 97.58%.

  — [arXiv 2509.06006](https://arxiv.org/abs/2509.06006); [site](https://khana.omkar.xyz)
- **IndianFood10 / IndianFood20** (Indian food platter object detection, YOLOv4, 2022):
  - IndianFood10: 11,547 annotated images across 10 classes; mAP 91.8%, F1 0.90. Per-class AP ranged from 94.9% (rasgulla) to 78.3% (aloo paratha).
  - IndianFood20: 17,817 images across 20 classes; results were preliminary and not reported.
  - Licence not stated in the snippet.

  — [arXiv 2205.04841](https://arxiv.org/pdf/2205.04841)
- **IndianFoodNet** (Agarwal et al., IJCMEM 2023): more than 5,500 images and more than 5,000 annotations across 30 classes, comparing YOLOv5, v7 and v8 for detection. — [IIETA](https://www.iieta.org/journals/ijcmem/paper/10.18280/ijcmem.110403)
- **DataCluster Labs Indian Food Image Dataset**: more than 1,000 images from more than 800 urban and rural locations (a commercial data vendor). — [Kaggle](https://www.kaggle.com/datasets/dataclusterlabs/indian-food-image-dataset); [GitHub](https://github.com/datacluster-labs/Indian-Food-Image-Dataset)
- **Hugging Face indian-foods-dataset**: 15 categories (biryani, chole bhature, dabeli, dosa, jalebi, paneer, ...). — [HF](https://huggingface.co/datasets/bharat-raghunathan/indian-foods-dataset). Another variant: [rajistics/indian_food_images](https://huggingface.co/datasets/rajistics/indian_food_images)
- A 50-class x 100-image Indian food dataset is referenced in transfer-learning tutorials. — [Medium / Analytics Vidhya](https://medium.com/analytics-vidhya/indian-food-image-classification-using-transfer-learning-b8878187ddd1) (secondary)
- One study reports a dataset of more than 15,000 images of 56 Indian food items evaluated with YOLOv5-v12, plus a RAG module that links detections to nutrition, ingredients and recipes. — search summary; the source paper was not identified precisely [unverified]

### Inferences
- Commercial use of Khana appears barred by NC-ND. Training a shipped model on it is risky without a separate licence from the author. Prefer datasets with explicit commercial-permissive licences, or the iOS 27 Apple vision model, which needs no training data from FITme.
- If using the Apple on-device VLM, a better use of these datasets is as an **evaluation set** for measuring how well the model names Indian dishes, subject to licence.

### Gaps
- I could not verify the existence or details of "INDoFoodNet" or an "Indian Food 101" benchmark. No primary source was found, so I do not cite them.
- Licences for IndianFood10/20 and IndianFoodNet were not confirmed.
- I found no Indian food dataset with weighed portion or nutrition ground truth, comparable to Nutrition5k.

## 5. Best-practice hybrid architecture (grounding, confidence, clarifying questions, correction loops) and evidence users care about on-device privacy

### Takeaway
The evidence favours a two-stage design. The AI identifies items and quantities, and the numbers come from a vetted food-composition database. Every study shows accuracy improves sharply when quantities or ingredient details are supplied. For India, an open recipe-level database (INDB, 1,014 recipes built on ICMR-NIN IFCT 2017) can ground the numbers. On privacy, surveys show broad concern about health data and AI, and an Indian survey links on-device AI to privacy. Willingness to pay for AI is low, though, so privacy works better as a trust differentiator than as a paid feature.

### Cited Findings
**Grounding data**
- The Indian Nutrient Databank (INDB, Current Developments in Nutrition, 2024; Gates Foundation funded) is open access. It has 1,095 food items, derived mainly from ICMR-NIN IFCT 2017 with gaps filled from IFCT 2004 and UK/US databases, plus 1,014 commonly consumed recipes. It is downloadable as Excel, and its generating code is on GitHub. — [PMC11277795](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11277795/); [GitHub INDB](https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-); [News-Medical](https://www.news-medical.net/news/20240616/New-open-access-resource-reveals-nutrient-content-of-Indian-foods.aspx)
- Related: FKG.in automates Indian food composition analysis through a food knowledge graph. — [arXiv 2412.05248](https://arxiv.org/html/2412.05248v3)
- NutriBench evaluated retrieval-augmented generation (RAG) alongside standard and chain-of-thought prompting for meal-description nutrition estimation. — [arXiv 2407.12843](https://arxiv.org/pdf/2407.12843v2)

**Clarifying questions**
- Adding fat, sweetener and meat type cut energy MAPE from 30.5% to 24.4%. Adding ingredient quantities cut it to 13.9%. — [PMC12655113](https://pmc.ncbi.nlm.nih.gov/articles/PMC12655113/)
- Additional user information raised GPT-4o energy R² from 0.59 to 0.94. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S088915752501659X) [unverified detail]

**Correction loops**
- ChatGPT is good at food identification (93% precision) and ranking meals, but poor on absolute portions. — [PMC11858203](https://pmc.ncbi.nlm.nih.gov/articles/PMC11858203/)
- MyFitnessPal manual or barcode entry reached 9.1% MAPE in an unverified meta-analysis, better than photo AI. — [clinicalnutritionreport.com](https://clinicalnutritionreport.com/research/ai-calorie-tracker-accuracy-meta-analysis-2026/) [unverified]
- Human review also helps: SnapCalorie layers human reviewers on top of AI to get under 20% error (company claim). — [TechCrunch](https://techcrunch.com/2023/06/26/snapcalorie-computer-vision-health-app-raises-3m/)

**Privacy evidence**
- A CMR (CyberMedia Research) survey of Indian smartphone buyers, reported Jul 2026, found 82% value transparent data practices and trust as purchase drivers, and 61% believe on-device AI processing improves responsiveness and privacy. Sample size was not reported. — [Free Press Journal](https://www.freepressjournal.in/tech/68-consumers-prioritise-ai-features-while-buying-smartphones-82-value-data-privacy-cmr-report)
- 78% of adults use digital health tools, but large majorities worry about privacy and data use and are cautious about AI features. — [URAC](https://www.urac.org/blog/consumers-rely-on-health-apps-yet-worry-about-privacy-and-ai/)
- Patients are less willing to use AI in healthcare if it requires access to personal data. About 89% say AI health responses need human oversight. — [Healthcare Dive](https://www.healthcaredive.com/news/data-privacy-concerns-could-hold-patients-back-from-using-ai/831902/)
- Importance of privacy varies by demographic: women, older people and college-educated users rate it higher. — [PR Newswire survey](https://www.prnewswire.com/news-releases/survey-users-of-digital-health-apps-are-divided-on-data-privacy-but-most-share-data-with-their-providers-or-family-members-301676372.html)
- Only 3% of smartphone owners would pay extra for AI features. — [eMarketer](https://www.emarketer.com/content/interest-on-device-ai-continues-decline-consumers-arent-willing-pay)

### Inferences
Recommended pipeline (synthesis, not a single sourced design):
1. Parse the text or photo into structured items with `@Generable`: dish, quantity, unit, cooking style, confidence.
2. Map each item to an INDB/IFCT recipe or food ID with a `Tool`, using local fuzzy and synonym search including Hinglish and regional names.
3. Compute macros deterministically as database value per gram x estimated grams. Use standard household-measure conversions (katori, roti, ladle) from a local table.
4. If confidence is low or the dish is fat-sensitive (curry, dal tadka, paratha, halwa), ask at most one or two quick-chip questions, such as "Oil/ghee: none / light / normal / restaurant" and "How many katoris/rotis?".
5. Show a range or confidence badge, not a falsely precise single number. Let users edit grams and items. Remember each user's corrections, such as typical roti size or home oil level, as on-device personal defaults.

Other inferences:
- Photo logging is worth adding on iOS 27 as a convenience front end to the same pipeline. Position it as "identify the dish, then confirm portion", not "instant calories". The evidence says photo-only calorie numbers are about 30% off and biased low.
- On privacy, keeping everything on-device lines up with a documented concern and a measurable Indian consumer belief (61%). Avoid PCC or cloud fallbacks entirely if "100% on-device" is the brand promise.

### Gaps
- I found no controlled study that directly compares user trust, retention or accuracy for confidence ranges vs point estimates in calorie apps, or that quantifies the benefit of clarifying-question UX outside LLM prompting studies.
- I found no survey that measures willingness to choose a nutrition app specifically because it processes data on-device rather than in the cloud. The CMR figure is about smartphones in general, and its methodology was not disclosed.
- INDB's licence terms for commercial redistribution inside an app were not confirmed.
