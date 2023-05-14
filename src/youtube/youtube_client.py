import random
import time
import logging
from typing import Union, Callable
import traceback
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from .youtube_client_parameters import ApiParameters, YTHDSettings, Path
from .credentials import Credentials


class YoutubeClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(YTHDSettings.LOG_FORMAT)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

        self.credentials = Credentials()

        self.logger.info("Created YoutubeClient")

    @staticmethod
    def __test_client(client):
        request = client.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        request.execute()

    @staticmethod
    def __quota_exceeded(ex: HttpError):
        return ex.status_code == 403 and ex.error_details and "domain" in ex.error_details[0] and ex.error_details[0]["domain"] == "youtube.quota" and "reason" in ex.error_details[0] and ex.error_details[0]["reason"] == "quotaExceeded"

    def get_build(self):
        credentials = self.credentials.get_generated_file()
        client = build(ApiParameters.API_SERVICE_NAME, ApiParameters.API_VERSION, credentials=credentials)
        YoutubeClient.__test_client(client)
        return client

    def __execute_request(self, method: Callable,  *args, **kwargs):
        self.logger.debug(f"Executing method <{method.__name__}> with parameters {args}")
        retries = ApiParameters.MAX_RETRIES
        val = None
        while retries > 0:
            try:
                val = method(*args, **kwargs)
            except HttpError as ex:
                if self.__quota_exceeded(ex):
                    self.logger.warning(f"Quota exceeded, retries left: {retries}")
                    self.credentials.switch_credentials()
                    retries -= 1
                else:
                    self.logger.error(f"Unknown HttpError during executing {method}")
                    raise ex
            else:
                retries = 0

        return val

    def __list_videos_request(self, list_deleted=False, list_only_ythd=True) -> list:
        client = self.get_build()
        request = client.search().list(
            part="snippet",
            forMine=True,
            maxResults=50,
            type="video"
        )
        response = request.execute()

        if not response:
            self.logger.warning("Couldn't list videos")
            return []

        response_dict = response["items"]
        response_dict = [r["id"] | r["snippet"] for r in response_dict]
        response_dict = [{k: v for k, v in r.items() if k in ['videoId', 'publishedAt', 'publishTime', 'title', 'description']} for r in response_dict]
        response_dict = [r | {"url": f"https://www.youtube.com/watch?v={r['videoId']}"} for r in response_dict]
        response_dict = [r | {"path": Path.description_to_path(r["description"])} for r in response_dict]
        response_dict = [r for r in response_dict if (list_deleted or YTHDSettings.DELETED_MARK not in r["description"]) and (not list_only_ythd or YTHDSettings.YTHD_MARK in r["description"])]

        return response_dict

    def list_videos(self, list_deleted=False, list_only_ythd=True) -> list:
        return self.__execute_request(self.__list_videos_request, list_deleted, list_only_ythd)

    def __get_video_resource_request(self, video_id) -> dict:
        self.logger.info(f"Getting resource for video {video_id}")

        client = self.get_build()
        request = client.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response:
            self.logger.warning(f"Couldn't get resource for video {video_id}")
            return {}

        return response

    def __get_video_resource(self, video_id) -> dict:
        return self.__execute_request(self.__get_video_resource_request, video_id)

    def __update_video_request(self, video_id, params) -> bool:
        self.logger.info(f"Updating video {video_id}")
        body = {
            "id": video_id,
            "kind": "youtube#video"
        }
        body = body | params
        client = self.get_build()
        request = client.videos().update(
            body=body,
            part="snippet"
        )
        return request.execute()

    def __update_video(self, video_id, params) -> bool:
        return self.__execute_request(self.__update_video_request, video_id, params)

    def __update_description(self, video_id, description, title, category_id) -> bool:
        self.logger.info(f"Updating description of video {video_id}")
        params = {
            "snippet": {
                "title": title,
                "categoryId": category_id,
                "description": description
            }
        }
        self.logger.debug(f"Updating description for video {video_id}")
        return self.__update_video(video_id, params)

    def __append_to_description(self, video_id, text) -> bool:
        self.logger.info(f"Appending to description of video {video_id}")
        video_resource = self.__get_video_resource(video_id)["items"][0]
        title = video_resource["snippet"]["title"]
        category_id = video_resource["snippet"]["categoryId"]
        description = video_resource["snippet"]["description"]
        description += "\n" + text
        self.logger.debug(f"Appending to description for video {video_id}")
        return self.__update_description(video_id, description, title, category_id)

    def mark_video_deleted(self, video_id) -> bool:
        self.logger.info(f"Marking video {video_id} deleted")
        return self.__append_to_description(video_id, YTHDSettings.DELETED_MARK)

    def __upload_video_request(self, file_path, body):
        client = self.get_build()
        request = client.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )

        response = None
        error = None
        retry = 0
        while response is None:
            try:
                self.logger.info("Uploading file...")
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        self.logger.info(f"Video id '{response['id']}' was successfully uploaded.")
                    else:
                        self.logger.error(f"The upload failed with an unexpected response: {response}")
                        return
            except HttpError as ex:
                if ex.status_code in ApiParameters.RETRIABLE_STATUS_CODES:
                    error = ex
                    self.logger.warning(f"A retriable HTTP error {ex.status_code} occurred:")
                    self.logger.warning(traceback.format_exc())
                else:
                    raise ex
            except ApiParameters.RETRIABLE_EXCEPTIONS as ex:
                error = ex
                self.logger.warning(f"A retriable error occurred: {ex}")

            if error is not None:
                self.logger.error(error)
                retry += 1
                if retry > ApiParameters.MAX_RETRIES:
                    self.logger.error("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                self.logger.warning(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)

    def upload_video(self, file_path, title: str = "", description: str = "", category: str = "22", privacy_status: str = "unlisted", tags: list = None, path: Union[Path, None] = None):
        self.logger.info(f"Uploading video {title}")

        if tags is None:
            tags = []

        if path is None:
            path = Path("", None)

        if YTHDSettings.YTHD_MARK not in description:
            description += "\n" + YTHDSettings.YTHD_MARK
        description += "\n" + YTHDSettings.PATH_PREFIX + str(path)

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        self.__execute_request(self.__upload_video_request, file_path, body)
