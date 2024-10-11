# moduals/binds.py
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button
from moduals.file import new_file, open_file, save_file, save_as_file
from moduals.color import change_bg_color, choose_custom_color


def new_window(app):
    new_win = Toplevel(app.master)
    new_win.geometry("600x400")
    new_win.configure(bg=app.text_area.cget("bg"))  # Same background color as current window
    new_win.title("New Notepad Window")

    # Create a new text area for the new window
    new_text_area = tk.Text(new_win, bg=app.text_area.cget("bg"))
    new_text_area.pack(expand=True, fill='both')

    # Set up the menu bar for the new window
    menu_bar = tk.Menu(new_win)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_file(app))  # Reuse same file commands
    file_menu.add_command(label="Open", command=lambda: open_file(app))
    file_menu.add_command(label="Save", command=lambda: save_file(app))
    file_menu.add_command(label="Save As", command=lambda: save_as_file(app))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=new_win.quit)

    # Color menu
    color_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Color", menu=color_menu)
    color_menu.add_command(label="Pale Violet Red", command=lambda: change_bg_color(app, "pale violet red"))
    color_menu.add_command(label="Thistle", command=lambda: change_bg_color(app, "thistle2"))
    color_menu.add_command(label="Pale Turquoise", command=lambda: change_bg_color(app, "pale turquoise"))
    color_menu.add_command(label="Dark Sea Green", command=lambda: change_bg_color(app, "DarkSeaGreen1"))
    color_menu.add_command(label="Misty Rose", command=lambda: change_bg_color(app, "misty rose"))
    color_menu.add_command(label="Lavender", command=lambda: change_bg_color(app, "lavender"))
    color_menu.add_command(label="Choose...", command=lambda: choose_custom_color(app))

    new_win.config(menu=menu_bar)



def find_text(app, open_replace=False):
    # Create the Find window
    find_win = Toplevel(app.master)
    find_win.title("Find")
    find_win.geometry("300x100")
    
    Label(find_win, text="Find:").grid(row=0, column=0, padx=5, pady=5)
    
    search_entry = Entry(find_win)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    search_entry.focus_set()
    search_entry.bind("<KeyRelease>", lambda event: highlight_text(app, search_entry.get()))  # Real-time highlight

    expand_button = Button(find_win, text="Replace", command=lambda: open_replace_menu(app, find_win, search_entry))
    expand_button.grid(row=0, column=2, padx=5, pady=5)

    find_win.bind("<Destroy>", lambda event: app.text_area.tag_remove('highlight', '1.0', tk.END))

    if open_replace:
        open_replace_menu(app, find_win, search_entry)

def open_replace_menu(app, find_win, search_entry):
    # Expand the Find window into Find and Replace mode
    find_win.geometry("300x150")
    
    Label(find_win, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
    
    replace_entry = Entry(find_win)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    replace_entry.bind("<Return>", lambda event: replace_one(app, search_entry.get(), replace_entry.get()))
    replace_entry.bind("<Shift-Return>", lambda event: replace_all(app, search_entry.get(), replace_entry.get()))

    Button(find_win, text="Replace One", command=lambda: replace_one(app, search_entry.get(), replace_entry.get())).grid(row=2, column=0, padx=5, pady=5)
    Button(find_win, text="Replace All", command=lambda: replace_all(app, search_entry.get(), replace_entry.get())).grid(row=2, column=1, padx=5, pady=5)
    
def replace_one(app, search_text, replace_text):
    content = app.text_area.get("1.0", tk.END)
    start_index = content.find(search_text)
    if start_index >= 0:
        end_index = start_index + len(search_text)
        app.text_area.delete(f"1.0+{start_index}c", f"1.0+{end_index}c")
        app.text_area.insert(f"1.0+{start_index}c", replace_text)

def replace_all(app, search_text, replace_text):
    content = app.text_area.get("1.0", tk.END)
    new_content = content.replace(search_text, replace_text)
    app.text_area.delete("1.0", tk.END)
    app.text_area.insert(tk.END, new_content)

def highlight_text(app, search_text):
    # Remove previous highlights
    app.text_area.tag_remove('highlight', '1.0', tk.END)
    
    if search_text:
        start_pos = '1.0'
        while True:
            start_pos = app.text_area.search(search_text, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            app.text_area.tag_add('highlight', start_pos, end_pos)
            app.text_area.tag_config('highlight', background='yellow')
            start_pos = end_pos

def delete_word(event):
    # Get the current cursor position
    pos = event.widget.index(tk.INSERT)
    # Move the cursor backward to find the start of the previous word
    while pos != '1.0':  # Don't go past the start of the text widget
        char = event.widget.get(pos + '-1c')
        if char.isspace() or char in ',.;:!?()[]{}\'"':
            break
        pos = event.widget.index(pos + '-1c')
    # Delete from the current cursor position to the found position
    event.widget.delete(pos, tk.INSERT)

def bind_shortcuts(app):
    # Bindings for shortcuts
    app.master.bind("<Control-n>", lambda event: new_window(app))
    app.master.bind("<Control-f>", lambda event: find_text(app))
    app.master.bind("<Control-h>", lambda event: find_text(app, open_replace=True))  # Directly open Find and Replace
    app.master.bind('<Control-BackSpace>', delete_word)