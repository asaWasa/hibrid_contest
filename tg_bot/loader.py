from common.config import api_key
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_key)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

