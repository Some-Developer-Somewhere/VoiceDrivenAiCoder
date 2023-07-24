import io
import os
import requests
import json
import queue
import threading
import concurrent.futures
# import pygame  # Import pygame
from settings import Settings

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# TODO: It seems that the stream from elevenlabs are not played while being recieved. This should be ok as long as the first few sentances are short enough.

class ElevenLabsTTS:
    def __init__(self, s):
        pygame.mixer.init()  # Initialize the mixer

        self.api_key = s.elevenlabsSettings.elevenlabs_api_key
        self.voice_model = s.elevenlabsSettings.voice_model
        self.voice_id = s.elevenlabsSettings.voice_id1
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        self.headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': self.api_key,
            'Content-Type': 'application/json',
        }
        self.audio_queue = queue.Queue()
        self.player_thread = threading.Thread(target=self._audio_player)
        self.player_thread.start()

    def _audio_player(self):
        while True:
            audio_data = self.audio_queue.get()
            if audio_data is None:
                break  # Exit if None is received

            # Create a BytesIO object and load it into pygame
            audio_file = io.BytesIO(audio_data)
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Wait for the audio to finish before continuing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    def get_audio_stream(self, text):
        data = {
            "text": text,
            "model_id": self.voice_model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            self.audio_queue.put(response.content)
        else:
            print(f"Request failed with status code {response.status_code}")

    def speak(self, text):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.get_audio_stream, text)

    def stop(self):
        self.audio_queue.put(None)
        self.player_thread.join()


if __name__ == '__main__':
    s = Settings()
    tts = ElevenLabsTTS(s)
    # print("0")
    # tts.speak('response = requests.post(self.url, headers=self.headers, data=json.dumps(data))')
    # print("1")
    tts.speak('Hello, world!')
    # print("2")
    tts.speak('How are you today?')
    # print("3")
    # ...
    tts.stop()  # when you're done
    # print("4")
