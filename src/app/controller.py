from model import Model
from view import View

class Controller:
    def __init__(self, root) -> None:
        self.model = Model()
        self.model.download_url.add_callback_function(self.set_download_url_callback)

        self.view = View(root)
        self.view.download_url_label.config(text=self.model.get_download_url())
        self.view.submit_url_button.config(command=self.set_download_url)
        self.view.grid_widgets([self.view.url_entry,
                                self.view.submit_url_button])
        self.view.grid_widgets([self.view.current_url_label,
                                self.view.download_url_label])

        return
    
    def set_download_url(self) -> None:
        self.model.set_download_url(self.view.url_entry.get())

        return
    
    def set_download_url_callback(self, url) -> None:
        self.view.download_url_label.config(text=url)

        return