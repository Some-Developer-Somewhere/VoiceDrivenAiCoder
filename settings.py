import os

class OpenAiSettings:
    def __init__(self):
        # self.temperature = 1 # default
        # self.temperature = 0.2
        self.temperature = 0
        self.frequency_penalty = 0 # default
        self.presence_penalty = 0 # default
        
        self.stream = True # Set to off to print token usage

        self.openai_api_key = os.environ['SECRET_OPENAI_API_KEY']

        self.model = None
        self.model_function_call = None
        self.select_gpt3()

        self.currentChatHistory = []
        self.lastChatAnswer = '' # TODO: write to file
        
    def select_gpt3(self):
        self.model = 'gpt-3.5-turbo'
        self.model_function_call = 'gpt-3.5-turbo-0613'
    
    def select_gpt4(self):
        self.model = 'gpt-4'
        self.model_function_call = 'gpt-4-0613'

    def select_gpt3_16k(self):
        self.model = 'gpt-3.5-turbo-16k'
        self.model_function_call = 'gpt-3.5-turbo-16k-0613'
        
    def select_gpt4_32k(self):
        self.model = 'gpt-4-32k'
        self.model_function_call = 'gpt-4-32k-0613'


class ElevenlabsSettings:
    def __init__(self):
        self.elevenlabs_api_key = os.environ['SECRET_ELEVENLABS_API_KEY']
        # self.voice_model = 'eleven_monolingual_v1'
        self.voice_model = 'eleven_multilingual_v1'
        self.voice_id1 = 'ErXwobaYiN019PkySvjV' # Antoni
        
        
class Settings:
    def __init__(self):
        self.openAiSettings = OpenAiSettings()
        self.elevenlabsSettings = ElevenlabsSettings()
        self.cwd = os.getcwd()

        self.exclude_folder_names = [
            '__pycache__',
            'node_modules',
        ]

        # TODO: Make player a class which holds settings. Then this can be set while running.
        self.audio_confirmation = True
        self.audio_volume = 0.05 # TODO: Set separete for commands and reading(?)

        self.script_root_path = None
        self.set_script_root_path()
        
        self.recording_fip = self.get_abs_path("out/audio/myrecording.wav")
        # self.transcription_fip = self.get_abs_path("out/transcription.txt")
        self.transcription_fip = self.get_abs_path("input/out_transcription.txt")

        self.answer_fip = self.get_abs_path("out/answer.md")
        self.conversation_fip = self.get_abs_path("out/conversation.md")

        
        self.default_context_fip = self.get_abs_path("input/default_context.txt")
        self.context_fip = self.default_context_fip
        self.multi_file_context_list_fip = self.get_abs_path("input/multi_file_context_list.txt")


        self.out_tags_file = self.get_abs_path("out/tags_json.txt")
        self.out_tags_structured_file = self.get_abs_path("out/tags_structured.txt")



    def set_script_root_path(self):
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        self.script_root_path = current_directory

    def get_abs_path(self, rel_path):
        abs_path = os.path.join(self.script_root_path, rel_path)
        return abs_path
    
    def set_context_fip_abs(self, abs_path):
        if abs_path:
            self.context_fip = abs_path
