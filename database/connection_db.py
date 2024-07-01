import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Optional, Union, Any
from database.config_db import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection() -> Optional[MySQLConnection]:
	try:
		connection: MySQLConnection = mysql.connector.connect(
			host = DB_HOST,
			database = DB_NAME,
			user = DB_USER,
			password = DB_PASSWORD
		)
		return connection
	except mysql.connector.Error as err:
		print(f"Error connection database: {err}")
		return None

def close_connection(connection: Optional[MySQLConnection], cursor: Optional[MySQLCursor] = None) -> None:
	if cursor is not None:
		try:
			cursor.close()
		except mysql.connector.Error as err:
			print(f"Error closing cursor: {err}")
	if connection is not None:
		try:
			connection.close()
		except mysql.connector.Error as err:
			print(f"Error closing connection: {err}")

def execute_query(query: str, values: Optional[tuple] = None) -> None:
	connection = get_connection()
	if connection:
		try:
			cursor = connection.cursor()
			cursor.execute(query, values)
			connection.commit()
		except mysql.connector.Error as err:
			print(f"Error: {err}")
		finally:
			close_connection(connection, cursor)

def execute_query_fetchone(query: str, values: Optional[tuple] = None) -> Optional[Any]:
	connection = get_connection()
	result = None
	if connection:
		try:
			cursor = connection.cursor()
			cursor.execute(query,values)
			result = cursor.fetchone()
		except mysql.connector.Error as err:
			print(f"Error: {err}")
		finally:
			close_connection(connection, cursor)
	return result

def execute_query_fetchall(query: str, values: Optional[tuple] = None) -> Optional[list]:
	connection = get_connection()
	result = None
	if connection:
		try:
			cursor = connection.cursor()
			cursor.execute(query, values)
			result = cursor.fetchall()
		except mysql.connector.Error as err:
			print(f"Error: {err}")
		finally:
			close_connection(connection, cursor)
	return result

