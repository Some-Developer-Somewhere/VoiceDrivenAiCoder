import requests
import json


class Function_call_rest_request:
    def __init__(self, s):
        self.s = s
        self.function_name = "send_rest_request"
        # self.api_keys = {
        #     "base_url": "api.spotify.com",
        #     "api_key": "bearer spotify_api_key"
        # }
    
    def execute(self, functionArgs):
        # Parse the string into a JSON object
        parsedArgs = json.loads(functionArgs)

        # Extract the necessary parameters
        method = parsedArgs["method"]
        url = parsedArgs["url"]
        headers = parsedArgs.get("headers", {})
        body = parsedArgs.get("body", {})

        # # Check if the url contains a base url that we have an API key for
        # for base_url, api_key in self.api_keys.items():
        #     if base_url in url:
        #         # Add or replace the Authorization header with the API key
        #         headers["Authorization"] = api_key

        # Send the REST request
        response = requests.request(method, url, headers=headers, data=json.dumps(body))

        # Return the response as a string
        function_call_result = "{ \"status\": \"" + str(response.status_code) + "\", \"response\": \"" + response.text + "\" }"
        return function_call_result

    def get_function_schema(self):
        function_schema = {
                "name": "send_rest_request",
                "description": "Send a REST request based on the provided parameters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "method": {"type": "string"},
                        "url": {"type": "string"},
                        "headers": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string"
                            }
                        },
                        "body": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["method", "url"]
                }
            }
        return function_schema
