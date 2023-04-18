from .model import Model
from .view import View

class Controller:
    def __init__(self, root) -> None:
        self.model = Model()
        self.model.download_url.add_callback_function(self.set_download_url_callback)
        self.model.download_video_success.add_callback_function(self.set_success_label_callback)

        self.view = View(root)
        self.view.download_url_label.config(text=self.model.get_download_url())
        self.view.submit_url_button.config(command=self.on_set_download_url)

        self.view.grid_widgets([self.view.url_entry,
                                self.view.submit_url_button])

        self.view.grid_widgets([self.view.current_url_label,
                                self.view.download_url_label])

        self.view.download_video_button.config(command=self.on_download_video, state='disabled')
        self.view.grid_widgets([self.view.download_video_button,
                                self.view.download_video_success])

        return
    
    def on_set_download_url(self) -> None:
        self.model.set_download_url(self.view.url_entry.get())

        return
    
    def set_download_url_callback(self, data) -> None:
        new_state = 'normal'
        if data == '' or data == 'Not a valid URL!':
            new_state = 'disabled'
        self.view.download_video_button.config(state=new_state)

        self.view.download_url_label.config(text=data)
        self.view.download_video_success.config(text='')

        return
    
    def on_download_video(self) -> None:
        self.model.download_video()

        return
    
    def set_success_label_callback(self, _) -> None:
        self.view.download_video_success.config(text="Video Downloaded!")

        return
