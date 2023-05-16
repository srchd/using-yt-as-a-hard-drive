from model import Model
from view import View
from tkinter import filedialog
from tkinter import END, TOP

class Controller:
    def __init__(self, root) -> None:
        self.model = Model()
        self.view = View(root)
        """
        YouTube Client stuff from here
        """
        self.model.upload_selected_filepath.add_callback_function(self.set_upload_file_callback)
        self.model.videos_on_yt.add_callback_function(self.update_videos_listbox_callback)
        self.model.is_video_uploaded.add_callback_function(self.video_uploaded_callback)
        
        # File selector Frame
        self.view.file_selector_frame.pack(side=TOP)
        self.view.browse_file_button.config(command=self.on_browse_files)

        # Upload file Frame
        self.view.upload_video_frame.pack()
        self.view.upload_file_button.config(command=self.on_upload_video, state='disabled')

        # Videos Listbox Frame
        self.view.videos_listbox_frame.pack()
        self.model.list_videos()

        # Feedback Frame
        self.view.video_upload_download_feedback_frame.pack(fill='both')

        return
    
    def on_browse_files(self) -> None:
        filepath = filedialog.askopenfilename(initialdir='./', title='Select a file', filetypes=(('MP4 Video Formats', '*.mp4*'),
                                                                                                ('all_files','*.*')))

        self.model.reset_is_video_uploaded()
        self.model.set_selected_upload_file(filepath)
        return
    
    def on_upload_video(self) -> None:
        self.model.upload_video()
        self.model.list_videos()

        return

    def set_upload_file_callback(self, data) -> None:
        self.view.selecting_file_entry.delete(0, END)
        if data != '':
            self.view.selecting_file_entry.insert(0, data)
            self.view.upload_file_button.config(state='normal')
        else:
            self.view.upload_file_button.config(state='disabled')

        return
    
    def video_uploaded_callback(self, data) -> None:
        new_text = "Upload "
        if data:
            new_text += 'SUCCESSFUL'
        else:
            new_text += 'FAILED'

        self.view.video_upload_download_feedback_label.config(text=new_text)

        return
    
    def update_videos_listbox_callback(self, data) -> None:
        self.view.videos_listbox.delete(0, END)
        for video in data:
            # print(video)
            self.view.videos_listbox.insert(END, video.title)
