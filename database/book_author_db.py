from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional

class BookAuthorManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists book_author (
			author_id int,
			book_id int,
			primary key (author_id, book_id),
			foreign key (author_id) references authors(id),
			foreign key (book_id) references books(id)
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists book_author"
		execute_query(query)

	@staticmethod
	def add(author_id: int, book_id: int) -> None:
		query: str = "insert into book_author (author_id, book_id) values (%s, %s)"
		values: tuple = (author_id, book_id,)
		execute_query(query, values)

	@staticmethod
	def delete(author_id: int, book_id: int) -> None:
		query: str = "delete from book_author where author_id = %s and book_id = %s"
		values: tuple = (author_id, book_id,)
		execute_query(query, values)

	@staticmethod
	def get_by_author(author_id: int) -> Optional[tuple]:
		query: str = "select book_id from book_author where author_id = %s"
		values: tuple = (author_id,)
		result: Optional[tuple] = execute_query_fetchall(query, values)
		return result

	@staticmethod
	def get_by_book(book_id: int) -> Optional[tuple]:
		query: str = "select author_id from book_author where book_id = %s"
		values: tuple = (book_id,)
		result: Optional[tuple] = execute_query_fetchall(query, values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select author_id, book_id from book_author"
		result: Optional[list] = execute_query_fetchall(query)
		return result