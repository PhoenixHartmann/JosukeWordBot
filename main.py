
from flask import Flask, request
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
import asyncio
from aiohttp import web
import ssl

# Configuration
API_TOKEN = '7963543492:AAEh2tnLbplI5bNN2CnLQYPhBpJ50mVf0_0'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
APP_URL = 'https://' + input("Введите URL вашего Replit (например: my-bot.username.repl.co): ")
WEBHOOK_URL = APP_URL + WEBHOOK_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = web.Application()

# Список запрещенных слов
FORBIDDEN_WORDS = ['хуй', 'пример', 'плохое_слово3']

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
                        caption="Пред\nЧто ты сказал про мою прическу?"
                    )
                    await asyncio.sleep(10)
                    await warning_msg.delete()
                except Exception as e:
                    logging.error(f"Error processing message: {e}")

@dp.message()
async def check_message(message: types.Message):
    await check_forbidden_words(message)

@dp.edited_message()
async def check_edited_message(message: types.Message):
    await check_forbidden_words(message)

async def on_startup(app):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle_webhook(request):
    if request.match_info.get('token') == API_TOKEN:
        update = types.Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot=bot, update=update)
        return web.Response()
    return web.Response(status=403)

app.router.add_post(f'/webhook/{API_TOKEN}', handle_webhook)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
