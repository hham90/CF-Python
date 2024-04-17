from sqlalchemy import create_engine
engine = create_engine("mysql://cf-python:password@localhost/my_database")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# creation of Recipe class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
# simple string representation of recipe
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
# indepth representation of recipe
    def __str__(self):
        return (
            "-----------------------------\n"
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.calc_difficulty()}\n"
            "-----------------------------\n"
        )
# function to calculate difficulty of recipe
    def calc_difficulty(self):
        num_ingredients = len(self.ingredients)
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        if self.cooking_time < 10 and num_ingredients <= 4:
            return "Medium"
        if self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        if self.cooking_time > 10 and num_ingredients >= 4:
            return "Hard"
        return self.difficulty
# function to return ingredients as a list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(", ")

# creating table on the database
Base.metadata.create_all(engine)

# function to input a new recipe
def create_recipe():
    name = input("Enter name of the recipe (max 50 chars): ")
    ingredients_input = input("Enter ingredients: ")
    cooking_time = input("Enter cooking time in minutes: ")

    # Validate input
    if len(name) > 50:
        print(
            "Invalid recipe name. Please ensure it is alphanumeric and less than 50 characters."
        )
        return
    if not cooking_time.isnumeric():
        print("Invalid cooking time. Please ensure it is a number.")
        return

    recipe_entry = Recipe(
        name=name, ingredients=ingredients_input, cooking_time=int(cooking_time)
    )
    recipe_entry.difficulty = recipe_entry.calc_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("Recipe successfully created.")

# function to view all recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are currently no recipes.")
    for recipe in recipes:
        print(recipe)

# function to search recipes by ingredient
def search_by_ingredients():
    results = session.query(Recipe.ingredients).all()
    # function to check if ingredients > 0
    apples = session.query(Recipe.ingredients).count()
    if apples == 0:
        print("There are no recipes in the database.")
        return
    all_ingredients = []
    # get ingredients from DB
    for ingredient in results:
        ingredient_list = ingredient[0].split(", ")
        for ingredients in ingredient_list:
            if not ingredients in all_ingredients:
                all_ingredients.append(ingredients)
    for count, ingredients in enumerate(all_ingredients):
        print(count, ingredients)

    ingredients_input = input("Please enter the corresponding number to see all recipes that use that ingredient: ")
    ing = ingredients_input.split()
    search_ingredients = []
    for ings in ing:
        if not ings.isnumeric():
            print("Input is not valid!")
            return
        else: ings = int(ings)
        if ings < 0 or ings >= len(all_ingredients):
            print("Input is not valid!")
            return
        search_ingredients.append(all_ingredients[int(ings)])

    conditions = []
    for search_ingredient in search_ingredients:
        like_term = "%" + search_ingredient + "%"
        conditions.append(Recipe.ingredients.like(like_term))
    recipes = session.query(Recipe).filter(*conditions).all()
    # Print all resulting recipes
    for recipe in recipes:
        print(recipe)

# function to edit recipe
def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id}. {recipe_name}")

    recipe_id_to_edit = input("Enter the ID of the recipe you want to edit: ")
    if not recipe_id_to_edit.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    recipe_to_edit = session.query(Recipe).get(int(recipe_id_to_edit))
    if not recipe_to_edit:
        print("Recipe not found.")
        return

    print("1. Name\n2. Ingredients\n3. Cooking Time")
    attribute_to_edit = input("Enter the number of the attribute you want to edit: ")

    if attribute_to_edit == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute_to_edit == "2":
        new_ingredients = input("Enter the new ingredients, separated by a comma: ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute_to_edit == "3":
        new_cooking_time = input("Enter the new cooking time in minutes: ")
        if not new_cooking_time.isnumeric():
            print("Invalid cooking time. Please enter a number.")
            return
        recipe_to_edit.cooking_time = int(new_cooking_time)

    recipe_to_edit.difficulty = recipe_to_edit.calc_difficulty()
    session.commit()
    print("Recipe updated successfully.")

# function to delete a recipe
def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id}. {recipe_name}")

    recipe_id_to_delete = input("Enter the ID of the recipe you want to delete: ")
    if not recipe_id_to_delete.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    recipe_to_delete = session.query(Recipe).get(int(recipe_id_to_delete))
    if not recipe_to_delete:
        print("Recipe not found.")
        return

    confirmation = input("Are you sure you want to delete this recipe? (yes/no): ")
    if confirmation.lower() == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully.")

# main loop for application

while True:
    print("1. Create new recipe")
    print("2. View all recipes")
    print("3. Search for recipes by ingredients")
    print("4. Edit recipe")
    print("5. Delete a recipe")
    print("Type 'quit' to leave the application")
    choice = input("Enter your choice: ")

    if choice == "1":
        create_recipe()
    if choice == "2":
        view_all_recipes()
    if choice == "3":
        search_by_ingredients()
    if choice == "4":
        edit_recipe()
    if choice == "5":
        delete_recipe()
    if choice == 'quit':
        break

session.close()
engine.dispose()