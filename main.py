import logging
import asyncio
from threading import Thread

from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile

API_TOKEN = 'тут_замени_на_твой_токен'  # Никогда не храни токен в коде, используй переменные окружения!

# Запускаем Flask-сервер
app = Flask(__name__)

@app.route('/')
def index():
    return 'Бот работает ✅'

# aiogram setup
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

FORBIDDEN_WORDS = ['хуй', 'пример', 'плохое_слово3']

from asyncio import sleep

async def check_forbidden_words(message: types.Message):
    if message.text:
        text_lower = message.text.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in text_lower:
                try:
                    await message.delete()
                    animation = FSInputFile("josuke_angry.gif")
                    warning_msg = await message.answer_animation(
                        animation,
                        caption="Пред\nЧто ты сказал про мою прическу?")
                    await asyncio.sleep(10)
                    await warning_msg.delete()
                except Exception as e:
                    if "retry after" in str(e).lower():
                        retry_after = int(
                            str(e).split("retry after")[1].split()[0])
                        await sleep(retry_after)
                    else:
                        logging.error(f"Error: {e}")
                return

@dp.message()
async def check_message(message: types.Message):
    await check_forbidden_words(message)

@dp.edited_message()
async def check_edited_message(message: types.Message):
    await check_forbidden_words(message)

async def start_bot():
    await dp.start_polling(bot)

def start_aiogram():
    asyncio.run(start_bot())

# Flask и aiogram будут работать параллельно
if __name__ == '__main__':
    Thread(target=start_aiogram).start()
    app.run(host="0.0.0.0", port=10000)
