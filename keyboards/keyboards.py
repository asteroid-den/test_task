# Since this bot is kinda low-functional, I don't see the point in distributing
# keyboards in separate files. For real, there's only 2 keyboards.

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from . import buttons_text

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons_text.my_addresses)],
        [KeyboardButton(text=buttons_text.add_address)],
    ],
    resize_keyboard=True,
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons_text.cancel)],
    ],
    resize_keyboard=True,
)
