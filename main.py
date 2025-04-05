
import logging
import asyncio
import time
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
                        warning_msg = await message.answer_animation(
                            animation,
                            caption="Пред\nЧто ты сказал про мою прическу?"
                        )
                        await asyncio.sleep(10)
                        await warning_msg.delete()
                        return
                    except Exception as e:
                        if "retry after" in str(e).lower():
                            retry_after = int(str(e).split("retry after")[1].split()[0])
                            await sleep(retry_after)
                        else:
                            logging.error(f"Error sending message: {e}")
                            return

@dp.message(Command("chatid"))
async def cmd_chatid(message: types.Message):
    await message.reply(f"ID этого чата: {message.chat.id}")

@dp.message()
async def check_message(message: types.Message):
    await check_forbidden_words(message)

@dp.edited_message()
async def check_edited_message(message: types.Message):
    await check_forbidden_words(message)

async def broadcast_time():
    while True:
        try:
            current_time = time.strftime("%H:%M")
            # Замените CHAT_ID на ID вашего чата или группы
            chat_id = input("Введите ID чата или группы куда отправлять время: ")
            await bot.send_message(chat_id=chat_id, text=f"What time is it? {current_time}")
            print(f"Sent time message: {current_time}")
        except Exception as e:
            print(f"Error sending time: {e}")
        await asyncio.sleep(60)

async def main():
    keep_alive()
    asyncio.create_task(broadcast_time())
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Polling error: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
