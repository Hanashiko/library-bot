from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMGenres:
	class Add(StatesGroup):
		genre_name = State()

	class Delete(StatesGroup):
		genre_id = State()

	class Edit(StatesGroup):
		genre_id = State()
		genre_name = State()

	class Get(StatesGroup):
		genre_id = State()