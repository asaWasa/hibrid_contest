from tg_bot.loader import dp, bot, db_users
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from database.cv_interface import CVInterface as CV
import aiogram.utils.markdown as md
from constants import *


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    markup.add('Посмотреть встречи')
    markup.add('Заполнить профиль')
    return markup

def about_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Закончить')
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
    about = State()
    end = State()


@dp.message_handler(commands='start', state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    user = message.from_user.get_current()
    async with state.proxy() as user_data:
        user_data['tg_data'] = user
    if user_in_base(user.id):
        markup = main_keyboard()
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
               'Kakao', 'Marshmello', 'Закончить выбор']
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


@dp.callback_query_handler(Text(equals='add_coffee_' + 'Закончить выбор'), state=AuthState.coffee_type)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Напишите о себе:')
    await query.message.answer('Как тебя зовут?')
    await AuthState.name.set()


@dp.message_handler(state=AuthState.name)
async def auth_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as user_data:
        user_data['name'] = name
    await message.answer('Выбери отдел(ы) в котором работаешь:')
    await AuthState.department.set()
    departments = ['Marketing', 'Finance', 'Dev and testing',
                   'Media_Bayer', 'Sales', 'Partner relations', "Media", "Administrative staff", "Закончить выбор"]
    btns = list()
    media = types.InlineKeyboardMarkup(row_width=1)
    for dep in departments:
        btns.append(types.InlineKeyboardButton("{}".format(dep), callback_data='add_dep_{}'.format(dep)))
    media.add(*btns)
    await message.answer('Выберите отдел(ы):', reply_markup=media)
    await AuthState.department.set()

# -----------------------------------------------------------------


@dp.callback_query_handler(Text(equals='add_dep_' + 'Marketing'), state=AuthState.department)
async def callback_button_marketing(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.MARKETING in user_data['department']:
                user_data['department'].pop(DEPARTMENT.MARKETING)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.MARKETING)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MARKETING)

        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Finance'), state=AuthState.department)
async def callback_button_finance(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.FINANCE in user_data['department']:
                user_data['department'].pop(DEPARTMENT.FINANCE)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.FINANCE)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.FINANCE)

        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Dev and testing'), state=AuthState.department)
async def callback_button_dev_test(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.DEV_AND_TESTING in user_data['department']:
                user_data['department'].pop(DEPARTMENT.DEV_AND_TESTING)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.DEV_AND_TESTING)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.DEV_AND_TESTING)

        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Media_Bayer'), state=AuthState.department)
async def callback_button_media_bayer(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.MEDIA_BAYER in user_data['department']:
                user_data['department'].pop(DEPARTMENT.MEDIA_BAYER)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.MEDIA_BAYER)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MEDIA_BAYER)
        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Sales'), state=AuthState.department)
async def callback_button_sales(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.SALES in user_data['department']:
                user_data['department'].pop(DEPARTMENT.SALES)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.SALES)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.SALES)
        await query.message.answer(user_data)

@dp.callback_query_handler(Text(equals='add_dep_' + 'Partner relations'), state=AuthState.department)
async def callback_button_partner_rel(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.PARTNER_RELATIONS in user_data['department']:
                user_data['department'].pop(DEPARTMENT.PARTNER_RELATIONS)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.PARTNER_RELATIONS)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.PARTNER_RELATIONS)
        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + "Media"), state=AuthState.department)
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


@dp.callback_query_handler(Text(equals='add_dep_' + "Administrative staff"), state=AuthState.department)
async def callback_button_administrative_stuff(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.ADMINISTRATIVE_STAFF in user_data['department']:
                user_data['department'].pop(DEPARTMENT.ADMINISTRATIVE_STAFF)
            elif user_data['department']:
                user_data['department'].add(DEPARTMENT.ADMINISTRATIVE_STAFF)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.ADMINISTRATIVE_STAFF)
        await query.message.answer(user_data)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Закончить выбор'), state=AuthState.department)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    markup = about_keyboard()
    await query.message.answer('Напишите о себе:', reply_markup=markup)
    await AuthState.about.set()


@dp.message_handler(state=AuthState.about)
async def auth_dep(message: types.Message, state: FSMContext):
    _id = get_id()
    data = dict()
    data['id'] = _id
    async with state.proxy() as user_data:
        data["coffee_type"] = user_data['coffee_type']
        data["real_name"] = user_data['name']
        data['deportment'] = user_data['deportment']
        data["tg_id"] = user_data['tg_data']['id']
        data["tg_is_bot"] = user_data['tg_data']['is_bot']
        data["tg_first_name"] = user_data['tg_data']['id']
        data["tg_first_name"] = user_data['tg_data']['first_name']
        data["tg_username"] = user_data['tg_data']['username']
        data["tg_language_code"] = user_data['tg_data']['language_code']

    db_users.push(CV(data).to_dict())
    await message.answer('Отлично! профиль успешно создан', reply_markup=main_keyboard())
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
