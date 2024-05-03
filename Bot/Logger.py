from datetime import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class TelegramLogger():
    def __init__(self, message: str):
        ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.Zeitstempel = ts
        self.message = [(self.Zeitstempel, message)]
        self.TOKEN = os.getenv("TBOT_TOKEN")
        self.CHAT_ID = os.getenv("TBOT_LukasMeinzer_CHAT_ID")
        self.releaseMessage = None

    def neueMessage(self, message: str):
        ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.message.append((ts, message))
        
    def release(self):
        ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.message.append((ts, "Released"))
        
        self.releaseMessage = "\n".join(["\t".join(item) for item in self.message])
        
        send_url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={self.releaseMessage}"
        requests.get(send_url)