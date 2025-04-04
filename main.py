import logging
import asyncio
from background import keep_alive
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart, Text

API_TOKEN = '7963543492:AAEh2tnLbplI5bNN2CnLQYPhBpJ50mVf0_0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message(Text(regexp='(^cat[s]?$|puss)'))
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())