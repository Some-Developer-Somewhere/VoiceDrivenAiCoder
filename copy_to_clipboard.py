import pyperclip
from settings import Settings

def copy_transcription_to_clipboard(s):
    with open(s.transcription_fip, 'r', encoding='utf-8') as file:
        transcription = file.read()
    pyperclip.copy(transcription)
    print("Transcription copied to clipboard.")
