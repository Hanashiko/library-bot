from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.users_db import UsersManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find

async def command_create_table_users(message: types.Message) -> None:
	UsersManager.create_table()
	await message.reply("Створив таблицю користувачів")

async def comamnd_delete_table_users(message: types.Message) -> None:
	UsersManager.delete_table()
	await message.reply("Видалив таблицю користувачів")

async def command_add_user(message: types.Message) -> None:
	await FSMUsers.Add.user_name.set()
	await message.reply("Напишіть ім'я користувача")
	await cancel_notification(message)

async def command_add_user_name(message: types.Message, state: FSMContext) -> None:
	name: Optional[str] = await validation_name(message)
	if name is None: return

	async with state.proxy() as data:
		data['name'] = name

	await FSMUsers.Add.next()
	await message.reply("Введіть прізвище користувача")

async def command_add_user_surname(message: types.Message, state: FSMContext) -> None:
	surname: Optional[str] = await validation_name(message)
	if surname is None: return
	
	async with state.proxy() as data:
		data['surname'] = surname

	await FSMUsers.Add.next()
	await message.reply("Введіть номер телефону користувача\nЯкщо у нього відсутній номер телефону, можете написати просто 0")

async def command_add_user_phone(message: types.Message, state: FSMContext) -> None:
	phone: Optional[int] = await validation_int(message)
	if phone is None: return

	async with state.proxy() as data:
		name: str = data['name']
		surname: str = data['surname']

	UsersManager.add(name=name, surname=surname, phone=phone)		
	user_id: int = UsersManager.get_id(name=name, surname=surname)[0]

	await message.reply(f"Добавив користувача:\nID: {user_id}\nІм'я: {name}\nПрізвище: {surname}\nТелефон: {phone}")
	await state.finish()

async def command_delete_user(message: types.Message) -> None:
	await FSMUsers.Delete.user_id.set()
	await message.reply("Напишіть id користувача")
	await cancel_notification(message)

async def command_delete_user_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return
	user = UsersManager.get(id=id)
	if not user:
		await not_find(message)
		return

	UsersManager.delete(id=id)
	user_name: str = user[1]
	user_surname: str = user[2]
	user_phone: int = user[3]
	await message.reply(f"Видалив користувача:\nid: {id}; Ім'я: {user_name}; Прізвище: {user_surname}; Телефон: {user_phone}")
	await state.finish()

async def command_edit_user(message: types.Message) -> None:
	await FSMUsers.Edit.user_id.set()
	await message.reply("Напишіть id користувача")
	await cancel_notification(message)

async def command_edit_user_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	async with state.proxy() as data:
		data['id'] = id

	await FSMUsers.Edit.next()
	await message.reply("Введіть ім'я користувача")

async def command_edit_user_name(message: types.Message, state: FSMContext) -> None:
	name: Optional[str] = await validation_name(message)
	if name is None: return

	async with state.proxy() as data:
		data['name'] = name

	await FSMUsers.Edit.next()
	await message.reply("Введіть прізвище користувача")

async def command_edit_user_surname(message: types.Message, state: FSMContext) -> None:
	surname: Optional[str] = await validation_name(message)
	if surname is None: return

	async with state.proxy() as data:
		data['surname'] = surname

	await FSMUsers.Edit.next()
	await message.reply("Введіть номер телефону користувача\nЯкщо у нього відсутній номер телефону, можете написати просто 0")

async def command_edit_user_phone(message: types.Message, state: FSMContext) -> None:
	phone: Optional[int] = await validation_int(message)
	if phone is None: return

	async with state.proxy() as data:
		user_id: int = data['id']
		user_name: str = data['name']
		user_surname: str = data['surname']
		user_phone: int = phone

	old_user: Optional[tuple] = UsersManager.get(id=user_id)
	old_user_name: str = old_user[1]
	old_user_surname: str = old_user[2]
	old_user_phone: int = old_user[3]

	UsersManager.edit(id=user_id, new_name=user_name, new_surname=user_surname, new_phone=phone)

	await message.reply(f"Відредагував користувача (#{user_id});\nСтарі дані:\nІм'я: {old_user_name}; Прізвище: {old_user_surname}; Телефон: {old_user_phone}\nНові дані:\nІм'я: {user_name}; Прізвище: {user_surname}; Телефон: {user_phone}")
	await state.finish()

async def command_get_user(message: types.Message) ->  None:
	await FSMUsers.Get.user_id.set()
	await message.reply("Напишіть id користувача")
	await cancel_notification(message)

async def command_get_user_id(message: types.Message, state: FSMContext) -> None:
	user_id: Optional[int]  = await validation_int(message)
	if user_id is None: return

	user: Optional[tuple] = UsersManager.get(id=user_id)

	if user is None or not user:
		await not_find(message)
		return

	user_id: int = user[0]
	user_name: str = user[1]
	user_surname: str = user[2]
	user_phone: int = user[3]

	await message.reply(f"Інформація про користувача:\nid: {user_id}; Ім'я: {user_name}; Прізвище: {user_surname}; Телефон: {user_phone}")
	await state.finish()

async def command_get_all_users(message: types.Message) -> None:
	users: list = UsersManager.get_all()
	result: str = f"ID | Ім'я | Прізвище | Телефон\n"
	for user in users:
		user_id: int = user[0]
		user_name: str = user[1]
		user_surname: str = user[2]
		user_phone: int = user[3]
		result += f"{user_id} | {user_name} | {user_surname} | {user_phone}\n"
	await message.reply(f"Усі користувачі:\n{result}")


def register_handlers_users(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_users, lambda message: message.text == keyboards_text.Users().create_table)
	dp.register_message_handler(comamnd_delete_table_users, lambda message: message.text == keyboards_text.Users().delete_table)
	dp.register_message_handler(command_add_user, lambda message: message.text == keyboards_text.Users().add)
	dp.register_message_handler(command_add_user_name, state=FSMUsers.Add.user_name)
	dp.register_message_handler(command_add_user_surname, state=FSMUsers.Add.user_surname)
	dp.register_message_handler(command_add_user_phone, state=FSMUsers.Add.user_phone)
	dp.register_message_handler(command_delete_user, lambda message: message.text == keyboards_text.Users().delete)
	dp.register_message_handler(command_delete_user_id, state=FSMUsers.Delete.user_id)
	dp.register_message_handler(command_edit_user, lambda message: message.text == keyboards_text.Users().edit)
	dp.register_message_handler(command_edit_user_id, state=FSMUsers.Edit.user_id)
	dp.register_message_handler(command_edit_user_name, state=FSMUsers.Edit.user_name)
	dp.register_message_handler(command_edit_user_surname, state=FSMUsers.Edit.user_surname)
	dp.register_message_handler(command_edit_user_phone, state=FSMUsers.Edit.user_phone)
	dp.register_message_handler(command_get_user, lambda message: message.text == keyboards_text.Users().get)
	dp.register_message_handler(command_get_user_id, state=FSMUsers.Get.user_id)
	dp.register_message_handler(command_get_all_users, lambda message: message.text == keyboards_text.Users().get_all)