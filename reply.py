from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message,ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Это кнопочка для игры
reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="PLAY A GAME!"
        )
    ],
],resize_keyboard=True,one_time_keyboard=True)

# Кнопка для той функции, где я хотел передать анкету мужичка в другой хэндлер
you_detected = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Кто это?")],
],resize_keyboard=True,one_time_keyboard=True)

# Клава для выбора пола
keyboard = ReplyKeyboardMarkup(keyboard= [
				[KeyboardButton(text ="MAN")],
				[KeyboardButton(text ="WOMAN")],
			],resize_keyboard=True, one_time_keyboard=True)

which_one = ReplyKeyboardMarkup(keyboard= [
        	[KeyboardButton(text ="Я парень🤠")],
       		[KeyboardButton(text ="Я девушка💁‍♀️")],
    		],resize_keyboard=True,one_time_keyboard=True)