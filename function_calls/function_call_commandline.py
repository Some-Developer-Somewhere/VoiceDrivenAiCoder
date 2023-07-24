import os
import subprocess
import json

class Function_call_commandline:
    def __init__(self, s):
        self.s = s
        self.function_name = "run_command"
    
    def execute(self, functionArgs):
        # Parse the string into a JSON object
        parsedArgs = json.loads(functionArgs)

        # Extract the 'command' string
        command = parsedArgs["command"]
        print(f'Running command: {command}')

        # Run the command and capture the output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        # Prepare the result
        function_call_result = {
            "output": output.decode('utf-8'),
            "error": error.decode('utf-8') if error else None
        }

        return json.dumps(function_call_result)

    def get_function_schema(self):
        function_schema = {
                "name": "run_command",
                "description": "Runs a command directly and returns the result",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"}
                    },
                    "required": ["command"]
                }
            }
        return function_schema