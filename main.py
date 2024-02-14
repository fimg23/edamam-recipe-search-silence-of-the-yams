import requests as rq   # rq assigned as alias to requests
import json

# Function to search for recipes using the Edamam API
def search_recipes(ingredient, cuisine_type):
    # Construct the API URL for recipe search using your app_id and app_key credentials
    app_id = ""   # Replace with your Edamam app_id
    app_key = ""   # Replace with your Edamam app_key
    url = f"https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}"

    # Include cuisine type in the request if provided
    if cuisine_type:
        url += f"&cuisineType={cuisine_type}"

    # Make the API request
    response = rq.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Parse the JSON data from the response and return the 'hits' field or an empty list
        return data.get('hits', [])   # Return recipe data if available. Square brackets get an empty list as opposed to 'None'. Does not assume that the hits key is always present and returns a value.
    else:
        # Print an error message and return an empty list in case of an unsuccessful response
        print(f"Error: Unable to retrieve recipes. Status Code: {response.status_code}")
        return []

# Function to display recipe information
def display_recipes(recipes):
    # Check if the recipes list is empty
    if not recipes:
        # Print a message if no recipes are found
        print("No recipes found.")
    else:
        # Display information for each recipe in the list
        stop_index = 5
        for index, recipe in enumerate(recipes[:stop_index], start=1):
            recipe_data = recipe['recipe']
            print(f"\nRecipe {index}:")
            print(f"Label: {recipe_data['label']}")
            print(f"Cuisine Type: {', '.join(recipe_data.get('cuisineType', []))}")
            servings = recipe['recipe']['yield']
            calories_per_serving = int(recipe['recipe']['totalNutrients']['ENERC_KCAL']['quantity'] / servings)
            print(f"{calories_per_serving} cal per serving")
            print("Ingredients:")
            for ingredient in recipe_data.get('ingredientLines', []):
                print(f"- {ingredient}")
            print(f"URL: {recipe_data.get('url', '')}")
            print("")

# Function to save recipe information to a JSON file
def save_to_json(recipes, ingredient):
    file_path = f"{ingredient}_recipes.json"
    recipe_data = []
    for recipe in recipes:
        # Extract relevant information from the recipe data
        recipe_info={
            'Recipe': recipe['recipe']['label'],
            'Cuisine Type': recipe['recipe'].get('cuisineType', []),
            'Calories per Serving': int(
                recipe['recipe']['totalNutrients']['ENERC_KCAL']['quantity'] / recipe['recipe']['yield']),
            'Ingredients': recipe['recipe']['ingredientLines'],
            'Link to Recipe': recipe['recipe']['url'],
        }
        recipe_data.append(recipe_info)
        
    # Save the recipe information to a JSON file
    with open(file_path, 'w')as file:
        json.dump(recipe_data, file, indent=4)

    print(f"Recipes saved to {file_path}")

# Function to run the recipe search and display process
def run():
    # Get user input for the ingredient to search for recipes
    ingredient = input("Enter an ingredient (or ingredients) to search for recipes: \n")
    while True:   # created an Infinite loop so the program continues to execute indefinitely until the break statement is encountered or e certain condition is met.
        cuisine_type = input("Enter the cuisine type to filter recipes (press 'Enter' to leave blank): \n")
        if cuisine_type == 'british':
            confirm = input("British... are you sure?? (Y/N) \n").lower()
            if confirm == 'y':
                break   # Exit the loop if Y
            elif confirm == 'n':
                continue # Continue to the next iteration of the loop if N
            else:
                print("Invalid input. Let's try again.")   # Prints an error message and continues the loop to ask for input again.
        else:
            break   # # Exits the loop if the user enters a different cuisine or leaves blank
            
    # Call the search_recipes function to get the recipes based on the user input
    recipes = search_recipes(ingredient, cuisine_type)

    # Display the recipes using the display_recipes function
    display_recipes(recipes)

    # Calls the save to JSON function askin the user if they want to save the recipes to a JSON file
    save_to_json(recipes, ingredient)

# Call the run function to start the program
run()

