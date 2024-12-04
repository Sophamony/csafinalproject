import requests
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Text, Scrollbar, Frame, END
from PIL import Image, ImageTk
import io
from pathlib import Path
import os
import mysql.connector

# Define the output and assets paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  
            user="root", 
            password="MONY@2024SQL",
            database="recipefinder"
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

def swap_to_home():
    window.destroy()
    os.system('python home.py')

def swap_to_saved():
    window.destroy()
    os.system('python saved.py')

def swap_to_list():
    window.destroy()
    os.system('python list.py')

def swap_to_logout():
    window.destroy()
    os.system('python first.py')

# Function to save a recipe
def save_recipe(recipe):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO saved_recipes (title, ingredients, instructions, image_url)
            VALUES (%s, %s, %s, %s)
            """
            ingredients = ', '.join([
                recipe[f"strIngredient{i}"]
                for i in range(1, 21)
                if recipe[f"strIngredient{i}"]
            ])
            values = (recipe["strMeal"], ingredients, recipe["strInstructions"], recipe["strMealThumb"])
            cursor.execute(sql, values)
            connection.commit()
            print(f"Recipe '{recipe['strMeal']}' saved successfully.")
            messagebox.showinfo("Success", f"Recipe '{recipe['strMeal']}' saved successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", f"Failed to save recipe: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to add ingredients to the shopping list
def add_to_shopping_list(title, ingredients):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO shopping_list (title, ingredients) VALUES (%s, %s)"
            
            ingredients_str = ', '.join(ingredients)  # Join ingredients into a single string
            
            cursor.execute(sql, (title, ingredients_str))  # Execute the insert statement
            
            connection.commit()
            print(f"Ingredients added to shopping list: {title} - {ingredients_str}")
            messagebox.showinfo("Success", "Ingredients added to shopping list.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", f"Failed to add ingredients: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to display random recipes
def display_random_recipes():
    text_widget.delete(1.0, END)  # Clear the text widget
    text_widget.image_list = []  # Reset image references

    for _ in range(3):  # Display 3 random recipes
        try:
            api_url = "https://www.themealdb.com/api/json/v1/1/random.php"
            response = requests.get(api_url)
            response.raise_for_status()
            meal = response.json()

            if 'meals' in meal and meal['meals']:
                recipe = meal['meals'][0]
                title = recipe["strMeal"]
                image_url = recipe["strMealThumb"]
                instructions = recipe.get("strInstructions", "No instructions available.")
                ingredients = [
                    recipe[f"strIngredient{i}"]
                    for i in range(1, 21)
                    if recipe[f"strIngredient{i}"]
                ]

                # Fetch the image
                img_data = requests.get(image_url).content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((200, 200))
                img_tk = ImageTk.PhotoImage(img)

                # Add the image to the widget
                text_widget.image_create(END, image=img_tk)
                text_widget.image_list.append(img_tk)

                # Insert recipe details
                text_widget.insert(END, f"\n{title}\n")
                text_widget.insert(END, f"Ingredients:\n")
                for ingredient in ingredients:
                    text_widget.insert(END, f"- {ingredient}\n")
                text_widget.insert(END, f"\nInstructions:\n{instructions}\n")

                # Add buttons
                button_frame = Frame(text_widget, bg="#FFFFFF")
                save_button = Button(
                    button_frame, text="Save Recipe", width=20, height=2, command=lambda r=recipe: save_recipe(r)
                )
                shopping_list_button = Button(
                    button_frame,
                    text="Add to Shopping List", width=20, height=2,
                    command=lambda title=title, ingredients=ingredients: add_to_shopping_list(title, ingredients)
                )

                save_button.pack(side="left", padx=5, pady=5)
                shopping_list_button.pack(side="left", padx=5, pady=5)
                text_widget.window_create(END, window=button_frame)

                # Divider line
                text_widget.insert(END, "\n" + "-" * 40 + "\n\n")

        except requests.exceptions.RequestException as e:
            text_widget.insert(END, f"An error occurred while fetching a random recipe: {e}\n")

# Function to search for recipes by ingredient
def search_recipe():
    ingredient = entry_1.get().strip()  # Get user input from the Entry widget
    if not ingredient:
        text_widget.delete(1.0, END)
        text_widget.insert(END, "Please enter an ingredient to search for recipes.")
        return

    # URL for searching by ingredient
    api_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        meals = response.json()

        # Clear the text widget
        text_widget.delete(1.0, END)
        text_widget.image_list = []  # Reset image references

        if 'meals' not in meals or not meals['meals']:
            text_widget.insert(END, "No recipes found for the given ingredient.")
            return

        for meal in meals['meals']:
            meal_id = meal["idMeal"]
            detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
            detail_response = requests.get(detail_url)
            detail_response.raise_for_status()
            recipe_details = detail_response.json()

            if 'meals' in recipe_details:
                recipe = recipe_details['meals'][0]
                title = recipe["strMeal"]
                image_url = recipe["strMealThumb"]
                instructions = recipe.get("strInstructions", "No instructions available.")
                ingredients = [
                    recipe[f"strIngredient{i}"]
                    for i in range(1, 21)
                    if recipe[f"strIngredient{i}"]
                ]

                # Fetch the image
                img_data = requests.get(image_url).content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((200, 200))
                img_tk = ImageTk.PhotoImage(img)

                # Add the image to the widget
                text_widget.image_create(END, image=img_tk)
                text_widget.image_list.append(img_tk)

                # Insert recipe details
                text_widget.insert(END, f"\n{title}\n")
                text_widget.insert(END, f"Ingredients:\n")
                for ingredient in ingredients:
                    text_widget.insert(END, f"- {ingredient}\n")
                text_widget.insert(END, f"\nInstructions:\n{instructions}\n")

                # Add buttons
                button_frame = Frame(text_widget, bg="#FFFFFF")
                save_button = Button(
                    button_frame, text="Save Recipe", command=lambda r=recipe: save_recipe(r)
                )
                shopping_list_button = Button(
                    button_frame,
                    text="Add to Shopping List", width=20, height=2,
                    command=lambda title=title, ingredients=ingredients: add_to_shopping_list(title, ingredients)
                )

                save_button.pack(side="left", padx=5, pady=5)
                shopping_list_button.pack(side="left", padx=5, pady=5)
                text_widget.window_create(END, window=button_frame)

                # Divider line
                text_widget.insert(END, "\n" + "-" * 40 + "\n\n")

    except requests.exceptions.RequestException as e:
        text_widget.delete(1.0, END)
        text_widget.insert(END, f"An error occurred: {e}")


window = Tk()

window.geometry("1450x780")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 780,
    width = 1450,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    150.0,
    390.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    149.0,
    117.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_saved,
    relief="flat"
)
button_1.place(
    x=0.0,
    y=397.0,
    width=300.0,
    height=100.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_list,
    relief="flat"
)
button_2.place(
    x=0.0,
    y=497.0,
    width=300.0,
    height=100.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_home,
    relief="flat"
)
button_3.place(
    x=0.0,
    y=297.0,
    width=300.0,
    height=100.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_logout,
    relief="flat"
)
button_4.place(
    x=1665.0,
    y=57.0,
    width=197.0,
    height=88.0
)

canvas.create_text(
    60.0,
    214.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Content", 32 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_logout,
    relief="flat"
)
button_5.place(
    x=0.0,
    y=597.0,
    width=300.0,
    height=100.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    770.0,
    78.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F6AE85",
    fg="#000716",
    highlightthickness=0,
    font=("Arial", 20)
)
entry_1.place(
    x=387.0,
    y=43.0,
    width=766.0,
    height=68.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=search_recipe,
    relief="flat"
)
button_6.place(
    x=1217.0,
    y=40.0,
    width=175.0,
    height=73.0
)

# Text widget to display results
text_widget = Text(
    window,
    bg="#FFFFFF",
    fg="#000000",
    font=("Content", 14),
    wrap="word",
    highlightthickness=0
)
text_widget.place(x=355.0, y=130.0, width=1035.0, height=600.0)

# Scrollbar for the text widget
scrollbar = Scrollbar(window, command=text_widget.yview)
text_widget.configure(yscrollcommand=scrollbar.set)
scrollbar.place(x=1390.0, y=130.0, height=600.0)

display_random_recipes()
window.resizable(False, False)
window.mainloop()
