# moduals/binds.py
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button
from moduals.file import new_file, open_file, save_file, save_as_file, mark_as_modified
from moduals.color import change_bg_color, choose_custom_color
from tkinter import font
import platform

def new_window(app):
    # Create a new window (top-level window)
    new_win = tk.Toplevel(app.master)
    new_win.geometry("600x400")
    new_win.title("New Notepad Window")
    new_win.focus_set()  # Set focus to the new window

    new_win.topmost_var = tk.BooleanVar(value=True)
    new_win.attributes('-topmost', new_win.topmost_var.get()) 

    new_win.configure(bg=app.text_area.cget("bg"))

    new_text_area = tk.Text(new_win, bg=app.text_area.cget("bg"), font=("Segoe Print", 14))
    new_text_area.pack(expand=True, fill='both')

    # Store the text area in the new window instance
    new_win.text_area = new_text_area

    menu_bar = tk.Menu(new_win)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_window(app))  # Recursively open new windows
    file_menu.add_command(label="Open", command=lambda: open_file(app))
    file_menu.add_command(label="Save", command=lambda: save_file(app))
    file_menu.add_command(label="Save As", command=lambda: save_as_file(app))
    file_menu.add_checkbutton(label="Float", onvalue=True, offvalue=False, variable=new_win.topmost_var,
                          command=lambda: toggle_topmost(new_win))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=new_win.quit)

    # Color menu
    color_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Color", menu=color_menu)
    color_menu.add_command(label="Notepad Yellow", command=lambda: change_bg_color(app, "pale goldenrod"))
    color_menu.add_command(label="Thistle", command=lambda: change_bg_color(app, "thistle2"))
    color_menu.add_command(label="Pale Turquoise", command=lambda: change_bg_color(app, "pale turquoise"))
    color_menu.add_command(label="Dark Sea Green", command=lambda: change_bg_color(app, "DarkSeaGreen1"))
    color_menu.add_command(label="Misty Rose", command=lambda: change_bg_color(app, "misty rose"))
    color_menu.add_command(label="Lavender", command=lambda: change_bg_color(app, "lavender"))
    color_menu.add_command(label="Choose...", command=lambda: choose_custom_color(app))

    # Apply the menu bar to the new window
    new_win.config(menu=menu_bar)

    # Apply the shortcuts to the new window as well
    bind_shortcuts(new_win)

    return new_win

def toggle_topmost(window):
    window.attributes('-topmost', window.topmost_var.get())

def find_text(app, open_replace=False):

    # Use app.master if no new window is passed
    active_win = app if isinstance(app, tk.Tk) else app.master

    # Create the Find window
    find_win = Toplevel(app.master)
    find_win.title("Find")
    find_win.geometry("400x150")  
    find_win.attributes('-topmost', True)
    
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
    find_win.geometry("400x150")
    find_win.attributes('-topmost', True)
    
    Label(find_win, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
    
    replace_entry = Entry(find_win)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    replace_entry.bind("<Return>", lambda event: replace_one(app, search_entry.get(), replace_entry.get()))
    replace_entry.bind("<Shift-Return>", lambda event: replace_all(app, search_entry.get(), replace_entry.get()))

    Button(find_win, text="Replace One", command=lambda: replace_one(app, search_entry.get(), replace_entry.get())).grid(row=2, column=0, padx=5, pady=5)
    Button(find_win, text="Replace All", command=lambda: replace_all(app, search_entry.get(), replace_entry.get())).grid(row=2, column=1, padx=5, pady=5)
    
def replace_one(app, search_text, replace_text):
    # Handle special case for carriage return
    if replace_text == "\\n":
        replace_text = "\n"

    content = app.text_area.get("1.0", tk.END)
    start_index = content.find(search_text)
    if start_index >= 0:
        end_index = start_index + len(search_text)
        app.text_area.delete(f"1.0+{start_index}c", f"1.0+{end_index}c")
        app.text_area.insert(f"1.0+{start_index}c", replace_text)

def replace_all(app, search_text, replace_text):
    # Handle special case for carriage return
    if replace_text == "\\n":
        replace_text = "\n"
        
    content = app.text_area.get("1.0", tk.END)
    new_content = content.replace(search_text, replace_text)
    app.text_area.delete("1.0", tk.END)
    app.text_area.insert(tk.END, new_content)

def highlight_text(app, search_text):
    # Determine if the function is running on the main app window or a new window
    text_area = app.text_area if hasattr(app, 'text_area') else app.master.text_area

    # Remove previous highlights
    text_area.tag_remove('highlight', '1.0', tk.END)
    
    if search_text:
        start_pos = '1.0'
        while True:
            start_pos = text_area.search(search_text, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            text_area.tag_add('highlight', start_pos, end_pos)
            text_area.tag_config('highlight', background='yellow')
            start_pos = end_pos

def delete_word(event):
    pos = event.widget.index(tk.INSERT)
    while pos != '1.0': 
        char = event.widget.get(pos + '-1c')
        if char.isspace() or char in ',.;:!?()[]{}\'"':
            break
        pos = event.widget.index(pos + '-1c')
    event.widget.delete(pos, tk.INSERT)

def adjust_font_size(app, increment):
    new_size = app.text_font.cget("size") + increment
    if new_size > 0: 
        app.text_font.configure(size=new_size)

def bind_shortcuts(app):
    if platform.system() == 'Darwin':  # Mac OS
        app.master.bind("<Command-n>", lambda event: new_window(app))
        app.master.bind("<Command-o>", lambda event: open_file(app))
        app.master.bind("<Command-s>", lambda event: save_file(app))
        app.master.bind("<Command-Shift-s>", lambda event: save_as_file(app))
        app.master.bind("<Command-f>", lambda event: find_text(app))
        app.master.bind("<Command-h>", lambda event: find_text(app, open_replace=True))
        app.master.bind("<Command-BackSpace>", delete_word)
        app.master.bind("<Command-=>", lambda event: adjust_font_size(app, 1)) 
        app.master.bind("<Command-minus>", lambda event: adjust_font_size(app, -1)) 

    else:  # Windows/Linux
        app.master.bind("<Control-n>", lambda event: new_window(app))
        app.master.bind("<Control-o>", lambda event: open_file(app))
        app.master.bind("<Control-s>", lambda event: save_file(app))
        app.master.bind("<Control-Shift-s>", lambda event: save_as_file(app))
        app.master.bind("<Control-f>", lambda event: find_text(app))
        app.master.bind("<Control-h>", lambda event: find_text(app, open_replace=True))
        app.master.bind("<Control-BackSpace>", delete_word)
        app.master.bind("<Control-=>", lambda event: adjust_font_size(app, 1)) 
        app.master.bind("<Control-minus>", lambda event: adjust_font_size(app, -1)) 

        app.master.bind("<Key>", lambda event: mark_as_modified(event, app))