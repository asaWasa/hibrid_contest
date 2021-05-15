from common.config import api_key
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
bot = Bot(token=api_key)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

