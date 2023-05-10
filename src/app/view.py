import tkinter as tk

class View(tk.Toplevel):
    def __init__(self, master) -> None:
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.row_count = 0
        
        self.width = "720"
        self.height = "720"
        self.geometry(self.get_window_size())

        """
        YouTube Client stuff from here
        """
        self.selecting_file_label = tk.Label(self)
        self.selecting_file_entry = tk.Entry(self)
        self.browse_file_button = tk.Button(self, text='Browse Files')
        self.upload_file_button = tk.Button(self, text='Upload video')
        self.videos_listbox = tk.Listbox(self)
        
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)

    def grid_widgets(self, widgets : list[tk.Widget]) -> None:
        for i, widget in enumerate(widgets):
            widget.grid(row=self.row_count, column=i, padx=(50, 50))
        self.row_count += 1

        return
