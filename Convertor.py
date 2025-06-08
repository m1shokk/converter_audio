import tkinter as tk
from tkinter import filedialog, ttk
from pydub import AudioSegment
from midiutil import MIDIFile
import os
import numpy as np
from scipy.io.wavfile import write as write_wav
from tkinter import messagebox
import subprocess

# Global variable to store the path to the last saved file
last_saved_file_path = None

# Variable to store the current theme (light or dark)
current_theme = "light"

def convert_to_mp3():
    global last_saved_file_path
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    song_name = os.path.basename(file_path)
    song_label.config(text=song_name)
    audio = AudioSegment.from_file(file_path)
    output_file = "music_1.mp3"
    counter = 1
    while os.path.exists(output_file):
        output_file = f"music_{counter}.mp3"
        counter += 1
    audio.export(output_file, format="mp3", bitrate="320k")
    progress_bar['value'] = 100
    last_saved_file_path = os.path.abspath(output_file)
    messagebox.showinfo("Done", f"Saved as: {output_file}")

def convert_to_midi():
    global last_saved_file_path
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    song_name = os.path.basename(file_path)
    song_label.config(text=song_name)

    track = 0
    channel = 0
    time = 0
    tempo = 120
    volume = 100

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, tempo)

    note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3,
                'E': 4, 'F': 5, 'F#': 6, 'G': 7,
                'G#': 8, 'A': 9, 'A#': 10, 'B': 11}

    def note_to_midi(n):
        name = n[:-1]
        octave = int(n[-1])
        return 12 * (octave + 1) + note_map[name]

    chords = [
        ['A3', 'C4', 'E4'],  # Am
        ['E3', 'G#3', 'B3'], # E
        ['A3', 'C4', 'E4'],
        ['E3', 'G#3', 'B3'],
        ['A3', 'C4', 'E4'],
        ['D3', 'F3', 'A3'],  # Dm
        ['E3', 'G#3', 'B3'],
        ['A3', 'C4', 'E4'],
    ]

    for i, chord_notes in enumerate(chords):
        for n in chord_notes:
            MyMIDI.addNote(track, channel, note_to_midi(n), time + i * 2, 2, volume)

    output_file = "music_1.midi"
    counter = 1
    while os.path.exists(output_file):
        output_file = f"music_{counter}.midi"
        counter += 1
    with open(output_file, "wb") as output:
        MyMIDI.writeFile(output)
    progress_bar['value'] = 100
    last_saved_file_path = os.path.abspath(output_file)
    messagebox.showinfo("Done", f"Saved as: {output_file}")

def convert_to_wav():
    global last_saved_file_path
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    song_name = os.path.basename(file_path)
    song_label.config(text=song_name)
    audio = AudioSegment.from_file(file_path)
    output_file = "music_1.wav"
    counter = 1
    while os.path.exists(output_file):
        output_file = f"music_{counter}.wav"
        counter += 1
    audio.export(output_file, format="wav", bitrate="1411k")
    progress_bar['value'] = 100
    last_saved_file_path = os.path.abspath(output_file)
    messagebox.showinfo("Done", f"Saved as: {output_file}")

def convert_to_8bit():
    global last_saved_file_path
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    song_name = os.path.basename(file_path)
    song_label.config(text=song_name)

    try:
        # Load the original audio file
        audio = AudioSegment.from_file(file_path)

        # Apply 8-bit characteristics
        audio = audio.set_frame_rate(16000)
        audio = audio.set_sample_width(1)  # 8-bit = 1 byte
        audio = audio.set_channels(1)      # mono

        # Unique name
        output_file = "music_1_8bit.wav"
        counter = 1
        while os.path.exists(output_file):
            output_file = f"music_{counter}_8bit.wav"
            counter += 1

        audio.export(output_file, format="wav")
        progress_bar['value'] = 100
        last_saved_file_path = os.path.abspath(output_file)
        messagebox.showinfo("Done", f"Saved as: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Error processing: {e}")
        return


def choose_and_convert_8bit():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac *.aac *.m4a")])
    if file_path:
        convert_to_8bit(file_path)

# Function to toggle theme
def toggle_theme():
    global current_theme
    if current_theme == "light":
        current_theme = "dark"
        root.configure(bg="#00002B")  # Very dark blue background, almost black
        song_label.config(bg="#00002B", fg="white")
        mp3_button.config(bg="#00002B", fg="white")  # Very dark blue for buttons
        midi_button.config(bg="#00002B", fg="white")
        wav_button.config(bg="#00002B", fg="white")
        eight_bit_button.config(bg="#00002B", fg="white")
        view_location_button.config(bg="#00002B", fg="white")
    else:
        current_theme = "light"
        root.configure(bg="white")
        song_label.config(bg="white", fg="darkgray")
        mp3_button.config(bg="darkgray", fg="white")
        midi_button.config(bg="darkgray", fg="white")
        wav_button.config(bg="darkgray", fg="white")
        eight_bit_button.config(bg="darkgray", fg="white")
        view_location_button.config(bg="darkgray", fg="white")

# GUI setup
root = tk.Tk()
root.title("Music Converter by m1shokk")
root.geometry("400x300")  # Set fixed window size
root.resizable(False, False)  # Disable window resizing

song_label = tk.Label(root, text="", font=("Arial", 12), bg="white", fg="darkgray")
song_label.pack(pady=10)

mp3_button = tk.Button(root, text="Convert to MP3", command=convert_to_mp3, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
mp3_button.pack(pady=5)

midi_button = tk.Button(root, text="Convert to MIDI", command=convert_to_midi, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
midi_button.pack(pady=5)

wav_button = tk.Button(root, text="Convert to WAV", command=convert_to_wav, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
wav_button.pack(pady=5)

eight_bit_button = tk.Button(root, text="Convert to 8-bit", command=convert_to_8bit, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
eight_bit_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", style="Horizontal.TProgressbar")
progress_bar.pack(pady=10)

def open_file_location():
    if last_saved_file_path:
        if os.name == 'nt':
            os.system(f'explorer /select,"{last_saved_file_path}"')
        elif os.name == 'posix':
            subprocess.run(['open', '-R', last_saved_file_path])
    else:
        messagebox.showinfo("Information", "File has not been saved yet")

view_location_button = tk.Button(root, text="View File Location", command=open_file_location, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
view_location_button.pack(pady=5)

# Button to toggle theme
theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg="darkgray", fg="white", font=("Arial", 10, "bold"))
theme_button.pack(pady=5, side=tk.TOP, anchor=tk.NE)

root.mainloop()
