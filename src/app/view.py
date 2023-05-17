import tkinter as tk

class View(tk.Toplevel):
    def __init__(self, master) -> None:
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title("Using YouTube as a Hard Drive #YTHD")
        
        self.width = "600"
        self.height = "400"
        self.geometry(self.get_window_size())

        """
        YouTube Client stuff from here
        """

        # File selector Frame
        self.file_selector_frame = tk.Frame(self)

        self.selecting_file_label = tk.Label(self.file_selector_frame, padx=20, text='Select a file:')
        self.selecting_file_entry = tk.Entry(self.file_selector_frame, width=50)
        self.browse_file_button = tk.Button(self.file_selector_frame, padx=20, text='Browse Files')

        self.selecting_file_label.pack(side=tk.LEFT)
        self.selecting_file_entry.pack(side=tk.LEFT)
        self.browse_file_button.pack(side=tk.RIGHT)

        # Upload video Frame
        self.upload_video_frame = tk.Frame(self, pady=20)

        self.upload_file_button = tk.Button(self.upload_video_frame, width=30, text='Upload video')

        self.upload_file_button.pack()

        # Videos Listbox Frame
        self.videos_listbox_frame = tk.Frame(self)

        self.videos_listbox = tk.Listbox(self.videos_listbox_frame, height=15, width=90)

        self.videos_listbox.pack()

        # Video upload/download feedback Frame
        self.video_upload_download_feedback_frame = tk.Frame(self)

        self.video_upload_download_feedback_label = tk.Label(self.video_upload_download_feedback_frame, padx=10)

        self.video_upload_download_feedback_label.pack(side='right')

        # Download video Frame
        self.download_video_frame = tk.Frame(self)

        self.download_video_button = tk.Button(self.download_video_frame, width=30, text='Download Video')

        self.download_video_button.pack()
        
        return
    
    def get_window_size(self) -> str:
        return "{0}x{1}".format(self.width, self.height)
