from aiogram import Dispatcher
from aiogram.types import ChatMember, User
from aiogram.bot import Bot
from aiogram.utils.executor import start_polling
from create_bot import dp, bot
from config_bot import LOG_CHAT

async def on_startup(_) -> None:
	me: User = await bot.get_me()
	UserInfo: ChatMember = await bot.get_chat_member(me.id, me.id)
	username: str = f"@{UserInfo.user.username}"

	text: str = f"Бот запущений | {username} - {me.first_name}"
	print(text)

from handlers import general
from handlers import authors
from handlers import books
from handlers import book_author
from handlers import genres
from handlers import book_genre
from handlers import users
from handlers import borrows

def register_handlers(dp: Dispatcher) -> None:
	general.register_handlers_general(dp)
	books.register_handlers_books(dp)
	authors.register_handlers_authors(dp)
	book_author.register_handlers_book_author(dp)
	genres.register_handlers_genres(dp)
	book_genre.register_handlers_book_genre(dp)
	users.register_handlers_users(dp)
	borrows.register_handlers_borrows(dp)

def main() -> None:
	register_handlers(dp)
	start_polling(dp, skip_updates=False, on_startup=on_startup)

if __name__ == "__main__":
	main()