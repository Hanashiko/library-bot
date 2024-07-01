from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class FSMBorrows:
	class Add(StatesGroup):
		user_id = State()
		book_id = State()
		taken_date = State()
		end_date = State()
		returned = State()

	class Delete(StatesGroup):
		borrow_id = State()

	class Edit(StatesGroup):
		borrow_id_be = State()
		user_id_be = State()
		book_id_be = State()
		taken_date_be = State()
		end_date_be = State()
		returned_be = State()

	class EditReturned(StatesGroup):
		borrow_id_ber = State()
		returned_ber = State()

	class Get(StatesGroup):
		borrow_id_bg = State()

