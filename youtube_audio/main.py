#!/opt/homebrew/Caskroom/miniconda/base/envs/pytube/bin/python3
import urllib.request
import argparse
import sys

import typer
from pytube import YouTube


app = typer.Typer()


@app.command()
def download(youtube_url: str):
    yt = YouTube(youtube_url)
    for s in yt.streams.filter(only_audio=True):
        print(s)
    itag = input("Which stream do you want to download? (Enter itag number:)")
    yt.streams.get_by_itag(itag).download(
        output_path="/Users/davidkuda/Desktop")
    print(f'Downloaded "{yt.title}"\n')


if __name__ == "__main__":
    app()

