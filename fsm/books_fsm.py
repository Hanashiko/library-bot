from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMBooks:
	class Add(StatesGroup):
		book_title = State()
		book_year = State()
		book_author_name = State()
		book_author_surname = State()
		book_genre = State()

	class Delete(StatesGroup):
		book_id = State()

	class Edit(StatesGroup):
		book_id = State()
		book_title = State()
		book_year = State()
		book_author_name = State()
		book_author_surname = State()
		book_genre = State()

	class Get(StatesGroup):
		book_id = State()

	class BookByAuthor(StatesGroup):
		author_name_bba = State()
		author_surname_bba = State()

	class BookByName(StatesGroup):
		book_name_bbb = State()

	class BookByGenre(StatesGroup):
		genre_name_bbg = State()


