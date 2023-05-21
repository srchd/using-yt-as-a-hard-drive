from model import Model
from view import View
from subwindows.upload_window import UploadWindow
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
        self.model.is_video_uploaded.add_callback_function(self.file_uploaded_callback)
        self.model.is_video_downloaded.add_callback_function(self.video_downloaded_callback)
        
        # File selector Frame
        self.view.file_selector_frame.pack(side=TOP)
        self.view.browse_file_button.config(command=self.on_browse_files)

        # Upload file Frame
        self.view.upload_file_frame.pack()
        self.view.upload_file_button.config(command=self.on_upload_file, state='disabled')

        # Path frame
        self.view.path_frame.pack()
        self.view.current_path_entry.insert(0, self.model.get_current_path())
        self.view.current_path_entry.bind('<Return>', self.save_new_path)

        # Videos Listbox Frame
        self.view.videos_listbox_frame.pack()
        self.view.videos_listbox.bind('<<ListboxSelect>>', lambda _: self.on_listbox_select_change())
        self.model.list_videos()

        # Feedback Frame
        self.view.video_upload_download_feedback_frame.pack(fill='both')

        # Download Video Frame
        self.view.download_file_frame.pack()
        self.view.download_file_button.config(command=self.on_download_from_listbox, state='disabled')

        self.selected_video = None

        return
    
    def reset_feedback_label(self) -> None:
        self.model.reset_is_video_uploaded()
        self.model.reset_is_video_downloaded()
        self.view.video_upload_download_feedback_label.config(text='')

    def on_browse_files(self) -> None:
        filepath = filedialog.askopenfilename(initialdir='./', title='Select a file')

        self.reset_feedback_label()
        self.model.set_selected_upload_file(filepath)
        return
    
    def on_upload_video(self) -> None:
        file_path = self.model.upload_selected_filepath.get()
        if not file_path:
            file_path = ""
        upload_window = UploadWindow(self.view, file_path)
        upload_window.grab_set()  # Grabbing the UploadWindow, so user can't interact with the Main while this is open

        self.view.wait_window(upload_window)  # Waiting for the UploadWindow to be closed

        title = upload_window.title_var.get()
        description = upload_window.description_var.get()
        path = upload_window.path_var.get()

        self.model.upload_video(title, description, path)
        self.model.list_videos()

        return
    
    def on_download_from_listbox(self) -> None:
        if self.selected_video is not None:
            video_idx = int(self.selected_video.split(':')[0])
            self.model.download_video(video_idx)

    def on_listbox_select_change(self) -> None:
        try:
            self.selected_video = self.view.videos_listbox.get(self.view.videos_listbox.curselection())
            print(self.selected_video)
            self.view.download_file_button.config(state='normal')
            self.reset_feedback_label()
        except:
            print('No videos for you!')
            self.view.download_file_button.config(state='disabled')

    def set_upload_file_callback(self, data) -> None:
        self.view.selecting_file_entry.delete(0, END)
        if data != '':
            self.view.selecting_file_entry.insert(0, data)
            self.view.upload_file_button.config(state='normal')
        else:
            self.view.upload_file_button.config(state='disabled')

        return
    
    def file_uploaded_callback(self, data) -> None:
        new_text = "Upload "
        if data:
            new_text += 'SUCCESSFUL'
        else:
            new_text += 'FAILED'

        self.view.video_upload_download_feedback_label.config(text=new_text)
        self.model.reset_is_video_uploaded()

        return

    def save_new_path(self, data):
        print(data)
        new_path = self.view.current_path_entry.get()
        self.model.set_current_path(new_path)
        self.view.current_path_entry.delete(0, END)
        self.view.current_path_entry.insert(0, self.model.get_current_path())
        self.model.list_videos()

    def update_videos_listbox_callback(self, data) -> None:
        self.view.videos_listbox.delete(0, END)
        # Filter videos so that it will only show videos in current folder
        data = [d for d in data if d.path.startswith(self.model.get_current_path())]
        for idx, video in enumerate(data):
            # print(video)
            title = f'{idx}: {video.title} - {video.path}'
            self.view.videos_listbox.insert(END, title)

    def video_downloaded_callback(self, data) -> None:
        new_text = 'Download '
        if data:
            new_text += 'SUCCESSFUL'
        else:
            new_text += 'FAILED'

        self.view.video_upload_download_feedback_label.config(text=new_text)
        self.model.reset_is_video_downloaded()

        return
