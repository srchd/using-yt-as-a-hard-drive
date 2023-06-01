import tkinter as tk
from subwindows.advanced_settings_window import AdvancedSettingsWindow
from utils.generic_functions import combine_funcs


class UploadWindow(tk.Toplevel):
    def __init__(self, parent: tk.Toplevel, file_path: str) -> None:
        tk.Toplevel.__init__(self, parent)
        self.title('Uploading a Video')

        self.width = "467"
        self.height = "230"

        self.patch_height_var = tk.IntVar(parent, value=8)
        self.patch_width_var = tk.IntVar(parent, value=8)
        self.repetitions_var = tk.IntVar(parent, value=10)

        self.advanced_settings_window_submitted = False

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

        self.submit_button = tk.Button(self, text='OK')
        self.submit_button.pack()

        self.advanced_settings_button = tk.Button(self, text='Advanced Settings...', command=self.on_advanced_settings)
        self.advanced_settings_button.pack()
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)
    
    def on_advanced_settings(self) -> None:
        def on_advanced_settings_window_submit() -> None:
            self.advanced_settings_window_submitted = True

        self.advanced_settings_window_submitted = False
        settings_window = AdvancedSettingsWindow(self)
        settings_window.grab_set()

        settings_window.submit_button.config(command=combine_funcs(on_advanced_settings_window_submit, settings_window.close_window))

        self.wait_window(settings_window)

        try:
            self.patch_height_var.set(int(settings_window.patch_height_var.get()))
            self.patch_width_var.set(int(settings_window.patch_width_var.get()))
            self.repetitions_var.set(int(settings_window.repetitions_var.get()))
        except:
            self.patch_height_var.set(8)
            self.patch_width_var.set(8)
            self.repetitions_var.set(10)

        return
    
    def close_window(self) -> None:
        self.destroy()

        return
