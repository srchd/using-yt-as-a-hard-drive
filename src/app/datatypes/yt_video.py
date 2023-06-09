

class YouTubeVideo:
    def __init__(self, response_dict : dict) -> None:
        self.videoId = response_dict['videoId']
        self.publishedAt = response_dict['publishedAt']
        self.title = response_dict['title']
        self.description = response_dict['description']
        self.publishTime = response_dict['publishTime']
        self.url = response_dict['url']
        self.path = str(response_dict['path'])

        return
    
    def __str__(self) -> str:
        return f'Video ID: {self.videoId}\nPublished At:{self.publishedAt}\nTitle: {self.title}\nDesc: {self.description}\nPublish time:{self.publishTime}\nURL: {self.url}\nPath: {self.path}'
