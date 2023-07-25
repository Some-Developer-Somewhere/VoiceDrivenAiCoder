import msvcrt
import os
from settings import Settings
from gpt_chat_agent import ChatAgent
from read_files_for_context import read_files
from function_calls_manager import Function_calls
from play_audio import play_audio_asynchronously


def print_chat_options():
    print("\nChoose between the following options:")
    print("[1] Start a new chat without context")
    print("[2] Continue a chat")
    print("[3] Start a new chat with selected file context")
    print("[4] Start a new chat with multi-file-context")
    print("[5] Start a new chat with all files in folder as context")
    print("[6] Function Call")
    print("[7] Function Call from new message")
    print("[c] Cancel")


def read_transcription(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    return contents


def printUserMessage(userMessage):
    print("\n\n")
    print("user:")
    print("-"*40)
    print(userMessage)
    print("")


def create_system_message_text_from_context_files_list(context_files):
    text_string = "CONTEXT:"
    text_string += "\n\n"

    text_string += read_files(context_files) # Returns empty string if there is an error reading any file.
    text_string += "\n\n"
    
    text_string += "INSTRUCTIONS:"
    text_string += "\n"
    text_string += "Use the files above as context when answering the user."

    print('context')
    print(text_string)
    return text_string


def do_chat(s, chatAgent, clear_history=False, context_files=None, do_function_call=False):
    if clear_history:
        chatAgent.clear_self_chat_history()

    if context_files:
        print('context_files')
        print(context_files)
        system_message_text = create_system_message_text_from_context_files_list(context_files)
        chatAgent.append_system_msg(system_message_text)

    userMessage = read_transcription(s.transcription_fip)
    printUserMessage(userMessage)

    if do_function_call:
        # (answer, functionCallResult) = None, None
        fc = Function_calls(s)
        function_scemas_list = fc.get_function_definitions()
        (answer, function_call_message) = chatAgent.function_call(userMessage, function_scemas_list)
        
        # print('function call response:')
        # print(functionCallResult)

        if function_call_message:
            (function_name, function_call_result) = fc.execute_function(function_call_message)
            # print('function_call_result')
            # print(function_call_result)

            # agent.add-function: function_call_result
            print('function_call_result: ', end='')
            print(function_call_result)
            chatAgent.append_function_result_msg(function_name, function_call_result)

            # print('chatAgent.chatHistory')
            # [print(e) for e in chatAgent.chatHistory]

            answer = chatAgent.chatCompleationCall()


            # if not answer:
            #     return
    else:
        answer = chatAgent.chat(userMessage)

    s.openAiSettings.currentChatHistory = chatAgent.chatHistory
    s.openAiSettings.lastChatAnswer = answer

def choose_chat_action(s):
    chatAgent = ChatAgent(s)
    print_chat_options()

    while True:
        key_pressed = msvcrt.getch().decode("utf-8")

        if key_pressed == '1':
            play_audio_asynchronously('new.mp3')
            clear_history = True
            do_chat(s, chatAgent, clear_history)
            break

        elif key_pressed == '2':
            play_audio_asynchronously('continue.mp3')
            clear_history = False
            do_chat(s, chatAgent, clear_history)
            break

        elif key_pressed == '3':
            play_audio_asynchronously('new_with_file_as_context.mp3')
            print("Starting a new chat with selected file context.")
            chatAgent.clear_self_chat_history()
            context_files = [s.context_fip]
            clear_history = True
            do_chat(s, chatAgent, clear_history, context_files)
            break

        elif key_pressed == '4':
            play_audio_asynchronously('multi-file_context.mp3')
            print("Starting a new chat with multi-file-context.")
            print(s.multi_file_context_list_fip)
            context_files = []
            with open(s.multi_file_context_list_fip, 'r') as file:
                lines = file.readlines()
                context_files = [line.strip() for line in lines if line.strip()]
                context_files = [f for f in context_files if f[0] != '#']
            clear_history = True
            do_chat(s, chatAgent, clear_history, context_files)
            break

        elif key_pressed == '5':
            play_audio_asynchronously('files_in_folder_as_context.mp3')
            print("Starting a new chat with all files in folder as context.")
            # return "new_with_context_of_files_in_folder"
            # print(s.cwd)
            clear_history = True
            # context_files = os.listdir(s.cwd)
            context_files = [f for f in os.listdir(s.cwd) if os.path.isfile(os.path.join(s.cwd, f))]
            do_chat(s, chatAgent, clear_history, context_files)
            break

        elif key_pressed == '6':
            play_audio_asynchronously('function_call_with_context.mp3')
            print("TODO: Function Call with context")
            do_chat(s, chatAgent, do_function_call=True) # TODO: Doublecheck if they are sendt correctly to function
            break

        elif key_pressed == '7':
            play_audio_asynchronously('clean_function_call_without_context.mp3')
            print("TODO: Function Call from new message")
            clear_history = True
            do_chat(s, chatAgent, clear_history, do_function_call=True)
            break

        elif key_pressed.lower() == 'c':
            play_audio_asynchronously('cancel.mp3')
            print("Cancel.")
            # return None
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    s = Settings()
    chosen_option = choose_chat_action(s)
