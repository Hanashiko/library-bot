from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional

class BookGenreManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists book_genre (
			genre_id int,
			book_id int,
			primary key (book_id, genre_id),
			foreign key (book_id) references books(id),
			foreign key (genre_id) references genres(id)
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists book_genre"
		execute_query(query)

	@staticmethod
	def add(genre_id: int, book_id: int) -> None:
		query: str = "insert into book_genre (genre_id, book_id) values (%s, %s)"
		values: tuple = (genre_id, book_id,)
		execute_query(query, values)

	@staticmethod
	def delete(genre_id: int, book_id: int) -> None:
		query: str = "delete from book_genre where genre_id = %s and book_id = %s"
		values: tuple = (genre_id, book_id,)
		execute_query(query, values)

	@staticmethod
	def delete_by_book(book_id: int) -> None:
		query: str = "DELETE FROM book_genre WHERE book_id = %s"
		values: tuple = (book_id,)
		execute_query(query, values)

	@staticmethod
	def delete_by_genre(genre_id: int) -> None:
		query: str = "DELETE FROM book_genre WHERE genre_id = %s"
		values: tuple = (genre_id,)
		execute_query(query, values)

	@staticmethod
	def get_by_genre(genre_id: int) -> Optional[list]:
		query: str = "select book_id from book_genre where genre_id = %s"
		values: tuple = (genre_id,)
		result: Optional[list] = execute_query_fetchall(query, values)
		return result

	@staticmethod
	def get_by_book(book_id: int) -> Optional[tuple]:
		query: str = "select genre_id from book_genre where book_id = %s"
		values: tuple = (book_id,)
		result: Optional[tuple] = execute_query_fetchall(query, values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select genre_id, book_id from book_genre"
		result: Optional[list] = execute_query_fetchall(query)
		return result