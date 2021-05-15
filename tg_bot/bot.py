from tg_bot.loader import dp, bot, db_users
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from database.cv_interface import CVInterface as CV
import aiogram.utils.markdown as md
from constants import *


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
    end = State()


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
    coffees = ['Ristretto', 'Espresso', 'Americano',
               'Double_espresso', 'Kapucino', 'Latte',
               'Kakao', 'Marshmello']
    btns = list()
    media = types.InlineKeyboardMarkup(row_width=1)
    for coffee in coffees:
        btns.append(types.InlineKeyboardButton("{}".format(coffee), callback_data='add_coffee_{}'.format(coffee)))
    media.add(*btns)
    await message.answer('Выберите какие виды вы педпочитаете:', reply_markup=media)


@dp.callback_query_handler(Text(equals='add_coffee_' + 'Ristretto'), state=AuthState.coffee_type)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.RISTRETTO in user_data['coffee']:
                user_data['coffee'].pop(COFFEE.RISTRETTO)
            elif user_data['coffee']:
                user_data['coffee'].add(COFFEE.RISTRETTO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.RISTRETTO)

        await query.message.answer(user_data)

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
    await message.answer('Выбери отдел в котором работаешь:')
    await AuthState.department.set()
    departments = ['Marketing', 'Finance', 'Dev and testing',
                   'Media_Bayer', 'Sales', 'Partner relations', "Media", "Administrative staff"]
    btns = list()
    media = types.InlineKeyboardMarkup(row_width=1)
    for dep in departments:
        btns.append(types.InlineKeyboardButton("{}".format(dep), callback_data='add_dep_{}'.format(dep)))
    media.add(*btns)
    await message.answer('Выберите отдел:', reply_markup=media)
    await AuthState.department.set()


@dp.callback_query_handler(Text(equals='add_dep_' + 'Marketing'), state=AuthState.department)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.MEDIA in user_data['department']:
                user_data['department'].pop(DEPARTMENT.MEDIA)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.MEDIA)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MEDIA)

        await query.message.answer(user_data)


@dp.message_handler(state=AuthState.department)
async def auth_dep(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state=AuthState.end)
async def auth_dep(message: types.Message, state: FSMContext):
    _id = get_id()
    data = dict()
    data['id'] = _id
    data = add_list_elem(data, 'departament', message.text)
    async with state.proxy() as user_data:
        data["coffee_type"] = user_data['coffee_type']
        data["real_name"] = user_data['name']
        data["tg_id"] = user_data['tg_data']['id']
        data["tg_is_bot"] = user_data['tg_data']['is_bot']
        data["tg_first_name"] = user_data['tg_data']['id']
        data["tg_first_name"] = user_data['tg_data']['first_name']
        data["tg_username"] = user_data['tg_data']['username']
        data["tg_language_code"] = user_data['tg_data']['language_code']

    db_users.push(CV(data).to_dict())
    await message.answer('Профиль успешно создан', reply_markup=main_key_board())
    await MainState.main.set()


def add_list_elem(object, key, element):
    try:
        if object[key] is None:
            raise
        object[key].append(element)
    except:
        object[key] = list()
        object[key].append(element)


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
