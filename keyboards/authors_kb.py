from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = Authors()

b1 = KeyboardButton(text.create_table)
b2 = KeyboardButton(text.delete_table)
b3 = KeyboardButton(text.add)
b4 = KeyboardButton(text.delete)
b5 = KeyboardButton(text.edit)
b6 = KeyboardButton(text.get)
b7 = KeyboardButton(text.get_all)
b8 = KeyboardButton(main_menu)


kb_authors = ReplyKeyboardMarkup(resize_keyboard=True)

kb_authors.row(b1,b2).row(b3,b4,b5).row(b6,b7).add(b8)