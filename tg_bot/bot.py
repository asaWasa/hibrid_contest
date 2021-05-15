from tg_bot.loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from database.cv_interface import CVInterface as CV


def main_key_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    markup.add('Посмотреть встречи')
    markup.add('Заполнить профиль')
    return markup


def user_in_base(id):
    #todo добавить базу данных
    # if db_users.find_id(id):
    #     return True
    # else:
    #     return False
    return False


class MainState(StatesGroup):
    registration = State()
    main = State()
    settings = State()


class AuthState(StatesGroup):
    name = State()
    department = State()
    coffee_type = State()


@dp.message_handler(commands='start', state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # todo проверить что человек в базе
    user = message.from_user.get_current()
    async with state.proxy() as user_data:
        user_data['tg_data'] = user
    if user_in_base(user.id):
        markup = main_key_board()
        await message.answer("Привет!, {}".format(str(user)), reply_markup=markup)
    else:
        markup.add('Регистрация')
        await message.answer("Привет!", reply_markup=markup)


@dp.message_handler(Text(equals='Регистрация'), state="*")
async def cmd_auth(message: types.Message, state: FSMContext):
    await message.answer("Расскажи о себе")
    await message.answer('Какой кофе любишь?')
    await AuthState.coffee_type.set()


@dp.message_handler(state=AuthState.coffee_type)
async def auth_name(message: types.Message, state: FSMContext):
    coffee_type = message.text
    async with state.proxy() as user_data:
        user_data['coffee_type'] = coffee_type
    await message.answer('Как тебя зовут?')
    await AuthState.name.set()


@dp.message_handler(state=AuthState.name)
async def auth_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as user_data:
        user_data['name'] = name
    await message.answer('Как называется твой отдел?')
    await AuthState.department.set()


@dp.message_handler(state=AuthState.department)
async def auth_dep(message: types.Message, state: FSMContext):
    data = dict()
    data["department"] = message.text
    async with state.proxy() as user_data:
        data["coffee_type"] = user_data['coffee_type']
        data["real_name"] = user_data['name']
        data["tg_id"] = user_data['tg_data']['id']
        data["tg_is_bot"] = user_data['tg_data']['is_bot']
        data["tg_first_name"] = user_data['tg_data']['id']

        data["tg_first_name"] = user_data['tg_data']['first_name']
        data["tg_username"] = user_data['tg_data']['username']
        data["tg_language_code"] = user_data['tg_data']['language_code']
    await message.answer(CV(data).to_dict())
    await message.answer('Профиль успешно создан', reply_markup=main_key_board())
    await MainState.main.set()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
