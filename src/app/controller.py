from .model import Model
from .view import View
from tkinter import filedialog
from tkinter import END

class Controller:
    def __init__(self, root) -> None:
        self.model = Model()
        self.view = View(root)
        """
        YouTube Client stuff from here
        """
        self.model.upload_selected_filename.add_callback_function(self.set_upload_file_callback)
        self.model.videos_on_yt.add_callback_function(self.update_videos_listbox)
        
        #TODO Consider using Entry instead of label
        self.view.selecting_file_label.config(text=self.model.get_selected_upload_filename())
        self.view.browse_file_button.config(command=self.on_browse_files)
        self.view.upload_file_button.config(command=self.on_upload_video, state='normal')
        # self.view.videos_listbox.config(state='disabled')
        # self.update_videos_listbox()
        self.model.list_videos()

        self.view.grid_widgets([self.view.selecting_file_label, self.view.browse_file_button])
        self.view.grid_widgets([self.view.upload_file_button])
        self.view.grid_widgets([self.view.videos_listbox])

        return
    
    def on_browse_files(self) -> None:
        filepath = filedialog.askopenfilename(initialdir='/', title='Select a file', filetypes=(('MP4 Video Formats', '*.mp4*'),
                                                                                                ('all_files','*.*')))

        self.model.set_selected_upload_file(filepath)
        return
    
    def on_upload_video(self) -> None:
        # self.model.upload_video()
        self.model.list_videos()
        # self.view.videos_listbox.insert(END, 'ASDASDASDASD')

        return

    def set_upload_file_callback(self, data) -> None:
        self.view.selecting_file_label.config(text='File selected: {0}'.format(data))
        self.view.upload_file_button.config(state='normal')

        return
    
    def update_videos_listbox(self, data) -> None:
        # self.view.videos_listbox.delete(0, END)
        for video in data:
            self.view.videos_listbox.insert(END, video)
