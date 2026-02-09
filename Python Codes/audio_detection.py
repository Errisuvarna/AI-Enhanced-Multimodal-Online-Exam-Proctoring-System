# audio_detection.py
import speech_recognition as sr
import threading

def detect_audio(duration=3):
    """
    Records audio for a few seconds and detects suspicious sounds.
    Returns 'Normal' or 'Suspicious'.
    """
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening for audio...")
            audio_data = r.record(source, duration=duration)
            try:
                text = r.recognize_google(audio_data)
                print(f"Audio recognized: {text}")
                suspicious_words = ["hello", "hey", "phone", "help", "teacher", "exam"]
                if any(word.lower() in text.lower() for word in suspicious_words):
                    return "Suspicious"
            except sr.UnknownValueError:
                return "Normal"
            except Exception as e:
                print("Error in speech recognition:", e)
                return "Normal"
    except Exception as e:
        print("Microphone not accessible:", e)
        return "Normal"

def continuous_audio_detection(callback=None, interval=5):
    """
    Continuously checks audio every `interval` seconds.
    Calls callback(result) if provided.
    """
    def run():
        while True:
            result = detect_audio(duration=3)
            if callback:
                callback(result)
    t = threading.Thread(target=run, daemon=True)
    t.start()
