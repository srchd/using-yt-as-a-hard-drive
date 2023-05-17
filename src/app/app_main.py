import tkinter as tk
from controller import Controller

def run() -> None:
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()

    return
