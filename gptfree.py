from multiprocessing import Process
import asyncio

from flask import Flask
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

import TOKEN

app = Flask(__name__)

token = TOKEN.TG_API_KEY

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Добро пожаловать!')


async def main():
    await dp.start_polling(bot)


def run_bot():
    asyncio.run(main())


@app.route('/start_bot')
def start_bot():
    bot_process = Process(target=run_bot())
    bot_process.start()
    return "Bot process started!"


@app.route('/sign')
def sign_in():
    return 'hello world!!1'


if __name__ == '__main__':
    app.run()