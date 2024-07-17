import sounddevice as sd
from scipy.io.wavfile import write


# function records audio and stores it in a file
def record_audio(file_path, duration=6, fs=48000):
    print(f"Recording {duration} seconds of audio... Press Ctrl+C to stop.")
    # Record audio
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    # Save audio to file
    write(file_path, fs, audio_data)
