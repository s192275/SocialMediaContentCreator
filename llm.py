from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

class LLM():
    def __init__(self, user_input:str) -> None:
        self.user_input = user_input
    
    def generate_response(self) -> str:
        response = client.models.generate_content(
                    model = 'gemini-2.5-flash',
                    config = types.GenerateContentConfig(
                        system_instruction = """Sen bir sosyal medya içerik üretme uzmanısın. 
                        Sana verilen içerik fikri ile alakalı sosyal medya için bir metin üret.
                        Ürettiğin metinde emoji ve hashtag kullanma."""),
                        contents = self.user_input
                        )
        return response.text