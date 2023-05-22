from datatypes.observable import Observable
from datatypes.yt_video import YouTubeVideo
from download.download_ytdlp import download_video_with_yt_dlp
from youtube.youtube_client import YoutubeClient
from youtube import Path


class Model:
    # Set this variable to `None` when testing, so won't exceed the quota.
    __youtube_client = YoutubeClient()

    def __init__(self) -> None:
        self.download_video_success = Observable(0)
        self.upload_selected_filename = Observable('No File Selected!')
        self.upload_selected_filepath = Observable('')
        self.videos_on_yt = Observable(list())
        self.is_video_uploaded = Observable(False)
        self.is_video_downloaded = Observable(False)
        self.current_path = Observable("/")

        """
        TESTING
        """
        # self.videos = []

        return

    def get_current_path(self):
        return self.current_path.get()

    def set_current_path(self, path: str):
        if not path:
            path = "/"
        self.current_path.set(path)

    def download_video(self, video_idx : int) -> None:
        try:
            video_to_download = self.videos_on_yt.get()[video_idx]
            video_to_download_url = video_to_download.url
            # ======================================================
            # The line below only for testing, so won't exceed the quota
            # video_to_download_url = 'https://www.youtube.com/watch?v=eyQTJnMw5B0'
            # ======================================================
            download_video_with_yt_dlp(video_to_download_url)

            self.is_video_downloaded.set(True)
        except:
            self.is_video_downloaded.set(False)

        return
    
    def get_selected_upload_filename(self):
        return self.upload_selected_filename.get()
    
    def get_selected_upload_filepath(self):
        return self.upload_selected_filepath.get()
    
    def set_selected_upload_file(self, filepath):
        filename = filepath.split('/')[-1]
        self.upload_selected_filename.set(filename)
        self.upload_selected_filepath.set(filepath)

        return
    
    def reset_is_video_uploaded(self):
        self.is_video_uploaded.set_without_callback(False)

    def reset_is_video_downloaded(self):
        self.is_video_downloaded.set_without_callback(False)
    
    def list_videos(self):
        videos = self.__youtube_client.list_videos(list_deleted=False, list_only_ythd=True)
        # ======================================================
        # The line below only for testing, so won't exceed the quota
        # videos = self.videos
        # ======================================================
        yt_videos : list
        if videos:
            yt_videos = [YouTubeVideo(video) for video in videos]
        else:
            yt_videos = self.videos_on_yt.get()

        self.videos_on_yt.set(yt_videos)

        return

    def upload_video(self, title, description, path):

        # ======================================================
        # The lines below are only for testing, so won't exceed the quota
        # self.is_video_uploaded.set(True)
        # self.videos.append({
        #      'videoId': 'null',
        #      'publishedAt': 'JUST NOW',
        #      'title': title,
        #      'description': description,
        #      'publishTime': 'WHEN i SAID',
        #      'url': 'https://google.com',
        #      'path': self.get_selected_upload_filepath()
        # })
        # ======================================================
        self.__youtube_client.upload_video(self.upload_selected_filepath.get(), title=title, description=description, path=Path(path))
        self.is_video_uploaded.set(True)

        return
