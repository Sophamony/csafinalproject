from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Text, Scrollbar, Frame, END
from PIL import Image, ImageTk
import io
import requests
import os
import mysql.connector

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame3")

#  Function to connect to MySQL database
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

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

# Fetch recipes from the database
def fetch_saved_recipes():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT title, ingredients, instructions, image_url FROM saved_recipes")
            recipes = cursor.fetchall()
            return recipes
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
            
def remove_recipe(title):
    """Remove a recipe by title from the database."""
    connection = connect_to_db()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM saved_recipes WHERE title = %s", (title,))
        connection.commit()
        messagebox.showinfo("Success", f"Recipe '{title}' removed successfully!")
        display_saved_recipes()  # Refresh the recipes
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error deleting recipe: {err}")
    finally:
        connection.close()

# Display recipes in the Text widget with scrollbar
def display_saved_recipes():
    text_widget.delete(1.0, END)  # Clear the Text widget
    text_widget.image_list = []  # Reset the image references to prevent garbage collection

    recipes = fetch_saved_recipes()
    if not recipes:
        text_widget.insert(END, "No saved recipes found.\n")
        return

    for recipe in recipes:
        title, ingredients, instructions, image_url = recipe
        ingredients_list = ingredients.split(",")  # Assuming ingredients are comma-separated

        try:
            # Fetch and resize the image
            response = requests.get(image_url)
            img_data = io.BytesIO(response.content)
            img = Image.open(img_data).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)

            # Add the image to the Text widget
            text_widget.image_create(END, image=img_tk)
            text_widget.image_list.append(img_tk)  # Store a reference to prevent garbage collection

            # Add recipe details
            text_widget.insert(END, f"\n{title}\n", "title")
            text_widget.insert(END, "Ingredients:\n", "header")
            for ingredient in ingredients_list:
                text_widget.insert(END, f"- {ingredient.strip()}\n")
            text_widget.insert(END, f"\nInstructions:\n{instructions}\n", "body")

        except Exception as e:
            text_widget.insert(END, f"Error loading image for {title}: {e}\n")

# Add a remove button
        remove_button = Button(
            text_widget,
            text="Remove",
            command=lambda title=title: remove_recipe(title),
            bg="red",
            fg="white",
            font=("Arial", 12)
        )
        text_widget.window_create(END, window=remove_button)
        text_widget.insert(END, "\n" + "-" * 40 + "\n\n")


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

canvas.create_text(
    83.0,
    214.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Content", 26 * -1)
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
    x=0.0,
    y=597.0,
    width=300.0,
    height=100.0
)

# Scrollable Text widget setup
frame = Frame(window)
frame.place(x=300, y=100, width=1120, height=580)

text_widget = Text(frame, wrap="word", font=("Arial", 14))
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# Tag configuration for text styling
text_widget.tag_configure("title", font=("Arial", 16, "bold"))
text_widget.tag_configure("header", font=("Arial", 14, "bold"))
text_widget.tag_configure("body", font=("Arial", 12))

# Button to display saved recipes
button_saved = Button(
    text="Show Saved Recipes",
    command=display_saved_recipes,
    bg="#D9D9D9",
    font=("Arial", 14)
)
button_saved.place(x=300, y=50, width=200, height=40)

window.resizable(False, False)
window.mainloop()

