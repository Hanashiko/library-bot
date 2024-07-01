from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = General()

b1 = KeyboardButton(text.books)
b2 = KeyboardButton(text.borrows)
b3 = KeyboardButton(text.users)
b4 = KeyboardButton(text.authors)
b5 = KeyboardButton(text.book_author)
b6 = KeyboardButton(text.genres)
b7 = KeyboardButton(text.book_genre)

kb_general = ReplyKeyboardMarkup(resize_keyboard=True)

kb_general.row(b1,b2,b3).row(b4,b6).row(b5,b7)