import tkinter as tk
import speech_recognition as sr
import pronouncing
import nltk
import pyttsx3
from nltk.corpus import cmudict

# Download the CMU Pronouncing Dictionary
nltk.download('cmudict')
cmu_dict = cmudict.dict()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set speech rate (lower value for slower speech)
engine.setProperty('rate', 125)  # Adjust this value to control speed

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Request error from Google Speech Recognition"

def detect_pronunciation_errors(text):
    detected_words = text.split()
    mispronounced_words = []
    for word in detected_words:
        # Check if the word exists in the CMU dictionary
        if word.lower() in cmu_dict:
            correct_phonemes = cmu_dict[word.lower()][0]
            recognized_phonemes = pronouncing.phones_for_word(word.lower())
            if recognized_phonemes and correct_phonemes != recognized_phonemes[0]:
                mispronounced_words.append(f"{word} (Expected: {correct_phonemes}, Got: {recognized_phonemes[0]})")
                # Provide voice feedback for the correct pronunciation
                pronunciation_guide = ' '.join(correct_phonemes)
                engine.say(f"The correct pronunciation for {word} is {word}. It should be pronounced as {pronunciation_guide}")
                engine.runAndWait()
        else:
            # If word not in CMU dictionary, flag it as unrecognized
            mispronounced_words.append(f"{word} (Not in dictionary)")
    return mispronounced_words

def start_detection():
    recognized_text = recognize_speech_from_mic()
    if recognized_text not in ["Could not understand audio", "Request error from Google Speech Recognition"]:
        errors = detect_pronunciation_errors(recognized_text)
        error_list = "\n".join(errors) if errors else "No pronunciation mistakes detected."
        result_text.set(f"Recognized Text: {recognized_text}\n\nPronunciation Mistakes:\n{error_list}")
    else:
        result_text.set(recognized_text)

# Setting up the GUI
root = tk.Tk()
root.title("Pronunciation Mistake Detector")

frame = tk.Frame(root)
frame.pack(pady=20)

start_button = tk.Button(frame, text="Start Detection", command=start_detection)
start_button.pack()

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, wraplength=400, justify="left")
result_label.pack(pady=20)

root.mainloop()
