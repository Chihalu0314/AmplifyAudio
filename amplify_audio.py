import tkinter as tk
from tkinter import filedialog
import librosa
import soundfile as sf
import pygame.mixer
import os
import numpy as np

def amplify_audio(file_path, volume_increase):
    # オーディオファイルを読み込む
    y, sr = librosa.load(file_path, sr=None)

    # 音量を上げる
    y_amplified = np.clip(y * volume_increase, -1.0, 1.0)

    # 新しいオーディオファイルを保存する
    sf.write(file_path.replace('.mp3', '_amplified.wav'), y_amplified, sr)

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

root = tk.Tk()
volume = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
volume.pack()

input_files = []

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    if file_path:
        input_files.append(file_path)
        file_label = tk.Label(root, text=os.path.basename(file_path))
        file_label.pack()

def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        for file in os.listdir(folder_path):
            if file.endswith(".mp3") or file.endswith(".wav"):
                file_path = os.path.join(folder_path, file)
                input_files.append(file_path)
                file_label = tk.Label(root, text=os.path.basename(file_path))
                file_label.pack()

def process_audio():
    for file_path in input_files:
        amplify_audio(file_path, volume.get())

def play_all():
    for file_path in input_files:
        play_audio(file_path.replace('.mp3', '_amplified.wav'))

open_file_button = tk.Button(root, text="ファイルを開く", command=open_file)
open_file_button.pack()

open_folder_button = tk.Button(root, text="フォルダを開く", command=open_folder)
open_folder_button.pack()

process_button = tk.Button(root, text="音量を上げて保存", command=process_audio)
process_button.pack()

play_button = tk.Button(root, text="再生", command=play_all)
play_button.pack()

stop_button = tk.Button(root, text="停止", command=stop_audio)
stop_button.pack()

root.mainloop()
