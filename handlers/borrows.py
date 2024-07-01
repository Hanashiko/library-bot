from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.borrows_db import BorrowsManager
from database.users_db import UsersManager
from database.books_db import BooksManager
from database.book_author_db import BookAuthorManager
from database.authors_db import AuthorManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find

async def command_create_table_borrows(message: types.Message) -> None:
	BorrowsManager.create_table()
	await message.reply("Створив таблицю боргів")

async def comamnd_delete_table_borrows(message: types.Message) -> None:
	BorrowsManager.delete_table()
	await message.reply("Видалив таблицю боргів")

async def command_add_borrow(message: types.Message) -> None:
	await FSMBorrows.Add.user_id.set()
	await message.reply("Напишіть id користувача")
	await cancel_notification(message)

async def command_add_borrow_user_id(message: types.Message, state: FSMContext) -> None:
	user_id: Optional[int] = await validation_int(message)
	if user_id is None: return

	user: Optional[tuple] = UsersManager.get(id=user_id)
	if not user:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['user_id'] = user_id

	await FSMBorrows.Add.next()
	await message.reply("Введіть id книги")

async def command_add_borrow_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['book_id'] = book_id

	await FSMBorrows.Add.next()
	await message.reply("Введіть дату, коли взяли книгу")

async def command_add_borrow_taken_date(message: types.Message, state: FSMContext) -> None:
	taken_date: Optional[str] = await validation_date(message)
	if taken_date is None: return

	async with state.proxy() as data:
		data['taken_date'] = taken_date

	await FSMBorrows.Add.next()
	await message.reply("Введіть дату, коли повертають книгу")

async def command_add_borrow_end_date(message: types.Message, state: FSMContext) -> None:
	end_date: Optional[str] = await validation_date(message)
	if end_date is None: return

	async with state.proxy() as data:
		data['end_date'] = end_date

	await FSMBorrows.Add.next()
	await message.reply("Введіть стан повернення (0 - не повернули; 1 - повернули)")

async def command_add_borrow_returned(message: types.Message, state: FSMContext) -> None:
	returned: Optional[int] = await validation_int(message)
	if returned is None: return

	async with state.proxy() as data:
		user_id: int = data['user_id']
		book_id: int = data['book_id']
		taken_date: str = data['taken_date']
		end_date: str = data['end_date']

	BorrowsManager.add(user_id=user_id, book_id=book_id, taken_date=taken_date, end_date=end_date, returned=returned)
	borrow_id: int = BorrowsManager.get_id(user_id=user_id, book_id=book_id, taken_date=taken_date, end_date=end_date)[0]

	user: Optional[tuple] = UsersManager.get(id=user_id)
	book: Optional[tuple] = BooksManager.get(id=book_id)

	user_name: str = user[1]
	user_surname: str = user[2]
	book_title: str = book[1]
	book_year: int = book[2]

	await message.reply(f"Добавив борг:\nID боргу: {borrow_id}\nID користувача: {user_id}\nКористувач: {user_name} {user_surname}\nID книги: {book_id}\nКнига: {book_title} ({book_year})\nДата взятя: {taken_date:%Y-%m-%d}\nДата повернення: {end_date:%Y-%m-%d}\nСтан повернення: {returned}")
	await state.finish()

async def command_delete_borrow(message: types.Message) -> None:
	await FSMBorrows.Delete.borrow_id.set()
	await message.reply("Введіть id боргу")
	await cancel_notification(message)

async def command_delete_borrow_id(message: types.Message, state: FSMContext) -> None:
	borrow_id: Optional[int] = await validation_int(message)
	if borrow_id is None: return

	borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	if not borrow:
		await not_find(message)
		return

	user_id: int = borrow[1]
	book_id: int = borrow[2]

	user: Optional[tuple] = UsersManager.get(id=user_id)
	book: Optional[tuple] = BooksManager.get(id=book_id)

	taken_date: str = borrow[3]
	end_date: str = borrow[4]
	returned: int = borrow[5]
	user_name: str = user[1]
	user_surname: str = user[2]
	book_title: str = book[1]
	book_year: int = book[2]

	BorrowsManager.delete(id=borrow_id)

	await message.reply(f"Видалив борг:\nID боргу: {borrow_id}\nID користувача: {user_id}\nКористувач: {user_name} {user_surname}\nID книги: {book_id}\nКнига: {book_title} ({book_year})\nДата виадчі: {taken_date}\nДата повернення: {end_date}\nСтан повернення: {returned}")
	await state.finish()

async def command_edit_borrow(message: types.Message) -> None:
	await FSMBorrows.Edit.borrow_id_be.set()
	await message.reply("Напишіть id боргу")
	await cancel_notification(message)

async def command_edit_borrow_id(message: types.Message, state: FSMContext) -> None:
	borrow_id: Optional[int] = await validation_int(message)
	if borrow_id is None: return

	borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	if not borrow:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['borrow_id'] = borrow_id

	await FSMBorrows.Edit.next()
	await message.reply("Введіть id користувача")

async def command_edit_borrow_user_id(message: types.Message, state: FSMContext) -> None:
	user_id: Optional[int] = await validation_int(message)
	if user_id is None: return

	user: Optional[tuple] = UsersManager.get(id=user_id)
	if not user:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['user_id'] = user_id

	await FSMBorrows.Edit.next()
	await message.reply("Введіть id книги")

async def command_edit_borrow_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['book_id'] = book_id

	await FSMBorrows.Edit.next()
	await message.reply("Введіть дату видачі")

async def command_edit_borrow_taken_date(message: types.Message, state: FSMContext) -> None:
	taken_date: Optional[str] = await validation_date(message)
	if taken_date is None: return

	async with state.proxy() as data:
		data['taken_date'] = taken_date

	await FSMBorrows.Edit.next()
	await message.reply("Введіть дату повернення")

async def command_edit_borrow_end_date(message: types.Message, state: FSMContext) -> None:
	end_date: Optional[str] = await validation_date(message)
	if end_date is None: return

	async with state.proxy() as data:
		data['end_date'] = end_date

	await FSMBorrows.Edit.next()
	await message.reply("Введіть стан повернення (0 - не повернули; 1 - повернули)")

async def command_edit_borrow_returned(message: types.Message, state: FSMContext) -> None:
	returned: Optional[int] = await validation_int(message)
	if returned is None: return

	async with state.proxy() as data:
		borrow_id: int = data['borrow_id']
		user_id: int = data['user_id']
		book_id: int = data['book_id']
		taken_date: str = data['taken_date']
		end_date: str = data['end_date']

	old_borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	old_user_id: int = old_borrow[1]
	old_book_id: int = old_borrow[2]
	old_taken_date: str = old_borrow[3]
	old_end_date: str = old_borrow[4]
	old_returned: int = old_borrow[5]

	old_user: Optional[tuple] = UsersManager.get(id=old_user_id)
	old_book: Optional[tuple] = BooksManager.get(id=old_book_id)

	old_user_name: str = old_user[1]
	old_user_surname: str = old_user[2]
	old_book_title: str = old_book[1]
	old_book_year: int = old_book[2]

	user: Optional[tuple] = UsersManager.get(id=user_id)
	book: Optional[tuple] = BooksManager.get(id=book_id)

	user_name: str = user[1]
	user_surname: str = user[2]
	book_title: str = book[1]
	book_year: int = book[2]

	BorrowsManager.edit(borrow_id=borrow_id, new_user_id=user_id, new_book_id=book_id, new_taken_date=taken_date, new_end_date=end_date, new_returned=returned)

	result_message: str = f"Змінив інформацію про борг (#{borrow_id}):\n"
	result_message += f"\nСтірі дані:\nКористувач:\nID: {old_user_id}; Ім'я: {old_user_name}; Прізвище: {old_user_surname}\nКнига:\nID: {old_book_id}; Назва: {old_book_title}; Рік публікації: {old_book_year};\nДати:\nВзяття: {old_taken_date}; Повернення: {old_end_date}\nСтан повернення: {old_returned}\n"
	result_message += f"\nНові дані:\nКористувач:\nID: {user_id}; Ім'я: {user_name}; Прізвище: {user_surname}\nКнига:\nID: {book_id}; Назва: {book_title}; Рік публікації: {book_year};\nДати:\nВзяття: {taken_date:%Y-%m-%d}; Повернення: {end_date:%Y-%m-%d}\nСтан повернення: {returned}\n"

	await message.reply(result_message)
	await state.finish()

async def command_edit_returned_borrow(message: types.Message) -> None:
	await FSMBorrows.EditReturned.borrow_id_ber.set()
	await message.reply("Напишіть id боргу")
	await cancel_notification(message)

async def command_edit_returned_borrow_id(message: types.Message, state: FSMContext) -> None:
	borrow_id: Optional[int] = await validation_int(message)
	if borrow_id is None: return
	borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	if not borrow:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['borrow_id'] = borrow_id

	await FSMBorrows.EditReturned.next()
	await message.reply("Введіть стан повернення (0 - не повернули; 1 - повернули)")

async def command_edit_returned_borrow_returned(message: types.Message, state: FSMContext) -> None:
	returned: Optional[int] = await validation_int(message)
	if returned is None: return

	async with state.proxy() as data:
		borrow_id: int = data['borrow_id']

	old_borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	old_returned: int = old_borrow[5]

	BorrowsManager.edit_returned(borrow_id=borrow_id, returned=returned)
	await message.reply(f"В боргу #{borrow_id} змінив стан повернення з {old_returned} на {returned}")
	await state.finish()

async def command_get_borrow(message: types.Message) -> None:
	await FSMBorrows.Get.borrow_id_bg.set()
	await message.reply("Напишіть id боргу")
	await cancel_notification(message)

async def command_get_borrow_id(message: types.Message, state: FSMContext) -> None:
	borrow_id: Optional[int] = await validation_int(message)
	if borrow_id is None: return

	borrow: Optional[tuple] = BorrowsManager.get(id=borrow_id)
	if not borrow:
		await not_find(message)
		return

	user_id: int = borrow[1]
	book_id: int = borrow[2]
	taken_date: str = borrow[3]
	end_date: str = borrow[4]
	returned: int = borrow[5]

	user: Optional[tuple] = UsersManager.get(id=user_id)
	book: Optional[tuple] = BooksManager.get(id=book_id)

	user_name: str = user[1]
	user_surname: str = user[2]
	book_title: str = book[1]
	book_year: int = book[2]

	await message.reply(f"Інформація про борг:\nID боргу: {borrow_id}\nДата взятя: {taken_date}\nДата повернення: {end_date}\nСтан повернення: {returned}\nID користувача: {user_id}\nКористувач: {user_name} {user_surname}\nID книги: {book_id}\nНазва книги: {book_title}\nРік публікації книги: {book_year}")
	await state.finish()

async def command_get_all_borrows(message: types.Message) -> None:
	borrows: list = BorrowsManager.get_all()
	result: str = f"ID Боргу | Дата взятя | Дата повернення | Статус повернули | ID Користувача | Користувач | ID Книги | Книга\n"
	for borrow in borrows:
		borrow_id: int = borrow[0]
		user_id: int = borrow[1]
		book_id: int = borrow[2]
		taken_date: str = borrow[3]
		end_date: str = borrow[4]
		returned: int = borrow[5]

		user: Optional[tuple] = UsersManager.get(id=user_id)
		book: Optional[tuple] = BooksManager.get(id=book_id)

		user_name: str = user[1]
		user_surname: str = user[2]
		book_title: str = book[1]
		book_year: int = book[2]

		result += f"{borrow_id} | {taken_date} | {end_date} | {returned} | {user_id} | {user_name} {user_surname} | {book_id} | {book_title} - {book_year}\n\n"

	await message.reply(f"Усі борги:\n{result}")

async def command_using_books(message: types.Message) -> None:
	not_returned: Optional[list] = BorrowsManager.get_not_returned()
	if not not_returned:
		await message.reply("Наразі усі книги повернуті")
		return

	result_message: str = f"Книги що ще не повернули:\n\n"

	for borrow in not_returned:
		if not borrow: continue
		borrow_id: int = borrow[0]
		user_id: int = borrow[1]
		book_id: int = borrow[2]
		taken_date: str = borrow[3]
		end_date: str = borrow[4]
		
		user: Optional[tuple] = UsersManager.get(id=user_id)
		book: Optional[tuple] = BooksManager.get(id=book_id)
		if (not user or user is None) or (not book or book is None): continue

		user_name: str = user[1]
		user_surname: str = user[2]
		user_phone: int = user[3]
		book_title: str = book[1]
		book_year: int = book[2]

		author_id: Optional[int] = BookAuthorManager.get_by_book(book_id=book_id)
		if not author_id or author_id is None: continue

		author_id = author_id[0][0]

		author: Optional[tuple] = AuthorManager.get(id=author_id)
		if not author or author is None: continue

		author_name: str = author[1]
		author_surname: str = author[2]

		result_message += f"Борг #{borrow_id}\nДата взятя: {taken_date}\nДата повернення: {end_date}\nКнига #{book_id}\nНавза: {book_title}\nАвтор: {author_name} {author_surname}\nРік публікації: {book_year}\nКористувач #{user_id}\nКористувач: {user_name} {user_surname}\nТелефон: {user_phone}\n\n"

	await message.reply(result_message)

async def command_get_overdue(message: types.Message) -> None:
	overdues: Optional[list] = BorrowsManager.get_overdue()
	if not overdues:
		await message.reply("Немає просрочених боргів")
		return
	result_message: str = f"Порушили термін боргу:\n\n"
	for borrow in overdues:
		if not borrow: continue
		borrow_id: int = borrow[0]
		user_id: int = borrow[1]
		book_id: int = borrow[2]
		taken_date: str = borrow[3]
		end_date: str = borrow[4]

		user: Optional[tuple] = UsersManager.get(id=user_id)
		book: Optional[tuple] = BooksManager.get(id=book_id)
		if (not user or user is None) or (not book or book is None): continue

		user_name: str = user[1]
		user_surname: str = user[2]
		user_phone: int = user[3]
		book_title: str = book[1]
		book_year: int = book[2]

		author_id: Optional[int] = BookAuthorManager.get_by_book(book_id=book_id)
		if not author_id or author_id is None: continue

		author_id = author_id[0][0]

		author: Optional[tuple] = AuthorManager.get(id=author_id)
		if not author or author is None: continue

		author_name: str = author[1]
		author_surname: str = author[2]

		result_message += f"Борг #{borrow_id}\nДата взятя: {taken_date}\nДата повернення: {end_date}\nКнига #{book_id}\nНавза: {book_title}\nАвтор: {author_name} {author_surname}\nРік публікації: {book_year}\nКористувач #{user_id}\nКористувач: {user_name} {user_surname}\nТелефон: {user_phone}\n\n"

	await message.reply(result_message)

def register_handlers_borrows(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_borrows, lambda message: message.text == keyboards_text.Borrows.create_table)
	dp.register_message_handler(comamnd_delete_table_borrows, lambda message: message.text == keyboards_text.Borrows.delete_table)
	dp.register_message_handler(command_add_borrow, lambda message: message.text == keyboards_text.Borrows.add)
	dp.register_message_handler(command_add_borrow_user_id, state=FSMBorrows.Add.user_id)
	dp.register_message_handler(command_add_borrow_book_id, state=FSMBorrows.Add.book_id)
	dp.register_message_handler(command_add_borrow_taken_date, state=FSMBorrows.Add.taken_date)
	dp.register_message_handler(command_add_borrow_end_date, state=FSMBorrows.Add.end_date)
	dp.register_message_handler(command_add_borrow_returned, state=FSMBorrows.Add.returned)
	dp.register_message_handler(command_delete_borrow, lambda message: message.text == keyboards_text.Borrows.delete)
	dp.register_message_handler(command_delete_borrow_id, state=FSMBorrows.Delete.borrow_id)
	dp.register_message_handler(command_edit_borrow, lambda message: message.text == keyboards_text.Borrows.edit)
	dp.register_message_handler(command_edit_borrow_id, state=FSMBorrows.Edit.borrow_id_be)
	dp.register_message_handler(command_edit_borrow_user_id, state=FSMBorrows.Edit.user_id_be)
	dp.register_message_handler(command_edit_borrow_book_id, state=FSMBorrows.Edit.book_id_be)
	dp.register_message_handler(command_edit_borrow_taken_date, state=FSMBorrows.Edit.taken_date_be)
	dp.register_message_handler(command_edit_borrow_end_date, state=FSMBorrows.Edit.end_date_be)
	dp.register_message_handler(command_edit_borrow_returned, state=FSMBorrows.Edit.returned_be)
	dp.register_message_handler(command_edit_returned_borrow, lambda message: message.text == keyboards_text.Borrows.edit_returned)
	dp.register_message_handler(command_edit_returned_borrow_id, state=FSMBorrows.EditReturned.borrow_id_ber)
	dp.register_message_handler(command_edit_returned_borrow_returned, state=FSMBorrows.EditReturned.returned_ber)
	dp.register_message_handler(command_get_borrow, lambda message: message.text == keyboards_text.Borrows.get)
	dp.register_message_handler(command_get_borrow_id, state=FSMBorrows.Get.borrow_id_bg)
	dp.register_message_handler(command_get_all_borrows, lambda message: message.text == keyboards_text.Borrows.get_all)
	dp.register_message_handler(command_using_books, lambda message: message.text == keyboards_text.Borrows.not_returned)
	dp.register_message_handler(command_get_overdue, lambda message: message.text == keyboards_text.Borrows.overdue)
	