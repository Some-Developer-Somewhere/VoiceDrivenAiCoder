import json
from read_files_for_context import read_files

class Function_call_read_files:
    def __init__(self, s):
        self.s = s
        self.function_name = "read_files"
    
    def execute(self, functionArgs):
        print('Reading files')
        
        # Parse the string into a JSON object
        parsedArgs = json.loads(functionArgs)

        # Extract the 'file_paths' array
        file_paths = parsedArgs["file_paths"]
        print(file_paths)
        files_contents = read_files(file_paths) 

        # TODO: Read the content of the files based on the file paths
        # and return the content as a result

        function_call_result = "{ \"status\": \"Reading files done.\", \"contents\": \""+ files_contents + "\" }"
        return function_call_result

    def get_function_schema(self):
        function_schema = {
            "name": "read_files",
            "description": "Read the content of files based on a list of file paths",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["file_paths"]
            }
        }
        return function_schema
