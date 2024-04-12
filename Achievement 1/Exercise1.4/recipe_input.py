import pickle

# takes user input and creates a dictionary
def take_recipe():
    name = input("Recipe Name: ")
    cooking_time = int(input("Cooking time in minutes: "))
    ingredients = input("Ingredients: ").split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty,
        }
    return recipe

# calculates difficulty of recipe
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    if cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    if cooking_time > 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    if cooking_time > 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty

# prompts user to enter a filename
filename = input("Enter filename of file you wish to open: ")

# tries to open the file, if it doesn't exist, create a new file
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
# file does not exist error message
except FileNotFoundError:
    print("No such files match that name - creating a new file")
    data = {"recipes_list": [], "all_ingredients": []}
# general error message
except:
    print("Oops! Something went wrong. Try again.")
    data = {"recipes_list": [], "all_ingredients": []}
# closes file
else:
    file.close()
# extracts the data into two variables
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# asks user how many recipes they want to enter
n = int(input("How many recipes would you like to enter?: "))

# loops to add ingredients to new recipe
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

# new dictionary with updated data
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# creates/updates/closes new bin file
updated_file = open(filename, 'wb')
pickle.dump(data, updated_file)
updated_file.close()
print("Recipe has been updated!")