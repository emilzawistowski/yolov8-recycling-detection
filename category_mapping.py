CATEGORY_COLORS = {
    "Furniture": (0, 128, 255),
    "Household items": (144, 238, 144),
    "Kitchenware": (255, 0, 255),
    "Lamps/Vases/Ceramics": (0, 255, 255),
    "Decorations": (128, 0, 128),
    "Books": (255, 165, 0),
    "Toys and games": (0, 215, 255),
    "Electronics": (0, 128, 0),
    "Media": (128, 128, 0),
    "Garden": (34, 139, 34),
}

COCO_TO_CATEGORY = {
    # Furniture
    "chair": "Furniture",
    "couch": "Furniture",
    "bed": "Furniture",
    "dining table": "Furniture",
    "bench": "Furniture",

    # Household / kitchen / glassware / cutlery
    "bottle": "Household items",
    "cup": "Kitchenware",
    "wine glass": "Kitchenware",
    "fork": "Kitchenware",
    "knife": "Kitchenware",
    "spoon": "Kitchenware",
    "bowl": "Kitchenware",
    "microwave": "Household items",
    "toaster": "Household items",
    "refrigerator": "Household items",

    # Lamps / vases
    "vase": "Lamps/Vases/Ceramics",

    # Decorations
    "clock": "Decorations",

    # Books
    "book": "Books",

    # Toys & games
    "teddy bear": "Toys and games",
    "kite": "Toys and games",
    "sports ball": "Toys and games",
    "board": "Toys and games",

    # Electronics
    "laptop": "Electronics",
    "mouse": "Electronics",
    "keyboard": "Electronics",
    "tv": "Electronics",
    "cell phone": "Electronics",
    "remote": "Electronics",
    "oven": "Electronics",

    # Garden
    "potted plant": "Garden",
}

def map_to_category(coco_name):

    return COCO_TO_CATEGORY.get(coco_name, None)


PLATFORMS_PER_OBJECT = {
    # Furniture
    "chair": 1,
    "couch": 4,
    "bed": 4,
    "dining table": 2,
    "bench": 2,

    # Household items / Kitchenware
    "bottle": 1,
    "cup": 1,
    "wine glass": 1,
    "fork": 1,
    "knife": 1,
    "spoon": 1,
    "bowl": 1,
    "microwave": 2,
    "toaster": 1,
    "refrigerator": 4,

    # Lamps / Vases / Ceramics
    "vase": 1,

    # Decorations
    "clock": 1,

    # Books / Media
    "book": 1,

    # Toys & games
    "teddy bear": 1,
    "kite": 1,
    "sports ball": 1,
    "board": 1,

    # Electronics
    "laptop": 1,
    "mouse": 1,
    "keyboard": 1,
    "tv": 2,
    "cell phone": 1,
    "remote": 1,
    "oven": 2,

    # Garden
    "potted plant": 1,
}
