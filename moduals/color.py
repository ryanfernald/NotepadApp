# moduals/color.py
from tkinter import colorchooser

def change_bg_color(app, color):
    app.text_area.configure(bg=color)
    app.master.configure(bg=color)

def choose_custom_color(app):
    color_code = colorchooser.askcolor(title="Choose color")[1] 
    if color_code:
        change_bg_color(app, color_code)
