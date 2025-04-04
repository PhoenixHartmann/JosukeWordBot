import logging
import asyncio
from background import keep_alive
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import pymorphy2

API_TOKEN = '7963543492:AAEh2tnLbplI5bNN2CnLQYPhBpJ50mVf0_0'  # ЗАМЕНИ на свой токен!

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Морфологический анализатор для обработки слов
morph = pymorphy2.MorphAnalyzer()

# Список запрещенных слов (в начальной форме)
TRIGGER_WORDS = {"дом", "пример", "предложение", "вариант"}

# Ответное сообщение
RESPONSE_TEXT = "Пред\nЗапретка"

def normalize_words(text):
    """Функция, которая приводит слова к начальной форме"""
    words = text.lower().split()
    normalized_words = {morph.parse(word)[0].normal_form for word in words}
    return normalized_words

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    """Обработчик команды /start и /help"""
    await message.reply("Привет! Я бот, который следит за сообщениями 🚨")

@dp.message()
async def check_message(message: types.Message):
    """Проверяет сообщение на наличие запрещенных слов"""
    if TRIGGER_WORDS & normalize_words(message.text):
        await message.reply(RESPONSE_TEXT)

async def main():
    """Запуск бота"""
    await bot.delete_webhook(drop_pending_updates=True)  # Чистит старые сообщения при запуске
    await dp.start_polling(bot)
    
async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
