from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def swap_to_login():
    window.destroy()
    os.system('python login.py')

def swap_to_signup():
    window.destroy()
    os.system('python signup.py')

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
    725.0,
    390.0,
    image=image_image_1
)

canvas.create_text(
    320.0,
    67.0,
    anchor="nw",
    text="Welcome to Recipe Finder",
    fill="#000000",
    font=("Content", 64 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_login,
    relief="flat"
)
button_1.place(
    x=367.0,
    y=568.0,
    width=260.0,
    height=70.0
)

canvas.create_text(
    413.0,
    199.0,
    anchor="nw",
    text="Join us today or log in to\nstart exploring delicious\nrecipes and meal plans.",
    fill="#000000",
    font=("Content", 48 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=swap_to_signup,
    relief="flat"
)
button_2.place(
    x=754.0,
    y=568.0,
    width=260.0,
    height=70.0
)
window.resizable(False, False)
window.mainloop()
