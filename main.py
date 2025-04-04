
import logging
import asyncio
from background import keep_alive
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile

API_TOKEN = '7963543492:AAEh2tnLbplI5bNN2CnLQYPhBpJ50mVf0_0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список запрещенных слов
FORBIDDEN_WORDS = ['хуй', 'пример', 'плохое_слово3']

from asyncio import sleep

async def check_forbidden_words(message: types.Message):
    if message.text:
        text_lower = message.text.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in text_lower:
                while True:
                    try:
                        # Delete the message with forbidden word
                        await message.delete()
                        # Send warning with animation
                        animation = FSInputFile("josuke_angry.gif")
                        await message.answer_animation(
                            animation,
                            caption="Пред\nЧто ты сказал про мою прическу?"
                        )
                        return
                    except Exception as e:
                        if "retry after" in str(e).lower():
                            retry_after = int(str(e).split("retry after")[1].split()[0])
                            await sleep(retry_after)
                        else:
                            logging.error(f"Error sending message: {e}")
                            return

@dp.message()
async def check_message(message: types.Message):
    await check_forbidden_words(message)

@dp.edited_message()
async def check_edited_message(message: types.Message):
    await check_forbidden_words(message)

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
