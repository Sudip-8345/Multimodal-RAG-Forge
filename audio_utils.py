import speech_recognition as sr

# Convert audio to text using Whisper
def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_whisper(audio_data)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
            return None

# Save text to file
def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Text data saved to {output_path} successfully!")
