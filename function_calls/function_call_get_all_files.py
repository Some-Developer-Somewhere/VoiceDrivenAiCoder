import os
import json

class Function_call_get_all_files:
    def __init__(self, s):
        self.s = s
        self.function_name = "get_all_files"
    
    def execute(self, functionArgs):
        print('Getting all files')
        
        # Parse the string into a JSON object
        # parsedArgs = json.loads(functionArgs)

        # Extract the 'directory' string
        # directory = parsedArgs["directory"]
        directory = self.s.cwd
        print(directory)

        # Get the list of all files in directory and subdirectories
        all_files = []
        for dirpath, dirnames, filenames in os.walk(directory):
            dirnames[:] = [d for d in dirnames if d not in self.s.exclude_folder_names]
            for filename in filenames:
                file_path = os.path.relpath(os.path.join(dirpath, filename), directory)
                all_files.append(file_path)

        # Return the list of all files as a result
        function_call_result = "{ \"status\": \"Getting all files done.\", \"files\": \""+ json.dumps(all_files) + "\" }"
        return function_call_result

    def get_function_schema(self):
        function_schema = {
            "name": "get_all_files",
            "description": "Get an overview of all the files in a folder and its subfolders",
            "parameters": {
                "type": "object",
                "properties": {
                    # "directory": {
                    #     "type": "string"
                    # }
                },
                # "required": ["directory"]
            }
        }
        return function_schema
    
