import msvcrt
from settings import Settings
from play_audio import play_audio_asynchronously


def print_settings_options():
    print("\nChoose between the following options:")
    print("[1] Stream answer True")
    print("[2] Stream answer False")
    print("[3] Use GPT-3")
    print("[4] Use GPT-4")
    print("[5] Use GPT-3-16K")
    print("[6] Use GPT-4-32K (not available)")
    print("[c] Cancel")


# TODO: Make two-step selections:
#   - Select model
#       - gpt-3
#       - gpt-4
#   - Stream GPT-answer
#       - on
#       - off
#   - Answer with speach while streaming (This should maybe be reset to false due to cost)


def choose_settings_action(s):
    print_settings_options()

    while True:
        key_pressed = msvcrt.getch().decode("utf-8")

        if key_pressed == '1':
            play_audio_asynchronously('stream_on.mp3')
            s.openAiSettings.stream = True
            print(s.openAiSettings.stream)
            break
        elif key_pressed == '2':
            play_audio_asynchronously('stream_off.mp3')
            s.openAiSettings.stream = False
            print(s.openAiSettings.stream)
            break
        elif key_pressed == '3':
            play_audio_asynchronously('GPT-3.mp3')
            s.openAiSettings.select_gpt3()
            print(s.openAiSettings.model)
            break
        elif key_pressed == '4':
            play_audio_asynchronously('GPT-4.mp3')
            s.openAiSettings.select_gpt4()
            print(s.openAiSettings.model)
            break
        elif key_pressed == '5':
            play_audio_asynchronously('GPT-3_16K.mp3')
            s.openAiSettings.select_gpt3_16k()
            print(s.openAiSettings.model)
            break
        elif key_pressed == '6':
            s.openAiSettings.select_gpt4_32k()
            print(s.openAiSettings.model)
            break
        elif key_pressed.lower() == 'c':
            play_audio_asynchronously('cancel.mp3')
            print("Cancel.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    s = Settings()
    chosen_option = choose_settings_action(s)
