import tkinter as tk


class UploadWindow(tk.Toplevel):
    def __init__(self, parent: tk.Toplevel) -> None:
        tk.Toplevel.__init__(self, parent)
        self.title('Uploading a Video')

        self.width = "467"
        self.height = "230"

        self.geometry(self.get_window_size())

        self.test_label = tk.Label(self, text='TEST')
        self.test_label.pack()

        self.test_button = tk.Button(self, text='Get Window Dimensions', command=self.__print_window_size)
        self.test_button.pack()
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)
    
    def __print_window_size(self) -> None:
        print(f'{self.winfo_width()} x {self.winfo_height()}')