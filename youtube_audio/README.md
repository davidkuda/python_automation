# Download Audio from YouTube

As a musician you probably want to transcribe music by ear. Transcribing is a lot easier if you can open audio files with transcription software such as ["transcribe!"](https://www.seventhstring.com/xscribe/overview.html). There are fantastic covers that I would like to open in transcribe!, and this little script enables me to download the audio from youtube videos directly so that I can transcribe them. (The other use case: Listen to long talks.)

### Environment

You need to have `ffmpeg` installed (`brew install ffmpeg`).

```sh
# Create a new conda / virtual environment
conda create --name pytube

# Activate the new environment
conda activate pytube

# optionally install python3
conda install -y python

# Install pytube with pip
pip install pytube
```

### Usage

Run the file `yt_audio_download.py` with the link to the YouTube video as argument. It will buffer an audio stream to stdin. Eventually you need to pipe it to ffmpeg. 

```shell
# Basic formula:
python3 yt_audio_download.py "<url_to_youtube>" | ffmpeg -i pipe: "<filename>.m4a"

# Examples:
python3 yt_audio_download.py "https://www.youtube.com/watch?v=uJDOK0M4u2g" | ffmpeg -i pipe: "Gravity -- Arsonite.m4a"
python3 yt_audio_download.py "https://www.youtube.com/watch?v=XExB45GRrfc" | ffmpeg -i pipe: "How to Get Well, Stay Well & Never Be Sick Again- Raymond Francis (Nov 2017).m4a"
```

### Simplified usage

```sh
function dlyt {
    mkdir -v -p "$HOME/Desktop/audio_out" \
    && conda activate pytube \
    && python3 $DEV/repos/youtube_audio/yt_audio_download.py $1 | \
        ffmpeg \
            -hide_banner \
            -loglevel error \
            -i pipe: "$HOME/Desktop/audio_out/$2.m4a"
    && conda deactivate
}
dlyt "https://www.youtube.com/watch?v=NuGT3dQai7w" this_love_yoni
```
