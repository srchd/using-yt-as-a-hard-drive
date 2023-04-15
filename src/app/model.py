from observable import Observable

class Model:
    def __init__(self) -> None:
        self.download_url = Observable('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    def set_download_url(self, url : str) -> None:
        self.download_url.set(url)

    def get_download_url(self) -> str:
        return self.download_url.get()