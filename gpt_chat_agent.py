import openai
from settings import Settings


class ChatAgent:
    def __init__(self, s):
        self.s = s
        openai.api_key = s.openAiSettings.openai_api_key
        # self.chatHistory = []
        self.chatHistory = s.openAiSettings.currentChatHistory
        self.model = s.openAiSettings.model
        self.model_function_call = s.openAiSettings.model_function_call
        self.stream = s.openAiSettings.stream
        # self.temperature = 1
        # self.temperature = 0.2
        self.temperature = s.openAiSettings.temperature
        self.frequency_penalty = s.openAiSettings.frequency_penalty
        self.presence_penalty = s.openAiSettings.presence_penalty

    def clear_self_chat_history(self):
        self.chatHistory = []

    def append_system_msg(self, msg):
        self.chatHistory.append({"role": "system", "content": msg})
    
    def append_user_msg(self, msg):
        self.chatHistory.append({"role": "user", "content": msg})

    def append_assistant_msg(self, msg, function_call_message=None):
        if function_call_message:
            self.chatHistory.append({
                "role": "assistant",
                "content": msg,
                "function_call": function_call_message
            })
        else:
            self.chatHistory.append({
                "role": "assistant",
                "content": msg
            })

    def append_function_result_msg(self, function_name, function_result):
        self.chatHistory.append({
            "role": "function",
            "name": function_name,
            "content": function_result
        })

    def move_sys_messages_last():
        raise NotImplementedError() # TODO:
    
    def chat(self, userMessage):
        try:
            self.append_user_msg(userMessage)
            answer = self.chatCompleationCall()
            self.append_assistant_msg(answer)
        # except openai.error.InvalidRequestError as e:
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Returning to the main menu...")
            # Remove the last user message that caused the error
            self.chatHistory.pop()
            return None

        with open(self.s.answer_fip, 'w', encoding='utf-8') as f:
            f.write(answer)
        with open(self.s.conversation_fip, 'w', encoding='utf-8') as f:
            # [print(e) for e in self.chatHistory]
            formatted_messages = [self.format_chat_message(e) for e in self.chatHistory]
            text = "\n\n\n".join(formatted_messages)
            f.write(text)

        return answer
    
    def function_call(self, userMessage, function_scemas_list):
        self.append_user_msg(userMessage)
        (answer, function_call_message) = self.functionCallCompleationCall(function_scemas_list)
        # print('** function_call_message')
        # print(function_call_message)
        # print('** End function_call_message')
        self.append_assistant_msg(answer, function_call_message)

        # with open(self.s.answer_fip, 'w', encoding='utf-8') as f:
        #     f.write(answer)
        # with open(self.s.conversation_fip, 'w', encoding='utf-8') as f:
        #     # [print(e) for e in self.chatHistory]
        #     formatted_messages = [self.format_chat_message(e) for e in self.chatHistory]
        #     text = "\n\n\n".join(formatted_messages)
        #     f.write(text)

        return (answer, function_call_message)
    
    
    def functionCallCompleationCall(self, function_scemas_list):
        print('function_scemas_list')
        print(function_scemas_list)
        print('self.chatHistory')
        [print(e) for e in self.chatHistory]

        response = openai.ChatCompletion.create(
            model=self.model_function_call,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            messages=self.chatHistory,
            functions=function_scemas_list,
            stream=False)

        message = response['choices'][0]['message']
        answer = message['content']
        function_response = None
        if 'function_call' in message:
            function_response = message['function_call']

        if answer:
            print("\nAssistant:")
            print("-"*30 + "\n")
            print(answer)
            
        
        usage = response['usage']
        completion_tokens = usage["completion_tokens"]
        prompt_tokens = usage["prompt_tokens"]
        total_tokens = usage["total_tokens"]
        print(f"\nUsage: {total_tokens}, (p: {prompt_tokens}, c: {completion_tokens}), {self.s.openAiSettings.model}")

        if not function_response:
            print("\nERROR: No function call made by GPT!")
        return (answer, function_response)
    

    def chatCompleationCall(self, stopStreamOverride=False):
        stream = self.stream
        if stopStreamOverride:
            stream=False

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            messages=self.chatHistory,
            stream=stream)

        print("\nAssistant:")
        print("-"*30 + "\n")
        if self.stream:
            answer = self.stream_chat(response)
        else:
            answer = response['choices'][0]['message']['content']
            print(answer)
            
            usage = response['usage']
            completion_tokens = usage["completion_tokens"]
            prompt_tokens = usage["prompt_tokens"]
            total_tokens = usage["total_tokens"]
            print(f"Usage: {total_tokens}, (p: {prompt_tokens}, c: {completion_tokens}), {self.s.openAiSettings.model}")

        return answer
    
    def stream_chat(self, response):
        collected_chunks = []
        collected_messages = []
        textContent = []

        for chunk in response:
            collected_chunks.append(chunk)
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)

            if 'content' in chunk_message:
                text = chunk_message['content']
                print(text, end='', flush=True)
                textContent.append(text)
        print()

        textResult = "".join(textContent)
        # print('collected_chunks')
        # print(collected_chunks)
        return textResult
    
    def format_chat_message(self, chatMessage):
        # TODO: support function calls? Maybe those should be excluded from history.
        text = ''
        text += chatMessage['role']
        text += "\n" + "-"*30 + "\n"
        if chatMessage['content']:
            text += chatMessage['content']
        if 'function_call' in chatMessage and chatMessage['function_call']: 
            fc_chat_message = chatMessage['function_call']
            # print('fc_chat_message:')
            # print(fc_chat_message)
            text += str(fc_chat_message)
        return text



if __name__ == '__main__':
    s = Settings()
    chatAgent = ChatAgent(s)
    userMessage = "Hello there!"
    answer = chatAgent.chat(userMessage)
    # print(answer)
