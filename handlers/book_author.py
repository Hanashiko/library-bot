from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.book_author_db import BookAuthorManager
from database.books_db import BooksManager
from database.authors_db import AuthorManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find


async def command_create_table_book_author(message: types.Message) -> None:
	BookAuthorManager.create_table()
	await message.reply("Створив таблицю зв'язку індентифікаторів книг та авторів")

async def command_delete_table_book_author(message: types.Message) -> None:
	BookAuthorManager.delete_table()
	await message.reply("Видалив таблицю зв'язку індентифікаторів книг та авторів")

async def comamnd_add_book_author(message: types.Message) -> None:
	await FSMBookAuthor.Add.author_id_baa.set()
	await message.reply("Напишіть id автора")
	await cancel_notification(message)

async def comamnd_add_book_author_author_id(message: types.Message, state: FSMContext) -> None:
	author_id: Optional[int] = await validation_int(message)
	if author_id is None: return

	author: Optional[tuple] = AuthorManager.get(id=author_id)
	if not author:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['author_id'] = author_id
	await FSMBookAuthor.Add.next()
	await message.reply("Напишіть id книги")

async def comamnd_add_book_author_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		author_id: int = data['author_id']

	BookAuthorManager.add(author_id=author_id, book_id=book_id)

	author: Optional[tuple] = AuthorManager.get(id=author_id)

	await message.reply(f"Добавив зв'язок:\n\nКнига:\nID: {book_id}\nНазва: {book[1]}\nРік публікації: {book[2]}\n\nАвтор:\nID: {author_id}\nІм'я: {author[1]}\nПрізвище: {author[2]}")
	await state.finish()

async def command_delete_book_author(message: types.Message) -> None:
	await FSMBookAuthor.Delete.author_id_bad.set()
	await message.reply("Введіть id автора")
	await cancel_notification(message)

async def command_delete_book_author_author_id(message: types.Message, state: FSMContext) -> None:
	author_id: Optional[int] = await validation_int(message)
	if author_id is None: return

	author: Optional[tuple] = AuthorManager.get(id=author_id)
	if not author:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['author_id'] = author_id
	await FSMBookAuthor.Delete.next()
	await message.reply("Напишіть id книги")

async def comamnd_delete_book_author_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		author_id: int = data['author_id']

	BookAuthorManager.delete(author_id=author_id, book_id=book_id)

	author: Optional[tuple] = AuthorManager.get(id=author_id)

	await message.reply(f"Видалив зв'язок:\n\nКнига:\nID: {book_id}\nНазва: {book[1]}\nРік публікації: {book[2]}\n\nАвтор:\nID: {author_id}\nІм'я: {author[1]}\nПрізвище: {author[2]}")
	await state.finish()

async def command_get_by_author_book_author(message: types.Message) -> None:
	await FSMBookAuthor.GetByAuthor.author_id_bag.set()
	await message.reply("Напищіть id автора")
	await cancel_notification(message)

async def command_get_by_author_book_author_author_id(message: types.Message, state: FSMContext) -> None:
	author_id: Optional[int] = await validation_int(message)
	if author_id is None: return

	books_id: Optional[tuple] = BookAuthorManager.get_by_author(author_id=author_id)
	if books_id is None or not books_id:
		await not_find(message)
		return

	author: Optional[tuple] = AuthorManager.get(id=author_id)
	result_message: str = f"Автор:\nID: {author_id}\nІм'я: {author[1]}\nПрізвище: {author[2]}\n"
	result_message += "\nКниги:\nID | Назва | Рік публікації\n"
	for book_id in books_id:
		if not book_id: return
		book: Optional[tuple] = BooksManager.get(id=book_id[0])
		book_id: int = book[0]
		book_title: str = book[1]
		book_year: int = book[2]
		result_message += f"{book_id} | {book_title} | {book_year}\n"

	await message.reply(f"Зв'язок:\n\n{result_message}")
	await state.finish()

async def command_get_by_book_book_author(message: types.Message) -> None:
	await FSMBookAuthor.GetByBook.book_id_bag.set()
	await message.reply("Напищіть id книги")
	await cancel_notification(message)

async def command_get_by_book_book_author_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	authors_id: Optional[tuple] = BookAuthorManager.get_by_book(book_id=book_id)
	if authors_id is None or not authors_id:
		await not_find(message)
		return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	result_message: str = f"Книга:\nID: {book_id}\nНазва: {book[1]}\nРік публікації: {book[2]}\n"
	result_message += "\nАвтори:\n"

	for author_id in authors_id:
		if not author_id: return
		author: Optional[tuple] = AuthorManager.get(id=author_id[0])
		author_id: int = author[0]
		author_name: str = author[1]
		author_surname: str = author[2]
		result_message += f"ID: {author_id}\nІм'я: {author_name}\nПрізвище: {author_surname}\n"

	await message.reply(f"Зв'язок:\n\n{result_message}")
	await state.finish()

async def command_get_all_book_author(message: types.Message) -> None:
	book_authors: list = BookAuthorManager.get_all()
	result: str = f"ID книги | Назва | Рік публікації | ID автора | Ім'я автора | Прізвище автора\n"
	for book_author in book_authors:
		author_id: int = book_author[0]
		book_id: int = book_author[1]

		author: Optional[tuple] = AuthorManager.get(id=author_id)
		author_name: str = author[1]
		author_surname: str = author[2]

		book: Optional[tuple] = BooksManager.get(id=book_id)
		book_title: str = book[1]
		book_year: int = book[2]

		result += f"{book_id} | {book_title} | {book_year} | {author_id} | {author_name} | {author_surname}\n\n"

	await message.reply(f"Усі зв'язки книга & автор:\n{result}")


def register_handlers_book_author(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_book_author, lambda message: message.text == keyboards_text.BookAuthor().create_table)
	dp.register_message_handler(command_delete_table_book_author, lambda message: message.text == keyboards_text.BookAuthor().delete_table)
	dp.register_message_handler(comamnd_add_book_author, lambda message: message.text == keyboards_text.BookAuthor().add)
	dp.register_message_handler(comamnd_add_book_author_author_id, state=FSMBookAuthor.Add.author_id_baa)
	dp.register_message_handler(comamnd_add_book_author_book_id, state=FSMBookAuthor.Add.book_id_baa)
	dp.register_message_handler(command_delete_book_author, lambda message: message.text == keyboards_text.BookAuthor().delete)
	dp.register_message_handler(command_delete_book_author_author_id, state=FSMBookAuthor.Delete.author_id_bad)
	dp.register_message_handler(comamnd_delete_book_author_book_id, state=FSMBookAuthor.Delete.book_id_bad)
	dp.register_message_handler(command_get_by_author_book_author, lambda message: message.text == keyboards_text.BookAuthor().get_by_author)
	dp.register_message_handler(command_get_by_author_book_author_author_id, state=FSMBookAuthor.GetByAuthor.author_id_bag)
	dp.register_message_handler(command_get_by_book_book_author, lambda message: message.text == keyboards_text.BookAuthor().get_by_book)
	dp.register_message_handler(command_get_by_book_book_author_book_id, state=FSMBookAuthor.GetByBook.book_id_bag)
	dp.register_message_handler(command_get_all_book_author, lambda message: message.text == keyboards_text.BookAuthor().get_all)