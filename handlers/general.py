from aiogram import types, Dispatcher
from create_bot import dp, bot
from typing import Optional
from datetime import datetime
from handlers.validation import *
from keyboards import *
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from database.backup_db import create_backup

async def command_start(message: types.Message) -> None:
	await message.reply("Привіт. Виберіть розділ взаємодії:",reply_markup=kb_general)

async def command_backup(message: types.Message) -> None:
	backup_file = create_backup()
	if backup_file:
		with open(backup_file, 'rb') as file:
			await message.reply_document(file)
	else:
		await message.reply("Проблеми з створенням резервної копії")

async def command_authors(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом авторів:",reply_markup=kb_authors)

async def command_main_menu(message: types.Message) -> None:
	await message.reply("Виберіть розділ взаємодії:",reply_markup=kb_general)

async def command_book_author(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом зв'язку книга & автор:\n||к&а \- книга & автоар||", reply_markup=kb_book_author, parse_mode="MarkdownV2")

async def command_book_genre(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом зв'язку книга & жанр:\n||к&ж \- книга & жанр||", reply_markup=kb_book_genre, parse_mode="MarkdownV2")

async def command_books(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом книг:", reply_markup=kb_books)

async def command_borrows(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом боргів:", reply_markup=kb_borrows)

async def command_genres(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом жанрів:", reply_markup=kb_genres)

async def command_users(message: types.Message) -> None:
	await message.reply("Виберіть подальші дії з розділом користувачів:", reply_markup=kb_users)

async def command_cancel(message: types.Message, state: FSMContext) -> None:
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply("ОК")

async def cancel_notification(message: types.Message) -> None:
	await message.reply("Для відміни дії використовуйте /cancel")

async def not_find(message: types.Message) -> None:
	await message.reply("Не знайшов запису за цим індентифікатором")

def register_handlers_general(dp: Dispatcher) -> None:
	dp.register_message_handler(command_start, commands=['start'])
	dp.register_message_handler(command_backup, commands=['backup'])
	dp.register_message_handler(command_cancel, state="*", commands="cancel")
	dp.register_message_handler(command_authors, lambda message: message.text == keyboards_text.General().authors)
	dp.register_message_handler(command_main_menu, lambda message: message.text == keyboards_text.main_menu)
	dp.register_message_handler(command_book_author, lambda message: message.text == keyboards_text.General().book_author)
	dp.register_message_handler(command_book_genre, lambda message: message.text == keyboards_text.General().book_genre)
	dp.register_message_handler(command_books, lambda message: message.text == keyboards_text.General().books)
	dp.register_message_handler(command_borrows, lambda message: message.text == keyboards_text.General().borrows)
	dp.register_message_handler(command_genres, lambda message: message.text == keyboards_text.General().genres)
	dp.register_message_handler(command_users, lambda message: message.text == keyboards_text.General().users)
