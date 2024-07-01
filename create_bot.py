from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os
from config_bot import TOKEN_API

storage: MemoryStorage = MemoryStorage()

bot: Bot = Bot(token=TOKEN_API)
dp: Dispatcher = Dispatcher(bot, storage=storage)