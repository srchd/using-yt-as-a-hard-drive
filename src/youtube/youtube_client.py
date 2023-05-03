import random
import time
import logging
from typing import Union
import traceback

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

from .youtube_client_parameters import ApiParameters
from .youtube_client_parameters import YTHDSettings
from .youtube_client_parameters import Credentials
from .youtube_client_parameters import Path as Path


class YoutubeClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

        self.client = self.get_build()

    @staticmethod
    def __test_client(client):
        request = client.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        request.execute()

    def get_build(self):
        client = None
        retry = True

        while retry:
            try:
                credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(Credentials.GENERATED_CLIENT_SECRETS_FILE)
                client = build(ApiParameters.API_SERVICE_NAME, ApiParameters.API_VERSION, credentials=credentials)
                YoutubeClient.__test_client(client)
            except Exception:
                self.logger.info("Creating credentials")
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(Credentials.ORIGINAL_CLIENT_SECRETS_FILE, ApiParameters.SCOPES)
                credentials = flow.run_local_server(port=8090)
                with open(Credentials.GENERATED_CLIENT_SECRETS_FILE, "w") as f:
                    f.write(credentials.to_json())
            finally:
                retry = False

        if client is None:
            self.logger.warning("Couldn't build client")

        return client

    def upload_video(self, file_path, title="", description=YTHDSettings.YTHD_MARK, category="22", privacy_status="unlisted", tags=None, path: Union[Path, None] = None):
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

        request = self.client.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )

        self.__upload_video(request)

    def list_videos(self, list_deleted=False, list_only_ythd=True) -> list:
        request = self.client.search().list(
            part="snippet",
            forMine=True,
            maxResults=50,
            type="video"
        )
        response = request.execute()

        if not response:
            return []

        response_dict = response["items"]
        response_dict = [r["id"] | r["snippet"] for r in response_dict]
        response_dict = [{k: v for k, v in r.items() if k in ['videoId', 'publishedAt', 'publishTime', 'title', 'description']} for r in response_dict]
        response_dict = [r | {"url": f"https://www.youtube.com/watch?v={r['videoId']}"} for r in response_dict]
        response_dict = [r | {"path": Path.description_to_path(r["description"])} for r in response_dict]
        response_dict = [r for r in response_dict if (list_deleted or YTHDSettings.DELETED_MARK not in r["description"]) and (not list_only_ythd or YTHDSettings.YTHD_MARK in r["description"])]

        return response_dict

    def mark_video_deleted(self, video_id) -> bool:
        self.logger.debug(f"Marking video {video_id} deleted")
        return self.__append_to_description(video_id, YTHDSettings.DELETED_MARK)

    def __upload_video(self, request):
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

    def __get_video_resource(self, video_id) -> dict:
        request = self.client.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response:
            return {}

        return response

    def __update(self, video_id, params) -> bool:
        body = {
            "id": video_id,
            "kind": "youtube#video"
        }
        body = body | params
        request = self.client.videos().update(
            body=body,
            part="snippet"
        )
        response = request.execute()
        self.logger.debug(f"Updated video resource: {response}")

        if not response:
            return False

        return True

    def __update_description(self, video_id, description, title, category_id) -> bool:
        params = {
            "snippet": {
                "title": title,
                "categoryId": category_id,
                "description": description
            }
        }
        self.logger.debug(f"Updating description for video {video_id}")
        return self.__update(video_id, params)

    def __append_to_description(self, video_id, text) -> bool:
        video_resource = self.__get_video_resource(video_id)["items"][0]
        title = video_resource["snippet"]["title"]
        category_id = video_resource["snippet"]["categoryId"]
        description = video_resource["snippet"]["description"]
        description += "\n" + text
        self.logger.debug(f"Appending to description for video {video_id}")
        return self.__update_description(video_id, description, title, category_id)
