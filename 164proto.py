import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import threading
import queue
import json
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from textblob import TextBlob

# === Settings ===
MODEL_PATH = "model"
GIF_FOLDER = "Mp4file"
SAMPLERATE = 16000
BLOCKSIZE = 8000

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

# === Offline Speech Recognition using Vosk ===
def recognize_speech_offline():
    if not os.path.exists(MODEL_PATH):
        messagebox.showerror("Model Missing", f"No Vosk model found at '{MODEL_PATH}'")
        return ""

    model = Model(MODEL_PATH)
    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, SAMPLERATE)

        print("Calibrating silence...")
        sd.sleep(1000)
        print("Speak now...")

        result_text = ""
        try:
            while True:
                data = q.get(timeout=5)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    result_text = result.get("text", "")
                    break
        except queue.Empty:
            print("Timeout. No input detected.")

        corrected = TextBlob(result_text).correct()
        return str(corrected)

# === Display GIF Sequence for Words ===
def play_gifs_for_words(words):
    def show_next(index):
        if index >= len(words):
            return
        word = words[index].lower()
        gif_path = os.path.join(GIF_FOLDER, f"{word}.gif")
        if not os.path.exists(gif_path):
            print(f"[SKIP] No gif found for: {word}")
            show_next(index + 1)
            return

        img = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(img)]

        def animate(i=0):
            if i < len(frames):
                gif_label.config(image=frames[i])
                gif_label.image = frames[i]
                root.after(100, animate, i+1)
            else:
                show_next(index + 1)

        animate()

    show_next(0)

# === GUI Event: Handle Text Input ===
def handle_text_input():
    text = entry.get().strip()
    if text:
        words = text.split()
        play_gifs_for_words(words)

# === GUI Event: Handle Microphone Input ===
def handle_microphone():
    def listen_and_fill():
        text = recognize_speech_offline()
        if text:
            entry.delete(0, tk.END)
            entry.insert(0, text)
            play_gifs_for_words(text.split())
    threading.Thread(target=listen_and_fill).start()

# === GUI Setup ===
root = tk.Tk()
root.title("Speech to Sign Language Translator")
root.geometry("650x500")
root.config(bg="#f9f9f9")

tk.Label(root, text="Speech to Sign Language", font=("Helvetica", 18, "bold"), bg="#f9f9f9").pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 16), width=45, bd=2, relief="groove")
entry.pack(pady=10)

btn_frame = tk.Frame(root, bg="#f9f9f9")
btn_frame.pack(pady=10)

mic_btn = tk.Button(btn_frame, text="🎤 Speak", font=("Helvetica", 14), bg="#d1e7dd", command=handle_microphone)
mic_btn.grid(row=0, column=0, padx=10)

translate_btn = tk.Button(btn_frame, text="▶ Translate", font=("Helvetica", 14), bg="#cfe2ff", command=handle_text_input)
translate_btn.grid(row=0, column=1, padx=10)

gif_label = tk.Label(root, bg="#f9f9f9")
gif_label.pack(pady=20)

if __name__=='__main__':
    root.mainloop()
