# FITme food database expansion

1,752 foods ready to bundle offline in FITme. 824 are tagged `diet_friendly`.

| File | What it is |
|---|---|
| `fitme_foods.json` | Full database (1,752 foods): per-100 g and per-serving macros, portions, tags, diet type, source |
| `fitme_foods.csv` | The same data flattened, for checking in Excel / Google Sheets |
| `fitme_diet_foods.csv` | The 824 diet-friendly foods only, Indian first |
| `indian_recipes.py` | The 309 Indian recipes in raw grams (edit these to change values) |
| `build_foods.py` | Rebuilds everything: `python3 build_foods.py` (downloads USDA data on first run) |

## What's inside

- **309 Indian dishes** computed from recipes: 40 dals, 52 sabzis, 30 veg curries, 26 non-veg curries, 21 rotis/breads, 14 rice dishes, 22 breakfasts, 24 snacks, 17 drinks, 14 sides, 11 sweets, 26 diet meals.
  - 77 of these are **low-oil versions** of everyday dishes (dal, sabzi, curry), so a dieter can log "Bhindi masala (low oil)" at 66 kcal instead of 99.
  - 161 Indian dishes are diet-friendly. Examples: moong chilla, egg-white bhurji, sprouts chaat, paneer tikka, hung curd, millet khichdi, roasted makhana, chaas.
- **887 foods as eaten** from USDA FNDDS 2021–2023 (eggs, oatmeal, breads, fruit, vegetables, fish, drinks, and USDA versions of naan, chapati, paratha, paneer, ghee, channa saag and filled dosa).
- **556 raw ingredients** from USDA SR Legacy (fruits, vegetables, pulses, grains, nuts and seeds, dairy, fish, poultry, oils, spices).
- **Diet types:** 1,059 vegan, 289 vegetarian, 80 eggetarian, 324 non-vegetarian. 334 foods are high-protein, 105 of them vegetarian or vegan.

## Legal / attribution

USDA FoodData Central is public domain (CC0), so you can bundle it in a paid app. USDA asks for a citation, so put this line on your About/Credits screen:

> Nutrition data: U.S. Department of Agriculture, Agricultural Research Service. FoodData Central. fdc.nal.usda.gov

No IFCT 2017, INDB or Kaggle data was used. IFCT forbids electronic reuse "for creating a product" without written permission from ICMR-NIN (see the research report). Indian values here are FITme's own recipe estimates built from USDA ingredients.

## How to load it in the app (Swift)

Add `fitme_foods.json` to the Xcode project (target membership on), then:

```swift
struct FoodDB: Decodable { let foods: [Food] }
struct Food: Decodable, Identifiable {
    struct Nutrients: Decodable {
        let kcal: Double; let protein_g: Double; let carbs_g: Double; let fat_g: Double
        let fiber_g: Double; let sugar_g: Double; let sodium_mg: Double
    }
    struct Portion: Decodable { let label: String; let grams: Double }
    let id: String; let name: String; let aka: String?; let category: String
    let cuisine: String; let diet_type: String; let serving: Portion
    let portions: [Portion]; let per_100g: Nutrients; let per_serving: Nutrients
    let tags: [String]; let source: String
}

let url = Bundle.main.url(forResource: "fitme_foods", withExtension: "json")!
let foods = try JSONDecoder().decode(FoodDB.self, from: Data(contentsOf: url)).foods
```

Search should match both `name` and `aka`, so "arhar dal" finds "Toor dal tadka" and "chapati" finds "Phulka". To log a custom amount, use `per_100g × grams / 100`.

## Things to know before shipping

1. **Indian values are estimates.** Home recipes vary, and oil/ghee is the biggest swing (a tablespoon is about 120 kcal). Show a "low oil / normal / restaurant" choice, or let users edit oil. The `ingredients_g` and `cooked_batch_g` fields show exactly how each dish was calculated.
2. **Proxies** where USDA has no exact Indian ingredient:
   - soya chunks = defatted soy flour
   - poha = raw white rice
   - daliya = bulgur
   - rohu/katla = carp
   - jaggery = brown sugar
   - bajra = millet
   - methi in thepla = spinach

   Ragi (finger millet) is **not included** because USDA has no entry for it.
3. **Diet type for mixed USDA dishes** comes from USDA's ingredient lists (`diet_type_basis`), not guessed from the name. Baked goods can still hide egg, so show "check the label" for packaged items.
4. **Dedupe against your existing 60+ foods** on import (match on lower-cased `name`/`aka`) so users don't see two "Dal" entries.
5. Before showing any **"diet_friendly"** badge, decide your wording. It's a rule-based tag: high protein, low calorie or high fibre, without high sugar, fat or sodium. It is not medical advice.

The rules behind each tag are in `tags_for()` in `build_foods.py` if you want to tune them.
