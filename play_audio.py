import threading
import io
import os
from settings import Settings

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

def _audio_player(s, audio_file_name):
    if s.audio_confirmation:
        try:
            pygame.mixer.init()

            current_dir = os.path.dirname(os.path.abspath(__file__))
            audio_file_path = os.path.join(current_dir, 'audio_messages', audio_file_name)

            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.set_volume(s.audio_volume)
            pygame.mixer.music.play()

            # Wait for the audio to finish before continuing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
        except:
            print(f"Error playing: '{audio_file_name}'")


def play_audio_asynchronously(audio_file_name):
    s = Settings()
    player_thread = threading.Thread(target=_audio_player, args=(s, audio_file_name,))
    player_thread.start()


if __name__ == '__main__':
    audio_file_name = 'Continuing.mp3'
    play_audio_asynchronously(audio_file_name)
    print("done")