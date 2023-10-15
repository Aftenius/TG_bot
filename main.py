import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, BotCommandScopeDefault, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message

import json
import sys
import logging
import keyboards
import TOKEN

token = TOKEN.TG_API_KEY


def read_json(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []


def write_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)


def post_id(new_data):
    existing_data = read_json("output.json")
    for sublist in existing_data:
        if sublist[0]['id'] == new_data[0]['id']:
            print('дa')
        else:
            existing_data.append(new_data)
            write_json("output.json", existing_data)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='/start',
            description='Запускает начальную настройку'
        ),
        BotCommand(
            command='/sendall',
            description="123"
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_session(message: Message, bot: Bot):
    img_url = 'https://uxui.one/images/world.png'
    await set_commands(bot)
    await message.answer(f"Добро пожаловать. Хотите подписаться на рассылку сообщений <a href='{img_url}'>?</a>", reply_markup=keyboards.subscribe_kb)


async def database_entry(call: CallbackQuery, bot: Bot):
    new_data = [
                {"name": call.from_user.first_name, "id": call.from_user.id}
            ]
    post_id(new_data)
    await call.message.answer(f"{call.from_user.first_name} <b>вы подписались на сообщения, скоро вы их получите.</b>")
    await call.answer()


async def send_all(message: Message, bot: Bot):
    if message.chat.type == 'private':
        if message.from_user.id == 908849227:
            text = message.text[9:]
            existing_data = read_json("output.json")
            id_values = id_values = set(sublist[0]["id"] for sublist in existing_data)
            for i in id_values:
                try:
                    await bot.send_message(i, text)

                except:
                    pass


async def no_words(message: Message, bot: Bot):
    await message.answer(f"Я вас не понимаю <b>{message.from_user.id}</b>")


# Запуск бота и логирование
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()

    dp.callback_query.register(database_entry, F.data == 'Подписаться')
    dp.message.register(send_all, Command(commands=['sendall']))
    dp.message.register(start_session, CommandStart())
    dp.message.register(no_words)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())

