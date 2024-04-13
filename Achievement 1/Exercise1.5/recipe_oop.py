class Recipe:
    all_ingredients = []
    # Initialization method
    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None
    # Method to retreive name
    def get_name(self):
        output = self.name
        return output
    # Method to set name
    def set_name(self, name):
        self.name = name
    # Method to get cooking time
    def get_cookingtime(self):
        output = self.cooking_time
        return output
    # Method to set cooking time
    def set_cookingtime(self, cooking_time):
        self.cooking_time = cooking_time
    # Method to add new items to self.shopping_list
    def add_ingredient(self, ingredient):
        # Simple filter to avoid repeated items
        if not ingredient in self.ingredients:
          self.ingredients.append(ingredient)
          self.update_all_ingredients()

    # Method to get ingredients
    def get_ingredients(self):
        output = self.ingredients
        return output

    # Method to calculate difficulty
    def calc_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            difficulty = "Easy"
        if self.cooking_time < 10 and len(self.ingredients) >= 4:
            difficulty = "Medium"
        if self.cooking_time > 10 and len(self.ingredients) < 4:
            difficulty = "Intermediate"
        if self.cooking_time > 10 and len(self.ingredients) >= 4:
            difficulty = "Hard"
        return difficulty

    # Method to get difficulty
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # Method to search ingredients
    def search_ingredients(self, ingredient):
        return ingredient in self.ingredients

    # Method to update all ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    # Method to view the Recipes
    def __str__(self):
        output = "Recipe Name: " + str(self.name) + "\n" + "Ingredients: " + str(self.ingredients) + "\n" + "Cooking Time: " + str(self.cooking_time) + " minutes" + "\n" + "Difficulty: " + str(self.calc_difficulty())
        return output

# Method to search recipes
def recipe_search(data, search_term):
    for recipe in data:
        if recipe.search_ingredients(search_term):
            print(recipe)


# MAIN CODE

# RECIPES
tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

recipes_list = [tea, coffee, cake, smoothie]

print("Recipes with SUGAR: ")
recipe_search(recipes_list, "Sugar")
print("\n")
print("Recipes with BANANAS: ")
recipe_search(recipes_list, "Bananas")
print("\n")
print("Recipes with WATER: ")
recipe_search(recipes_list, "Water")

