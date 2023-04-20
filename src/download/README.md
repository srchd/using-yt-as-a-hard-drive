# Scripts for downloading youtube videos
## USECASE 0 (ytdlp):
>> python download_ytdlp.py -url- <br />
## USECASE 1:
List out the available formats for video in -url-:
>> python download_urllib.py https://www.youtube.com/watch?v=OTVE5iPMKLg&ab_channel=CGPGrey --formats <br />
Out: <br />
format_str - quality_lable - height <br />
FORMATS: <br />
video/mp4; codecs="avc1.42001E, mp4a.40.2" - 360p - 360p <br />
video/mp4; codecs="avc1.64001F, mp4a.40.2" - 720p - 720p <br />


## USECASE 2:
Download youtube video with a specified format: <br />
>> python download_urllib.py <url> --format_str <> --quality <> <br />
>> python download_urllib.py "https://www.youtube.com/watch?v=OTVE5iPMKLg&ab_channel=CGPGrey" --format_str "video/mp4;\ codecs=\"avc1.42001E,\ mp4a.40.2\"" --quality 360 <br />
>> python download_urllib.py "https://www.youtube.com/watch?v=OTVE5iPMKLg&ab_channel=CGPGrey" --format_str "video/mp4;\ codecs=\"avc1.64001F,\ mp4a.40.2\"" --quality 720 <br />
