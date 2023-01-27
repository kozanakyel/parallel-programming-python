from flask import Flask, request, jsonify, make_response 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import openai
from telegram import Bot
import asyncio
from gtts import gTTS
from io import BytesIO

load_dotenv()

app = Flask(__name__)

PSQL_USER_ENV=os.getenv('PSQL_USER')
PSQL_PWD_ENV=os.getenv('PSQL_PWD')
PSQL_URI_ENV=os.getenv('PSQL_URI')
PSQL_PORT_ENV=os.getenv('PSQL_PORT')
PSQL_DB_NAME_ENV=os.getenv('PSQL_DB_NAME')

CHATGPT_ENV=os.getenv('CHATGPT')

TELEGRAM_BOT_API_ENV = os.getenv('TELEGRAM_BOT_API')

openai.api_key = CHATGPT_ENV
bot = Bot(TELEGRAM_BOT_API_ENV)

async def send_telegram_message(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

@app.route('/question', methods=['POST'])
async def question():
    data = request.get_json()
    question = data['question']
    print(f'Question : {question}')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=256,
        n=1
    )
    response_text = response['choices'][0]['text']
    print(f'Response : {response_text}') 
    tts = gTTS(response_text, lang='tr', tld="com")
    tts.save('response.mp3')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    asyncio.ensure_future(send_telegram_message(bot=bot,
                                                chat_id='756050439',
                                                message=response_text))
    #bot.send_message(chat_id='756050439', text=response_text)
    return response_text

if __name__ == '__main__':
    app.run(debug=True)