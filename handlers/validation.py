from aiogram import types, Dispatcher
from create_bot import dp, bot
from typing import List, Union, Optional
from datetime import datetime
import re

async def check_args(message: types.Message, min_args: int, arg_names: List[str] = None) -> List[str]:	
	args: list = message.text.split()
	if len(args) < min_args+1:
		if arg_names is None:
			await message.reply("Неправильний формат команди. Занадто мало аргументів")
		else:
			await message.reply(f"Неправильний формат команди. Потрібно вказати {', '.join(arg_names)}")
		return []
	return args[1:]

async def validation_int(message: types.Message) -> int:
	number: str = message.text
	try:
		return int(number)
	except ValueError:
		await message.reply("Аргумент повинен бути цілим числом")
		return None

async def validation_name(message: types.Message) -> str:
	name: str = message.text
	if not name.strip():
		await message.reply("Аргумент не може складатися з пробілів")
		return None
	return name


async def validation_date(message: types.Message) -> str:
# async def validation_date(message: types.Message) -> datetime:
    date_str: str = message.text
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")  # або інший формат дати, який вам потрібен
        return date
    except ValueError:
        await message.reply("Дата повинна бути у форматі РРРР-ММ-ДД")
        return None


# async def validation_name(message: types.Message) -> str:
# 	name: str = message.text
# 	# if not re.match("^[a-zA-Zа-яА-ЯіїєІЇЄґҐ'0-9 -]+$", name):
# 	# 	await message.reply("Аргумент не має містити надлишкових символів")
# 	# 	return None
# 	if not name.strip():
# 		await message.reply("Аргумент не може складатися з пробілів")
# 		return None
# 	# name_parts = name.split(' ')
# 	# for part in name_parts:
# 	# 	if not part[:1].isupper() or not part[1:].islower():
# 	# 		await message.reply("Аргумент повинен записуватись в форматі, де перша літера кожного слова велика, а решта - маленькі")
# 	# 		return None
# 	return name

async def validation_genre(message: types.Message, name: str) -> str:
	name = name.replace(",","").strip()
	if not name:
		await message.reply("Аргумент не може складатися з пробілів")
		return None
	return name

async def validate_id(id: str) -> Optional[int]:
	try:
		return int(id)
	except ValueError:
		return None

async def validate_number(number: str) -> Optional[int]:
	try:
		return int(number)
	except ValueError:
		return None

# async def validate_name(name: str) -> bool:
# 	if all(char.isalnum() or char == "_" for char in name):
# 	# if len(name) > 0 and all(char.isalnum() or char == "_" for char in name):
# 		return True
# 	return False

async def validate_name(name: str) -> bool:
	if not name: return False
	if not (2 <= len(name) <= 50): return False
	pattern = r'^[A-ZА-ЯЇЄІ][a-zа-яїєі\s\'-]*$'
	return bool(re.match(pattern, name))

async def validate_date(data_str: str) -> Optional[datetime.date]:
	try:
		return datetime.strptime(data_str, "%Y-%m-%d").date()
	except ValueError:
		return None

async def validate_bool(bool_str: str) -> Optional[bool]:
	if bool_str.lower() in ["true", "false"]:
		return bool_str.lower == "true"
	return None

async def get_validated_id(message: types.Message, index: int) -> Optional[int]:
	id: Optional[int] = await validate_id(message.text.split()[index])
	if id is None:
		await message.reply("ID повинен бути цілим числом")
	return id

# async def get_validated_name(message: types.Message, index: int) -> Optional[str]:
# 	name: str = message.text.split()[index]
# 	if not await validate_name(name):
# 		await message.reply("Неправильний формат імені")
# 		return None
# 	return name

async def get_validated_number(message: types.Message) -> Optional[int]:
	number: Optional[int] = await validate_number(message.text)
	if number is None:
		await message.reply("Аргумент повинен бути цілим числом")
	return number

async def get_validated_name(message: types.Message) -> Optional[str]:
	name: str = message.text
	if not await validate_name(name):
		await message.reply("Неправильний формат імені")
		return None
	return name

async def get_validated_date(message: types.Message, index: int) -> Optional[datetime.date]:
	date_str: str = message.text.split()[index]
	date: Optional[datetime.date] = await validate_date(date_str)
	if date is None:
		await message.reply("Дата повину бути в форматі YYYY-MM-DD")
	return date

async def get_validated_bool(message: types.Message, index: int) -> Optional[int]:
	bool_str: str = message.text.split()[index]
	result: Optional[int] = await validate_id(bool_str)
	if result is None:
		await message.reply("Параметр повинен бути числом")
	if result in [0,1]:
		return result
	return None
