from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional, List, Tuple

class AuthorManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		CREATE TABLE IF NOT EXISTS authors (
			id INT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(30) NOT NULL,
			surname VARCHAR(30) NOT NULL
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "DROP TABLE IF EXISTS authors"
		execute_query(query)

	@staticmethod
	def ckeck_table() -> bool:
		query: str = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'library' AND table_name = 'authors'"
		result = execute_query_fetchone(query)
		return result[0] == 1

	@staticmethod
	def add(name: str, surname: str) -> None:
		query: str = "INSERT INTO authors (name, surname) VALUES (%s, %s)"
		values: Tuple[str, str] = (name, surname)
		execute_query(query, values)

	@staticmethod
	def delete(author_id: int) -> None:
		query: str = "DELETE FROM authors WHERE id = %s"
		values: Tuple[int] = (author_id,)
		execute_query(query, values)

	@staticmethod
	def edit(author_id: int, new_name: str, new_surname: str) -> None:
		query: str = "UPDATE authors SET name = %s, surname = %s WHERE id = %s"
		values: Tuple[str, str, int] = (new_name, new_surname, author_id)
		execute_query(query, values)

	@staticmethod
	def get(id: int) -> Optional[tuple]:
		query: str = "SELECT id, name, surname FROM authors WHERE id = %s"
		values: tuple = (id,)
		result: Optional[tuple] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_id(name: str, surname: str) -> Optional[int]:
		query: str = "SELECT id FROM authors WHERE name = %s AND surname = %s"
		values: tuple = (name, surname, )
		result: Optional[int] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_all() -> Optional[List[Tuple[int, str, str]]]:
		query: str = "SELECT id, name, surname FROM authors"
		result: Optional[List[Tuple[int, str, str]]] = execute_query_fetchall(query)
		return result

	@staticmethod
	def author_exists(name: str, surname: str) -> bool:
		query: str = "SELECT COUNT(*) FROM authors WHERE name = %s AND surname = %s"
		values: tuple = (name, surname)
		result = execute_query_fetchone(query, values)
		return result[0] > 0