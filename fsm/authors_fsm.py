from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMAuthor:
	class Add(StatesGroup):
		author_name = State()
		author_surname = State()

	class Delete(StatesGroup):
		author_id = State()

	class Edit(StatesGroup):
		author_id = State()
		author_name = State()
		author_surname = State()

	class Get(StatesGroup):
		author_id = State()