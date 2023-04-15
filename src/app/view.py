import tkinter as tk

class View(tk.Toplevel):
    def __init__(self, master) -> None:
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.row_count = 0
        
        self.width = "720"
        self.height = "720"
        self.geometry(self.get_window_size())

        self.url_entry = tk.Entry(self, width=64)
        self.submit_url_button = tk.Button(self, text='Submit URL', width=8)

        self.current_url_label = tk.Label(self, text='Current URL: ')
        self.download_url_label = tk.Label(self)
        
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)

    def grid_widgets(self, widgets : list[tk.Widget]) -> None:
        for i, widget in enumerate(widgets):
            widget.grid(row=self.row_count, column=i)
        self.row_count += 1

        return
