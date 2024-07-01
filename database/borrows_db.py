from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional
from datetime import date

class BorrowsManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists borrows (
			borrow_id int primary key auto_increment,
			user_id int not null,
			book_id int not null,
			taken_date date not null,
			end_date date not null,
			returned boolean,
			foreign key (user_id) references users(id),
			foreign key (book_id) references books(id)
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists borrows"
		execute_query(query)

	@staticmethod
	def add(user_id: int, book_id: int, taken_date: str, end_date: str, returned: int) -> None:
		query: str = "insert into borrows (user_id, book_id, taken_date, end_date, returned) values (%s, %s, %s, %s, %s)"
		values: tuple = (user_id, book_id, taken_date, end_date, returned)
		execute_query(query,values)

	@staticmethod
	def delete(id: int) -> None:
		query: str = "delete from borrows where borrow_id = %s"
		values: tuple = (id,)
		execute_query(query,values)

	@staticmethod
	def edit(borrow_id: int, new_user_id: int, new_book_id: int, new_taken_date: str, new_end_date: str, new_returned: int) -> None:
		query: str = "update borrows set user_id = %s, book_id = %s, taken_date = %s, end_date = %s, returned = %s where borrow_id = %s"
		values: tuple = (new_user_id, new_book_id, new_taken_date, new_end_date, new_returned, borrow_id)
		execute_query(query, values)

	@staticmethod
	def edit_returned(borrow_id: int, returned: int) -> None:
		query: str = "update borrows set returned = %s where borrow_id = %s"
		values: tuple = (returned, borrow_id,)
		execute_query(query,values)

	@staticmethod
	def get(id: int) -> Optional[tuple]:
		query: str = "select borrow_id, user_id, book_id, taken_date, end_date, returned from borrows where borrow_id = %s"
		values: tuple = (id,)
		result: Optional[tuple] = execute_query_fetchone(query, values)
		return result

	@staticmethod
	def get_id(user_id: int, book_id: int, taken_date: str, end_date: str) -> Optional[int]:
		query: str = "SELECT borrow_id FROM borrows WHERE user_id = %s AND book_id = %s AND taken_date = %s AND end_date = %s"
		values: tuple = (user_id, book_id, taken_date, end_date, )
		result: Optional[int] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select borrow_id, user_id, book_id, taken_date, end_date, returned from borrows"
		result: Optional[list] = execute_query_fetchall(query)
		return result

	@staticmethod
	def get_not_returned() -> Optional[list]:
		query: str = "SELECT borrow_id, user_id, book_id, taken_date, end_date, returned FROM borrows WHERE returned = 0"
		result: Optional[list] = execute_query_fetchall(query)
		return result

	@staticmethod
	def get_returned() -> Optional[list]:
		query: str = "SELECT borrow_id, user_id, book_id, taken_date, end_date, returned FROM borrows WHERE returned = 1"
		result: Optional[list] = execute_query_fetchall(query)
		return result

	@staticmethod
	def get_overdue() -> Optional[list]:
		today = date.today()
		query: str = "SELECT borrow_id, user_id, book_id, taken_date, end_date, returned FROM borrows WHERE end_date < %s AND returned = 0"
		values: tuple = (today,)
		result: Optional[list] = execute_query_fetchall(query,values)
		return result

	@staticmethod
	def get_popular_books() -> Optional[list]:
		query: str = "SELECT book_id, COUNT(book_id) AS borrow_count FROM borrows GROUP BY book_id ORDER BY borrow_count DESC LIMIT 5"
		result: Optional[list] = execute_query_fetchall(query)
		return result