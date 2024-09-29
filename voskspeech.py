import sys
import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Load the Vosk model
model_path = "vosk-model-small-en-in-0.4\\vosk-model-small-en-in-0.4"

if not os.path.exists(model_path):
    print(f"Model not found at {model_path}. Please download it from the Vosk website.")
    sys.exit(1)

model = Model(model_path)

# Function to transcribe from microphone
def transcribe_from_microphone():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    rec = KaldiRecognizer(model, 16000)
    
    print("Listening... (Press Ctrl+C to stop)")
    
    while True:
        data = stream.read(8000)
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(json.loads(result)['text'])
    
    # Final result (to be executed on exit)
    final_result = rec.FinalResult()
    print(json.loads(final_result)['text'])

# Call this function to start transcribing from the microphone
transcribe_from_microphone()
