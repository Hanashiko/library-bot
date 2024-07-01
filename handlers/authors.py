from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.authors_db import AuthorManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find


async def command_create_table_authors(message: types.Message) -> None:
	AuthorManager.create_table()
	await message.reply("Створив таблицю авторів")

async def command_delete_table_authors(message: types.Message) -> None:
	AuthorManager.delete_table()
	await message.reply("Видалив таблицю авторів")

async def command_add_author(message: types.Message) -> None:
	await FSMAuthor.Add.author_name.set()
	await message.reply("Напишіть ім'я автора:")
	await cancel_notification(message)

async def command_add_author_name(message: types.Message, state: FSMContext) -> None:
	name: Optional[str] = await validation_name(message)
	if name is None: return
	async with state.proxy() as data:
		data['name'] = name
	await FSMAuthor.Add.next()
	await message.reply("Введіть прізвище автора")

async def command_add_author_surname(message: types.Message, state: FSMContext) -> None:
	surname: Optional[str] = await validation_name(message)
	if surname is None: return
	async with state.proxy() as data:
		name: str = data['name']

	author_exists = AuthorManager.author_exists(name=name, surname=surname)
	if author_exists:
		author_id: int = AuthorManager.get_id(name=name, surname=surname)[0]
		await message.reply(f"Такий автор вже є в базі даних.\nЙого id: {author_id}")
		return

	AuthorManager.add(name=name, surname=surname)
	author_id: int = AuthorManager.get_id(name=name, surname=surname)[0]

	await message.reply(f"Добавив автора:\nID: {author_id}\nІм'я: {name}; Прізвище: {surname}")
	await state.finish()

async def command_delete_author(message: types.Message) -> None:
	await FSMAuthor.Delete.author_id.set()
	await message.reply("Напишіть id автора:")
	await cancel_notification(message)

async def command_delete_author_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return
	author = AuthorManager.get(id=id)
	if not author:
		await not_find(message)
		return
	AuthorManager.delete(author_id=id)
	await message.reply(f"Видалив автора:\nid: {author[0]}; ім'я: {author[1]}; прізвище: {author[2]}")
	await state.finish()

async def command_edit_author(message: types.Message) -> None:
	await FSMAuthor.Edit.author_id.set()
	await message.reply("Напишіть id автора:")
	await cancel_notification(message)

async def command_edit_author_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	async with state.proxy() as data:
		data["id"] = id

	await FSMAuthor.Edit.next()
	await message.reply("Введіть ім'я автора")

async def command_edit_author_name(message: types.Message, state: FSMContext) -> None:
	name: Optional[str] = await validation_name(message)
	if name is None: return

	async with state.proxy() as data:
		data["name"] = name

	await FSMAuthor.Edit.next()
	await message.reply("Введіть прізвище автора")

async def command_edit_author_surname(message: types.Message, state: FSMContext) -> None:
	surname: Optional[str] = await validation_name(message)
	if surname is None: return

	async with state.proxy() as data:
		id: int = data["id"]
		name: str = data["name"]

	author: Optional[tuple] = AuthorManager.get(id=id)

	AuthorManager.edit(author_id=id, new_name=name, new_surname=surname)
	await message.reply(f"Відредагував автора (#{id}):\nСтарі данні:\nІм'я: {author[1]}; Прізвище: {author[2]}\nНові данні:\nІм'я: {name}; Прізвище: {surname}")
	await state.finish()

async def command_get_author(message: types.Message) -> None:
	await FSMAuthor.Get.author_id.set()
	await message.reply("Напишіть id автора:")
	await cancel_notification(message)

async def command_get_author_id(message: types.Message, state:FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	author: Optional[tuple] = AuthorManager.get(id=id)

	if author is None or not author:
		await not_find(message)
		return

	await message.reply(f"Інформація про автора:\nid: {author[0]}; ім'я: {author[1]}; прізвище: {author[2]}")
	await state.finish()

async def command_get_all_authors(message: types.Message) -> None:
	authors: list = AuthorManager.get_all()
	result: str = f"ID | Ім'я | Прізвище\n" 
	for author in authors:
		result += f"{author[0]} | {author[1]} | {author[2]}\n"
	await message.reply(f"Усі автори:\n{result}")


def register_handlers_authors(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_authors, lambda message: message.text == keyboards_text.Authors().create_table)
	dp.register_message_handler(command_delete_table_authors, lambda message: message.text == keyboards_text.Authors().delete_table)
	dp.register_message_handler(command_add_author, lambda message: message.text == keyboards_text.Authors().add)
	dp.register_message_handler(command_add_author_name, state=FSMAuthor.Add.author_name)
	dp.register_message_handler(command_add_author_surname, state=FSMAuthor.Add.author_surname)
	dp.register_message_handler(command_delete_author, lambda message: message.text == keyboards_text.Authors().delete)
	dp.register_message_handler(command_delete_author_id, state=FSMAuthor.Delete.author_id)
	dp.register_message_handler(command_edit_author, lambda message: message.text == keyboards_text.Authors().edit)
	dp.register_message_handler(command_edit_author_id, state=FSMAuthor.Edit.author_id)
	dp.register_message_handler(command_edit_author_name, state=FSMAuthor.Edit.author_name)
	dp.register_message_handler(command_edit_author_surname, state=FSMAuthor.Edit.author_surname)
	dp.register_message_handler(command_get_author, lambda message: message.text == keyboards_text.Authors().get)
	dp.register_message_handler(command_get_author_id, state=FSMAuthor.Get.author_id)
	dp.register_message_handler(command_get_all_authors, lambda message: message.text == keyboards_text.Authors().get_all)