import requests
import environment as env

class LLMHelper:
    def __init__(self):
        self.organization_id = env.get_openai_organization_id()
        self.api_key = env.get_openai_api_key()

    def __get_openai_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Organization": self.organization_id
        }
    
    def __get_openai_data(self, prompt):
        return {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000
        }
    
    def __get_openai_url(self):
        return "https://api.openai.com/v1/chat/completions"
    
    def __process_openai_response(self, response):
        if response.status_code == 200:
            return response.json().get("choices")[0].get("message").get("content").strip()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def get_translation(self, input_string):
        prompt = f"For '{input_string}', what is it's english meaning, chinese meaning? Please give me themorphology, etymology and mnemonics descriptions of it as well. Please use json format, do not use tab character, prompt should be encoded as text string value of 'prompt' key, english meaning should be encode as text string value of 'english_meaning' key, chinese meaning should be encode as text string value of 'chinese_meaning' key, morphology description should be encode as text string value of 'morphology' key, etymology description should be encode as text string value of 'etymology' key, mnemonics description should be encode as text string value of 'mnemonics' key."
        response = requests.post(self.__get_openai_url(), headers=self.__get_openai_headers(), json=self.__get_openai_data(prompt))
        return self.__process_openai_response(response)

    def get_question_about(self, input_string):
        prompt = f"Could you give a single choice question regarding '{input_string}'. Please use json format, do not use tab character, question should be encoded as the text string value of 'question' key, options should be encoded as a map of text string values for 'options' key, correct answer should be encoded as the value of 'answer' key."
        response = requests.post(self.__get_openai_url(), headers=self.__get_openai_headers(), json=self.__get_openai_data(prompt))
        return self.__process_openai_response(response)
    