# moduals/app.py
import tkinter as tk
from moduals.file import new_file, open_file, save_file, save_as_file, toggle_topmost
from moduals.color import change_bg_color, choose_custom_color
from moduals.binds import bind_shortcuts

class NotepadApp:
    def __init__(self, master):
        self.master = master
        master.title("Notepad")
        master.geometry("600x400")
        master.configure(bg="pale goldenrod")
        self.topmost_var = tk.BooleanVar(value=True)
        self.master.attributes('-topmost', self.topmost_var.get())
        self.create_widgets()
        self.create_menu()
        bind_shortcuts(self) 

    def create_widgets(self):
        # Create the text widget for writing
        self.text_area = tk.Text(self.master, wrap='word', undo=True, bg="pale goldenrod", font=("Rosewood Std Regular", 12))
        self.text_area.pack(fill='both', expand=True)
        self.file_path = None  # To store current file path

    def create_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: new_file(self))
        file_menu.add_command(label="Open", command=lambda: open_file(self))
        file_menu.add_command(label="Save", command=lambda: save_file(self))
        file_menu.add_command(label="Save As", command=lambda: save_as_file(self))
        file_menu.add_checkbutton(label=" Float", onvalue=True, offvalue=False,
                          variable=self.topmost_var,
                          command=lambda: toggle_topmost(self))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Color menu
        color_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Notepad Yellow", command=lambda: change_bg_color(self, "pale goldenrod"))
        color_menu.add_command(label="Thistle", command=lambda: change_bg_color(self, "thistle2"))
        color_menu.add_command(label="Pale Turquoise", command=lambda: change_bg_color(self, "pale turquoise"))
        color_menu.add_command(label="Dark Sea Green", command=lambda: change_bg_color(self, "DarkSeaGreen1"))
        color_menu.add_command(label="Misty Rose", command=lambda: change_bg_color(self, "misty rose"))
        color_menu.add_command(label="Lavender", command=lambda: change_bg_color(self, "lavender"))
        color_menu.add_command(label="Choose...", command=lambda: choose_custom_color(self))

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
