from tg_bot.loader import dp
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


def main_key_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    markup.add('Посмотреть встречи')
    return markup


def user_in_base(id):
    #todo добавить базу данных
    # if db_users.find_id(id):
    #     return True
    # else:
    #     return False
    return True


class MainState(StatesGroup):
    registration = State()
    main = State()
    settings = State()


class AuthState(StatesGroup):
    name = State()
    department = State()


@dp.message_handler(commands='start', state="*")
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    #todo проверить что человек в базе
    user = message.from_user.get_current()
    if user_in_base(user.id):
        markup = main_key_board()
        await message.answer("Привет!, {}".format(str(user)), reply_markup=markup)
    else:
        markup.add('Регистрация')
        await message.answer("Привет!", reply_markup=markup)
        await MainState.registration.set()




@dp.message_handler(Text(equals='Регистрация'), state="*")
async def cmd_auth(message: types.Message):
    await message.answer("Расскажи о себе")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
