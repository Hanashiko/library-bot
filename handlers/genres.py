from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.genres_db import GenreManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find

async def command_create_table_genres(message: types.Message) -> None:
	GenreManager.create_table()
	await message.reply("Створив таблицю жанрів")

async def command_delete_table_genres(message: types.Message) -> None:
	genres_db.delete_table()
	await message.reply("Видалив таблицю жанрів")

async def command_add_genre(message: types.Message) -> None:
	await FSMGenres.Add.genre_name.set()
	await message.reply("Напишіть назву жанра")
	await cancel_notification(message)

async def command_add_genre_name(message: types.Message, state: FSMContext) -> None:
	name: Optional[str] = await validation_name(message)
	if name is None: return

	genre_exists = GenreManager.genre_exists(name=name)
	if genre_exists:
		genre_id: int = GenreManager.get_id(name=name)[0]
		await message.reply(f"Такий жанр вже є в базі даних.\nЙого id: {genre_id}")
		return

	GenreManager.add(name=name)
	genre_id: int = GenreManager.get_id(name=name)[0]

	await message.reply(f"Добавив жанр: {name}.\nЙого id: {genre_id}")
	await state.finish()

async def comamnd_delete_genre(message: types.Message) -> None:
	await FSMGenres.Delete.genre_id.set()
	await message.reply("Напишіть id жанру")
	await cancel_notification(message)

async def comamnd_delete_genre_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return
	genre_exists = GenreManager.get(id=id)
	if not genre_exists:
		await not_find(message)
		return
	genre: Optional[tuple] = GenreManager.get(id=id)
	genre_name: str = genre[1]
	GenreManager.delete(id=id)
	await message.reply(f"Видалив жанр:\nid: {id}\nНазва: {genre_name}")
	await state.finish()

async def command_edit_genre(message: types.Message) -> None:
	await FSMGenres.Edit.genre_id.set()
	await message.reply("Напишіть id жанру")
	await cancel_notification(message)

async def command_edit_genre_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	genre_exists: Optional[tuple] = GenreManager.get(id=id)
	if not genre_exists:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['id'] = id

	await FSMGenres.Edit.next()
	await message.reply("Введіть нову назву жанра")

async def command_edit_genre_name(message: types.Message, state: FSMContext) -> None:
	genre_name: Optional[str] = await validation_name(message)
	if genre_name is None: return

	async with state.proxy() as data: 
		genre_id: int = data['id']

	old_genre: Optional[tuple] = GenreManager.get(id=genre_id)
	if not old_genre:
		await not_find(message)
		return
	old_genre_name: str = old_genre[1]

	check_name = GenreManager.get_id(name=genre_name)
	if check_genre:
		await message.reply("Уже є жанр з такою назвою.\nЙого id: ")
		return

	GenreManager.edit(id=genre_id, new_name=genre_name)
	await message.reply(f"Відредагував жанр (#{genre_id}):\nСтара назва: {old_genre_name}\nНова назва: {genre_name}")
	await state.finish()

async def command_get_genre(message: types.Message) -> None:
	await FSMGenres.Get.genre_id.set()
	await message.reply("Напишіть id жанру")
	await cancel_notification(message)

async def command_get_genre_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	genre: Optional[tuple] = GenreManager.get(id=id)

	if genre is None or not genre:
		await not_find(message)
		return

	genre_name: str = genre[1]

	await message.reply(f"Інформація про жанр:\nid: {id}\nНазва: {genre_name}")
	await state.finish()

async def command_get_all_genres(message: types.Message) -> None:
	genres: list = GenreManager.get_all()
	result: str = f"ID | Name\n"
	for genre in genres:
		result += f"{genre[0]} | {genre[1]}\n"
	await message.reply(f"Усі жанри:\n{result}")


def register_handlers_genres(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_genres, lambda message: message.text == keyboards_text.Genres().create_table)
	dp.register_message_handler(command_create_table_genres, lambda message: message.text == keyboards_text.Genres().delete_table)
	dp.register_message_handler(command_add_genre, lambda message: message.text == keyboards_text.Genres().add)
	dp.register_message_handler(command_add_genre_name, state=FSMGenres.Add.genre_name)
	dp.register_message_handler(comamnd_delete_genre, lambda message: message.text == keyboards_text.Genres().delete)
	dp.register_message_handler(comamnd_delete_genre_id, state=FSMGenres.Delete.genre_id)
	dp.register_message_handler(command_edit_genre, lambda message: message.text == keyboards_text.Genres().edit)
	dp.register_message_handler(command_edit_genre_id, state=FSMGenres.Edit.genre_id)
	dp.register_message_handler(command_edit_genre_name, state=FSMGenres.Edit.genre_name)
	dp.register_message_handler(command_get_genre, lambda message: message.text == keyboards_text.Genres().get)
	dp.register_message_handler(command_get_genre_id, state=FSMGenres.Get.genre_id)
	dp.register_message_handler(command_get_all_genres, lambda message: message.text == keyboards_text.Genres().get_all)