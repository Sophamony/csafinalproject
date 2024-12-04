from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import os
import mysql.connector
import re
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_home_page():
    # Close the current signup window
    window.destroy()
    # Open the home page
    os.system('python home.py')

def is_valid_email(email):
    """Validate email using regex."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def handle_signup():
    username = entry_1.get().strip()
    email = entry_3.get().strip()
    password = entry_2.get().strip()

    # Ensure all fields are filled
    if not username or not email or not password:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    # Validate email format
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address!")
        return

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="MONY@2024SQL",
            database="recipefinder"
        )
        cursor = connection.cursor()

        # Check if the email already exists
        email = email.lower()  # Normalize email to lowercase
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Duplicate Email", "This email is already registered!")
            return

        # Insert new user into the database
        cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        ''', (username, email, password))

        connection.commit()
        cursor.close()
        connection.close()

        # Display success message and clear input fields
        messagebox.showinfo("Signup Successful", "You have successfully signed up!")
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        entry_3.delete(0, 'end')
        open_home_page()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


window = Tk()
window.geometry("1450x780")
window.configure(bg="#FFFFFF")

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
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    725.0,
    390.0,
    image=image_image_1
)

canvas.create_text(
    325.0,
    49.0,
    anchor="nw",
    text="Welcome! Sign up and get started",
    fill="#000000",
    font=("Content", 48 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=handle_signup,
    relief="flat"
)
button_1.place(
    x=595.0,
    y=663.0,
    width=260.0,
    height=70.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    687.0,
    259.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=359.0,
    y=224.0,
    width=656.0,
    height=68.0
)

canvas.create_text(
    342.0,
    165.0,
    anchor="nw",
    text="Username:",
    fill="#000000",
    font=("Content", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    687.0,
    572.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=359.0,
    y=537.0,
    width=656.0,
    height=68.0
)

canvas.create_text(
    342.0,
    478.0,
    anchor="nw",
    text="Password:",
    fill="#000000",
    font=("Content", 32 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    687.0,
    419.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=359.0,
    y=384.0,
    width=656.0,
    height=68.0
)

canvas.create_text(
    342.0,
    325.0,
    anchor="nw",
    text="Email:",
    fill="#000000",
    font=("Content", 32 * -1)
)

window.resizable(False, False)
window.mainloop()
