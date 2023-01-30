import requests
from dotenv import load_dotenv
import os
from telegram import Bot
import asyncio
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_API')
chat_id = "1678406668"
message = "deneme mesaji"

url_bot_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

url_info = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

def send_audio_with_telegram(chat_id: str, file_path: str, post_file_title: str, bot_token: str) -> None:
    with open(file_path, 'rb') as audio:
        payload = {
            'chat_id': chat_id,
            'title': post_file_title,
            'parse_mode': 'HTML'
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=bot_token),
            data=payload,
            files=files).json()
 
#send_audio_with_telegram(chat_id=chat_id, 
#                         file_path='response.mp3',
#                         post_file_title='received-response.mp3', 
#                         bot_token=TOKEN)   

    

print(requests.get(url=url_info).json()['result'][-1]['message']['text'])