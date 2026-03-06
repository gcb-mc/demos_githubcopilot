"""
Cooking AI Agent - Tool definitions for recipe search and ingredient extraction.
"""

import json
from typing import Annotated


# ── Sample recipe database ──────────────────────────────────────────────────
RECIPE_DB = [
    {
        "name": "Classic Margherita Pizza",
        "cuisine": "Italian",
        "ingredients": [
            "2 cups all-purpose flour",
            "1 tsp salt",
            "1 tsp sugar",
            "1 packet active dry yeast",
            "3/4 cup warm water",
            "1 tbsp olive oil",
            "1/2 cup tomato sauce",
            "8 oz fresh mozzarella",
            "Fresh basil leaves",
        ],
        "instructions": "Mix flour, salt, sugar, and yeast. Add water and oil to form dough. "
        "Let rise 1 hour. Roll out, top with sauce, mozzarella, and basil. Bake at 475°F for 12 min.",
        "servings": 4,
        "prep_time": "90 min",
        "tags": ["vegetarian", "classic"],
    },
    {
        "name": "Chicken Tikka Masala",
        "cuisine": "Indian",
        "ingredients": [
            "1.5 lbs chicken breast, cubed",
            "1 cup plain yogurt",
            "2 tbsp lemon juice",
            "2 tsp garam masala",
            "1 tsp turmeric",
            "1 tsp cumin",
            "1 can (14 oz) crushed tomatoes",
            "1 cup heavy cream",
            "1 large onion, diced",
            "4 cloves garlic, minced",
            "1 inch ginger, grated",
            "2 tbsp butter",
            "Fresh cilantro",
            "Salt to taste",
        ],
        "instructions": "Marinate chicken in yogurt, lemon juice, and spices for 1 hour. "
        "Grill or pan-sear chicken. Sauté onion, garlic, ginger in butter. Add tomatoes, simmer 15 min. "
        "Add cream and chicken, simmer 10 min. Garnish with cilantro. Serve with rice or naan.",
        "servings": 4,
        "prep_time": "45 min + marination",
        "tags": ["protein-rich", "spicy"],
    },
    {
        "name": "Caesar Salad",
        "cuisine": "American",
        "ingredients": [
            "1 large head romaine lettuce",
            "1/2 cup parmesan cheese, grated",
            "1 cup croutons",
            "2 anchovy fillets",
            "1 clove garlic",
            "1 egg yolk",
            "2 tbsp lemon juice",
            "1 tsp Dijon mustard",
            "1/2 cup olive oil",
            "Salt and pepper to taste",
        ],
        "instructions": "Blend anchovies, garlic, egg yolk, lemon juice, and mustard. "
        "Slowly drizzle in olive oil. Toss romaine with dressing, top with parmesan and croutons.",
        "servings": 2,
        "prep_time": "15 min",
        "tags": ["quick", "classic"],
    },
    {
        "name": "Pad Thai",
        "cuisine": "Thai",
        "ingredients": [
            "8 oz rice noodles",
            "2 tbsp tamarind paste",
            "2 tbsp fish sauce",
            "1 tbsp sugar",
            "2 eggs",
            "1 cup bean sprouts",
            "1/4 cup crushed peanuts",
            "2 green onions, chopped",
            "1 lime, cut into wedges",
            "8 oz shrimp or tofu",
            "2 tbsp vegetable oil",
            "2 cloves garlic, minced",
        ],
        "instructions": "Soak noodles in warm water 30 min. Mix tamarind, fish sauce, sugar for sauce. "
        "Stir-fry shrimp/tofu and garlic. Push aside, scramble eggs. Add noodles and sauce, toss. "
        "Top with sprouts, peanuts, green onions. Serve with lime wedges.",
        "servings": 2,
        "prep_time": "40 min",
        "tags": ["quick", "asian"],
    },
    {
        "name": "Chocolate Lava Cake",
        "cuisine": "French",
        "ingredients": [
            "4 oz dark chocolate",
            "1/2 cup unsalted butter",
            "2 eggs",
            "2 egg yolks",
            "1/4 cup sugar",
            "2 tbsp all-purpose flour",
            "Pinch of salt",
            "Butter and cocoa for ramekins",
        ],
        "instructions": "Melt chocolate and butter together. Whisk eggs, yolks, and sugar until thick. "
        "Fold in chocolate mixture, then flour and salt. Pour into buttered ramekins. "
        "Bake at 425°F for 12-14 min. Invert onto plates and serve immediately.",
        "servings": 4,
        "prep_time": "25 min",
        "tags": ["dessert", "indulgent"],
    },
    {
        "name": "Vegetable Stir Fry",
        "cuisine": "Chinese",
        "ingredients": [
            "1 cup broccoli florets",
            "1 red bell pepper, sliced",
            "1 carrot, julienned",
            "1 cup snap peas",
            "8 oz firm tofu, cubed",
            "3 tbsp soy sauce",
            "1 tbsp sesame oil",
            "1 tbsp cornstarch",
            "2 cloves garlic, minced",
            "1 inch ginger, grated",
            "2 tbsp vegetable oil",
            "Cooked rice for serving",
        ],
        "instructions": "Press and cube tofu. Mix soy sauce, sesame oil, cornstarch for sauce. "
        "Stir-fry tofu until golden, set aside. Stir-fry vegetables with garlic and ginger 3-4 min. "
        "Return tofu, add sauce, cook until thickened. Serve over rice.",
        "servings": 3,
        "prep_time": "25 min",
        "tags": ["vegan", "healthy", "quick"],
    },
    {
        "name": "Beef Tacos",
        "cuisine": "Mexican",
        "ingredients": [
            "1 lb ground beef",
            "1 packet taco seasoning",
            "8 small corn tortillas",
            "1 cup shredded lettuce",
            "1 cup diced tomatoes",
            "1/2 cup shredded cheddar cheese",
            "1/4 cup sour cream",
            "1 avocado, sliced",
            "Fresh cilantro",
            "Lime wedges",
            "Hot sauce (optional)",
        ],
        "instructions": "Brown ground beef, drain fat. Add taco seasoning and water per packet directions. "
        "Warm tortillas. Fill with seasoned beef and desired toppings. Squeeze lime and add hot sauce to taste.",
        "servings": 4,
        "prep_time": "20 min",
        "tags": ["quick", "family-friendly"],
    },
    {
        "name": "Greek Salad",
        "cuisine": "Greek",
        "ingredients": [
            "2 large cucumbers, chopped",
            "4 ripe tomatoes, chopped",
            "1 red onion, thinly sliced",
            "1 green bell pepper, chopped",
            "1 cup Kalamata olives",
            "8 oz feta cheese, cubed",
            "3 tbsp extra virgin olive oil",
            "1 tbsp red wine vinegar",
            "1 tsp dried oregano",
            "Salt and pepper to taste",
        ],
        "instructions": "Combine cucumbers, tomatoes, onion, pepper, and olives in a large bowl. "
        "Top with feta. Drizzle with olive oil and vinegar. Season with oregano, salt, and pepper. Toss gently.",
        "servings": 4,
        "prep_time": "10 min",
        "tags": ["vegetarian", "healthy", "no-cook"],
    },
]

# ── Substitution database ───────────────────────────────────────────────────
SUBSTITUTIONS = {
    "butter": ["coconut oil", "olive oil", "applesauce (for baking)", "avocado"],
    "egg": ["flax egg (1 tbsp ground flax + 3 tbsp water)", "chia egg", "banana (1/4 mashed)", "aquafaba (3 tbsp)"],
    "milk": ["oat milk", "almond milk", "soy milk", "coconut milk"],
    "heavy cream": ["coconut cream", "cashew cream", "silken tofu blended"],
    "all-purpose flour": ["almond flour", "oat flour", "coconut flour (use 1/3 amount)", "gluten-free flour blend"],
    "sugar": ["honey (3/4 amount)", "maple syrup (3/4 amount)", "stevia", "coconut sugar"],
    "soy sauce": ["tamari (gluten-free)", "coconut aminos", "liquid aminos"],
    "parmesan cheese": ["nutritional yeast", "pecorino romano", "aged asiago"],
    "fish sauce": ["soy sauce + lime juice", "coconut aminos + salt"],
    "yogurt": ["coconut yogurt", "sour cream", "silken tofu blended"],
    "chicken breast": ["tofu", "tempeh", "seitan", "jackfruit"],
    "ground beef": ["ground turkey", "lentils", "mushroom crumbles", "plant-based ground"],
    "mozzarella": ["vegan mozzarella", "provolone", "burrata"],
    "feta cheese": ["tofu feta (marinated tofu)", "goat cheese", "ricotta salata"],
    "shrimp": ["tofu", "hearts of palm", "king oyster mushroom"],
}

# ── Unit conversion data ────────────────────────────────────────────────────
CONVERSIONS = {
    ("cup", "ml"): 236.588,
    ("cup", "tbsp"): 16,
    ("cup", "tsp"): 48,
    ("cup", "oz"): 8,
    ("tbsp", "tsp"): 3,
    ("tbsp", "ml"): 14.787,
    ("tsp", "ml"): 4.929,
    ("oz", "g"): 28.3495,
    ("oz", "ml"): 29.5735,
    ("lb", "g"): 453.592,
    ("lb", "kg"): 0.453592,
    ("lb", "oz"): 16,
    ("kg", "lb"): 2.20462,
    ("kg", "g"): 1000,
    ("l", "ml"): 1000,
    ("l", "cup"): 4.22675,
    ("g", "oz"): 0.035274,
}


# ── Tool functions ──────────────────────────────────────────────────────────


def search_recipes(
    query: Annotated[str, "Search query: dish name, ingredient, cuisine type, or tag (e.g. 'Italian', 'chicken', 'quick', 'vegan')"],
) -> str:
    """Search for recipes by name, ingredient, cuisine, or tag. Returns matching recipes with full details."""
    query_lower = query.lower()
    results = []

    for recipe in RECIPE_DB:
        match = False
        # Match by name
        if query_lower in recipe["name"].lower():
            match = True
        # Match by cuisine
        elif query_lower in recipe["cuisine"].lower():
            match = True
        # Match by ingredient
        elif any(query_lower in ing.lower() for ing in recipe["ingredients"]):
            match = True
        # Match by tag
        elif any(query_lower in tag.lower() for tag in recipe["tags"]):
            match = True

        if match:
            results.append(
                {
                    "name": recipe["name"],
                    "cuisine": recipe["cuisine"],
                    "servings": recipe["servings"],
                    "prep_time": recipe["prep_time"],
                    "tags": recipe["tags"],
                    "ingredients": recipe["ingredients"],
                    "instructions": recipe["instructions"],
                }
            )

    if results:
        return json.dumps({"found": len(results), "recipes": results}, indent=2)
    return json.dumps({"found": 0, "message": f"No recipes found matching '{query}'. Try searching by cuisine (Italian, Thai, Mexican), ingredient (chicken, tofu), or tag (quick, vegan, dessert)."})


def extract_ingredients(
    recipe_text: Annotated[str, "A recipe description or name to extract ingredients from. Can be a full recipe text or a recipe name from the database."],
) -> str:
    """Extract and return a structured ingredient list from recipe text. Breaks down each ingredient into quantity, unit, and item."""
    # Check if it matches a known recipe name
    recipe_text_lower = recipe_text.lower()
    for recipe in RECIPE_DB:
        if recipe_text_lower in recipe["name"].lower() or recipe["name"].lower() in recipe_text_lower:
            ingredients = []
            for ing in recipe["ingredients"]:
                ingredients.append(_parse_ingredient(ing))
            return json.dumps(
                {
                    "recipe": recipe["name"],
                    "ingredient_count": len(ingredients),
                    "ingredients": ingredients,
                },
                indent=2,
            )

    # For free-text, return as-is for the LLM to parse
    return json.dumps(
        {
            "note": "Parsed from provided text. The AI will structure the ingredients.",
            "raw_text": recipe_text,
        },
        indent=2,
    )


def get_substitutions(
    ingredient: Annotated[str, "The ingredient to find substitutions for (e.g. 'butter', 'egg', 'milk')"],
    reason: Annotated[str, "Reason for substitution: 'vegan', 'allergy', 'dietary', 'unavailable', or 'any'"] = "any",
) -> str:
    """Suggest ingredient substitutions for dietary restrictions, allergies, or availability."""
    ingredient_lower = ingredient.lower().strip()

    # Direct match
    for key, subs in SUBSTITUTIONS.items():
        if ingredient_lower in key or key in ingredient_lower:
            return json.dumps(
                {
                    "ingredient": key,
                    "reason": reason,
                    "substitutions": subs,
                    "tip": "Amounts may vary; adjust to taste. Check specific baking ratios for baked goods.",
                },
                indent=2,
            )

    return json.dumps(
        {
            "ingredient": ingredient,
            "substitutions": [],
            "message": f"No pre-defined substitutions found for '{ingredient}'. The AI assistant can suggest alternatives based on context.",
        },
        indent=2,
    )


def convert_units(
    value: Annotated[float, "The numeric value to convert"],
    from_unit: Annotated[str, "Source unit (cup, tbsp, tsp, oz, g, lb, kg, ml, l)"],
    to_unit: Annotated[str, "Target unit (cup, tbsp, tsp, oz, g, lb, kg, ml, l)"],
) -> str:
    """Convert between common cooking measurement units."""
    from_u = from_unit.lower().strip().rstrip("s")  # normalize plurals
    to_u = to_unit.lower().strip().rstrip("s")

    if from_u == to_u:
        return json.dumps({"value": value, "from": from_unit, "to": to_unit, "result": value})

    # Direct conversion
    if (from_u, to_u) in CONVERSIONS:
        result = value * CONVERSIONS[(from_u, to_u)]
        return json.dumps({"value": value, "from": from_unit, "to": to_unit, "result": round(result, 3)})

    # Reverse conversion
    if (to_u, from_u) in CONVERSIONS:
        result = value / CONVERSIONS[(to_u, from_u)]
        return json.dumps({"value": value, "from": from_unit, "to": to_unit, "result": round(result, 3)})

    return json.dumps(
        {
            "error": f"Cannot convert from '{from_unit}' to '{to_unit}'. Supported units: cup, tbsp, tsp, oz, g, lb, kg, ml, l."
        }
    )


# ── Helper ──────────────────────────────────────────────────────────────────


def _parse_ingredient(text: str) -> dict:
    """Simple parser to split an ingredient string into components."""
    parts = text.strip().split(" ", 2)
    if len(parts) >= 3:
        try:
            qty = parts[0]
            # Try to interpret as number
            float(qty.replace("/", "."))
            return {"quantity": qty, "unit": parts[1], "item": parts[2]}
        except ValueError:
            pass
    return {"quantity": "", "unit": "", "item": text}
