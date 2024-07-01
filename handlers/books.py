from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from typing import Optional
from datetime import datetime

from database.books_db import BooksManager
from database.authors_db import AuthorManager
from database.genres_db import GenreManager
from database.book_author_db import BookAuthorManager
from database.book_genre_db import BookGenreManager
from database.borrows_db import BorrowsManager

from create_bot import dp, bot
from handlers.validation import *
from keyboards import *
from fsm import *
from handlers.general import cancel_notification, not_find

async def command_create_table_book(message: types.Message) -> None:
	BooksManager.create_table()
	await message.reply("Створив таблицю книг")

async def comamnd_delete_table_book(message: types.Message) -> None:
	BooksManager.delete_table()
	await message.reply("Видалив таблицю книг")

async def command_add_book(message: types.Message) -> None:
	await FSMBooks.Add.book_title.set()
	await message.reply("Напишіть назву книги:")
	await cancel_notification(message)

async def command_add_book_title(message: types.Message, state: FSMContext) -> None:
	title: Optional[str] = await validation_name(message)
	if title is None: return
	async with state.proxy() as data:
		data['title'] = title
	await FSMBooks.Add.next()
	await message.reply("Введіть рік публікації твору:")

async def command_add_book_year(message: types.Message, state: FSMContext) -> None:
	year: Optional[int] = await validation_int(message)
	if year is None: return
	async with state.proxy() as data:
		data['year'] = year
	await FSMBooks.Add.next()
	await message.reply("Введіть ім'я автора книги:")

async def command_add_book_author_name(message: types.Message, state: FSMContext) -> None:
	author_name: Optional[str] = await validation_name(message)
	if author_name is None: return
	async with state.proxy() as data:
		data['author_name'] = author_name
	await FSMBooks.Add.next()
	await message.reply("Введіть прізвище автора книги:")

async def command_add_book_author_surname(message: types.Message, state: FSMContext) -> None:
	author_surname: Optional[str] = await validation_name(message)
	if author_surname is None: return
	async with state.proxy() as data:
		data['author_surname'] = author_surname
	await FSMBooks.Add.next()
	await message.reply("Введіть жанри книги, розділивши їх комою(,):")

async def command_add_book_genre(message: types.Message, state: FSMContext):
	genres: Optional[list] = message.text.split(", ")
	checked_genres: Optional[list] = []
	for genre in genres:
		check_genre = await validation_genre(message, genre)
		if check_genre is None: 
			return
		else:
			checked_genres.append(check_genre.lower())

	async with state.proxy() as data:
		title: str = data['title']
		year: int = data['year']
		author_name: str = data['author_name']
		author_surname: str = data['author_surname']

	BooksManager.add(title=title, year=year)
	book_id = BooksManager.get_id(title=title, year=year)[0]

	author_exists = AuthorManager.author_exists(name=author_name, surname=author_surname)
	if author_exists:
		author_id: int = AuthorManager.get_id(name=author_name, surname=author_surname)[0]
		BookAuthorManager.add(author_id=author_id, book_id=book_id)
	else:
		AuthorManager.add(name=author_name, surname=author_surname)
		author_id: int = AuthorManager.get_id(name=author_name, surname=author_surname)[0]
		BookAuthorManager.add(author_id=author_id, book_id=book_id)

	for genre in checked_genres:
		genre_exists = GenreManager.genre_exists(name=genre)
		if genre_exists:
			genre_id: int = GenreManager.get_id(name=genre)
			genre_id = genre_id[0]
			BookGenreManager.add(genre_id=genre_id, book_id=book_id)
		else:
			GenreManager.add(name=genre)
			genre_id: int = GenreManager.get_id(name=genre)
			genre_id = genre_id[0]
			BookGenreManager.add(genre_id=genre_id, book_id=book_id)

	await message.reply(f"Добавив книгу:\nНазва: {title}\nАвтор: {author_name} {author_surname}\nЖанри: {', '.join(checked_genres)}\nРік публікації: {year}")
	await state.finish()

async def command_delete_book(message: types.Message, state: FSMContext) -> None:
	await FSMBooks.Delete.book_id.set()
	await message.reply("Напишіть id книги:")
	await cancel_notification(message)

async def command_delete_book_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	await message.reply(f"boook {id = }")

	book: Optional[tuple] = BooksManager.get(id=id)

	if book is None or not book:
		await not_find(message)
		return

	book_id = book[0]
	book_name = book[1]
	book_year = book[2]
	
	book_author: Optional[tuple] = BookAuthorManager.get_by_book(book_id=id)
	author_id = book_author[0][0]
	
	author: Optional[tuple] = AuthorManager.get(id=author_id)
	
	author_name = author[1]
	author_surname = author[2]

	BookAuthorManager.delete(author_id=author_id, book_id=book_id)

	book_genre: Optional[tuple] = BookGenreManager.get_by_book(book_id=id)
	genres = []
	for genre_id_tuple in book_genre:
		genre_id = genre_id_tuple[0]
		BookGenreManager.delete(genre_id=genre_id, book_id=book_id)
		genre: Optional[tuple] = GenreManager.get(id=genre_id)[1]
		if genre:
			genres.append(genre)

	BooksManager.delete(id=book_id)

	await message.reply(f"Видалив книгу:\nID: {book_id}\nНазва: {book_name}\nАвтор: {author_name} {author_surname}\nЖанри: {', '.join(genres)}\nРік публікації: {book_year}")
	await state.finish()

async def command_edit_book(message: types.Message) -> None:
	await FSMBooks.Edit.book_id.set()
	await message.reply("Напигіть id книги")
	await cancel_notification(message)

async def command_edit_book_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	async with state.proxy() as data:
		data["id"] = id

	await FSMBooks.Edit.next()
	await message.reply("Введіть назву книги")

async def command_edit_book_title(message: types.Message, state: FSMContext) -> None:
	title: Optional[str] = await validation_name(message)
	if title is None: return

	async with state.proxy() as data:
		data['title'] = title

	await FSMBooks.Edit.next()
	await message.reply("Введіть рік публікації твору")

async def command_edit_book_year(message: types.Message, state: FSMContext) -> None:
	year: Optional[int] = await validation_int(message)
	if year is None: return

	async with state.proxy() as data:
		data['year'] = year

	await FSMBooks.Edit.next()
	await message.reply("Введіть ім'я автора")

async def command_edit_book_author_name(message: types.Message, state: FSMContext) -> None:
	author_name: Optional[str] = await validation_name(message)
	if author_name is None: return

	async with state.proxy() as data:
		data['author_name'] = author_name

	await FSMBooks.Edit.next()
	await message.reply("Введіть прізвище автора")

async def command_edit_book_author_surname(message: types.Message, state: FSMContext) -> None:
	author_surname: Optional[str] = await validation_name(message)
	if author_surname is None: return

	async with state.proxy() as data:
		data['author_surname'] = author_surname

	await FSMBooks.Edit.next()
	await message.reply("Введіть жанри твору, розділивши їх комою(,)")

async def command_edit_book_genre(message: types.Message, state: FSMContext) -> None:
	genres: Optional[list] = message.text.split(", ")
	checked_genres: Optional[list] = []
	for genre in genres:
		check_genre = await validation_genre(message, genre)
		if check_genre is None: 
			return
		else:
			checked_genres.append(check_genre.lower())

	async with state.proxy() as data:
		book_id: int = data['id']
		title: str = data['title']
		year: int = data['year']
		author_name: str = data['author_name']
		author_surname: str = data['author_surname']

	BooksManager.edit(id=book_id, new_title=title, new_year=year)
	BookGenreManager.delete_by_book(book_id=book_id)

	author_id = BookAuthorManager.get_by_book(book_id=book_id)[0][0]
	AuthorManager.edit(author_id=author_id, new_name=author_name, new_surname=author_surname)

	for genre in checked_genres:
		genre_exists = GenreManager.genre_exists(name=genre)	
		if genre_exists:
			genre_id: int = GenreManager.get_id(name=genre)[0]
			BookGenreManager.add(genre_id=genre_id, book_id=book_id)
		else:
			GenreManager.add(name=genre)
			genre_id: int = GenreManager.get_id(name=genre)[0]
			BookGenreManager.add(genre_id=genre_id, book_id=book_id)

	await message.reply(f"Відредагував книгу:\nID: {book_id}\nНазва: {title}\nАвтор: {author_name} {author_surname}\nЖанри: {', '.join(checked_genres)}\nРік публікації: {year}")

	await state.finish()

async def command_get_book(message: types.Message) -> None:
	await FSMBooks.Get.book_id.set()
	await message.reply("Напишіть id книги")
	await cancel_notification(message)

async def command_get_book_id(message: types.Message, state: FSMContext) -> None:
	id: Optional[int] = await validation_int(message)
	if id is None: return

	book: Optional[tuple] = BooksManager.get(id=id)

	if book is None or not book:
		await not_find(message)
		return

	book_id: int = book[0]
	book_title: str = book[1]
	book_year: int = book[2]

	book_author: Optional[tuple] = BookAuthorManager.get_by_book(book_id=book_id)
	author: Optional[tuple] = AuthorManager.get(id=book_author[0][0])

	author_name: str = author[1]
	author_surname: str = author[2]

	book_genre: Optional[tuple] = BookGenreManager.get_by_book(book_id=book_id)
	genres: list = []
	for genre_id_tuple in book_genre:
		genre_id: int = genre_id_tuple[0]
		BookGenreManager.delete(genre_id=genre_id, book_id=book_id)
		genre: Optional[tuple] = GenreManager.get(id=genre_id)[1]
		if genre:
			genres.append(genre)

	result_genres: str = ', '.join(genres)

	await message.reply(f"Інформація про книгу:\nID: {book_id}\nНазва: {book_title}\nАвтор: {author_name} {author_surname}\nЖанри: {result_genres}\nРік публікації: {book_year}")
	await state.finish()

async def command_get_all_books(message: types.Message) -> None:
	books: list = BooksManager.get_all()
	result: str = f"ID | Назва | Автор | Жанри | Рік публікації\n\n"
	for book in books:
		book_id: int = book[0]
		book_title: str = book[1]
		book_year: int = book[2]

		author_id = BookAuthorManager.get_by_book(book_id)
		author_id: int = author_id[0][0]

		author: Optional[tuple] = AuthorManager.get(id=author_id)
		author_name: str = author[1]
		author_surname: str = author[2]

		book_genre: Optional[tuple] = BookGenreManager.get_by_book(book_id=book_id)
		genres: list = []
		for genre_id_tuple in book_genre:
			genre_id: int = genre_id_tuple[0]
			genre: Optional[tuple] = GenreManager.get(id=genre_id)[1]
			if genre:
				genres.append(genre)
		result_genres: str = ', '.join(genres)

		result += f"{book_id} | {book_title} | {author_name} {author_surname} | {result_genres} | {book_year}\n\n"

	await message.reply(f"Усі книги:\n{result}")


async def command_book_by_author(message: types.Message) -> None:
	await FSMBooks.BookByAuthor.author_name_bba.set()
	await message.reply("Напишіть ім'я автора")
	await cancel_notification(message)

async def command_book_by_author_name(message: types.Message, state: FSMContext) -> None:
	author_name: Optional[str] = await validation_name(message)
	if author_name is None: return

	async with state.proxy() as data:
		data['author_name'] = author_name

	await FSMBooks.BookByAuthor.next()
	await message.reply("Напишіть прізвище автора")

async def command_book_by_author_surname(message: types.Message, state: FSMContext) -> None:
	author_surname: Optional[str] = await validation_name(message)
	if author_surname is None: return

	async with state.proxy() as data:
		author_name: str = data['author_name']

	author_id: Optional[int] = AuthorManager.get_id(name=author_name, surname=author_surname)
	if not author_id:
		await not_find(message)
		return

	author_id = author_id[0]

	result_message: str = f"Автор(#{author_id}): {author_name} {author_surname}\nЙого книги:\n"

	books_id: Optional[tuple] = BookAuthorManager.get_by_author(author_id=author_id)
	for book_id in books_id:
		book_id = book_id[0]
		if not book_id: continue
		book: int = BooksManager.get(id=book_id)
		book_title: str = book[1]
		book_year: int = book[2]
		result_message += f"Книга #{book_id}: {book_title} - {book_year}\n"
	await message.reply(result_message)
	await state.finish()

async def command_book_by_name(message: types.Message) -> None:
	await FSMBooks.BookByName.book_name_bbb.set()
	await message.reply("Напишіть назву книги")
	await cancel_notification(message)

async def command_book_by_name_title(message: types.Message, state: FSMContext) -> None:
	book_title: Optional[str] = await validation_name(message)
	if book_title is None: return

	books: Optional[list] = BooksManager.get_by_title(title=book_title)
	if not books: 
		await not_find(message)
		return

	result_message: str = f"Книги за назвою «{book_title}»:\n\n"

	for book in books:
		if not book: continue
		book_id: int = book[0]
		book_title: str = book[1]
		book_year: int = book[2]

		author_id: Optional[int] = BookAuthorManager.get_by_book(book_id=book_id)[0][0]
		author: Optional[tuple] = AuthorManager.get(id=author_id)
		author_name: str = author[1]
		author_surname: str = author[2]

		genres_id: Optional[tuple] = BookGenreManager.get_by_book(book_id=book_id)
		genres: list = []
		for genre_id in genres_id:
			genre_id = genre_id[0]
			genre = GenreManager.get(id=genre_id)
			genre_name = genre[1]
			genres.append(genre_name)

		result_message += f"Книга #{book_id}:\nНазва: {book_title}\nАвтор: {author_name} {author_surname}\nЖанри: {', '.join(genres)}\nРік публікації: {book_year}\n\n"

	await message.reply(result_message)
	await state.finish()

async def command_book_by_genre(message: types.Message) -> None:
	await FSMBooks.BookByGenre.genre_name_bbg.set()
	await message.reply("Напишіть жанр")
	await cancel_notification(message)

async def command_book_by_genre_name(message: types.Message, state: FSMContext) -> None:
	genre_name: Optional[str] = await validation_name(message)
	if genre_name is None: return

	genre_id: Optional[tuple] = GenreManager.get_id(name=genre_name)
	if not genre_id:
		await not_find(message)
		return

	genre_id = genre_id[0]


	book_genre: Optional[list] = BookGenreManager.get_by_genre(genre_id=genre_id)
	if not book_genre:
		await not_find(message)
		return

	result_message: str = f"Книги за жанром «{genre_name}»:\n\n"

	for book_id in book_genre:
		if not book_id: continue
		book_id = book_id[0]
		book: Optional[tuple] = BooksManager.get(id=book_id)
		if not book or book is None: continue
		book_title: str = book[1]
		book_year: int = book[2]

		author_id: Optional[int] = BookAuthorManager.get_by_book(book_id=book_id)
		if not author_id or author_id is None: continue
		author_id = author_id[0][0]
		author: Optional[tuple] = AuthorManager.get(id=author_id)
		if not author or author is None: continue

		author_name: str = author[1]
		author_surname: str = author[2]

		result_message += f"Книга #{book_id}\nНазва: {book_title}\nАвтор: {author_name} {author_surname}\nРік публікації: {book_year}\n\n"

	await message.reply(result_message)
	await state.finish()

async def command_get_popular_books(message: types.Message) -> None:
	popular_books = BorrowsManager.get_popular_books()
	result_message: str = f"5 найпопулярніших книг:\n\n"
	for book_count in popular_books: 
		book_id: int = book_count[0]
		count: int = book_count[1]
		
		book: Optional[tuple] = BooksManager.get(id=book_id)
		if not book: continue

		book_title: str = book[1]
		book_year: int = book[2]

		author_id: Optional[tuple] = BookAuthorManager.get_by_book(book_id=book_id)
		if not author_id: continue
		author_id = author_id[0][0]

		author: Optional[tuple] = AuthorManager.get(id=author_id)
		if not author: continue

		author_name: str = author[1]
		author_surname: str = author[2]

		result_message += f"Книга #{book_id}\nНазва: {book_title}\nКількість прочитань: {count}\nАвтор: {author_name} {author_surname}\nРік публікації: {book_year}\n\n"

	await message.reply(result_message)


def register_handlers_books(dp: Dispatcher) -> None:
	dp.register_message_handler(command_create_table_book, lambda message: message.text == keyboards_text.Books().create_table)
	dp.register_message_handler(comamnd_delete_table_book, lambda message: message.text == keyboards_text.Books().delete_table)
	dp.register_message_handler(command_add_book, lambda message: message.text == keyboards_text.Books().add)
	dp.register_message_handler(command_add_book_title, state=FSMBooks.Add.book_title)
	dp.register_message_handler(command_add_book_year, state=FSMBooks.Add.book_year)
	dp.register_message_handler(command_add_book_author_name, state=FSMBooks.Add.book_author_name)
	dp.register_message_handler(command_add_book_author_surname, state=FSMBooks.Add.book_author_surname)
	dp.register_message_handler(command_add_book_genre, state=FSMBooks.Add.book_genre)
	dp.register_message_handler(command_delete_book, lambda message: message.text == keyboards_text.Books().delete)
	dp.register_message_handler(command_delete_book_id, state=FSMBooks.Delete.book_id)
	dp.register_message_handler(command_edit_book, lambda message: message.text == keyboards_text.Books().edit)
	dp.register_message_handler(command_edit_book_id, state=FSMBooks.Edit.book_id)
	dp.register_message_handler(command_edit_book_title, state=FSMBooks.Edit.book_title)
	dp.register_message_handler(command_edit_book_year, state=FSMBooks.Edit.book_year)
	dp.register_message_handler(command_edit_book_author_name, state=FSMBooks.Edit.book_author_name)
	dp.register_message_handler(command_edit_book_author_surname, state=FSMBooks.Edit.book_author_surname)
	dp.register_message_handler(command_edit_book_genre, state=FSMBooks.Edit.book_genre)
	dp.register_message_handler(command_get_book, lambda message: message.text == keyboards_text.Books().get)
	dp.register_message_handler(command_get_book_id, state=FSMBooks.Get.book_id)
	dp.register_message_handler(command_get_all_books, lambda message: message.text == keyboards_text.Books().get_all)
	dp.register_message_handler(command_book_by_author, lambda message: message.text == keyboards_text.Books().book_by_author)
	dp.register_message_handler(command_book_by_author_name, state=FSMBooks.BookByAuthor.author_name_bba)
	dp.register_message_handler(command_book_by_author_surname, state=FSMBooks.BookByAuthor.author_surname_bba)
	dp.register_message_handler(command_book_by_name, lambda message: message.text == keyboards_text.Books().book_by_name)
	dp.register_message_handler(command_book_by_name_title, state=FSMBooks.BookByName.book_name_bbb)
	dp.register_message_handler(command_book_by_genre, lambda message: message.text == keyboards_text.Books().book_by_genre)
	dp.register_message_handler(command_book_by_genre_name, state=FSMBooks.BookByGenre.genre_name_bbg)
	dp.register_message_handler(command_get_popular_books, lambda message: message.text == keyboards_text.Books().popular_books)
