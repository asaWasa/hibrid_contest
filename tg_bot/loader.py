from common.config import api_key
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from database.mongo_driver.mongodb_driver import MongoDBDriver
from constants import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_key)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

db_users = MongoDBDriver(db_name=USERS_DB.DB, col_name=USERS_DB.COLLECTION)
