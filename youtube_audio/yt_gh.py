import urllib.request
import subprocess
import argparse
import sys

from pytube import YouTube
from pytube.streams import Stream


def download_stream_to_memory(stream: Stream):
    pass


def download_and_convert_sequentially():
    with open("input.opus", "wb") as fout:
        fout.write(response.read())

    command = ("ffmpeg", "-y", "-i", "input.opus", "output.wav")
    process = subprocess.Popen(command)
    process.wait()


def download_and_convert_parallely(response, file_out_name: str):
    command = ("ffmpeg", "-y", "-i", "-", file_out_name + '.m4a')
    process = subprocess.Popen(command, stdin=subprocess.PIPE)

    while True:
        chunk = response.read(16 * 1024)
        if not chunk:
            break
        process.stdin.write(chunk)

    process.stdin.close()
    process.wait()


def parse_args():
    parser = argparse.ArgumentParser(description='Download YouTube Audio.')
    parser.add_argument('input', type=str, help="YouTube URL", nargs='?')
    parser.add_argument('-o', '--out', type=str, help="Where do you want to store the file?")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    url = args.input
    url = 'https://www.youtube.com/watch?v=zc071euiNQE'
    path = '~/Desktop/'

    # if not url:
    #     print('Provide a url after the command.')
    #     raise ValueError

    yt = YouTube(url)

    file_name = args.out if args.out else yt.title

    url_audio_stream_128kbps = yt.streams.filter(only_audio=True).filter(abr="128kbps")[0]
    response = urllib.request.urlopen(url_audio_stream_128kbps.url)

    print(f"Downloading \"{yt.title}\"")

    # stream_as_bytes = response.read()

    # with open('stream_as_bytes', 'wb') as f:
        # f.write(stream_as_bytes)

    with open('/Users/david.kuda/Desktop/stream_as_bytes', 'rb') as f:
        sys.stdout.buffer.write(f.read())
        # subprocess.run('xargs -I {} ffmpeg -i {} SABB.m4a', shell=True, stdin=f)
        # subprocess.run(args=['xargs', '-I', '{}', 'ffmpeg', '-i', '{}', 'HELLO_THERE.m4a'], stdin=f)
