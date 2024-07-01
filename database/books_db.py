from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional

class BooksManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists books (
			id int primary key auto_increment,
			title varchar(60),
			publishing_year int
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists books"
		execute_query(query)

	@staticmethod
	def add(title: str, year: int) -> None:
		query: str = "insert into books (title, publishing_year) values (%s, %s)"
		values: tuple = (title, year)
		execute_query(query,values)

	@staticmethod
	def delete(id: int) -> None:
		query: str = "delete from books where id = %s"
		values: tuple = (id,)
		execute_query(query, values)

	@staticmethod
	def edit(id: int, new_title: str, new_year: int) -> None:
		query: str = "update books set title = %s, publishing_year = %s where id = %s"
		values: tuple = (new_title, new_year, id)
		execute_query(query, values)

	@staticmethod
	def get(id: int) -> Optional[tuple]:
		query: str = "select id, title, publishing_year from books where id = %s"
		values: tuple = (id,)
		result: Optional[tuple] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_id(title: str, year: int) -> Optional[int]:
		query: str = "SELECT id FROM books WHERE title = %s AND publishing_year = %s"
		values: tuple = (title, year,)
		result: Optional[int] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_by_title(title: str) -> Optional[list]:
		query: str = "SELECT id, title, publishing_year FROM books WHERE title = %s"
		values: tuple = (title,)
		result: Optional[list] = execute_query_fetchall(query, values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select id, title, publishing_year from books"
		result: Optional[list] = execute_query_fetchall(query)
		return result 

	@staticmethod
	def book_exists(title: str, year: int) -> bool:
		query: str = "SELECT COUNT(*) FROM books WHERE title = %s AND publishing_year = %s"
		values: tuple = (title, year,)
		result = execute_query_fetchone(query, values)
		return result[0] > 0