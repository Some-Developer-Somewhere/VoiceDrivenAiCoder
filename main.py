import msvcrt
from transcribe_cli import record_and_transcribe
from select_file_cli import choose_file_option
from chat_action_cli import choose_chat_action
from settings_actions_cli import choose_settings_action
from ElevenlabsStream import ElevenLabsTTS
from settings import Settings
from copy_to_clipboard import copy_transcription_to_clipboard  # import the new function

    
def print_key_options(s):
    print("")
    print("Choose between the following options:")
    print("[1] Record and transcribe")
    print(f"[2] Chat ({s.openAiSettings.model})")
    print("[3] Copy transcription to clipboard")
    # print("[4] Code generation")
    print("[5] TTS")
    # print("[6] Terminal command")
    print("[8] Pick context file")
    print("[9] Settings")
    print("[q] Exit")


def choose_option():
    s = Settings()
    print('s.cwd')
    print(s.cwd)
    # print_key_options()

    while True:
        print_key_options(s)
        try:
            key_pressed = msvcrt.getch().decode("utf-8")
        except:
            key_pressed = "error"
            
        if key_pressed == '1':
            record_and_transcribe(s)
            msvcrt.getch() # Clear any keypress #TODO: Will not handle it if user presses [Arrow-Up]
            # print_key_options()

        elif key_pressed == '2':
            print("Chat chosen.")
            choose_chat_action(s)

        elif key_pressed == '3':
            print("Copy transcription to clipboard chosen.")
            copy_transcription_to_clipboard(s)

        # elif key_pressed == '4':
        #     print("Code generation chosen.")
        
        elif key_pressed == '5':
            print("TTS chosen.")
            print(s.openAiSettings.lastChatAnswer)
            tts = ElevenLabsTTS(s)
            # tts.speak(s.openAiSettings.lastChatAnswer)
            # answerText = s.openAiSettings.lastChatAnswer
            with open(s.answer_fip, 'r', encoding='utf-8') as file:
                answerText = file.read()
            [tts.speak(line) for line in answerText.split('\n')]
            tts.stop()  # when you're done

        # elif key_pressed == '6':
        #     print("Terminal command chosen.")

        elif key_pressed == '8':
            print("Pick context file")
            choose_file_option(s)
            # chosen_file = choose_file_option(s.cwd, s.default_context_fip)
            # s.context_fip = s.set_context_fip_abs(chosen_file)
        
        elif key_pressed == '9':
            print("Settings chosen.")
            choose_settings_action(s)
        
        elif key_pressed == 'q':
            print("Exit chosen.")
            exit()
        else:
            print("Invalid option. Try again.")


choose_option()
