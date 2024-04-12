import pickle

# displays recipe
def display_recipe(recipe):
    print("Recipe: ", recipe["name"])
    print("Cooking Time: ", recipe["cooking_time"])
    print("Ingredients: ", recipe["ingredients"])
    print("Difficulty: ", recipe["difficulty"])

# allows user to search recipes by ingredient
def search_ingredients(data):
    num_ingredients = enumerate(data["all_ingredients"])
    list_ing = list(num_ingredients)

    for number in list_ing:
        print(number[0], number[1])
    try:
        num = int(input("Pick the number corresponding to the ingredient: "))
        ingredient_searched = list_ing[num][1]
        print("Searching for recipes with", ingredient_searched)
    except ValueError:
        print("Please input a number.")
    else:
        for ing in data["recipes_list"]:
            if ingredient_searched in ing["ingredients"]:
                print(ing)


filename = input("Enter the name of the file you would like to save to: ")
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
except FileNotFoundError:
    print("No files match that name.")
else:
    search_ingredients(data)
