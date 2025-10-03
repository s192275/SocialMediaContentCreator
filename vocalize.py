from gtts import gTTS
from llm import LLM
from pydub import AudioSegment

class Vocalize():
    def __init__(self, content:str) -> None:
        self.llm = LLM(content)
        self.response = self.llm.generate_response()
        self.tts = gTTS(self.response, lang="tr")
        self.tts.save("sosyal_medya_icerik.mp3")
    
    def find_duration(self) -> int:
        audio = AudioSegment.from_file("sosyal_medya_icerik.mp3")
        duration_seconds = len(audio) / 1000 # ms -> s
        print(f"Seslendirme süresi: {duration_seconds:.2f} saniye")
        return int(duration_seconds)

    def return_script(self) -> str:
        return self.response