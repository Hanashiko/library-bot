from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from keyboards.keyboards_text import *

text = Borrows()

b1 = KeyboardButton(text.create_table)
b2 = KeyboardButton(text.delete_table)
b3 = KeyboardButton(text.add)
b4 = KeyboardButton(text.delete)
b5 = KeyboardButton(text.edit)
b6 = KeyboardButton(text.edit_returned)
b7 = KeyboardButton(text.get)
b8 = KeyboardButton(text.get_all)
b9 = KeyboardButton(text.not_returned)
b10 = KeyboardButton(text.overdue)
b11 = KeyboardButton(main_menu)

kb_borrows = ReplyKeyboardMarkup(resize_keyboard=True)

# kb_borrows.row(b1,b2).row(b3,b4,b5,b6).row(b7,b8).row(b9,b10).add(b11)
kb_borrows.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11)