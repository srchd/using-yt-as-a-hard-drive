import argparse
import yt_dlp


def download_video_with_yt_dlp(url, quality=None, cookies_file=None):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
    }

    if quality:
        ydl_opts['format'] = f'best[ext=mp4][height<={quality}]'

    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos using yt-dlp")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--quality",
        type=int,
        help="Preferred video quality (height in pixels), e.g., --quality 720",
    )
    parser.add_argument(
        "--cookies",
        type=str,
        help="Path to cookies file (to bypass age restrictions)",
    )

    args = parser.parse_args()

    download_video_with_yt_dlp(args.url, quality=args.quality, cookies_file=args.cookies)


if __name__ == "__main__":
    main()