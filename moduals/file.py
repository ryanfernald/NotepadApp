# moduals/file.py
from tkinter import filedialog, messagebox
import tkinter as tk

def mark_as_modified(event, app):
    if not app.is_modified:
        app.is_modified = True
        
        if "*" not in app.master.title():
            app.master.title(f"{app.master.title()} *")


def new_file(app):
    app.text_area.delete(1.0, tk.END)
    app.file_path = None
    app.is_modified = False
    app.master.title("Notepad - New File")

def open_file(app):
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        app.text_area.delete(1.0, tk.END)
        app.text_area.insert(tk.END, content)
        app.file_path = file_path
        app.is_modified = False
        app.master.title(f"Notepad - {file_path}")

def save_file(app):
    if app.file_path:
        write_to_file(app, app.file_path)
        app.is_modified = False
        app.master.title(f"Notepad - {app.file_path}")
    else:
        save_as_file(app)

def save_as_file(app):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        write_to_file(app, file_path)
        app.is_modified = False
        app.master.title(f"Notepad - {file_path}")

def write_to_file(app, file_path):
    try:
        with open(file_path, "w") as file:
            content = app.text_area.get(1.0, tk.END)
            file.write(content)
        app.file_path = file_path
        app.master.title(f"Notepad - {file_path}")  
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving file: {e}")

def toggle_topmost(self):
    is_topmost = self.topmost_var.get()
    self.master.attributes('-topmost', is_topmost)