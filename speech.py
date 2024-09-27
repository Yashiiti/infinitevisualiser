import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone as source for input
with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("Listening...")
    audio = recognizer.listen(source)

try:
    # Using Google Web Speech API (online)
    data=recognizer.recognize_google(audio)
    print("You said: " + data)
    
    # Optionally, you can use the offline Sphinx recognizer as well
    # print("You said (Sphinx): " + recognizer.recognize_sphinx(audio))
    
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print(f"Request error from Google Web Speech API; {e}")
