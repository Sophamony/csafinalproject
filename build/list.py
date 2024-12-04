from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Text, Scrollbar, Frame, END
import mysql.connector
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame3")

# Utility to get asset paths
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to connect to MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1", 
            user="root",  
            password="MONY@2024SQL",
            database="recipefinder"
        )
        if connection.is_connected():
            print("Connected to MySQL database.")
            return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

# Page swapping functions
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
def fetch_shopping_list():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT title, ingredients FROM shopping_list")
            recipes = cursor.fetchall()
            print(f"Fetched recipes: {recipes}")  # Debugging output
            return recipes
        except mysql.connector.Error as err:
            print(f"Error fetching shopping list: {err}")
            messagebox.showerror("Database Error", f"Error fetching shopping list: {err}")
            return []
        finally:
            connection.close()
    else:
        print("No database connection.")
        return []

# Remove a recipe by title from the database
def remove_recipe(title):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM shopping_list WHERE title = %s", (title,))
            connection.commit()
            messagebox.showinfo("Success", f"'{title}' removed successfully!")
            display_shopping_list()  # Refresh the list
        except mysql.connector.Error as err:
            print(f"Error removing recipe: {err}")
            messagebox.showerror("Database Error", f"Error removing recipe: {err}")
        finally:
            connection.close()

# Display shopping list
def display_shopping_list():
    text_widget.delete(1.0, END) 

    recipes = fetch_shopping_list()
    if not recipes:
        text_widget.insert(END, "No shopping list found.\n")
        return

    for recipe in recipes:
        title, ingredients = recipe  
        ingredients_list = ingredients.split(",")  
        
        # Display the recipe title
        text_widget.insert(END, f"{title}\n", "title")
        
        # Display the ingredients
        text_widget.insert(END, "Ingredients:\n", "header")
        for ingredient in ingredients_list:
            text_widget.insert(END, f"- {ingredient.strip()}\n")

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


# Initialize main window
window = Tk()
window.geometry("1450x780")
window.configure(bg="#FFFFFF")

# Canvas for background and buttons
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=780,
    width=1450,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Add images to canvas (if needed)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(150.0, 390.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(149.0, 117.0, image=image_image_2)

# Navigation buttons
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=swap_to_saved, relief="flat").place(x=0, y=397, width=300, height=100)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=swap_to_list, relief="flat").place(x=0, y=497, width=300, height=100)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=swap_to_home, relief="flat").place(x=0, y=297, width=300, height=100)

canvas.create_text(83.0, 214.0, anchor="nw", text="Username", fill="#000000", font=("Content", 26 * -1))

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=swap_to_logout, relief="flat").place(x=0, y=597, width=300, height=100)

# Scrollable text widget
frame = Frame(window)
frame.place(x=300, y=100, width=1120, height=580)

text_widget = Text(frame, wrap="word", font=("Arial", 14))
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(yscrollcommand=scrollbar.set)

# Tag configuration for styling
text_widget.tag_configure("title", font=("Arial", 16, "bold"))
text_widget.tag_configure("header", font=("Arial", 14, "bold"))
text_widget.tag_configure("body", font=("Arial", 12))

# Button to display shopping list
button_saved = Button(
    text="Show Shopping List",
    command=display_shopping_list,
    bg="#D9D9D9",
    font=("Arial", 14)
)
button_saved.place(x=300, y=50, width=200, height=40)

window.resizable(False, False)
window.mainloop()
