from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = Genres()

b1 = KeyboardButton(text.create_table)
b2 = KeyboardButton(text.delete_table)
b3 = KeyboardButton(text.add)
b4 = KeyboardButton(text.delete)
b5 = KeyboardButton(text.get)
b6 = KeyboardButton(text.edit)
b7 = KeyboardButton(text.get_all)
b8 = KeyboardButton(main_menu)

kb_genres = ReplyKeyboardMarkup(resize_keyboard=True)

kb_genres.row(b1,b2).row(b3,b4).row(b5,b6,b7).add(b8)