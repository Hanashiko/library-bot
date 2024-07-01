from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = Books()

b1 = KeyboardButton(text.create_table)
b2 = KeyboardButton(text.delete_table)
b3 = KeyboardButton(text.add)
b4 = KeyboardButton(text.delete)
b5 = KeyboardButton(text.edit)
b6 = KeyboardButton(text.get)
b11 = KeyboardButton(text.popular_books)
b7 = KeyboardButton(text.get_all)
b8 = KeyboardButton(text.book_by_author)
b9 = KeyboardButton(text.book_by_name)
b10 = KeyboardButton(text.book_by_genre)
b12 = KeyboardButton(main_menu)

kb_books = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_books.row(b1,b2).row(b3,b4,b5).row(b6,b11,b7,b8,b9,b10).add(b12)
# kb_books.row(b1,b2).row(b3,b4,b5).row(b6,b11,b7).row(b8,b9,b10).add(b12)
kb_books.add(b1,b2,b3,b4,b5,b6,b11,b7,b8,b9,b10,b12)