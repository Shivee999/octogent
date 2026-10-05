"""Build FITme's expanded food database (JSON + CSV) from public-domain sources.

Sources (both CC0 / public domain, safe to bundle in a commercial app):
  - USDA FoodData Central, SR Legacy (April 2018): raw ingredients
  - USDA FoodData Central, FNDDS 2021-2023 (Oct 2024 release): foods as eaten
Indian dishes are computed from raw-ingredient recipes in indian_recipes.py.

Usage:
  python3 build_foods.py [--cache DIR]
Downloads the two USDA CSV zips into the cache dir on first run.
"""
import argparse
import csv
import glob
import io
import json
import os
import re
import urllib.request
import zipfile

import indian_recipes

SR_URL = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_csv_2018-04.zip"
FNDDS_URL = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_survey_food_csv_2024-10-31.zip"

# FDC nutrient ids
NUTRIENTS = {"kcal": "1008", "protein_g": "1003", "carbs_g": "1005", "fat_g": "1004",
             "fiber_g": "1079", "sugar_g": "2000", "sodium_mg": "1093"}

HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(url, cache):
    name = os.path.basename(url).replace(".zip", "")
    dest = os.path.join(cache, name)
    if not glob.glob(os.path.join(dest, "*", "food.csv")) and not os.path.exists(os.path.join(dest, "food.csv")):
        os.makedirs(dest, exist_ok=True)
        print("downloading", url)
        data = urllib.request.urlopen(url).read()
        zipfile.ZipFile(io.BytesIO(data)).extractall(dest)
    hits = glob.glob(os.path.join(dest, "**", "food.csv"), recursive=True)
    return os.path.dirname(hits[0])


def rows(d, name):
    with open(os.path.join(d, name), newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def load_dataset(d):
    foods = {r["fdc_id"]: r for r in rows(d, "food.csv")}
    nut = {}
    # FNDDS food_nutrient rows use the legacy nutrient number (208) where SR uses the id (1008).
    alias = {}
    for r in rows(d, "nutrient.csv"):
        nbr = (r.get("nutrient_nbr") or "").split(".")[0]
        if r["id"] in NUTRIENTS.values():
            alias[r["id"]] = r["id"]
            if nbr:
                alias[nbr] = r["id"]
    for r in rows(d, "food_nutrient.csv"):
        key = alias.get(r["nutrient_id"])
        if key:
            nut.setdefault(r["fdc_id"], {})[key] = float(r["amount"] or 0)
    units = {r["id"]: r["name"] for r in rows(d, "measure_unit.csv")}
    portions = {}
    for r in rows(d, "food_portion.csv"):
        g = float(r["gram_weight"] or 0)
        if g <= 0:
            continue
        desc = (r.get("portion_description") or "").strip()
        if not desc or desc == "Quantity not specified":
            unit = units.get(r["measure_unit_id"], "")
            amt = r["amount"] or "1"
            amt = amt[:-2] if amt.endswith(".0") else amt
            mod = (r.get("modifier") or "").strip()
            if unit and unit != "undetermined":
                desc = f"{amt} {unit}" + (f", {mod}" if mod and not mod.isdigit() else "")
            elif mod and not mod.isdigit():
                desc = f"{amt} {mod}"
        if not desc or desc == "Quantity not specified":
            continue
        portions.setdefault(r["fdc_id"], []).append((int(r["seq_num"] or 0), desc, g))
    for v in portions.values():
        v.sort()
    return foods, nut, portions


def choose_serving(por, category, kcal100=0.0):
    pick = _choose_serving(por, category)
    # Raw flours, dry pulses and syrups list "1 cup" first; ~700 kcal defaults mislead users.
    if kcal100 * pick[1] / 100 > 450:
        smaller = [(d, g) for _, d, g in por if 15 <= g < pick[1]]
        if smaller:
            return min(smaller, key=lambda x: abs(kcal100 * x[1] / 100 - 200))
        return ("100 g", 100.0) if kcal100 <= 450 else ("30 g", 30.0)
    return pick


def _choose_serving(por, category):
    """Pick a realistic default portion: a tablespoon for fats/condiments, a cup/glass
    for drinks, otherwise the first listed portion between 20 g and 350 g."""
    if not por:
        return ("100 g", 100.0)
    cat = category.lower()
    if re.search(r"oil|fats|butter|dressing|condiment|sauce|spice|sugar|jam|syrup|margarine|mayonnaise", cat):
        for _, d, g in por:
            if "tablespoon" in d or "tbsp" in d:
                return (d, g)
        for _, d, g in por:
            if g <= 30:
                return (d, g)
    if re.search(r"beverage|coffee|tea|juice|milk|drink|water|smoothie|beer|wine", cat):
        for _, d, g in por:
            if re.search(r"\bcup\b|mug|glass|bottle|can\b", d) and 150 <= g <= 400:
                return (d, g)
    for _, d, g in por:
        if 20 <= g <= 350:
            return (d, g)
    return (por[0][1], por[0][2])


def per100(nut_row):
    return {k: round(nut_row.get(i, 0.0), 2) for k, i in NUTRIENTS.items()}


# ---------------------------------------------------------------- selection

BRAND = re.compile(r"\b[A-Z][A-Z'&]{2,}\b")  # ALL-CAPS words are brand names in SR Legacy
EXCLUDE = re.compile(
    r"babyfood|baby food|infant|formula|toddler|navajo|northern plains|alaska native|apache|hopi|"
    r"shoshone|\(ns as to|ns as to|quality control|industrial|imitation|, with salt\b|\bwith salt\b|"
    r"\bdehydrated\b|freeze-dried|\bcanned\b.*\bheavy syrup\b|frankfurter|bologna|luncheon|"
    r"restaurant, |fast foods?,|school lunch|military|meatless|game meat, (bear|beaver|bison|boar|caribou|elk|moose|muskrat|opossum|raccoon|squirrel|antelope|beefalo)|"
    r"\bvariety meats\b|\bbrain\b|\blungs?\b|\bspleen\b|\bpancreas\b|\bthymus\b|\bmechanically\b|separable fat|"
    r"\bsuet\b|\blard\b|\btallow\b|cured|\bwhale\b|\bseal\b|walrus|\bbeluga\b|\bpoi\b|"
    r"\bhuman milk\b|nutritional powder|\(.*\b(zone|eas|slimfast|ensure|boost|glucerna|atkins|kellogg|quaker|general mills|nabisco)\b",
    re.I)

# SR Legacy: category id -> cap, and preference regex (preferred first)
SR_CAPS = {
    "1": 45, "2": 12, "4": 12, "5": 22, "8": 10, "9": 90, "11": 150, "12": 45, "13": 12,
    "10": 8, "14": 15, "15": 55, "16": 55, "17": 6, "20": 50,
}
SR_PREFER = re.compile(r"\braw\b|boiled|cooked|roasted|dry roasted|dried|plain|whole", re.I)
SR_KEEP_SPICES = re.compile(r"cumin|turmeric|coriander seed|chili powder|curry powder|fenugreek|"
                            r"black pepper|cinnamon|cardamom|cloves|ginger, ground|mustard seed|garlic powder", re.I)

FNDDS_CAPS_DEFAULT = 4
FNDDS_EXCLUDE = re.compile(r"as ingredient in|puerto rican|cuban|dominican|with cracklings|mixture, dried|"
                           r"\bNFS\b.*\bNFS\b|from school|cooking spray|baby|kosher|leaf$|for use (with|on)|as ingredient|"
                           r"chicken (feet|skin)|chicken, (tail|back|neck)|light (creamy|italian|mayonnaise)|"
                           r"fat free|goose egg|duck egg|pickled", re.I)
# Covered by FITme's own Indian recipes; keeping both would show two conflicting entries.
FNDDS_COVERED = {"dal", "idli", "samosa", "upma", "vada", "pakora", "palak paneer", "dosa, plain",
                 "chicken curry", "bread, puri", "biryani with chicken", "biryani with vegetables",
                 "sambar, vegetable stew", "ladoo, round ball", "lentil curry", "vegetable curry"}
FNDDS_CAPS = {
    # categories most useful to Indian / diet users get more slots
    "1002": 3, "1004": 2, "1006": 2, "1008": 2, "1602": 12, "1604": 6, "1820": 6, "1822": 8, "1902": 8,
    "2202": 14, "2206": 6, "2402": 18, "2404": 10, "2502": 12, "2802": 25, "2804": 25, "2806": 12,
    "3002": 10, "3004": 12, "3006": 8, "3102": 12, "3104": 15, "3202": 18, "3204": 8, "3208": 10,
    "3402": 6, "3404": 6, "3406": 6, "3602": 6, "3702": 6, "3804": 8, "4002": 15, "4004": 14,
    "4202": 14, "4204": 5, "4208": 5, "4402": 6, "4404": 6, "4602": 5, "4604": 8, "4802": 6,
    "4804": 10, "5002": 4, "5006": 5, "5202": 5, "5402": 6, "5404": 8, "5502": 6, "5504": 6,
    "5802": 6, "6002": 4, "6012": 6, "6016": 10, "6018": 20, "6024": 5, "6402": 4, "6404": 6,
    "6406": 8, "6407": 6, "6409": 8, "6410": 6, "6411": 20, "6412": 6, "6413": 6, "6414": 4,
    "6416": 6, "6418": 12, "6420": 30, "6430": 6, "6802": 8, "6804": 4, "6806": 6, "7002": 4,
    "7006": 6, "7008": 3, "7102": 3, "7208": 6, "7220": 10, "7302": 12, "7304": 12, "7502": 3,
    "7504": 4, "7506": 6, "7702": 1, "7802": 2, "8002": 4, "8006": 4, "8008": 5, "8012": 10,
    "8406": 8, "8408": 8, "8412": 8, "8802": 5, "8804": 4, "8806": 6, "9802": 6, "9999": 10,
}
FNDDS_SKIP_CATS = {"9002", "9004", "9006", "9007", "9008", "9010", "9012", "9202", "9204",
                   "9402", "9404", "9602", "3703", "3704", "3706", "3720", "3722", "3730", "3740",
                   "3742", "2602", "2604", "2606", "2608", "2204", "5702", "5704", "7202", "7204",
                   "7206", "7104", "7106", "7804", "8004", "8010", "8402", "8404", "8410", "6489"}
FNDDS_PENALTY = re.compile(r"fat added|from restaurant|from fast food|frozen|canned|NS as to|"
                           r"from school|with gravy|with cheese sauce|light syrup|heavy syrup|"
                           r"\(.*\)|baby|kosher", re.I)
FNDDS_ALWAYS = re.compile(r"paneer|ghee|idli|dosa|biryani|sambar|chutney|barfi|firni|saag|tikka|"
                          r"naan|chapati|roti\b|paratha|lassi|\bchai\b|masala|korma|tandoori", re.I)


def clean_name(s):
    s = re.sub(r"\s*\(Includes foods for USDA's Food Distribution Program\)", "", s)
    s = re.sub(r"\s*\(includes foods for usda's food distribution program\)", "", s, flags=re.I)
    s = s.replace(", without salt", "").replace(" without salt", "")
    s = re.sub(r",\s*all commercial varieties", "", s)
    s = re.sub(r"\s+", " ", s).strip(" ,")
    return s


def pick_sr(foods, nut):
    by_cat = {}
    for fid, r in foods.items():
        cat = r["food_category_id"]
        if cat not in SR_CAPS:
            continue
        d = r["description"]
        if EXCLUDE.search(d) or BRAND.search(d) or fid not in nut:
            continue
        if cat == "2" and not SR_KEEP_SPICES.search(d):
            continue
        if cat in ("13", "10", "17") and not re.search(r"ground|lean|tenderloin|loin|goat|leg", d, re.I):
            continue
        if cat == "4" and not re.search(r"^Oil, (olive|soybean, salad or cooking$|mustard|coconut|canola|sunflower|peanut|sesame|rice bran)|ghee|^Butter, (salted|without salt)|^Margarine", d, re.I):
            continue
        if "1008" not in nut[fid]:
            continue
        score = (0 if SR_PREFER.search(d) else 1, d.count(","), len(d))
        by_cat.setdefault(cat, []).append((score, fid))
    out = []
    for cat, lst in by_cat.items():
        lst.sort()
        out += [fid for _, fid in lst[: SR_CAPS[cat]]]
    return out


def pick_fndds(foods, nut, d):
    cat_of = {r["fdc_id"]: r["wweia_category_number"] for r in rows(d, "survey_fndds_food.csv")}
    by_cat = {}
    always = []
    for fid, r in foods.items():
        cat = cat_of.get(fid, "")
        desc = r["description"]
        if cat in FNDDS_SKIP_CATS or fid not in nut or "1008" not in nut[fid]:
            continue
        if EXCLUDE.search(desc) or FNDDS_EXCLUDE.search(desc) or desc.lower() in FNDDS_COVERED:
            continue
        if FNDDS_ALWAYS.search(desc) and not FNDDS_PENALTY.search(desc):
            always.append(fid)
            continue
        score = (1 if FNDDS_PENALTY.search(desc) else 0, desc.count(","), len(desc))
        by_cat.setdefault(cat, []).append((score, fid))
    out = list(always)
    for cat, lst in by_cat.items():
        lst.sort()
        cap = FNDDS_CAPS.get(cat, FNDDS_CAPS_DEFAULT)
        out += [fid for s, fid in lst[:cap] if s[0] == 0 or cap >= 10]
    return out, cat_of


# ---------------------------------------------------------------- tagging

NONVEG = re.compile(r"\b(chicken|turkey|duck|goose|beef|pork|lamb|mutton|goat|veal|ham|bacon|sausage|"
                    r"fish|salmon|tuna|cod|tilapia|shrimp|prawn|crab|lobster|clam|oyster|mussel|scallop|"
                    r"squid|octopus|anchov\w*|sardines?|mackerel|trout|catfish|carp|herring|pollock|haddock|"
                    r"halibut|snapper|meat|keema|kebab|gelatin|venison|rabbit|quail|pheasant|emu|ostrich|"
                    r"liver|gizzard|pepperoni|salami|jerky|caviar|roe|frankfurter|bologna|broth|stock|lard)\b", re.I)
NOT_NONVEG = re.compile(r"coconut meat|meatless|meat substitute|imitation|vegetarian|veggie|vegan|"
                        r"oyster mushroom|oyster crackers?|includes oyster|crab ?apple|vegetable (broth|stock)|mushroom broth", re.I)
EGG = re.compile(r"\b(egg|eggs|omelet|omelette|mayonnaise|custard|meringue|anda)\b|french toast|ladyfinger", re.I)
NOT_EGG = re.compile(r"eggplant|egg-free|eggless|egg substitute", re.I)
DAIRY = re.compile(r"\b(milk|cheese|paneer|yogurt|yoghurt|curd|dahi|cream|butter|ghee|whey|casein|lassi|"
                   r"kheer|kulfi|raita|chai|latte|cappuccino|mocha|pudding|barfi|rasgulla|shrikhand|chaas|"
                   r"makhani|malai|kadhi|honey)\b|ice cream", re.I)
NOT_DAIRY = re.compile(r"non-?dairy|coconut milk|almond milk|soy ?milk|oat milk|rice milk|cashew milk|"
                       r"plant-based|peanut butter|nut butter|almond butter|cocoa butter|butternut|"
                       r"milkweed|cream of tartar|soy yogurt|yogurt, soy|coconut cream|butterbur|butterhead", re.I)
FRIED_SWEET = re.compile(r"fried|pakora|samosa|puri\b|bhatura|jalebi|jamun|ladoo|laddu|halwa|cake|cookie|"
                         r"doughnut|pastry|candy|chocolate|ice cream|soft drink|soda|syrup|frosting|chips|"
                         r"butter chicken|butter masala|cream|beer|wine|liquor|cocktail|vodka|whiskey|\brum\b|\bgin\b", re.I)

# Recipe diet type comes from ingredient keys, which is exact, instead of name regexes.
REC_NONVEG = {"chicken_breast", "chicken_thigh", "mutton", "fish", "prawn"}
REC_EGG = {"egg", "egg_white"}
REC_DAIRY = {"milk", "milk_low", "curd", "curd_low", "paneer", "cream", "cottage_low", "ghee", "butter", "whey", "honey"}
SR_NONVEG_CATS = {"5", "7", "10", "13", "15", "17"}


def recipe_diet_type(keys):
    keys = set(keys)
    if keys & REC_NONVEG:
        return "non_vegetarian"
    if keys & REC_EGG:
        return "eggetarian"
    if keys & REC_DAIRY:
        return "vegetarian"
    return "vegan"


def diet_type(name, ingredients=None):
    """Strictest diet type implied by the name or any ingredient description."""
    nonveg = egg = dairy = False
    for t in [name] + list(ingredients or []):
        nonveg |= bool(NONVEG.search(t)) and not NOT_NONVEG.search(t)
        egg |= bool(EGG.search(t)) and not NOT_EGG.search(t)
        dairy |= bool(DAIRY.search(t)) and not NOT_DAIRY.search(t)
    if nonveg:
        return "non_vegetarian"
    if egg:
        return "eggetarian"
    if dairy:
        return "vegetarian"
    return "vegan"


def sr_diet_type(name, cat):
    if cat in SR_NONVEG_CATS:
        return "non_vegetarian"
    if cat == "1":
        if EGG.search(name) and not NOT_EGG.search(name):
            return "eggetarian"
        return "vegan" if NOT_DAIRY.search(name) else "vegetarian"
    return diet_type(name)


def tags_for(name, p100, serving_g, category, diet_variant=False, added_sugar_serving=0.0):
    t = []
    kcal = p100["kcal"] or 0.0001
    serv = {k: v * serving_g / 100 for k, v in p100.items()}
    protein_share = p100["protein_g"] * 4 / kcal if kcal > 1 else 0
    if protein_share >= 0.25 and serv["protein_g"] >= 8:
        t.append("high_protein")
    if p100["kcal"] <= 80 or (serv["kcal"] <= 120 and p100["kcal"] <= 150):
        t.append("low_calorie")
    if p100["fiber_g"] >= 6 or serv["fiber_g"] >= 5:
        t.append("high_fiber")
    if p100["fat_g"] <= 3:
        t.append("low_fat")
    natural_sugar = re.search(r"fruit|dairy|milk|yogurt|curd|dahi|raisin|date", category + " " + name, re.I)
    if (p100["sugar_g"] >= 15 and not natural_sugar) or added_sugar_serving >= 10:
        t.append("high_sugar")
    if p100["sodium_mg"] >= 600:
        t.append("high_sodium")
    healthy = any(x in t for x in ("high_protein", "low_calorie", "high_fiber"))
    fat_share = p100["fat_g"] * 9 / kcal if kcal > 1 else 0
    seasoning = re.search(r"spice|herb|oil|fats|condiment|sugar|syrup|alcohol|liquor|beer|wine", category, re.I)
    if (diet_variant or healthy) and not seasoning and "high_sugar" not in t and not FRIED_SWEET.search(name) \
            and added_sugar_serving < 5 and serv["kcal"] <= 450 and fat_share <= 0.45 \
            and p100["kcal"] <= 400 and "high_sodium" not in t:
        t.append("diet_friendly")
    return t


def round_nut(d):
    return {k: (round(v) if k in ("kcal", "sodium_mg") else round(v, 1)) for k, v in d.items()}


# ---------------------------------------------------------------- recipes

def compute_recipe(rec, lookup):
    total = {k: 0.0 for k in NUTRIENTS}
    names = []
    for key, grams in rec["ing"].items():
        if grams <= 0 or key == "water":
            continue
        src = indian_recipes.ING[key]
        p = lookup(src)
        for k in total:
            total[k] += p[k] * grams / 100
        names.append(key)
    cooked = rec["cooked"]
    p100 = {k: v * 100 / cooked for k, v in total.items()}
    return p100, names


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(HERE, ".usda_cache"))
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()

    sr_dir = fetch(SR_URL, args.cache)
    fn_dir = fetch(FNDDS_URL, args.cache)
    sr_foods, sr_nut, sr_por = load_dataset(sr_dir)
    fn_foods, fn_nut, fn_por = load_dataset(fn_dir)
    sr_cats = {r["id"]: r["description"] for r in rows(sr_dir, "food_category.csv")}
    wweia = {r["wweia_food_category"]: r["wweia_food_category_description"]
             for r in rows(fn_dir, "wweia_food_category.csv")}

    # FNDDS lists each food's ingredients (SR descriptions, sometimes other FNDDS foods);
    # deriving veg/non-veg from them is far more reliable than the dish name.
    fn_inputs = {}
    for r in rows(fn_dir, "input_food.csv"):
        fn_inputs.setdefault(r["fdc_id"], []).append((r.get("sr_description") or "", r.get("fdc_of_input_food") or ""))

    def fn_ingredient_texts(fid, depth=0):
        out = []
        for desc, sub in fn_inputs.get(fid, []):
            out.append(desc)
            if sub and depth < 3:
                out += fn_ingredient_texts(sub, depth + 1)
        return out

    def lookup(src):
        ds, fid = src
        nut = sr_nut if ds == "sr" else fn_nut
        return per100(nut[str(fid)])

    out, seen = [], set()

    def add(item):
        key = re.sub(r"[^a-z0-9]+", " ", item["name"].lower()).strip()
        if key in seen:
            return
        seen.add(key)
        out.append(item)

    # 1) Indian recipes first so their names win any dedupe
    for rec in indian_recipes.recipes():
        p100, ing_names = compute_recipe(rec, lookup)
        sg = rec["serving_g"]
        add({
            "id": "fitme-in-" + re.sub(r"[^a-z0-9]+", "-", rec["name"].lower()).strip("-"),
            "name": rec["name"],
            "aka": rec["aka"],
            "category": rec["category"],
            "cuisine": "Indian",
            "diet_type": recipe_diet_type(ing_names),
            "diet_type_basis": "recipe_ingredients",
            "serving": {"label": rec["serving"], "grams": sg},
            "portions": [{"label": rec["serving"], "grams": sg}, {"label": "100 g", "grams": 100}],
            "per_100g": round_nut(p100),
            "per_serving": round_nut({k: v * sg / 100 for k, v in p100.items()}),
            "tags": tags_for(rec["name"], p100, sg, rec["category"], rec.get("diet_variant", False),
                             added_sugar_serving=sum(rec["ing"].get(k, 0) for k in ("sugar", "jaggery", "honey"))
                             * sg / rec["cooked"]),
            "source": "FITme recipe estimate from USDA FoodData Central ingredients",
            "source_id": None,
            "ingredients_g": {k: v for k, v in rec["ing"].items() if v > 0},
            "cooked_batch_g": rec["cooked"],
            "note": rec.get("note") or "Home recipes vary; oil/ghee is the biggest swing. Let users edit oil.",
        })

    # 2) USDA FNDDS foods-as-eaten
    fn_ids, fn_cat = pick_fndds(fn_foods, fn_nut, fn_dir)
    for fid in fn_ids:
        r = fn_foods[fid]
        name = clean_name(r["description"])
        p100 = per100(fn_nut[fid])
        por = fn_por.get(fid, [])
        cat = wweia.get(fn_cat.get(fid, ""), "Other")
        serving = choose_serving(por, cat, fn_nut[fid].get("1008", 0))
        add({
            "id": f"usda-fndds-{fid}",
            "name": name, "aka": None, "category": cat,
            "cuisine": "Indian" if FNDDS_ALWAYS.search(name) and re.search(r"paneer|ghee|dal|idli|dosa|samosa|biryani|sambar|upma|vada|pakora|chutney|barfi|firni|ladoo|saag|naan|chapati|roti|paratha|lassi|chai|curry", name, re.I) else "Global",
            "diet_type": diet_type(name, fn_ingredient_texts(fid)),
            "diet_type_basis": "usda_ingredient_list" if fn_inputs.get(fid) else "name_only",
            "serving": {"label": serving[0], "grams": round(serving[1], 1)},
            "portions": [{"label": d, "grams": round(g, 1)} for _, d, g in por[:5]] + [{"label": "100 g", "grams": 100}],
            "per_100g": round_nut(p100),
            "per_serving": round_nut({k: v * serving[1] / 100 for k, v in p100.items()}),
            "tags": tags_for(name, p100, serving[1], cat),
            "source": "USDA FoodData Central - FNDDS 2021-2023",
            "source_id": int(fid),
            "ingredients_g": None, "cooked_batch_g": None, "note": None,
        })

    # 3) USDA SR Legacy ingredients
    for fid in pick_sr(sr_foods, sr_nut):
        r = sr_foods[fid]
        name = clean_name(r["description"])
        p100 = per100(sr_nut[fid])
        por = sr_por.get(fid, [])
        cat = sr_cats.get(r["food_category_id"], "Other")
        serving = choose_serving(por, cat, sr_nut[fid].get("1008", 0))
        add({
            "id": f"usda-sr-{fid}",
            "name": name, "aka": None, "category": cat, "cuisine": "Global",
            "diet_type": sr_diet_type(name, r["food_category_id"]),
            "diet_type_basis": "single_ingredient",
            "serving": {"label": serving[0], "grams": round(serving[1], 1)},
            "portions": [{"label": d, "grams": round(g, 1)} for _, d, g in por[:5]] + [{"label": "100 g", "grams": 100}],
            "per_100g": round_nut(p100),
            "per_serving": round_nut({k: v * serving[1] / 100 for k, v in p100.items()}),
            "tags": tags_for(name, p100, serving[1], cat),
            "source": "USDA FoodData Central - SR Legacy",
            "source_id": int(fid),
            "ingredients_g": None, "cooked_batch_g": None, "note": None,
        })

    meta = {
        "name": "FITme food database expansion",
        "version": "1.0.0",
        "count": len(out),
        "units": {"kcal": "kcal", "protein_g": "g", "carbs_g": "g", "fat_g": "g", "fiber_g": "g",
                  "sugar_g": "g", "sodium_mg": "mg"},
        "license": "USDA FoodData Central data is public domain (CC0 1.0). FITme recipe values are "
                   "derived estimates from those ingredients.",
        "attribution": "U.S. Department of Agriculture, Agricultural Research Service. FoodData Central. fdc.nal.usda.gov",
    }
    with open(os.path.join(args.out, "fitme_foods.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "foods": out}, f, ensure_ascii=False, indent=1)

    cols = ["id", "name", "aka", "category", "cuisine", "diet_type", "serving_label", "serving_g",
            "kcal_100g", "protein_100g", "carbs_100g", "fat_100g", "fiber_100g", "sugar_100g", "sodium_mg_100g",
            "kcal_serving", "protein_serving", "carbs_serving", "fat_serving", "tags", "source", "source_id"]
    with open(os.path.join(args.out, "fitme_foods.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for x in out:
            p, s = x["per_100g"], x["per_serving"]
            w.writerow([x["id"], x["name"], x["aka"] or "", x["category"], x["cuisine"], x["diet_type"],
                        x["serving"]["label"], x["serving"]["grams"], p["kcal"], p["protein_g"], p["carbs_g"],
                        p["fat_g"], p["fiber_g"], p["sugar_g"], p["sodium_mg"], s["kcal"], s["protein_g"],
                        s["carbs_g"], s["fat_g"], "|".join(x["tags"]), x["source"], x["source_id"] or ""])

    diet = [x for x in out if "diet_friendly" in x["tags"]]
    with open(os.path.join(args.out, "fitme_diet_foods.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "aka", "category", "cuisine", "diet_type", "serving_label", "serving_g",
                    "kcal_serving", "protein_serving", "carbs_serving", "fat_serving", "fiber_serving", "tags"])
        for x in sorted(diet, key=lambda x: (x["cuisine"] != "Indian", x["category"], x["name"])):
            s_ = x["per_serving"]
            w.writerow([x["id"], x["name"], x["aka"] or "", x["category"], x["cuisine"], x["diet_type"],
                        x["serving"]["label"], x["serving"]["grams"], s_["kcal"], s_["protein_g"], s_["carbs_g"],
                        s_["fat_g"], s_["fiber_g"], "|".join(x["tags"])])

    from collections import Counter
    print("total", len(out))
    print(Counter(x["source"].split(" - ")[-1] for x in out))
    print("diet_friendly", sum("diet_friendly" in x["tags"] for x in out))
    print("indian", sum(x["cuisine"] == "Indian" for x in out))


if __name__ == "__main__":
    main()
