from ctags import get_code_map

class Function_call_get_code_map:
    def __init__(self, s):
        self.s = s
        self.function_name = "get_code_map"
    
    def execute(self, functionArgs):
        print('Getting code map')
        
        # Call the getCodeMap() function from the ctags script
        code_map = get_code_map(self.s)

        # Return the code map as a result
        function_call_result = "{ \"status\": \"Getting code map done.\", \"code_map\": \""+ code_map + "\" }"
        return function_call_result

    def get_function_schema(self):
        function_schema = {
            "name": "get_code_map",
            "description": "Get the code map using the ctags script",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
        return function_schema
