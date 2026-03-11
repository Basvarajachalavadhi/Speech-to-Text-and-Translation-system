import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

recognizer = sr.Recognizer()

# -----------------------
# Record audio without PyAudio
# -----------------------
def record_audio(duration=5, samplerate=16000):
    status_label.config(text="🎤 Listening...")
    root.update()
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate,
                        channels=1, dtype="int16")
    sd.wait()
    status_label.config(text="⏳ Processing...")
    root.update()
    return np.squeeze(audio_data)

# -----------------------
# Speech Recognition Function
# -----------------------
def recognize_speech():
    try:
        audio = record_audio()
        # Convert numpy audio to AudioData for speech_recognition
        audio_data = sr.AudioData(audio.tobytes(), 16000, 2)

        source_lang = lang_choice.get()
        recognized_text = recognizer.recognize_google(audio_data, language=source_lang)
        input_text.set(recognized_text)
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the audio")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not request results")
    except Exception as e:
        messagebox.showerror("Error", f"Recording error: {e}")
    status_label.config(text="✅ Ready")

# -----------------------
# Translation Function
# -----------------------
def translate_text():
    text = input_text.get()
    target_lang = target_lang_choice.get()
    if text and target_lang:
        try:
            translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
            output_text.set(translated)
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {e}")
    else:
        messagebox.showwarning("Warning", "Please provide valid input and language")

# -----------------------
# Text-to-Speech Function
# -----------------------
def speak_translation():
    text = output_text.get()
    target_lang = target_lang_choice.get()
    if text:
        try:
            tts = gTTS(text=text, lang=target_lang)
            tts.save("translated_audio.mp3")
            if os.name == "nt":  # Windows
                os.system("start translated_audio.mp3")
            else:  # Linux/Mac
                os.system("mpg321 translated_audio.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Speech synthesis failed: {e}")
    else:
        messagebox.showwarning("Warning", "No translated text to speak")

# -----------------------
# Clear Text Fields
# -----------------------
def clear_text():
    input_text.set("")
    output_text.set("")

# -----------------------
# GUI Setup
# -----------------------
root = tk.Tk()
root.title("Speech-to-Text Language Converter (No PyAudio)")
root.geometry("600x600")
root.configure(bg="#222831")

# Frames
header_frame = tk.Frame(root, bg="#00ADB5", padx=15, pady=15)
header_frame.pack(fill="x")

main_frame = tk.Frame(root, bg="#393E46", padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

footer_frame = tk.Frame(root, bg="#00ADB5", padx=10, pady=10)
footer_frame.pack(fill="x")

# Header Label
header_label = tk.Label(header_frame, text="🎙️ Speech-to-Text Translator",
                        fg="white", bg="#00ADB5", font=("Arial", 18, "bold"))
header_label.pack()

# Status Label
status_label = tk.Label(main_frame, text="✅ Ready",
                        font=("Arial", 12), bg="#393E46", fg="white")
status_label.pack(pady=5)

# Record Button
record_btn = tk.Button(main_frame, text="🎤 Record Speech",
                       command=recognize_speech, bg="#FF5722", fg="white",
                       font=("Arial", 14, "bold"), padx=10, pady=5)
record_btn.pack(pady=5)

# Recognized Text
input_label = tk.Label(main_frame, text="Recognized Text:",
                       bg="#393E46", fg="white", font=("Arial", 12, "bold"))
input_label.pack()
input_text = tk.StringVar()
input_entry = tk.Entry(main_frame, textvariable=input_text,
                       width=50, font=("Arial", 12))
input_entry.pack(pady=5)

# Language Selection for Speech Recognition
source_lang_label = tk.Label(main_frame, text="Select Speech Language:",
                             bg="#393E46", fg="white", font=("Arial", 12, "bold"))
source_lang_label.pack()
lang_choice = tk.StringVar(value='en')
lang_menu = ttk.Combobox(main_frame, textvariable=lang_choice,
                         values=['en', 'es', 'fr', 'de', 'hi', 'zh-CN'],
                         font=("Arial", 12))
lang_menu.pack()

# Language Selection for Translation
target_lang_label = tk.Label(main_frame, text="Select Target Language:",
                             bg="#393E46", fg="white", font=("Arial", 12, "bold"))
target_lang_label.pack()
target_lang_choice = tk.StringVar(value='es')
target_lang_menu = ttk.Combobox(main_frame, textvariable=target_lang_choice,
                                values=['en', 'es', 'fr', 'de', 'hi', 'zh-CN'],
                                font=("Arial", 12))
target_lang_menu.pack()

# Translate Button
translate_btn = tk.Button(main_frame, text="🌍 Translate",
                          command=translate_text, bg="#03A9F4", fg="white",
                          font=("Arial", 14, "bold"), padx=10, pady=5)
translate_btn.pack(pady=5)

# Translated Text
output_label = tk.Label(main_frame, text="Translated Text:",
                        bg="#393E46", fg="white", font=("Arial", 12, "bold"))
output_label.pack()
output_text = tk.StringVar()
output_entry = tk.Entry(main_frame, textvariable=output_text,
                        width=50, font=("Arial", 12))
output_entry.pack(pady=5)

# Speak Button
speak_btn = tk.Button(main_frame, text="🔊 Speak Translation",
                      command=speak_translation, bg="#9C27B0", fg="white",
                      font=("Arial", 14, "bold"), padx=10, pady=5)
speak_btn.pack(pady=5)

# Clear Button
clear_btn = tk.Button(main_frame, text="🧹 Clear",
                      command=clear_text, bg="#FF5252", fg="white",
                      font=("Arial", 14, "bold"), padx=10, pady=5)
clear_btn.pack(pady=5)

# Footer
footer_label = tk.Label(footer_frame, text="© 2025 Speech Translator App",
                         fg="white", bg="#00ADB5", font=("Arial", 12, "bold"))
footer_label.pack()

root.mainloop()