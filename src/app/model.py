from .observable import Observable
from download.example_pytube import download_video_with_pytube
from download.utils import extract_video_id

import validators
import os
# from download.example_urllib import download_video, download_video_parallel

class Model:
    def __init__(self) -> None:
        self.download_url = Observable('')
        self.download_video_success = Observable(0)

        return

    def set_download_url(self, url : str) -> None:
        new_url = ''

        if self.validate_download_link(url):
            self.download_url.set(url)
        else:
            self.download_url.set('Not a valid URL!')

        return

    def get_download_url(self) -> str:
        return self.download_url.get()

    def download_video(self) -> None:
        # download_video_parallel(self.download_url.get(), 'video.mp4')
        # download_thread = os.popen('conda activate ythd && python src/download/example_urllib.py \"{0}\"'.format(self.download_url.get()))
        # download_thread.close()
        try:
            download_video_with_pytube(self.download_url.get())
            self.download_video_success.set(self.download_video_success.get() + 1)
        except Exception as e:
            print("Oh no! Something went wrong!\n{}".format(e))

        return
    
    def validate_download_link(self, _url) -> bool:
        return validators.url(_url)
