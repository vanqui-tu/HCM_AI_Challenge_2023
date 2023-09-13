import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from tqdm import tqdm
import os

NO_SCRIPT_PATH = "./../data/scripts/no_scripts.txt"

# Doc danh sach
with open(NO_SCRIPT_PATH, 'r', encoding="utf-8") as file:
    lines = file.readlines()

for line in tqdm(lines):
    # Xuat file audio
    transcribed_audio_file_name = f"./../data/scripts/{line.strip()}.wav"
    zoom_video_file_name = f"./../data/videos/{line.strip()}.mp4"  
    audioclip = AudioFileClip(zoom_video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name)

    # Tinh thoi gian
    with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)

    # Xuat file transcript
    r = sr.Recognizer()
    f = open(f"./../data/scripts/{line.strip()}.txt" , "a")  
    for i in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=i*60, duration=60) 
        f.write(r.recognize_google(audio, language='vi').lower())
        f.write(" ")    
    f.close()

    os.remove(transcribed_audio_file_name)
