from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = BookAuthor()

b1 = KeyboardButton(text.create_table)
b2 = KeyboardButton(text.delete_table)
b3 = KeyboardButton(text.add)
b4 = KeyboardButton(text.delete)
b5 = KeyboardButton(text.get_by_author)
b6 = KeyboardButton(text.get_by_book)
b7 = KeyboardButton(text.get_all)
b8 = KeyboardButton(main_menu)

kb_book_author = ReplyKeyboardMarkup(resize_keyboard=True)

kb_book_author.row(b1,b2).row(b3,b4).row(b5,b6,b7).add(b8)