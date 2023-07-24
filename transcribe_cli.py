import os
import openai
# import sounddevice as sd
# import numpy as np
# import threading
import msvcrt
from scipy.io.wavfile import write
import pyaudio
import wave
from settings import Settings

class AudioRecorder:
    def __init__(self, fip):
        self.fip = fip

    def record(self):
        key = None
        # set up the recording parameters
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        filename = self.fip

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks until a key press
        # TODO: Combination of these halts the script until another keypress: msvcrt.kbhit() and msvcrt.getch()
        # stop = False
        while not msvcrt.kbhit():
        # while not stop:
        # while True:
            data = stream.read(chunk)
            frames.append(data)
            # if msvcrt.kbhit():
            #     stop = True
            #     key = msvcrt.getch()
            #     break

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        return key


class WhisperTranscriber:
    def __init__(self, recording_fip, openai_api_key):
        self.recording_fip = recording_fip
        openai.api_key = openai_api_key


    def transcribe(self):
        try:
            with open(self.recording_fip, "rb") as file:
                result = openai.Audio.transcribe("whisper-1", file)
            transcription = result['text']
            return transcription
        except:
            print('Error in the following:\n\tresult = openai.Audio.transcribe("whisper-1", file)')
            return ""


def record_and_transcribe(s):
    recording_fip = s.recording_fip
    transcription_fip = s.transcription_fip
    openai_api_key = s.openAiSettings.openai_api_key

    recorder = AudioRecorder(recording_fip)
    transcriber = WhisperTranscriber(recording_fip, openai_api_key)

    print("Recording started. Press any key to stop...")
    
    # key = None
    keypress = recorder.record()
    # print('keypress')
    # print(keypress)
    # if keypress in ('c', 'q'):
    #     print(f"Canceled with: '{keypress}'")
    #     return

    print('Transcribing...')
    transcription = transcriber.transcribe()

    print("Transcription:\n")
    print(transcription)
    # print("")
    with open(transcription_fip, 'w', encoding='utf-8') as file:
        file.write(transcription)

    # msvcrt.getch() # Clear any keypress


if __name__ == "__main__":
    s = Settings()
    record_and_transcribe(s)
