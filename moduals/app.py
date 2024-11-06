import tkinter as tk
from tkinter import font, Menu
from spellchecker import SpellChecker
from moduals.file import new_file, open_file, save_file, save_as_file, toggle_topmost, mark_as_modified
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
        self.text_font = font.Font(family="Bradley Hand", size=18, weight="bold")
        self.create_widgets()
        self.create_menu()
        bind_shortcuts(self)

        self.spell_checker = SpellChecker()
        self.check_spelling_job = None
        self.text_area.bind("<<Modified>>", self.schedule_spell_check)
        self.text_area.bind("<Command-r>", self.show_suggestions_menu)
        self.create_context_menu()

    def create_widgets(self):
        self.text_area = tk.Text(self.master, wrap='word', undo=True, bg="pale goldenrod", font=self.text_font)
        self.text_area.pack(fill='both', expand=True)
        self.text_area.focus_set()
        self.file_path = None
        self.text_area.tag_configure("misspelled", underline=True, foreground="red")

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

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

        color_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Notepad Yellow", command=lambda: change_bg_color(self, "pale goldenrod"))
        color_menu.add_command(label="Thistle", command=lambda: change_bg_color(self, "thistle2"))
        color_menu.add_command(label="Pale Turquoise", command=lambda: change_bg_color(self, "pale turquoise"))
        color_menu.add_command(label="Dark Sea Green", command=lambda: change_bg_color(self, "DarkSeaGreen1"))
        color_menu.add_command(label="Misty Rose", command=lambda: change_bg_color(self, "misty rose"))
        color_menu.add_command(label="Lavender", command=lambda: change_bg_color(self, "lavender"))
        color_menu.add_command(label="Choose...", command=lambda: choose_custom_color(self))

    def schedule_spell_check(self, event=None):
        if self.check_spelling_job is not None:
            self.text_area.after_cancel(self.check_spelling_job)
        self.check_spelling_job = self.text_area.after(1000, self.check_spelling)

    def check_spelling(self):
        self.text_area.tag_remove("misspelled", "1.0", tk.END)
        words = self.text_area.get("1.0", tk.END).split()
        start_idx = "1.0"

        for word in words:
            if word not in self.spell_checker:
                start_idx = self.text_area.search(word, start_idx, stopindex=tk.END)
                if start_idx:
                    end_idx = f"{start_idx}+{len(word)}c"
                    self.text_area.tag_add("misspelled", start_idx, end_idx)
                    start_idx = end_idx

        self.text_area.edit_modified(False)

    def create_context_menu(self):
        self.context_menu = Menu(self.master, tearoff=0)

    def show_suggestions_menu(self, event=None):
        """Show replacement suggestions for the highlighted misspelled word."""
        try:
            self.context_menu.delete(0, tk.END)

            # Get the highlighted word and capture the start and end indices as strings
            if self.text_area.tag_ranges("sel"):
                start_idx = self.text_area.index(tk.SEL_FIRST)
                end_idx = self.text_area.index(tk.SEL_LAST)
                word = self.text_area.get(start_idx, end_idx)
            else:
                return  # Exit if no text is highlighted

            if word in self.spell_checker:
                return  # Exit if the word is spelled correctly

            # Generate and add spelling suggestions to the context menu
            suggestions = self.spell_checker.candidates(word)
            for suggestion in suggestions:
                # Pass start_idx and end_idx directly as strings to avoid selection issues
                self.context_menu.add_command(
                    label=suggestion,
                    command=lambda s=suggestion: self.replace_word(start_idx, end_idx, s)
                )

            # Show the context menu at the current cursor position
            x, y = self.master.winfo_pointerx(), self.master.winfo_pointery()
            self.context_menu.tk_popup(x, y)

        except Exception as e:
            print("Error showing suggestions menu:", e)


    def replace_word(self, start, end, new_word):
        """Replace the highlighted word with the selected suggestion."""
        self.text_area.delete(start, end)
        self.text_area.insert(start, new_word)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()