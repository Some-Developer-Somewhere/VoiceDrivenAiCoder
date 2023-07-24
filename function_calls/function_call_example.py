import os
import json


# https://openai.com/blog/function-calling-and-other-api-updates
# {"role": "function", "name": "get_current_weather", "content": "{\"temperature\": "22", \"unit\": \"celsius\", \"description\": \"Sunny\"}"}

# a = {
#     "messages": [
#         {
#             "role": "user",
#             "content": "What is the weather like in Boston?",
#             "function_call": '{"name": "my_function"}' #??
#         },
#         {
#             "role": "assistant",
#             "content": None,
#             "function_call": {"name": "get_current_weather", "arguments": "{ \"location\": \"Boston, MA\"}"}
#         },
#         {
#             "role": "function",
#             "name": "get_current_weather",
#             "content": "{\"temperature\": \"22\", \"unit\": \"celsius\", \"description\": \"Sunny\"}"
#         }
#     ]
# }


# https://platform.openai.com/docs/api-reference/chat/create
# function_call: Controls how the model responds to function calls. "none" means the model does not call a function, and responds to the end-user. "auto" means the model can pick between an end-user or calling a function. Specifying a particular function via {"name":\ "my_function"} forces the model to call that function. "none" is the default when no functions are present. "auto" is the default if functions are present.


class Function_call_example:
    def __init__(self, s):
        self.s = s
        self.function_name = "export_files"
    
    def execute(self, functionArgs):
        print('Exporting files')
        # print(functionArgs)
        # print('TODO:....')

        # Parse the string into a JSON object
        parsedArgs = json.loads(functionArgs)

        # Extract the 'files' array
        files = parsedArgs["files"]
        print(files)

        # TODO: select other dir?
        # TODO: Check full vs partial paths?
        self.create_multiple_files(files, self.s.cwd)

        # function_call_result = 'Exporting files done.'
        function_call_result = "{ \"status\": \"Exporting files done.\" }"
        # print('function_call_result')
        # print(function_call_result)
        return function_call_result

        
    def create_file(self, file_path, content, workDir):
        full_path = os.path.join(workDir, file_path)
        dir_name = os.path.dirname(full_path)
        
        # Create necessary directories if they don't exist
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        # Create the file and write the content
        with open(full_path, 'w') as file:
            file.write(content)


    def create_multiple_files(self, files, workDir):
        for file in files:
            file_path = file['file_path']
            content = file['content']
            self.create_file(file_path, content, workDir)

    
    def get_function_schema(self):
        function_schema = {
                "name": "export_files",
                "description": "Create multiple new files with given content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "file_path": {"type": "string"},
                                    "content": {"type": "string"}
                                },
                                "required": ["file_path", "content"]
                            }
                        }
                    },
                    "required": ["files"]
                }
            }
        return function_schema
