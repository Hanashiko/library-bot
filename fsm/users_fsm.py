from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMUsers:
	class Add(StatesGroup):
		user_name = State()
		user_surname = State()
		user_phone = State()

	class Delete(StatesGroup):
		user_id = State()

	class Edit(StatesGroup):
		user_id = State()
		user_name = State()
		user_surname = State()
		user_phone = State()

	class Get(StatesGroup):
		user_id = State()
