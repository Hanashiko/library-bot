from database.connection_db import get_connection, close_connection, execute_query, execute_query_fetchone, execute_query_fetchall
from typing import Optional

class UsersManager:
	@staticmethod
	def create_table() -> None:
		query: str = """
		create table if not exists users (
			id int primary key auto_increment,
			name varchar(30) not null,
			surname varchar(30) not null,
			phone int
		)
		"""
		execute_query(query)

	@staticmethod
	def delete_table() -> None:
		query: str = "drop table if exists users"
		execute_query(query)

	@staticmethod
	def add(name: str, surname: str, phone: int) -> None:
		query: str = "insert into users (name, surname, phone) values (%s, %s, %s)"
		values: tuple = (name, surname, phone)
		execute_query(query,values)

	@staticmethod
	def delete(id: int) -> None:
		query: str = "delete from users where id = %s"
		values: tuple = (id,)
		execute_query(query, values)

	@staticmethod
	def edit(id: int, new_name: str, new_surname: str, new_phone: int) -> None:
		query: str = "update users set name = %s, surname = %s, phone = %s where id = %s"
		values: tuple = (new_name, new_surname, new_phone, id)
		execute_query(query,values)

	@staticmethod
	def get(id: int) -> Optional[tuple]:
		query: str = "select id, name, surname, phone from users where id = %s"
		values: tuple = (id,)
		result: Optional[tuple] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_id(name: str, surname: str) -> Optional[int]:
		query: str = "SELECT id FROM users WHERE name = %s AND surname = %s"
		values: tuple = (name, surname,)
		result: Optional[int] = execute_query_fetchone(query,values)
		return result

	@staticmethod
	def get_all() -> Optional[list]:
		query: str = "select id, name, surname, phone from users"
		result: Optional[list] = execute_query_fetchall(query)
		return result

	@staticmethod
	def user_exists(name: str, surname: str) -> bool:
		query: str = "SELECT COUNT(*) FROM users WHERE name = %s AND surname = %s"
		values: tuple = (name, surname,)
		result = execute_query_fetchone(query,values)
		return result[0] > 0
