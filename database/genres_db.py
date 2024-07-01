from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional

class GenreManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists genres (
			id int primary key auto_increment,
			name varchar(30)
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists genres"
		execute_query(query)

	@staticmethod
	def add(name: str) -> None:
		query: str = "insert into genres (name) values (%s)"
		values: tuple = (name,)
		execute_query(query,values)

	@staticmethod
	def delete(id: int) -> None:
		query: str = "delete from genres where id = %s"
		values: tuple = (id,)
		execute_query(query,values)

	@staticmethod
	def edit(id: int, new_name: str) -> None:
		query: str = "update genres set name = %s where id = %s"
		values: tuple = (new_name, id,)
		execute_query(query,values)

	@staticmethod
	def get(id: int) -> Optional[tuple]:
		query: str = "select id, name from genres where id = %s"
		values: tuple = (id,)
		result: Optional[tuple] = execute_query_fetchone(query, values)
		return result 

	@staticmethod
	def get_id(name: str) -> Optional[int]:
		query: str = "SELECT id FROM genres WHERE name = %s"
		values: tuple = (name,)
		result: Optional[int] = execute_query_fetchone(query, values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select id, name from genres"
		result: Optional[list] = execute_query_fetchall(query)
		return result

	@staticmethod
	def genre_exists(name: str) -> bool:
		query: str = "SELECT COUNT(*) FROM genres WHERE name = %s"
		values: tuple = (name,)
		result = execute_query_fetchone(query, values)
		return result[0] > 0