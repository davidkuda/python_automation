import urllib.request
import argparse
import sys

from pytube import YouTube


def parse_args():
    parser = argparse.ArgumentParser(description='Download YouTube Audio.')
    parser.add_argument('input', type=str, help="YouTube URL", nargs='?')
    parser.add_argument('-o', '--out', type=str, help="Where do you want to store the file?")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    url = args.input

    if not url:
        print('Provide a url after the command.')
        raise ValueError

    yt = YouTube(url)

    file_name = args.out if args.out else yt.title

    url_audio_stream_128kbps = yt.streams.filter(only_audio=True).filter(abr="128kbps")[0]
    response = urllib.request.urlopen(url_audio_stream_128kbps.url)

    print(f"Downloading \"{yt.title}\"")
    stream_as_bytes = response.read()

    sys.stdout.buffer.write(stream_as_bytes)
