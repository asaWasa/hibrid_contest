from tg_bot.loader import dp, bot, db_users
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from database.cv_interface import CVInterface as CV
import aiogram.utils.markdown as md


def main_key_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    markup.add('Посмотреть встречи')
    markup.add('Заполнить профиль')
    return markup


def reply_selection_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Назначить встречу', '->')
    return markup


def user_in_base(id):
    if db_users.is_in('tg_id', id):
        return True
    else:
        return False


def get_id():
    try:
        f = db_users.get_last_item('id')['id']
        return db_users.get_last_item('id')['id'] + 1
    except:
        return 0


class MainState(StatesGroup):
    registration = State()
    main = State()
    selection = State()
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
        await message.answer("Привет!, {}".format(str(user.first_name)), reply_markup=markup)
        await MainState.main.set()
    else:
        markup.add('Регистрация')
        await message.answer("Привет!", reply_markup=markup)


@dp.message_handler(Text(equals='Регистрация'), state="*")
async def cmd_auth(message: types.Message, state: FSMContext):
    await message.answer("Расскажи о себе", reply_markup=types.ReplyKeyboardRemove())
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
    _id = get_id()
    data = dict()
    data['id'] = _id
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

    # await message.answer(CV(data).to_dict())
    db_users.push(CV(data).to_dict())
    await message.answer('Профиль успешно создан', reply_markup=main_key_board())
    await MainState.main.set()


@dp.message_handler(Text(equals='Предложить собеседника'), state=MainState.main)
async def get_random_user(message: types.Message, state: FSMContext):
    markup = reply_selection_keyboard()

    await message.answer('В этом разделе вы сможете выбрать собеседника', reply_markup=markup)
    await MainState.selection.set()


@dp.message_handler(state=MainState.selection)
async def get_random_user(message: types.Message, state: FSMContext):
    user_data = get_random_user()
    bot.send_message(message.chat.id,
                     md.text(
                         md.text("Меня зовут: ".format(user_data['name'])),
                         md.text("Мой любимый кофе: ".format(user_data['coffee_type'])),
                         md.text("Я работаю в отделе".format(user_data['department'])),

                     )
                     )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
