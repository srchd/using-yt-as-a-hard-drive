import tkinter as tk


class UploadWindow(tk.Toplevel):
    def __init__(self, parent: tk.Toplevel, file_path: str) -> None:
        tk.Toplevel.__init__(self, parent)
        self.title('Uploading a Video')

        self.width = "467"
        self.height = "230"

        self.geometry(self.get_window_size())

        self.title_var = tk.StringVar(parent, value='Some title')
        self.description_var = tk.StringVar(parent, value='Some description')
        self.path_var = tk.StringVar(parent, value=file_path)

        self.title_label = tk.Label(self, text='Title')
        self.description_label = tk.Label(self, text='Description')
        self.file_path_label = tk.Label(self, text='File path saved on video')

        self.title_entry = tk.Entry(self, textvariable=self.title_var)
        self.description_entry = tk.Entry(self, textvariable=self.description_var)
        self.path_entry = tk.Entry(self, textvariable=self.path_var)

        self.title_label.pack()
        self.title_entry.pack()

        self.description_label.pack()
        self.description_entry.pack()

        self.file_path_label.pack()
        self.path_entry.pack()

        self.submit_button = tk.Button(self, text='OK', command=self.destroy)
        self.submit_button.pack()
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)
