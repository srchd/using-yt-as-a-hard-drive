import tkinter as tk


class AdvancedSettingsWindow(tk.Toplevel):
    def __init__(self, parent: tk.Toplevel) -> None:
        tk.Toplevel.__init__(self, parent)
        self.title('Advanced Settings')

        self.width = "467"
        self.height = "230"
        self.geometry(self.get_window_size())

        self.warning_label = tk.Label(self, text='WARNING!!! Only change these if you know what are you doing!! c:')
        self.warning_label.pack()

        self.patch_height_var = tk.StringVar(parent, value='8')  # StringVar, later we change it to int, to avoid getting exceptions when a non-int type is submitted
        self.patch_width_var = tk.StringVar(parent, value='8')  # StringVar, later we change it to int, to avoid getting exceptions when a non-int type is submitted
        self.repetitions_var = tk.StringVar(parent, value='10')  # StringVar, later we change it to int, to avoid getting exceptions when a non-int type is submitted

        self.patch_height_label = tk.Label(self, text='Patch Height')
        self.patch_height_label.pack()
        self.patch_height_entry = tk.Entry(self, textvariable=self.patch_height_var)
        self.patch_height_entry.pack()

        self.patch_width_label = tk.Label(self, text='Patch Width')
        self.patch_width_label.pack()
        self.patch_width_entry = tk.Entry(self, textvariable=self.patch_width_var)
        self.patch_width_entry.pack()

        self.repetitions_label = tk.Label(self, text='Repetitions')
        self.repetitions_label.pack()
        self.repetitions_entry = tk.Entry(self, textvariable=self.repetitions_var)
        self.repetitions_entry.pack()

        self.submit_button = tk.Button(self, text='OK')
        self.submit_button.pack()

        return

    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)
    
    def close_window(self) -> None:
        self.destroy()

        return
