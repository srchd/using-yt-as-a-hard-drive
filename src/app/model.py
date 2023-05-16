from datatypes.observable import Observable
from datatypes.yt_video import YouTubeVideo
from download.download_ytdlp import download_video_with_yt_dlp
from youtube.youtube_client import YoutubeClient


class Model:
    __youtube_client = YoutubeClient()

    def __init__(self) -> None:
        self.download_url = Observable('')
        self.download_video_success = Observable(0)
        self.upload_selected_filename = Observable('No File Selected!')
        self.upload_selected_filepath = Observable('')
        self.videos_on_yt = Observable(list())
        self.is_video_uploaded = Observable(False)

        """
        TESTING
        """
        self.videos = []

        return

    # TODO remove maybe (?)
    def download_video(self) -> None:
        # download_video_parallel(self.download_url.get(), 'video.mp4')
        # download_thread = os.popen('conda activate ythd && python src/download/example_urllib.py \"{0}\"'.format(self.download_url.get()))
        # download_thread.close()
        try:
            download_video_with_yt_dlp(self.download_url.get())
            self.download_video_success.set(self.download_video_success.get() + 1)
        except Exception as e:
            print("Oh no! Something went wrong!\n{}".format(e))

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
    
    def list_videos(self):
        videos = self.__youtube_client.list_videos(list_deleted=False, list_only_ythd=True)
        # videos = self.videos
        yt_videos : list
        if videos:
            yt_videos = [YouTubeVideo(video) for video in videos]
        else:
            yt_videos = self.videos_on_yt.get()

        self.videos_on_yt.set(yt_videos)

        return
    def upload_video(self):
        self.is_video_uploaded.set(True)
        self.videos.append(self.get_selected_upload_filename())
        # self.__youtube_client.upload_video(self.upload_selected_filepath.get(), "Some title", "Some description")
        # self.is_video_uploaded.set(True)

        return
