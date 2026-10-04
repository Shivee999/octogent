"""Indian home-style and diet recipes for FITme, written as raw-ingredient grams.

Nutrition is computed from USDA FoodData Central (public domain) ingredient
values, never from IFCT 2017 / INDB, because IFCT forbids electronic reuse
"for creating a product" without written permission from ICMR-NIN.

Each recipe makes a batch; `cooked` is the finished batch weight in grams
(water absorbed / evaporated), and `serving` is the logged portion.
Portion sizes follow NIN household measures: medium katori = 200 ml,
1 tbsp = 15 g, 1 tsp = 5 g. Home recipes vary a lot, especially oil, so
every value here is an estimate and the app should let users edit oil.
"""

# Ingredient key -> (dataset, fdc_id). "proxy" notes mark the nearest
# USDA match where USDA has no exact Indian ingredient.
ING = {
    # pulses
    "toor": ("sr", 172436), "moong": ("sr", 174256), "masoor": ("sr", 174284),
    "urad": ("sr", 174259), "chana": ("sr", 173756), "rajma": ("sr", 173744),
    "lobia": ("sr", 173758), "moth": ("sr", 172425), "soybean": ("sr", 174270),
    "soy_chunks": ("sr", 174275),  # proxy: defatted soy flour (soya chunks are textured defatted soy)
    "besan": ("sr", 174288), "moong_sprouts": ("sr", 169957), "peanut": ("sr", 172430),
    # grains
    "rice": ("sr", 168877), "brown_rice": ("sr", 169703), "atta": ("sr", 168893),
    "maida": ("sr", 168894), "suji": ("sr", 169715),
    "daliya": ("sr", 170688),  # proxy: bulgur (cracked wheat)
    "oats": ("sr", 169705), "bajra": ("sr", 169702),  # millet, raw
    "jowar": ("sr", 168943), "makki": ("sr", 169697), "quinoa": ("sr", 168874),
    "amaranth": ("sr", 170682),
    "poha": ("sr", 168877),  # proxy: raw white rice (flattened rice is parboiled rice)
    "bread_ww": ("sr", 172688),
    # fats
    "oil": ("sr", 171411), "mustard_oil": ("sr", 172337), "coconut_oil": ("sr", 171412),
    "ghee": ("sr", 171314), "butter": ("sr", 173410),
    # vegetables
    "onion": ("sr", 170000), "tomato": ("sr", 170457), "potato": ("sr", 170026),
    "cauliflower": ("sr", 169986), "okra": ("sr", 169260), "brinjal": ("sr", 169228),
    "spinach": ("sr", 168462), "cabbage": ("sr", 169975), "peas": ("sr", 170419),
    "carrot": ("sr", 170393), "beans": ("sr", 169961), "capsicum": ("sr", 170427),
    "mushroom": ("sr", 169251), "pumpkin": ("sr", 168448), "lauki": ("sr", 169232),
    "tori": ("sr", 168414), "karela": ("sr", 168393), "garlic": ("sr", 169230),
    "ginger": ("sr", 169231), "green_chili": ("sr", 170497), "coriander": ("sr", 169997),
    "cucumber": ("sr", 168409), "corn": ("sr", 169998), "beetroot": ("sr", 169145),
    "radish": ("sr", 169276), "sweet_potato": ("sr", 168482), "red_capsicum": ("sr", 170108),
    "mustard_greens": ("fndds", 2709606),
    # dairy, eggs, meat, fish
    "milk": ("sr", 171265), "milk_low": ("sr", 170872), "curd": ("sr", 171284),
    "curd_low": ("sr", 170886), "paneer": ("fndds", 2705740), "cream": ("sr", 170859),
    "cottage_low": ("sr", 173417), "tofu": ("sr", 172475),
    "egg": ("sr", 171287), "egg_white": ("sr", 172183),
    "chicken_breast": ("sr", 171077), "chicken_thigh": ("sr", 173627),
    "mutton": ("sr", 175303),  # goat meat, raw
    "fish": ("sr", 171952),  # proxy: carp (rohu/katla are carps)
    "prawn": ("sr", 175179), "whey": ("sr", 173177),
    # sweeteners, nuts, fruit, misc
    "sugar": ("sr", 169655), "jaggery": ("sr", 168833),  # proxy: brown sugar
    "honey": ("sr", 169640), "cashew": ("sr", 170162), "almond": ("sr", 170567),
    "walnut": ("sr", 170187), "coconut": ("sr", 170169), "coconut_milk": ("sr", 170172),
    "makhana": ("sr", 170149),  # lotus seeds, dried
    "chia": ("sr", 170554), "flax": ("sr", 169414), "pumpkin_seed": ("sr", 170556),
    "sesame": ("sr", 170150), "peanut_butter": ("sr", 172470),
    "banana": ("sr", 173944), "lemon": ("sr", 167747), "tamarind": ("sr", 167763),
    "mango": ("sr", 169910), "dates": ("sr", 168191), "coconut_water": ("sr", 170174),
    "apple": ("sr", 171688), "papaya": ("sr", 169926), "pomegranate": ("sr", 169134),
    "guava": ("sr", 173044), "orange": ("sr", 169097),
    "tea": ("sr", 173227), "coffee": ("sr", 171890),
    "masala": ("sr", 170924),  # generic dry spice mix (curry powder) for turmeric/chili/coriander/garam masala
    "cumin": ("sr", 170923), "mustard_seed": ("sr", 170929), "salt": ("sr", 173468),
    "water": None,
}

# Oil per serving (g). Regular reflects typical home cooking; low-oil is
# roughly 1/2 tsp and is the "diet" variant users pick when cooking lighter.
OIL_REG = 7
OIL_LOW = 2.5


def _sabzi(name, aka, veg, extra=None, serves=3, veg_g=300, fat="oil"):
    """Dry vegetable stir-fry: veg + onion + tomato + spices, ~100 g serving."""
    out = []
    for low in (False, True):
        ing = {veg: veg_g, "onion": 50, "tomato": 40, "ginger": 3, "garlic": 3,
               "masala": 4, "cumin": 1, "salt": 3, fat: (OIL_LOW if low else OIL_REG) * serves}
        if extra:
            for k, v in extra.items():
                ing[k] = ing.get(k, 0) + v
        raw = sum(v for k, v in ing.items() if k not in ("salt",))
        cooked = round(raw * 0.8)
        out.append(dict(
            name=f"{name} (low oil)" if low else name, aka=aka, category="Sabzi (dry vegetable)",
            serving="1 katori (100 g)", serving_g=100, ing=ing, cooked=cooked,
            diet_variant=low, base=name))
    return out


def _dal(name, aka, pulse, serves=3, pulse_g=90, fat="oil", extra=None, cooked=450):
    """Pulse cooked with water and tempered; 1 medium katori = 150 g."""
    out = []
    for low in (False, True):
        ing = {pulse: pulse_g, "onion": 30, "tomato": 40, "ginger": 3, "garlic": 4,
               "masala": 3, "cumin": 1, "salt": 3, fat: (OIL_LOW if low else OIL_REG - 2) * serves}
        if extra:
            for k, v in extra.items():
                ing[k] = ing.get(k, 0) + v
        out.append(dict(
            name=f"{name} (low oil)" if low else name, aka=aka, category="Dal & legumes",
            serving="1 katori (150 g)", serving_g=150, ing=ing, cooked=cooked,
            diet_variant=low, base=name))
    return out


def _curry(name, aka, protein, protein_g, serves=3, category="Curry", extra=None,
           rich=None, cooked_factor=0.85, fat="oil"):
    """Onion-tomato gravy curry; `rich` adds butter/cream for restaurant style."""
    out = []
    for low in (False, True):
        ing = {protein: protein_g, "onion": 120, "tomato": 150, "ginger": 8, "garlic": 8,
               "masala": 6, "salt": 4, fat: (OIL_LOW if low else OIL_REG + 1) * serves,
               "water": 150}
        if extra:
            for k, v in extra.items():
                ing[k] = ing.get(k, 0) + v
        if rich and not low:
            for k, v in rich.items():
                ing[k] = ing.get(k, 0) + v
        raw = sum(v for k, v in ing.items() if k != "salt")
        out.append(dict(
            name=f"{name} (low oil)" if low else name, aka=aka, category=category,
            serving="1 katori (150 g)", serving_g=150, ing=ing, cooked=round(raw * cooked_factor),
            diet_variant=low, base=name))
    return out


def R(name, aka, category, serving, serving_g, ing, cooked=None, diet=False, note=None):
    if cooked is None:
        cooked = sum(v for k, v in ing.items() if k != "salt")
    return [dict(name=name, aka=aka, category=category, serving=serving, serving_g=serving_g,
                 ing=ing, cooked=cooked, diet_variant=diet, base=name, note=note)]


def recipes():
    r = []
    # ---------------- Dals and legumes ----------------
    r += _dal("Toor dal tadka", "Arhar dal", "toor")
    r += _dal("Moong dal (yellow)", "Peeli moong dal", "moong")
    r += _dal("Masoor dal", "Lal masoor dal", "masoor")
    r += _dal("Chana dal", "Chane ki dal", "chana")
    r += _dal("Urad dal (dhuli)", "Safed urad dal", "urad")
    r += _dal("Dal makhani", "Kali dal", "urad", extra={"rajma": 15, "cream": 30, "butter": 15}, cooked=520)
    r += _dal("Rajma masala", "Rajma", "rajma", pulse_g=100, extra={"tomato": 80, "onion": 40}, cooked=480)
    r += _dal("Chole masala", "Chana masala", "chana", pulse_g=100, extra={"tomato": 80, "onion": 50}, cooked=480)
    r += _dal("Lobia masala", "Rongi / black-eyed beans curry", "lobia", pulse_g=100, extra={"tomato": 60}, cooked=470)
    r += _dal("Moth bean usal", "Matki usal", "moth", pulse_g=100, extra={"coconut": 15}, cooked=420)
    r += _dal("Dal palak", "Palak dal", "toor", extra={"spinach": 120}, cooked=540)
    r += _dal("Lauki chana dal", "Ghiya chana dal", "chana", pulse_g=75, extra={"lauki": 200}, cooked=560)
    r += _dal("Sambar", "Sambhar", "toor", pulse_g=70, extra={"tamarind": 10, "brinjal": 60, "pumpkin": 60, "okra": 40, "carrot": 30}, cooked=650)
    r += _dal("Rasam", "Saaru", "toor", pulse_g=25, extra={"tamarind": 12, "tomato": 60}, cooked=600)
    r += _dal("Panchmel dal", "Rajasthani mixed dal", "toor", pulse_g=30, extra={"moong": 20, "masoor": 20, "urad": 10, "chana": 10}, cooked=460)
    r += _dal("Whole moong dal", "Sabut moong", "moong", pulse_g=90, cooked=430)
    r += _dal("Kadhi (besan)", "Punjabi kadhi without pakora", "besan", pulse_g=40, extra={"curd": 250, "onion": -30, "tomato": -40}, cooked=600)
    r += _dal("Soya chunks curry", "Soya badi sabzi", "soy_chunks", pulse_g=80, extra={"tomato": 80, "onion": 50}, cooked=450)
    r += _dal("Kala chana curry", "Black chickpea curry", "chana", pulse_g=100, extra={"tomato": 60}, cooked=460)
    r += _dal("Dal fry (mixed)", "Dal fry", "toor", pulse_g=50, extra={"moong": 40}, cooked=450)

    # ---------------- Dry sabzis ----------------
    r += _sabzi("Aloo sabzi (dry)", "Sukhi aloo", "potato")
    r += _sabzi("Aloo gobi", "Aloo gobhi", "cauliflower", extra={"potato": 150}, veg_g=200)
    r += _sabzi("Gobi sabzi", "Phool gobhi", "cauliflower")
    r += _sabzi("Bhindi masala", "Bhindi fry", "okra")
    r += _sabzi("Baingan bharta", "Bharta", "brinjal", veg_g=400)
    r += _sabzi("Lauki sabzi", "Ghiya / dudhi sabzi", "lauki", veg_g=400)
    r += _sabzi("Tori sabzi", "Turai / ridge gourd", "tori", veg_g=400)
    r += _sabzi("Karela sabzi", "Bitter gourd fry", "karela")
    r += _sabzi("Palak sabzi", "Spinach stir-fry", "spinach", veg_g=400)
    r += _sabzi("Patta gobhi sabzi", "Cabbage sabzi", "cabbage")
    r += _sabzi("Aloo matar (dry)", "Aloo mutter", "potato", extra={"peas": 120}, veg_g=180)
    r += _sabzi("Gajar matar", "Carrot peas sabzi", "carrot", extra={"peas": 120}, veg_g=200)
    r += _sabzi("Beans poriyal", "French beans sabzi", "beans", extra={"coconut": 20})
    r += _sabzi("Shimla mirch sabzi", "Capsicum sabzi", "capsicum")
    r += _sabzi("Mushroom masala (dry)", "Mushroom sabzi", "mushroom")
    r += _sabzi("Kaddu sabzi", "Pumpkin sabzi", "pumpkin", extra={"jaggery": 6})
    r += _sabzi("Aloo palak", "Palak aloo", "spinach", extra={"potato": 150}, veg_g=250)
    r += _sabzi("Sarson ka saag", "Saag", "mustard_greens", extra={"spinach": 100, "makki": 15}, veg_g=300, fat="ghee")
    r += _sabzi("Mixed veg sabzi", "Mix veg", "carrot", extra={"beans": 80, "peas": 60, "cauliflower": 80, "potato": 60}, veg_g=80)
    r += _sabzi("Chukandar sabzi", "Beetroot poriyal", "beetroot", extra={"coconut": 15})
    r += _sabzi("Mooli sabzi", "Radish sabzi", "radish", veg_g=350)
    r += _sabzi("Shakarkandi chaat sabzi", "Sweet potato sabzi", "sweet_potato")
    r += _sabzi("Corn capsicum sabzi", "Sweet corn sabzi", "corn", extra={"capsicum": 100}, veg_g=200)
    r += _sabzi("Paneer bhurji", "Paneer bhurji", "paneer", extra={"capsicum": 50}, veg_g=200)
    r += _sabzi("Tofu bhurji", "Tofu scramble", "tofu", extra={"capsicum": 50}, veg_g=250)
    r += _sabzi("Soya chunks bhurji", "Soya keema", "soy_chunks", extra={"water": 150, "peas": 60}, veg_g=90)

    # ---------------- Gravies and curries ----------------
    r += _curry("Paneer butter masala", "Paneer makhani", "paneer", 250, rich={"butter": 20, "cream": 50, "cashew": 15})
    r += _curry("Kadai paneer", "Karahi paneer", "paneer", 250, extra={"capsicum": 100})
    r += _curry("Palak paneer", "Saag paneer", "paneer", 200, extra={"spinach": 300, "tomato": -100}, rich={"cream": 30})
    r += _curry("Matar paneer", "Mutter paneer", "paneer", 200, extra={"peas": 150})
    r += _curry("Shahi paneer", "Paneer korma", "paneer", 250, rich={"cream": 60, "cashew": 25})
    r += _curry("Paneer tikka masala", "Paneer tikka gravy", "paneer", 250, extra={"curd": 60, "capsicum": 60}, rich={"butter": 10, "cream": 30})
    r += _curry("Malai kofta", "Kofta curry", "paneer", 150, extra={"potato": 120, "maida": 15}, rich={"cream": 60, "cashew": 20, "oil": 30})
    r += _curry("Mixed veg curry", "Sabz gravy", "carrot", 100, extra={"beans": 100, "peas": 80, "cauliflower": 100, "potato": 80})
    r += _curry("Dum aloo", "Dum aloo", "potato", 400, extra={"curd": 60})
    r += _curry("Aloo matar curry", "Aloo mutter gravy", "potato", 250, extra={"peas": 150})
    r += _curry("Mushroom matar", "Mushroom peas curry", "mushroom", 250, extra={"peas": 120})
    r += _curry("Chicken curry (home style)", "Murgh curry", "chicken_thigh", 450, category="Non-veg curry")
    r += _curry("Butter chicken", "Murgh makhani", "chicken_thigh", 450, category="Non-veg curry", extra={"curd": 60}, rich={"butter": 30, "cream": 70, "cashew": 15})
    r += _curry("Chicken tikka masala", "Chicken tikka gravy", "chicken_breast", 450, category="Non-veg curry", extra={"curd": 80}, rich={"butter": 15, "cream": 50})
    r += _curry("Kadai chicken", "Karahi chicken", "chicken_thigh", 450, category="Non-veg curry", extra={"capsicum": 120})
    r += _curry("Chicken breast curry", "Lean chicken curry", "chicken_breast", 450, category="Non-veg curry")
    r += _curry("Palak chicken", "Saag chicken", "chicken_thigh", 400, category="Non-veg curry", extra={"spinach": 300, "tomato": -100})
    r += _curry("Chicken korma", "Murgh korma", "chicken_thigh", 450, category="Non-veg curry", extra={"curd": 100}, rich={"cashew": 30, "cream": 40})
    r += _curry("Mutton curry", "Gosht curry", "mutton", 450, category="Non-veg curry", cooked_factor=0.8)
    r += _curry("Mutton rogan josh", "Rogan josh", "mutton", 450, category="Non-veg curry", extra={"curd": 100}, cooked_factor=0.8)
    r += _curry("Keema matar", "Mutton keema", "mutton", 400, category="Non-veg curry", extra={"peas": 150}, cooked_factor=0.75)
    r += _curry("Egg curry", "Anda curry", "egg", 300, category="Egg dishes")
    r += _curry("Fish curry (home style)", "Machli curry", "fish", 450, category="Non-veg curry", fat="mustard_oil")
    r += _curry("Goan fish curry", "Fish curry with coconut", "fish", 450, category="Non-veg curry", extra={"coconut_milk": 150, "tamarind": 8}, fat="coconut_oil")
    r += _curry("Prawn masala", "Jhinga masala", "prawn", 400, category="Non-veg curry")
    r += _curry("Chole (restaurant style)", "Pindi chole", "chana", 150, extra={"water": 350}, rich={"oil": 30, "butter": 10})
    r += _curry("Tofu curry", "Tofu masala", "tofu", 350)
    r += _curry("Soya chunks masala", "Nutrela curry", "soy_chunks", 100, extra={"water": 250})
    r += _curry("Kofta curry (lauki)", "Lauki kofta", "lauki", 300, extra={"besan": 50}, rich={"oil": 40})

    # ---------------- Breads ----------------
    r += R("Phulka (no ghee)", "Roti / chapati", "Roti & breads", "1 roti (30 g)", 30, {"atta": 25, "water": 15}, cooked=30, diet=True)
    r += R("Roti with ghee", "Chapati with ghee", "Roti & breads", "1 roti (33 g)", 33, {"atta": 25, "water": 15, "ghee": 3}, cooked=33)
    r += R("Plain paratha", "Tawa paratha", "Roti & breads", "1 paratha (60 g)", 60, {"atta": 40, "water": 20, "oil": 7}, cooked=60)
    r += R("Aloo paratha", "Aloo ka paratha", "Roti & breads", "1 paratha (120 g)", 120, {"atta": 50, "potato": 60, "onion": 5, "masala": 1, "water": 20, "oil": 8}, cooked=120)
    r += R("Gobi paratha", "Gobhi paratha", "Roti & breads", "1 paratha (110 g)", 110, {"atta": 50, "cauliflower": 50, "water": 20, "oil": 8}, cooked=110)
    r += R("Paneer paratha", "Paneer paratha", "Roti & breads", "1 paratha (110 g)", 110, {"atta": 50, "paneer": 40, "water": 20, "oil": 8}, cooked=110)
    r += R("Methi thepla", "Thepla (fenugreek leaves approximated by spinach)", "Roti & breads", "1 thepla (40 g)", 40, {"atta": 25, "besan": 3, "spinach": 8, "curd": 4, "oil": 3}, cooked=40)
    r += R("Puri", "Poori", "Roti & breads", "1 puri (25 g)", 25, {"atta": 17, "water": 6, "oil": 5}, cooked=25)
    r += R("Bhatura", "Bhature", "Roti & breads", "1 bhatura (80 g)", 80, {"maida": 50, "curd": 10, "water": 10, "oil": 14}, cooked=80)
    r += R("Missi roti", "Besan roti", "Roti & breads", "1 roti (45 g)", 45, {"atta": 20, "besan": 15, "onion": 5, "water": 10, "ghee": 2}, cooked=45)
    r += R("Makki ki roti", "Makki roti", "Roti & breads", "1 roti (60 g)", 60, {"makki": 45, "water": 20, "ghee": 4}, cooked=60)
    r += R("Bajra roti", "Bajre ki roti", "Roti & breads", "1 roti (50 g)", 50, {"bajra": 40, "water": 15}, cooked=50, diet=True)
    r += R("Jowar roti", "Jolada rotti / jowar bhakri", "Roti & breads", "1 roti (50 g)", 50, {"jowar": 40, "water": 15}, cooked=50, diet=True)
    r += R("Multigrain roti", "Mixed atta roti", "Roti & breads", "1 roti (35 g)", 35, {"atta": 15, "jowar": 5, "bajra": 5, "besan": 4, "water": 10}, cooked=35, diet=True)
    r += R("Tandoori roti", "Tandoori roti", "Roti & breads", "1 roti (50 g)", 50, {"atta": 40, "water": 15}, cooked=50)
    r += R("Butter naan", "Naan with butter", "Roti & breads", "1 naan (90 g)", 90, {"maida": 60, "curd": 10, "milk": 10, "water": 10, "butter": 8, "sugar": 2}, cooked=90)
    r += R("Plain naan", "Naan", "Roti & breads", "1 naan (85 g)", 85, {"maida": 60, "curd": 10, "milk": 10, "water": 12, "oil": 2, "sugar": 2}, cooked=85)
    r += R("Lachha paratha", "Laccha paratha", "Roti & breads", "1 paratha (80 g)", 80, {"maida": 30, "atta": 20, "water": 15, "ghee": 12}, cooked=80)
    r += R("Kulcha", "Amritsari kulcha (plain)", "Roti & breads", "1 kulcha (80 g)", 80, {"maida": 50, "curd": 10, "water": 10, "butter": 8}, cooked=80)
    r += R("Oats roti", "Oats chapati", "Roti & breads", "1 roti (35 g)", 35, {"atta": 15, "oats": 12, "water": 10}, cooked=35, diet=True)
    r += R("Jowar-bajra bhakri", "Bajra-jowar bhakri", "Roti & breads", "1 bhakri (50 g)", 50, {"jowar": 20, "bajra": 20, "water": 15}, cooked=50, diet=True)

    # ---------------- Rice ----------------
    r += R("Steamed rice", "Chawal / plain rice", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "water": 220}, cooked=300)
    r += R("Brown rice", "Brown chawal", "Rice dishes", "1 katori (150 g)", 150, {"brown_rice": 100, "water": 230}, cooked=300, diet=True)
    r += R("Jeera rice", "Cumin rice", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "ghee": 10, "cumin": 2, "salt": 2, "water": 210}, cooked=300)
    r += R("Veg pulao", "Vegetable pulav", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "peas": 40, "carrot": 40, "beans": 30, "onion": 30, "oil": 12, "salt": 3, "water": 220}, cooked=420)
    r += R("Matar pulao", "Peas pulao", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "peas": 70, "onion": 30, "ghee": 10, "salt": 3, "water": 210}, cooked=390)
    r += R("Moong dal khichdi", "Khichdi", "Rice dishes", "1 katori (200 g)", 200, {"rice": 60, "moong": 40, "ghee": 8, "masala": 2, "salt": 3, "water": 450}, cooked=520)
    r += R("Vegetable khichdi (low oil)", "Masala khichdi light", "Rice dishes", "1 katori (200 g)", 200, {"rice": 50, "moong": 40, "carrot": 40, "peas": 40, "tomato": 40, "oil": 4, "masala": 2, "salt": 3, "water": 450}, cooked=600, diet=True)
    r += R("Curd rice", "Thayir sadam / dahi chawal", "Rice dishes", "1 katori (200 g)", 200, {"rice": 70, "curd": 200, "milk": 30, "oil": 5, "mustard_seed": 1, "salt": 2, "water": 160}, cooked=470)
    r += R("Lemon rice", "Chitranna", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "peanut": 15, "lemon": 20, "oil": 12, "masala": 1, "mustard_seed": 1, "salt": 2, "water": 210}, cooked=340)
    r += R("Tamarind rice", "Puliyogare", "Rice dishes", "1 katori (150 g)", 150, {"rice": 100, "tamarind": 20, "peanut": 15, "sesame": 5, "oil": 15, "jaggery": 5, "salt": 2, "water": 210}, cooked=350)
    r += R("Chicken biryani (home style)", "Murgh biryani", "Rice dishes", "1 plate (250 g)", 250, {"rice": 200, "chicken_thigh": 350, "curd": 80, "onion": 150, "oil": 35, "ghee": 15, "masala": 8, "salt": 6, "water": 380}, cooked=1100)
    r += R("Veg biryani (home style)", "Subz biryani", "Rice dishes", "1 plate (250 g)", 250, {"rice": 200, "potato": 100, "carrot": 80, "beans": 60, "peas": 60, "curd": 60, "onion": 120, "oil": 30, "ghee": 10, "masala": 6, "salt": 6, "water": 380}, cooked=1050)
    r += R("Egg fried rice", "Egg fried rice", "Rice dishes", "1 plate (200 g)", 200, {"rice": 100, "egg": 100, "onion": 30, "capsicum": 30, "carrot": 30, "oil": 15, "salt": 3, "water": 200}, cooked=480)
    r += R("Jeera rice with quinoa", "Quinoa pulao", "Rice dishes", "1 katori (150 g)", 150, {"quinoa": 100, "peas": 40, "carrot": 40, "onion": 30, "oil": 6, "cumin": 2, "salt": 2, "water": 200}, cooked=380, diet=True)

    # ---------------- Breakfast ----------------
    r += R("Poha", "Kanda poha", "Breakfast", "1 plate (150 g)", 150, {"poha": 60, "onion": 40, "peas": 20, "peanut": 10, "oil": 7, "lemon": 5, "masala": 1, "salt": 2, "water": 60}, cooked=200)
    r += R("Poha (low oil, extra veg)", "Light poha", "Breakfast", "1 plate (150 g)", 150, {"poha": 50, "onion": 40, "peas": 30, "carrot": 30, "oil": 3, "lemon": 5, "salt": 2, "water": 50}, cooked=200, diet=True)
    r += R("Upma", "Rava upma", "Breakfast", "1 plate (180 g)", 180, {"suji": 50, "onion": 30, "peas": 15, "carrot": 15, "oil": 8, "mustard_seed": 1, "salt": 2, "water": 150}, cooked=260)
    r += R("Vegetable daliya", "Broken wheat upma", "Breakfast", "1 katori (180 g)", 180, {"daliya": 50, "onion": 30, "peas": 25, "carrot": 25, "tomato": 25, "oil": 4, "salt": 2, "water": 200}, cooked=330, diet=True)
    r += R("Sweet daliya (milk)", "Meetha daliya", "Breakfast", "1 katori (200 g)", 200, {"daliya": 40, "milk": 200, "jaggery": 15, "water": 100}, cooked=320)
    r += R("Oats upma", "Masala oats", "Breakfast", "1 katori (180 g)", 180, {"oats": 50, "onion": 30, "peas": 25, "carrot": 25, "tomato": 25, "oil": 4, "salt": 2, "water": 150}, cooked=290, diet=True)
    r += R("Oats porridge (milk)", "Oats with milk", "Breakfast", "1 bowl (250 g)", 250, {"oats": 40, "milk": 200, "banana": 50, "honey": 5}, cooked=300)
    r += R("Mango smoothie bowl (curd)", "Aam curd bowl", "Diet meals", "1 bowl (220 g)", 220, {"curd_low": 140, "mango": 70, "oats": 10}, diet=True)
    r += R("Dates and nuts (2 dates + 5 almonds)", "Khajur badam", "Snacks", "1 serving (30 g)", 30, {"dates": 24, "almond": 6})
    r += R("Overnight oats (curd, chia)", "Overnight oats", "Breakfast", "1 jar (250 g)", 250, {"oats": 40, "curd_low": 150, "milk_low": 60, "chia": 8, "banana": 40}, diet=True)
    r += R("Besan chilla", "Besan cheela", "Breakfast", "1 chilla (80 g)", 80, {"besan": 35, "onion": 15, "tomato": 10, "coriander": 3, "water": 35, "oil": 3}, cooked=80, diet=True)
    r += R("Moong dal chilla", "Pesarattu", "Breakfast", "1 chilla (90 g)", 90, {"moong": 35, "onion": 10, "ginger": 2, "green_chili": 2, "water": 50, "oil": 3}, cooked=90, diet=True)
    r += R("Paneer stuffed moong chilla", "Paneer chilla", "Breakfast", "1 chilla (120 g)", 120, {"moong": 35, "paneer": 30, "onion": 10, "water": 50, "oil": 3}, cooked=120, diet=True)
    r += R("Oats chilla", "Oats cheela", "Breakfast", "1 chilla (80 g)", 80, {"oats": 30, "besan": 10, "onion": 10, "tomato": 10, "water": 30, "oil": 3}, cooked=80, diet=True)
    r += R("Masala omelette (2 eggs)", "Anda omelette", "Egg dishes", "1 omelette (130 g)", 130, {"egg": 100, "onion": 20, "tomato": 15, "green_chili": 2, "oil": 5}, cooked=130)
    r += R("Egg bhurji (2 eggs)", "Anda bhurji", "Egg dishes", "1 serving (140 g)", 140, {"egg": 100, "onion": 25, "tomato": 25, "oil": 7, "masala": 1}, cooked=140)
    r += R("Egg white bhurji (4 whites)", "Egg white scramble", "Egg dishes", "1 serving (160 g)", 160, {"egg_white": 130, "onion": 20, "tomato": 20, "capsicum": 15, "oil": 2}, cooked=160, diet=True)
    r += R("Boiled eggs (2)", "Ubla anda", "Egg dishes", "2 eggs (100 g)", 100, {"egg": 100}, diet=True)
    r += R("Idli (home style)", "Idly", "Breakfast", "2 idlis (100 g)", 100, {"rice": 30, "urad": 10, "water": 60}, cooked=100, diet=True)
    r += R("Plain dosa (home style)", "Dosai", "Breakfast", "1 dosa (90 g)", 90, {"rice": 35, "urad": 12, "water": 45, "oil": 5}, cooked=90)
    r += R("Masala dosa (home style)", "Masala dosai", "Breakfast", "1 dosa (200 g)", 200, {"rice": 35, "urad": 12, "water": 45, "oil": 8, "potato": 90, "onion": 20}, cooked=200)
    r += R("Rava dosa", "Rava dosai", "Breakfast", "1 dosa (90 g)", 90, {"suji": 20, "rice": 15, "maida": 5, "water": 50, "oil": 7}, cooked=90)
    r += R("Uttapam", "Onion tomato uttapam", "Breakfast", "1 uttapam (150 g)", 150, {"rice": 40, "urad": 13, "onion": 25, "tomato": 20, "water": 55, "oil": 6}, cooked=150)
    r += R("Medu vada", "Vada", "Breakfast", "1 vada (50 g)", 50, {"urad": 22, "water": 18, "oil": 8, "onion": 3}, cooked=50)
    r += R("Dhokla", "Khaman dhokla", "Breakfast", "2 pieces (80 g)", 80, {"besan": 30, "curd": 10, "sugar": 3, "water": 35, "oil": 3, "mustard_seed": 1}, cooked=80, diet=True)
    r += R("Vegetable sandwich (brown bread)", "Veg sandwich", "Breakfast", "1 sandwich (150 g)", 150, {"bread_ww": 60, "cucumber": 30, "tomato": 30, "onion": 15, "butter": 5}, cooked=140)
    r += R("Paneer sandwich (brown bread)", "Paneer sandwich", "Breakfast", "1 sandwich (160 g)", 160, {"bread_ww": 60, "paneer": 50, "capsicum": 20, "onion": 15, "curd_low": 15}, diet=True)
    r += R("Sprouts poha", "Sprouts poha", "Breakfast", "1 plate (160 g)", 160, {"poha": 40, "moong_sprouts": 50, "onion": 30, "oil": 3, "lemon": 5, "water": 40}, cooked=160, diet=True)

    # ---------------- Snacks and street food ----------------
    r += R("Samosa (home style)", "Aloo samosa", "Snacks", "1 samosa (70 g)", 70, {"maida": 22, "potato": 35, "peas": 5, "oil": 12}, cooked=70)
    r += R("Onion pakora", "Pyaz bhajji", "Snacks", "5 pieces (60 g)", 60, {"besan": 20, "onion": 35, "oil": 12, "water": 10}, cooked=60)
    r += R("Paneer pakora", "Paneer pakoda", "Snacks", "4 pieces (80 g)", 80, {"paneer": 45, "besan": 15, "oil": 12, "water": 10}, cooked=80)
    r += R("Pav bhaji", "Pav bhaji", "Snacks", "1 plate (bhaji 200 g + 2 pav)", 280, {"potato": 80, "cauliflower": 40, "peas": 30, "capsicum": 30, "tomato": 60, "onion": 30, "butter": 20, "maida": 70, "water": 40}, cooked=280)
    r += R("Vada pav", "Vada pav", "Snacks", "1 vada pav (140 g)", 140, {"maida": 45, "potato": 50, "besan": 15, "oil": 12, "water": 18}, cooked=140)
    r += R("Pani puri (6 pieces)", "Golgappa", "Snacks", "6 puris (120 g)", 120, {"suji": 15, "maida": 5, "oil": 8, "potato": 30, "chana": 8, "tamarind": 8, "water": 60}, cooked=120)
    r += R("Bhel puri", "Bhel", "Snacks", "1 plate (120 g)", 120, {"poha": 35, "onion": 20, "tomato": 20, "peanut": 8, "tamarind": 8, "besan": 8, "oil": 4}, cooked=110)
    r += R("Aloo tikki", "Aloo patties", "Snacks", "2 tikkis (100 g)", 100, {"potato": 80, "peas": 10, "suji": 5, "oil": 8}, cooked=100)
    r += R("Dahi vada", "Dahi bhalla", "Snacks", "2 vadas with curd (150 g)", 150, {"urad": 30, "oil": 10, "curd": 90, "sugar": 5, "water": 20}, cooked=150)
    r += R("Chole bhature", "Chole bhature", "Snacks", "1 plate (1 katori chole + 2 bhature)", 310, {"chana": 45, "onion": 30, "tomato": 40, "oil": 22, "maida": 100, "curd": 20, "water": 120}, cooked=310)
    r += R("Kathi roll (paneer)", "Paneer frankie", "Snacks", "1 roll (180 g)", 180, {"maida": 50, "paneer": 60, "onion": 25, "capsicum": 20, "oil": 10, "curd": 10}, cooked=180)
    r += R("Kathi roll (chicken)", "Chicken frankie", "Snacks", "1 roll (180 g)", 180, {"maida": 50, "chicken_breast": 80, "onion": 25, "oil": 10, "curd": 10}, cooked=180)
    r += R("Veg momos (steamed)", "Momo", "Snacks", "6 momos (150 g)", 150, {"maida": 55, "cabbage": 50, "carrot": 20, "onion": 15, "oil": 3, "water": 20}, cooked=150)
    r += R("Chicken momos (steamed)", "Chicken momo", "Snacks", "6 momos (150 g)", 150, {"maida": 55, "chicken_thigh": 70, "onion": 15, "oil": 3, "water": 15}, cooked=150)
    r += R("Masala peanuts (roasted)", "Moongphali", "Snacks", "1 handful (30 g)", 30, {"peanut": 28, "besan": 2})
    r += R("Roasted chana", "Bhuna chana", "Snacks", "1 handful (30 g)", 30, {"chana": 33}, cooked=30, diet=True)
    r += R("Roasted makhana", "Phool makhana", "Snacks", "1 bowl (25 g)", 25, {"makhana": 24, "ghee": 2}, cooked=25, diet=True)
    r += R("Sprouts chaat", "Moong sprouts chaat", "Snacks", "1 bowl (150 g)", 150, {"moong_sprouts": 100, "onion": 20, "tomato": 20, "cucumber": 10, "lemon": 5}, cooked=150, diet=True)
    r += R("Chana chaat", "Kala chana chaat", "Snacks", "1 bowl (150 g)", 150, {"chana": 50, "water": 70, "onion": 20, "tomato": 20, "lemon": 5}, cooked=150, diet=True)
    r += R("Corn chaat", "Sweet corn chaat", "Snacks", "1 cup (120 g)", 120, {"corn": 100, "butter": 3, "lemon": 5, "onion": 10}, diet=True)
    r += R("Fruit chaat", "Fruit chaat", "Snacks", "1 bowl (150 g)", 150, {"apple": 40, "papaya": 40, "banana": 30, "guava": 25, "pomegranate": 15, "lemon": 3, "masala": 0.5}, diet=True)
    r += R("Paneer tikka (grilled)", "Paneer tikka", "Snacks", "6 pieces (150 g)", 150, {"paneer": 110, "curd_low": 30, "capsicum": 25, "onion": 20, "masala": 2, "oil": 3}, cooked=150, diet=True)
    r += R("Tandoori chicken (2 pieces)", "Tandoori murgh", "Non-veg dry", "2 pieces (180 g cooked)", 180, {"chicken_thigh": 240, "curd": 40, "masala": 4, "lemon": 5, "oil": 5}, cooked=220)
    r += R("Chicken tikka (grilled breast)", "Murgh tikka", "Non-veg dry", "6 pieces (150 g)", 150, {"chicken_breast": 200, "curd_low": 30, "masala": 3, "lemon": 5, "oil": 3}, cooked=180, diet=True)
    r += R("Fish tikka (grilled)", "Machli tikka", "Non-veg dry", "6 pieces (150 g)", 150, {"fish": 200, "curd_low": 25, "masala": 3, "lemon": 5, "oil": 3}, cooked=180, diet=True)
    r += R("Fish fry (tawa)", "Tawa machli", "Non-veg dry", "2 pieces (120 g)", 120, {"fish": 130, "besan": 8, "masala": 3, "oil": 10}, cooked=120)
    r += R("Chicken seekh kebab", "Seekh kebab", "Non-veg dry", "2 kebabs (100 g)", 100, {"chicken_thigh": 120, "onion": 15, "masala": 2, "oil": 3}, cooked=100)
    r += R("Mutton seekh kebab", "Gosht seekh", "Non-veg dry", "2 kebabs (100 g)", 100, {"mutton": 125, "onion": 15, "masala": 2, "oil": 3}, cooked=100)
    r += R("Dhokla-style steamed besan (no sugar)", "Plain besan dhokla", "Snacks", "2 pieces (80 g)", 80, {"besan": 30, "curd_low": 10, "water": 38, "oil": 2}, cooked=80, diet=True)

    # ---------------- Sides ----------------
    r += R("Cucumber raita", "Kheera raita", "Sides & salads", "1 katori (150 g)", 150, {"curd": 110, "cucumber": 40, "cumin": 1, "salt": 1})
    r += R("Cucumber raita (low-fat curd)", "Light raita", "Sides & salads", "1 katori (150 g)", 150, {"curd_low": 110, "cucumber": 40, "cumin": 1, "salt": 1}, diet=True)
    r += R("Boondi raita", "Boondi raita", "Sides & salads", "1 katori (150 g)", 150, {"curd": 120, "besan": 10, "oil": 6, "salt": 1}, cooked=135)
    r += R("Plain curd (dahi)", "Dahi", "Sides & salads", "1 katori (150 g)", 150, {"curd": 150})
    r += R("Low-fat curd (dahi)", "Toned-milk dahi", "Sides & salads", "1 katori (150 g)", 150, {"curd_low": 150}, diet=True)
    r += R("Hung curd (Greek-style)", "Chakka", "Sides & salads", "1 katori (100 g)", 100, {"curd_low": 220}, cooked=100, diet=True,
            note="Assumes whey drained away carries mostly water; protein is concentrated ~2x")
    r += R("Kachumber salad", "Indian salad", "Sides & salads", "1 bowl (150 g)", 150, {"cucumber": 60, "tomato": 50, "onion": 35, "lemon": 5, "coriander": 3}, diet=True)
    r += R("Green salad", "Salad", "Sides & salads", "1 plate (150 g)", 150, {"cucumber": 60, "tomato": 40, "carrot": 30, "radish": 20, "lemon": 5}, diet=True)
    r += R("Coconut chutney", "Nariyal chutney", "Sides & salads", "2 tbsp (30 g)", 30, {"coconut": 18, "chana": 3, "water": 8, "oil": 1})
    r += R("Green chutney", "Hari chutney", "Sides & salads", "1 tbsp (15 g)", 15, {"coriander": 10, "green_chili": 2, "lemon": 2, "salt": 0.3}, diet=True)
    r += R("Tamarind chutney", "Imli chutney", "Sides & salads", "1 tbsp (20 g)", 20, {"tamarind": 6, "jaggery": 8, "water": 10}, cooked=20)
    r += R("Papad (roasted)", "Papadum", "Sides & salads", "1 papad (12 g)", 12, {"urad": 11, "salt": 1}, cooked=12)
    r += R("Papad (fried)", "Fried papadum", "Sides & salads", "1 papad (15 g)", 15, {"urad": 11, "salt": 1, "oil": 4}, cooked=15)
    r += R("Pickle (oil-based)", "Achaar", "Sides & salads", "1 tsp (10 g)", 10, {"oil": 3, "salt": 1, "masala": 1, "mango": 5}, cooked=10,
            note="Approximation: oil-based pickle is mostly oil, salt, spice and fruit/veg")

    # ---------------- Drinks ----------------
    r += R("Masala chai (milk, sugar)", "Chai", "Drinks", "1 cup (150 ml)", 150, {"tea": 80, "milk": 70, "sugar": 8}, cooked=150)
    r += R("Chai without sugar", "Pheeki chai", "Drinks", "1 cup (150 ml)", 150, {"tea": 80, "milk": 70}, diet=True)
    r += R("Filter coffee", "Kaapi", "Drinks", "1 tumbler (150 ml)", 150, {"coffee": 60, "milk": 90, "sugar": 8}, cooked=150)
    r += R("Black coffee", "Black coffee", "Drinks", "1 cup (200 ml)", 200, {"coffee": 200}, diet=True)
    r += R("Chaas (buttermilk)", "Mattha", "Drinks", "1 glass (250 ml)", 250, {"curd_low": 100, "water": 150, "cumin": 1, "salt": 1}, diet=True)
    r += R("Sweet lassi", "Meethi lassi", "Drinks", "1 glass (250 ml)", 250, {"curd": 180, "milk": 50, "sugar": 20})
    r += R("Salted lassi", "Namkeen lassi", "Drinks", "1 glass (250 ml)", 250, {"curd": 180, "water": 70, "salt": 1})
    r += R("Mango lassi", "Aam lassi", "Drinks", "1 glass (250 ml)", 250, {"curd": 130, "mango": 80, "milk": 30, "sugar": 12})
    r += R("Nimbu pani (sugar)", "Shikanji", "Drinks", "1 glass (250 ml)", 250, {"lemon": 20, "sugar": 15, "water": 215, "salt": 1})
    r += R("Nimbu pani (no sugar)", "Lemon water", "Drinks", "1 glass (250 ml)", 250, {"lemon": 20, "water": 230, "salt": 1}, diet=True)
    r += R("Haldi doodh", "Turmeric milk", "Drinks", "1 glass (200 ml)", 200, {"milk": 200, "masala": 1, "jaggery": 5}, cooked=200)
    r += R("Sattu drink (savoury)", "Sattu sharbat (roasted gram approximated by chickpea flour)", "Drinks", "1 glass (250 ml)", 250, {"besan": 30, "water": 220, "lemon": 5, "salt": 1}, diet=True)
    r += R("Whey protein shake (water)", "Protein shake", "Drinks", "1 scoop in water (330 ml)", 330, {"whey": 30, "water": 300}, diet=True)
    r += R("Whey protein shake (toned milk)", "Protein shake with milk", "Drinks", "1 scoop in milk (280 ml)", 280, {"whey": 30, "milk_low": 250}, diet=True)
    r += R("Banana peanut butter smoothie", "Banana shake (PB)", "Drinks", "1 glass (300 ml)", 300, {"banana": 100, "milk_low": 180, "peanut_butter": 15, "oats": 10}, diet=True)
    r += R("Badam milk", "Almond milk (dairy)", "Drinks", "1 glass (200 ml)", 200, {"milk": 200, "almond": 10, "sugar": 10}, cooked=210)
    r += R("Coconut water", "Nariyal pani", "Drinks", "1 glass (240 ml)", 240, {"coconut_water": 240}, diet=True)

    # ---------------- Sweets ----------------
    r += R("Kheer (rice)", "Chawal ki kheer", "Sweets", "1 katori (150 g)", 150, {"milk": 500, "rice": 30, "sugar": 40, "almond": 8, "cashew": 5}, cooked=420)
    r += R("Suji halwa", "Sheera", "Sweets", "1 katori (100 g)", 100, {"suji": 50, "ghee": 35, "sugar": 50, "water": 150, "cashew": 5}, cooked=260)
    r += R("Gajar halwa", "Gajrela", "Sweets", "1 katori (100 g)", 100, {"carrot": 500, "milk": 400, "sugar": 80, "ghee": 30, "almond": 10}, cooked=500)
    r += R("Besan ladoo", "Besan laddu", "Sweets", "1 ladoo (35 g)", 35, {"besan": 100, "ghee": 70, "sugar": 90}, cooked=255)
    r += R("Rava ladoo", "Suji laddu", "Sweets", "1 ladoo (35 g)", 35, {"suji": 100, "ghee": 50, "sugar": 90, "coconut": 20}, cooked=255)
    r += R("Gulab jamun (with syrup)", "Gulab jamun", "Sweets", "1 piece (50 g)", 50, {"milk": 35, "maida": 5, "oil": 6, "sugar": 18, "water": 6}, cooked=50,
            note="Khoya approximated by reduced whole milk")
    r += R("Jalebi", "Jalebi", "Sweets", "2 pieces (50 g)", 50, {"maida": 15, "oil": 8, "sugar": 25, "water": 5}, cooked=50)
    r += R("Rasgulla", "Rosogolla", "Sweets", "1 piece (50 g)", 50, {"paneer": 22, "sugar": 18, "water": 15}, cooked=50)
    r += R("Seviyan kheer", "Vermicelli kheer", "Sweets", "1 katori (150 g)", 150, {"milk": 500, "maida": 40, "sugar": 40, "ghee": 8, "almond": 8}, cooked=430)
    r += R("Date-nut ladoo (no added sugar)", "Khajur dry fruit ladoo", "Sweets", "1 ladoo (25 g)", 25, {"dates": 120, "almond": 30, "cashew": 20, "walnut": 20, "ghee": 5}, cooked=190)
    r += R("Shrikhand", "Shrikhand", "Sweets", "1 katori (100 g)", 100, {"curd": 220, "sugar": 30}, cooked=130)

    # ---------------- Diet bowls and meal-prep (new diet foods) ----------------
    r += R("High-protein dal bowl", "Dal + curd + salad bowl", "Diet meals", "1 bowl (350 g)", 350, {"moong": 45, "water": 200, "curd_low": 100, "cucumber": 50, "tomato": 40, "oil": 3}, cooked=430, diet=True)
    r += R("Paneer salad bowl", "Paneer salad", "Diet meals", "1 bowl (250 g)", 250, {"paneer": 80, "cucumber": 60, "tomato": 50, "capsicum": 40, "onion": 20, "lemon": 5}, cooked=255, diet=True)
    r += R("Chicken salad bowl", "Grilled chicken salad", "Diet meals", "1 bowl (280 g)", 280, {"chicken_breast": 150, "cucumber": 60, "tomato": 50, "onion": 20, "lemon": 5, "oil": 5}, cooked=260, diet=True)
    r += R("Rajma salad", "Kidney bean salad", "Diet meals", "1 bowl (200 g)", 200, {"rajma": 50, "water": 70, "onion": 25, "tomato": 30, "cucumber": 30, "lemon": 5}, cooked=210, diet=True)
    r += R("Chickpea salad", "Chana salad", "Diet meals", "1 bowl (200 g)", 200, {"chana": 50, "water": 70, "onion": 25, "tomato": 30, "cucumber": 30, "lemon": 5, "oil": 3}, cooked=210, diet=True)
    r += R("Tofu stir-fry with vegetables", "Tofu veg stir-fry", "Diet meals", "1 bowl (250 g)", 250, {"tofu": 150, "capsicum": 50, "beans": 40, "carrot": 30, "onion": 20, "oil": 5}, cooked=260, diet=True)
    r += R("Soya chunks pulao (light)", "Soya pulao", "Diet meals", "1 plate (250 g)", 250, {"rice": 60, "soy_chunks": 35, "peas": 40, "carrot": 30, "onion": 30, "oil": 5, "water": 250}, cooked=440, diet=True)
    r += R("Quinoa khichdi", "Quinoa moong khichdi", "Diet meals", "1 katori (200 g)", 200, {"quinoa": 50, "moong": 40, "carrot": 40, "peas": 30, "oil": 4, "water": 400}, cooked=520, diet=True)
    r += R("Millet khichdi (bajra)", "Bajra khichdi", "Diet meals", "1 katori (200 g)", 200, {"bajra": 50, "moong": 40, "carrot": 30, "peas": 30, "ghee": 5, "water": 400}, cooked=520, diet=True)
    r += R("Grilled fish with sauteed veg", "Grilled fish plate", "Diet meals", "1 plate (280 g)", 280, {"fish": 180, "beans": 60, "carrot": 50, "capsicum": 40, "oil": 6, "lemon": 5}, cooked=290, diet=True)
    r += R("Egg white omelette with veg (4 whites)", "Egg white omelette", "Diet meals", "1 omelette (170 g)", 170, {"egg_white": 130, "spinach": 30, "onion": 15, "tomato": 15, "oil": 2}, cooked=170, diet=True)
    r += R("Paneer bhurji wrap (whole wheat)", "Paneer roll (atta)", "Diet meals", "1 wrap (180 g)", 180, {"atta": 35, "paneer": 60, "onion": 25, "capsicum": 25, "tomato": 20, "oil": 4, "water": 15}, cooked=180, diet=True)
    r += R("Chicken wrap (whole wheat)", "Chicken roll (atta)", "Diet meals", "1 wrap (200 g)", 200, {"atta": 35, "chicken_breast": 100, "onion": 25, "capsicum": 25, "curd_low": 15, "oil": 4, "water": 15}, cooked=200, diet=True)
    r += R("Greek-style curd bowl with fruit and seeds", "Hung curd bowl", "Diet meals", "1 bowl (220 g)", 220, {"curd_low": 300, "banana": 60, "chia": 5, "pumpkin_seed": 8}, cooked=220, diet=True,
            note="Uses ~300 g low-fat curd strained to ~150 g")
    r += R("Cottage cheese (low-fat) bowl", "Low-fat cottage cheese", "Diet meals", "1 bowl (150 g)", 150, {"cottage_low": 150}, diet=True)
    r += R("Sprouts and paneer salad", "Sprouts paneer salad", "Diet meals", "1 bowl (220 g)", 220, {"moong_sprouts": 100, "paneer": 50, "cucumber": 40, "tomato": 30, "lemon": 5}, cooked=225, diet=True)
    r += R("Lauki soup", "Bottle gourd soup", "Diet meals", "1 bowl (250 ml)", 250, {"lauki": 200, "onion": 20, "ghee": 2, "water": 100}, cooked=300, diet=True)
    r += R("Tomato soup (home, no cream)", "Tamatar shorba", "Diet meals", "1 bowl (250 ml)", 250, {"tomato": 250, "onion": 30, "garlic": 3, "oil": 3, "water": 100}, cooked=330, diet=True)
    r += R("Palak soup", "Spinach soup", "Diet meals", "1 bowl (250 ml)", 250, {"spinach": 150, "onion": 25, "garlic": 3, "milk_low": 60, "oil": 2, "water": 100}, cooked=320, diet=True)
    r += R("Moong dal soup", "Dal shorba", "Diet meals", "1 bowl (250 ml)", 250, {"moong": 30, "tomato": 30, "ginger": 3, "water": 300}, cooked=330, diet=True)
    r += R("Chicken clear soup", "Chicken shorba", "Diet meals", "1 bowl (250 ml)", 250, {"chicken_breast": 60, "carrot": 30, "onion": 20, "cabbage": 20, "water": 300}, cooked=380, diet=True)
    r += R("Mixed millet upma", "Millet upma", "Diet meals", "1 katori (180 g)", 180, {"bajra": 25, "jowar": 25, "onion": 25, "carrot": 25, "peas": 25, "oil": 4, "water": 180}, cooked=300, diet=True)
    r += R("Amaranth (rajgira) porridge", "Rajgira dalia", "Diet meals", "1 bowl (200 g)", 200, {"amaranth": 40, "milk_low": 180, "banana": 30}, cooked=240, diet=True)
    r += R("Sweet potato chaat", "Shakarkandi chaat", "Diet meals", "1 bowl (150 g)", 150, {"sweet_potato": 150, "lemon": 5, "masala": 1}, cooked=150, diet=True)
    r += R("Oats peanut protein ladoo", "Protein ladoo", "Diet meals", "1 ladoo (30 g)", 30, {"oats": 40, "peanut_butter": 40, "whey": 30, "honey": 20, "chia": 5}, cooked=135, diet=True)

    return r
