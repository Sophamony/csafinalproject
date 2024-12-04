from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import os
import mysql.connector
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_home_page():
    window.destroy()
    os.system("python home.py")

def login():
    username = entry_1.get()
    password = entry_2.get()

    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",  
            user="root",
            password="MONY@2024SQL",
            database="recipefinder"
        )

        cursor = connection.cursor()

        # Query to fetch user details
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]
            if password == stored_password:
                messagebox.showinfo("Login Successfully", f"Welcome, {username}!")
                open_home_page()
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            messagebox.showerror("Login Failed!", "Username not found.")
            
        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return    
window = Tk()

window.geometry("1453x780")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 780,
    width = 1453,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    725.0,
    390.0,
    image=image_image_1
)

canvas.create_text(
    225.0,
    49.0,
    anchor="nw",
    text="Welcome! Please fill in your info to login",
    fill="#000000",
    font=("Content", 48 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=login,
    relief="flat"
)
button_1.place(
    x=557.0,
    y=588.0,
    width=260.0,
    height=70.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    687.0,
    288.0,
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
    y=253.0,
    width=656.0,
    height=68.00000000000006
)

canvas.create_text(
    342.0,
    194.0,
    anchor="nw",
    text="Username:",
    fill="#000000",
    font=("Content", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    687.0,
    446.0,
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
    y=411.0,
    width=656.0,
    height=68.00000000000006
)

canvas.create_text(
    342.0,
    352.0,
    anchor="nw",
    text="Password:",
    fill="#000000",
    font=("Content", 32 * -1)
)
window.resizable(False, False)
window.mainloop()