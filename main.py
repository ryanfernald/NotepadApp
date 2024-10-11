# main.py

import tkinter as tk
from moduals.app import NotepadApp

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop() 