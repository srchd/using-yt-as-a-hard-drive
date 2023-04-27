# Scripts for downloading youtube videos
## USECASE - download_ytdlp
Download using a 3rd party library made by (possibly) professionals. <br />

#### List out available video formats (--formats argument):
>> python download_ytdlp.py "https://www.youtube.com/watch?v=qo_fUjb02ns" --formats <br />
#### Download best merged video (video+audio) (no arguments):
>> python download_ytdlp.py "https://www.youtube.com/watch?v=qo_fUjb02ns" <br />
#### Download with specific ID from available fromats list (--format_id id):
>> python download_ytdlp.py "https://www.youtube.com/watch?v=qo_fUjb02ns" --format_id 400 <br />

## USECASE - download_urllib
Download using hand-made code using urllib <br />

#### List out available video formats (--formats argument):
>> python download_urllib.py "https://www.youtube.com/watch?v=qo_fUjb02ns" --formats <br />
#### Download video with specified format AND/OR quality (--format_str s and --quality q arguments):
>> python download_urllib.py "https://www.youtube.com/watch?v=qo_fUjb02ns" --quality 1440 --format_str "video/webm" <br />
