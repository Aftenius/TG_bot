from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButtonPollType
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder

subscribe_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Подписаться",
            callback_data="Подписаться"
        )
    ]
])

