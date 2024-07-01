from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMBookGenre:
	class Add(StatesGroup):
		# baa = book genre add
		genre_id_bga = State()
		book_id_bga = State()

	class Delete(StatesGroup):
		genre_id_bgd = State()
		book_id_bgd = State()

	class GetByGenre(StatesGroup):
		genre_id_bgg = State()

	class GetByBook(StatesGroup):
		book_id_bgg = State()