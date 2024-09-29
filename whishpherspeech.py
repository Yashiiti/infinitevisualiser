import pyaudio
import numpy as np
import whisper

# Load the Whisper model (choose 'base', 'small', 'medium', or 'large' for higher accuracy)
model = whisper.load_model("base")

# Sampling rate for the Whisper model
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono audio

# List to accumulate audio chunks
audio_accumulator = []

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to transcribe accumulated audio
def transcribe_accumulated_audio():
    global audio_accumulator
    if len(audio_accumulator) == 0:
        return
    
    # Concatenate accumulated audio chunks
    audio_data = np.concatenate(audio_accumulator)
    audio_accumulator.clear()  # Clear the accumulator

    # Transcribe the audio using Whisper
    result = model.transcribe(audio_data, fp16=False)
    print("Transcription:", result['text'])

# Callback function to handle the audio stream
def callback(in_data, frame_count, time_info, status):
    global audio_accumulator

    # Convert byte data to numpy array (scale from int16 to float32)
    audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0

    # Accumulate the audio data
    audio_accumulator.append(audio_data)

    # If enough audio has been accumulated, transcribe it (e.g., every 5 seconds)
    if len(audio_accumulator) * CHUNK_SIZE >= SAMPLE_RATE * 5:  # Adjust time window here (5 seconds)
        transcribe_accumulated_audio()

    return (in_data, pyaudio.paContinue)

# Start listening to the microphone
def start_listening():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE,
                    stream_callback=callback)

    print("Listening... (Press Ctrl+C to stop)")
    stream.start_stream()

    # Keep the stream running
    try:
        while stream.is_active():
            pass
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Start listening
start_listening()
