import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import threading

# === Global Config ===
MODEL_PATH = "model"  # vosk model folder
GIF_FOLDER ={"hi":"hi.gif",
             "thanks":"thanks.gif",
        "calm":"calm.gif",
        "date":"date.gif",
        "no":"no.gif",
        "yes":"yes.gif"
      }


SAMPLERATE = 16000
BLOCKSIZE = 8000

# === Audio Queue ===
q = queue.Queue()

# === Speech Recognition Callback ===
def callback(indata, frames, time, status):
    q.put(bytes(indata))

# === Vosk Offline Speech Recognition ===
def recognize_speech_offline():
    if not os.path.exists(MODEL_PATH):
        messagebox.showerror("Model Error", f"Vosk model not found at: {MODEL_PATH}")
        return ""
    model = Model(MODEL_PATH)
    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, SAMPLERATE)
        print("Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")

# === GIF Display Logic ===
def play_gif_sequence(words):
    def show_next_gif(index):
        if index >= len(words):
            return
        word = words[index]
        gif_path = os.path.join(GIF_FOLDER, f"{word.lower()}.gif")
        if not os.path.exists(gif_path):
            print(f"No GIF found for '{word}'")
            show_next_gif(index + 1)
            return

        img = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(img)]

        def animate(i=0):
            if i < len(frames):
                gif_label.configure(image=frames[i])
                gif_label.image = frames[i]
                root.after(100, animate, i+1)
            else:
                show_next_gif(index + 1)

        animate()

    show_next_gif(0)

# === GUI Actions ===
def handle_text_input():
    text = entry.get()
    if text:
        words = text.strip().split()
        play_gif_sequence(words)

def handle_microphone_input():
    def listen_thread():
        text = recognize_speech_offline()
        entry.delete(0, tk.END)
        entry.insert(0, text)
        if text:
            play_gif_sequence(text.strip().split())

    threading.Thread(target=listen_thread).start()

# === GUI Setup ===
root = tk.Tk()
root.title("Speech to Sign Language Translator")
root.geometry("600x500")
root.config(bg="#f0f0f0")

title = tk.Label(root, text="Speech to Sign Language", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
title.pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 16), width=40, bd=2, relief="groove")
entry.pack(pady=10)

btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

mic_btn = tk.Button(btn_frame, text="🎤 Speak", font=("Helvetica", 14), command=handle_microphone_input, bg="#d1e7dd")
mic_btn.grid(row=0, column=0, padx=10)

submit_btn = tk.Button(btn_frame, text="▶ Translate", font=("Helvetica", 14), command=handle_text_input, bg="#cfe2ff")
submit_btn.grid(row=0, column=1, padx=10)

gif_label = tk.Label(root, bg="#f0f0f0")
gif_label.pack(pady=20)

root.mainloop()
