import streamlit as st
import os

from moviepy.editor import *
from pytube import YouTube
from youtubesearchpython import VideosSearch

OUTPUT_PATH = "static/mashup/"

def fetch_clips(artist_name, num_clips):
    """
    Fetch clips from YouTube
    """
    prefix = "https://www.youtube.com/watch?v="
    clips_search = VideosSearch(artist_name, limit=num_clips)
    clips = clips_search.result()["result"]
    clips = [prefix + clip["id"] for clip in clips]
    return clips

def download_video_clip(clip_url, save_path=OUTPUT_PATH):
    save_path = save_path + "/clips"
    yt = YouTube(clip_url)
    video = yt.streams.first()
    video_title = video.default_filename.replace(" ", "_")
    video.download(save_path, video_title)
    return video_title

def convert_to_audio(video_title, save_path=OUTPUT_PATH):
    audio_save_path = save_path
    video_path = save_path + "/clips/" + video_title
    audio_path = audio_save_path + "/" + video_title.split(".")[0] + ".mp3"
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()
    video_clip.close()
    return audio_path

def trim_audio_file(audio_path, duration):
    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.subclip(0, duration)
    audio_path=audio_path[:-4]+"_trimmed.mp3"
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

def download_and_process_video_clip(clip_url, save_path, duration):
    clip_title = download_video_clip(clip_url, save_path)
    audio_title = convert_to_audio(clip_title, save_path)
    trim_audio_file(audio_title, duration)

def merge_audio_files(artist_name, save_path=OUTPUT_PATH, output_filename="mashup.mp3"):
    final_audio_path = save_path + "/" + output_filename
    audio_files = [
        save_path + "/" + audio for audio in os.listdir(save_path) if audio.endswith("trimmed.mp3")
    ]
    final_clip = concatenate_audioclips([AudioFileClip(audio) for audio in audio_files])
    final_clip.write_audiofile(final_audio_path)
    final_clip.close()
    return final_audio_path

def create_mix(artist_name, num_clips, duration, output_filename):
    save_path = OUTPUT_PATH + artist_name
    clips = fetch_clips(artist_name, num_clips)

    for clip in clips:
        download_and_process_video_clip(clip, save_path, duration)

    download_path=merge_audio_files(artist_name, save_path, output_filename)
    return download_path

def main():
    st.title("YouTube Mashup Creator")

    artist_name = st.text_input("Enter Artist Name:")
    num_clips = st.number_input("Number of Clips:", min_value=1, step=1)
    duration = st.number_input("Duration (seconds):", min_value=1, step=1)
    output_filename = st.text_input("Output Filename:")

    if not output_filename.endswith("trimmed.mp3"):
        output_filename += ".mp3"
    if st.button("Create Mashup"):
        download_path = create_mix(artist_name, num_clips, duration, output_filename)
        st.success("Mashup created successfully!")
        st.download_button(label="Download Mashup", data=open(download_path, 'rb'), file_name=output_filename)

if __name__ == "__main__":
    main()
