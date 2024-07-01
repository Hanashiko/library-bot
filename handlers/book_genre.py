from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.book_genre_db import BookGenreManager
from database.books_db import BooksManager
from database.genres_db import GenreManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find

async def command_create_table_book_genre(message: types.Message) -> None:
	BookGenreManager.create_table()
	await message.reply("Створив таблицю зв'язку індентифікаторів книг та жанрів")

async def command_delete_table_book_genre(message: types.Message) -> None:
	book_genre_db.delete_table()
	await message.reply("Видалив таблицю зв'язку індентифікаторів книг та жанрів")

async def command_add_book_genre(message: types.Message) -> None:
	await FSMBookGenre.Add.genre_id_bga.set()
	await message.reply("Напишіть id жанру")
	await cancel_notification(message)

async def command_add_book_genre_genre_id(message: types.Message, state: FSMContext) -> None:
	genre_id: Optional[int] = await validation_int(message)
	if genre_id is None: return

	genre: Optional[tuple] = GenreManager.get(id=genre_id)
	if not genre:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['genre_id'] = genre_id

	await FSMBookGenre.Add.next()
	await message.reply("Напишіть id книги")

async def command_add_book_genre_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[tuple] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		genre_id: int = data['genre_id']

	BookGenreManager.add(genre_id=genre_id, book_id=book_id)

	genre: Optional[tuple] = GenreManager.get(id=genre_id)

	book_title: str = book[1]
	book_year: int = book[2]
	author_name: str = author[1]
	author_surname: str = author[2]

	await message.reply(f"Добавив зв'язок:\n\nКнига:\nID: {book_id}\nНазва: {book_title}\nРік публікації: {book_year}\n\nАвтор:\nID: {author_id}\nІм'я: {author_name}\nПрізвище: {author_surname}")
	await state.finish()

async def command_delete_book_genre(message: types.Message) -> None:
	await FSMBookGenre.Delete.genre_id_bgd.set()
	await message.reply("Введіть id жанра")
	await cancel_notification(message)

async def command_delete_book_genre_genre_id(message: types.Message, state: FSMContext) -> None:
	genre_id: Optional[int] = await validation_int(message)
	if genre_id is None: return

	genre: Optional[tuple] = GenreManager.get(id=genre_id)
	if not genre:
		await not_find(message)
		return

	async with state.proxy() as data:
		data['genre_id'] = genre_id
	await FSMBookGenre.Delete.next()
	await message.reply("Напишіть id книги")

async def command_delete_book_genre_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	if not book:
		await not_find(message)
		return

	async with state.proxy() as data:
		genre_id: int = data['genre_id']

	BookGenreManager.delete(genre_id=genre_id, book_id=book_id)

	genre: Optional[tuple] = GenreManager.get(id=genre_id)

	book_title: str = book[1]
	book_year: int = book[2]
	genre_name: str = genre[1]

	await message.reply(f"Видалив зв'язок:\n\nКнига:\nID: {book_id}\nНазва: {book_title}\nРік публікації: {book_year}\n\nЖанр:\nID: {genre_id}\nНазва: {genre_name}")
	await state.finish()

async def command_get_by_genre_book_genre(message: types.Message) -> None:
	await FSMBookGenre.GetByGenre.genre_id_bgg.set()
	await message.reply("Напишіть id жанра")
	await cancel_notification(message)

async def command_get_by_genre_book_genre_genre_id(message: types.Message, state: FSMContext) -> None:
	genre_id: Optional[int] = await validation_int(message)
	if genre_id is None: return

	books_id: Optional[tuple] = BookGenreManager.get_by_genre(genre_id=genre_id)
	if books_id is None or not books_id:
		await not_find(message)
		return

	genre: Optional[tuple] = GenreManager.get(id=genre_id)
	genre_name: str = genre[1]
	result_message: str = f"Жанр:\nID: {genre_id}\nНазва: {genre_name}\n"
	result_message += "\nКниги:\nID | Назва | Рік публікації\n"
	for book_id in books_id:
		if not book_id: return
		book: Optional[tuple] = BooksManager.get(id=book_id[0])
		book_id: int = book[0]
		book_title: str = book[1]
		book_year: int = book[2]
		result_message += f"{book_id} | {book_title} | {book_title}\n"

	await message.reply(f"Зв'язок:\n\n{result_message}")
	await state.finish()

async def command_get_by_book_book_genre(message: types.Message) -> None:
	await FSMBookGenre.GetByBook.book_id_bgg.set()
	await message.reply("Напишіть id книги")
	await cancel_notification(message)

async def command_get_by_book_book_genre_book_id(message: types.Message, state: FSMContext) -> None:
	book_id: Optional[int] = await validation_int(message)
	if book_id is None: return

	genres_id: Optional[tuple] = BookGenreManager.get_by_book(book_id=book_id)
	if genres_id is None or not genres_id:
		await not_find(message)
		return

	book: Optional[tuple] = BooksManager.get(id=book_id)
	book_title: str = book[1]
	book_year: int = book[2]

	result_message: str = f"Книги:\nID: {book_id}\nНазва: {book_title}\nРік публікації: {book_year}\n"
	result_message += "\nЖанри:\nID | Назва\n"

	for genre_id in genres_id:
		if not genre_id: return
		genre: Optional[tuple] = GenreManager.get(id=genre_id[0])
		genre_id: int = genre[0]
		genre_name: str = genre[1]
		result_message += f"{genre_id} | {genre_name}\n"

	await message.reply(f"Зв'язок:\n\n{result_message}")
	await state.finish()

async def command_get_all_book_genre(message: types.Message) -> None:
	book_genres: list = BookGenreManager.get_all()
	result: str = f"ID книги | Назва | Рік публікації | ID жанру | Назва\n"
	for book_genre in book_genres:
		genre_id: int = book_genre[0]
		book_id: int = book_genre[1]

		genre: Optional[tuple] = GenreManager.get(id=genre_id)
		genre_name: str = genre[1]

		book: Optional[tuple] = BooksManager.get(id=book_id)
		book_title: str = book[1]
		book_year: int = book[2]

		result += f"{book_id} | {book_title} | {book_year} | {genre_id} | {genre_name}\n\n"

	await message.reply(f"Усі зв'язки книга & жанр:\n{result}")


def register_handlers_book_genre(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_book_genre, lambda message: message.text == keyboards_text.BookGenre().create_table)
	dp.register_message_handler(command_delete_table_book_genre, lambda message: message.text == keyboards_text.BookGenre().delete_table)
	dp.register_message_handler(command_add_book_genre, lambda message: message.text == keyboards_text.BookGenre().add)
	dp.register_message_handler(command_add_book_genre_genre_id, state=FSMBookGenre.Add.genre_id_bga)
	dp.register_message_handler(command_add_book_genre_book_id, state=FSMBookGenre.Add.book_id_bga)
	dp.register_message_handler(command_delete_book_genre, lambda message: message.text == keyboards_text.BookGenre().delete)
	dp.register_message_handler(command_delete_book_genre_genre_id, state=FSMBookGenre.Delete.genre_id_bgd)
	dp.register_message_handler(command_delete_book_genre_book_id, state=FSMBookGenre.Delete.book_id_bgd)
	dp.register_message_handler(command_get_by_genre_book_genre, lambda message: message.text == keyboards_text.BookGenre().get_by_genre)
	dp.register_message_handler(command_get_by_genre_book_genre_genre_id, state=FSMBookGenre.GetByGenre.genre_id_bgg)
	dp.register_message_handler(command_get_by_book_book_genre, lambda message: message.text == keyboards_text.BookGenre().get_by_book)
	dp.register_message_handler(command_get_by_book_book_genre_book_id, state=FSMBookGenre.GetByBook.book_id_bgg)
	dp.register_message_handler(command_get_all_book_genre, lambda message: message.text == keyboards_text.BookGenre().get_all)