import argparse
import yt_dlp

def list_formats(url):
    ydl_opts = {
        'listformats': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_video_with_yt_dlp(url, quality=None, format_id=None, cookies_file=None):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }

    if quality and format_id:
        ydl_opts['format'] = f'best[height={quality}][format_id*={format_id}]/bestvideo[height<={quality}][format_id*={format_id}]'
    elif quality:
        ydl_opts['format'] = f'best[height={quality}]/bestvideo[height<={quality}]'
    elif format_id:
        ydl_opts['format'] = f'best[format_id*={format_id}]/bestvideo[format_id*={format_id}]'
    else:
        ydl_opts['format'] = 'best/bestvideo'

    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos using yt-dlp")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--formats",
        action="store_true",
        help="List available formats instead of downloading. Example: --formats",
    )
    parser.add_argument(
        "--quality",
        type=int,
        help="Preferred video quality (height in pixels), e.g., --quality 720",
    )
    parser.add_argument(
        "--format_id",
        type=int,
        help="Preferred video format id (e.g., '137')",
    )
    parser.add_argument(
        "--cookies",
        type=str,
        help="Path to cookies file (to bypass age restrictions)",
    )

    args = parser.parse_args()

    if args.formats:
        list_formats(args.url)
    else:
        download_video_with_yt_dlp(args.url, quality=args.quality, format_id=args.format_id, cookies_file=args.cookies)

if __name__ == "__main__":
    main()