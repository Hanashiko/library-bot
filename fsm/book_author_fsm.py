from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMBookAuthor:
	class Add(StatesGroup):
		# baa = book author add
		author_id_baa = State()
		book_id_baa = State()

	class Delete(StatesGroup):
		author_id_bad = State()
		book_id_bad = State()

	class GetByAuthor(StatesGroup):
		author_id_bag = State()

	class GetByBook(StatesGroup):
		book_id_bag = State()