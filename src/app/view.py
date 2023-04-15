import tkinter as tk

class View(tk.Toplevel):
    def __init__(self, master) -> None:
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        
        self.width = "720"
        self.height = "720"
        self.geometry(self.get_window_size())
        
        self.test_label = tk.Label(self, text="TEST")
        self.test_label.pack()
        
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)

