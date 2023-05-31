from datatypes.observable import Observable
from datatypes.yt_video import YouTubeVideo
from download.download_ytdlp import download_video_with_yt_dlp
from youtube.youtube_client import YoutubeClient
from youtube import Path
from logger.logger import log, logger

import os
import json
import shutil


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

    @log
    def download_video(self, video_idx : int) -> None:
        logger.info('Downloading video')
        self.is_video_downloaded.set(False)

        video_to_download = self.videos_on_yt.get()[video_idx]

        json_string = self.extract_json_string_from_description(video_to_download.description).replace("'", '"')

        video_to_download_url = video_to_download.url
        # ======================================================
        # The line below only for testing, so won't exceed the quota
        # video_to_download_url = 'https://www.youtube.com/watch?v=eyQTJnMw5B0'
        # ======================================================
        if not os.path.isdir('./files/'):
            os.mkdir('./files')

        download_video_with_yt_dlp(video_to_download_url)
        shutil.move(f'./{video_to_download.title}.mp4', f'./files/{video_to_download.title}.mp4')

        filename = f'./files/{video_to_download.title}.mp4'

        self.decode_video_to_file(filename, json.loads(json_string), video_to_download.path)
        shutil.rmtree('./files')

        self.is_video_downloaded.set(True)
        logger.info('Video Downloaded')

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
    
    @log
    def list_videos(self):
        logger.info('Listing videos')
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

        logger.info('Videos Listed')

        return

    @log
    def upload_video(self, title, description, path):
        logger.info('Uploading video')

        self.is_video_uploaded.set(False)

        __description = description.replace('||', '')

        truncated_filename = self.get_selected_upload_filename().split('.')[0]

        self.encode_file_to_video(self.get_selected_upload_filepath(), self.get_selected_upload_filename())

        with open(f'./files/{truncated_filename}.json', 'r') as f:
            data = json.load(f)

        __description += '\n||' + str(data) + '||'

        # ======================================================
        # The lines below are only for testing, so won't exceed the quota
        # self.videos.append({
        #     'videoId': 'null',
        #     'publishedAt': 'JUST NOW',
        #     'title': title,
        #     'description': __description,
        #     'publishTime': 'WHEN i SAID',
        #     'url': 'https://google.com',
        #     'path': Path(self.get_selected_upload_filepath())
        # })
        # ======================================================
        self.__youtube_client.upload_video(f'./files/{truncated_filename}.mp4', title=title, description=__description, path=Path(path))

        self.is_video_uploaded.set(True)

        logger.info('Video Uploaded')

        shutil.rmtree('./files')

        return

    @log
    def encode_file_to_video(self, filepath, filename) -> None:
        truncated_filename = filename.split('.')[0]

        if not os.path.isdir('./files/'):
            os.mkdir('./files')

        os.system('conda activate ythd')
        os.system(f'call python ./src/processing/encode.py -f {filepath} -o ./files/{truncated_filename}.mp4 -v ./src/examples/rick.mp4 --temp_path tmp --settings_file ./files/{truncated_filename}.json --repetitions 10 --patch_height 8 --patch_width 8')

        return

    @log
    def extract_json_string_from_description(self, desc : str) -> str:
        return desc.split('||')[1]
    
    @log
    def decode_video_to_file(self, filename, arg_dict : dict, path) -> None:
        patch_height = arg_dict['patch_height']
        patch_width = arg_dict['patch_width']
        repetitions = arg_dict['rep']

        os.system('conda activate ythd')
        os.system(f'call python ./src/processing/decode.py -v {filename} -o {path[1:]} --tail_size 704 --patch_height {patch_height} --patch_width {patch_width} --repetitions {repetitions}')

        return
