
from function_calls.function_call_get_all_files import Function_call_get_all_files
from function_calls.function_call_export_files import Function_call_export_files
from function_calls.function_call_read_files import Function_call_read_files
from function_calls.function_call_get_code_map import Function_call_get_code_map
from function_calls.function_call_rest_request import Function_call_rest_request
from function_calls.function_call_commandline import Function_call_commandline


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



class Function_calls:
    def __init__(self, s):
        self.s = s
        initiated_functions = [
            Function_call_export_files(s),
            Function_call_read_files(s),
            Function_call_get_code_map(s),
            Function_call_get_all_files(s),
            Function_call_rest_request(s),
            Function_call_commandline(s),
            # TODO:
            # - Get list of files for whole directory with sub folders.
            # - Get content from specified files.
            # - Vectorsearch to prioritize relevant files.
        ]
        self.functions_dict = {function.function_name: function for function in initiated_functions}

    def get_function_definitions(self):
        function_scemas_list = [self.functions_dict[key].get_function_schema() for key in self.functions_dict]
        return function_scemas_list

    def execute_function(self, function_call_message):
        functionName = function_call_message['name']
        # print(functionName)
        functionArgs = function_call_message['arguments']
        # print(functionArgs)

        function = self.functions_dict[functionName]
        try:
            function_call_result = function.execute(functionArgs)
        except Exception as e:
            function_call_result = str(e)

        return (functionName, function_call_result)

