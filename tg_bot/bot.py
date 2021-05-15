from tg_bot.loader import dp, bot, db_users, db_meetings
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from database.cv_interface import CVInterface as CV
import aiogram.utils.markdown as md
from constants import *
from _algorithm.selection_algorithm import *
import time

def main_keyboard(idx):
    cnt_meetings = db_meetings.find_one('tg_id', idx)
    if cnt_meetings is None:
        cnt_meetings = 0
    else:
        cnt_meetings = len(cnt_meetings['meetings'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    markup.add(f'Посмотреть встречи({cnt_meetings})')
    markup.add('Заполнить профиль')
    return markup


def reply_submit_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Через час')
    markup.add('Через 2 часа')
    markup.add('Через 5 часов')
    markup.add('Через 7 часа')
    markup.add('Через 1 день')
    return markup


def about_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Закончить')
    return markup


def reply_selection_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Да', '->')
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
    set_time = State()


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
        markup = main_keyboard(message.from_user.id)
        await message.answer("Привет, {}!".format(str(user.first_name)), reply_markup=markup)
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
async def callback_button_ristretto(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.RISTRETTO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.RISTRETTO)
            else:
                user_data['coffee'].add(COFFEE.RISTRETTO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.RISTRETTO)



@dp.callback_query_handler(Text(equals='add_coffee_' + 'Закончить выбор'), state=AuthState.coffee_type)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Как тебя зовут?')
    await AuthState.name.set()


@dp.callback_query_handler(Text(equals='add_coffee_' + 'Espresso'), state=AuthState.coffee_type)
async def callback_button_espresso(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.ESPRESSO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.ESPRESSO)
            else:
                user_data['coffee'].add(COFFEE.ESPRESSO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.ESPRESSO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)


@dp.callback_query_handler(Text(equals='add_coffee_' + 'Americano'), state=AuthState.coffee_type)
async def callback_button_americano(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.AMERICANO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.AMERICANO)
            else:
                user_data['coffee'].add(COFFEE.AMERICANO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.AMERICANO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)



@dp.callback_query_handler(Text(equals='add_coffee_' + 'Double_espresso'), state=AuthState.coffee_type)
async def callback_button_double_espresso(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.DOUBLE_ESPRESSO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.DOUBLE_ESPRESSO)
            else:
                user_data['coffee'].add(COFFEE.DOUBLE_ESPRESSO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.DOUBLE_ESPRESSO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)



@dp.callback_query_handler(Text(equals='add_coffee_' + 'Kapucino'), state=AuthState.coffee_type)
async def callback_button_kapucino(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.KAPUCINO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.KAPUCINO)
            else:
                user_data['coffee'].add(COFFEE.KAPUCINO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.KAPUCINO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)


@dp.callback_query_handler(Text(equals='add_coffee_' + 'Latte'), state=AuthState.coffee_type)
async def callback_button_latte(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.LATTE in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.LATTE)
            else:
                user_data['coffee'].add(COFFEE.LATTE)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.LATTE)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)



@dp.callback_query_handler(Text(equals='add_coffee_' + 'Kakao'), state=AuthState.coffee_type)
async def callback_button_kakao(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.KAKAO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.KAKAO)
            else:
                user_data['coffee'].add(COFFEE.KAKAO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.KAKAO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)



@dp.callback_query_handler(Text(equals='add_coffee_' + 'Marshmello'), state=AuthState.coffee_type)
async def callback_button_marshmello(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if COFFEE.MARSHMELLO in user_data['coffee']:
                user_data['coffee'].remove(COFFEE.MARSHMELLO)
            else:
                user_data['coffee'].add(COFFEE.MARSHMELLO)
        except:
            user_data['coffee'] = set()
            user_data['coffee'].add(COFFEE.MARSHMELLO)

        coffee_list = 'Вы выбрали: '
        for coffee in list(user_data['coffee']):
            coffee_list += DEPARTMENT.get_string(coffee) + ' '
        await query.message.answer(coffee_list)


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
                user_data['department'].remove(DEPARTMENT.MARKETING)
            else:
                user_data['department'].add(DEPARTMENT.MARKETING)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MARKETING)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)



@dp.callback_query_handler(Text(equals='add_dep_' + 'Finance'), state=AuthState.department)
async def callback_button_finance(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.FINANCE in user_data['department']:
                user_data['department'].remove(DEPARTMENT.FINANCE)
            else:
                user_data['department'].add(DEPARTMENT.FINANCE)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.FINANCE)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)



@dp.callback_query_handler(Text(equals='add_dep_' + 'Dev and testing'), state=AuthState.department)
async def callback_button_dev_test(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.DEV_AND_TESTING in user_data['department']:
                user_data['department'].remove(DEPARTMENT.DEV_AND_TESTING)
            else:
                user_data['department'].add(DEPARTMENT.DEV_AND_TESTING)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.DEV_AND_TESTING)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)



@dp.callback_query_handler(Text(equals='add_dep_' + 'Media_Bayer'), state=AuthState.department)
async def callback_button_media_bayer(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.MEDIA_BAYER in user_data['department']:
                user_data['department'].remove(DEPARTMENT.MEDIA_BAYER)
            else:
                user_data['department'].add(DEPARTMENT.MEDIA_BAYER)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MEDIA_BAYER)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Sales'), state=AuthState.department)
async def callback_button_sales(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.SALES in user_data['department']:
                user_data['department'].remove(DEPARTMENT.SALES)
            else:
                user_data['department'].add(DEPARTMENT.SALES)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.SALES)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)


@dp.callback_query_handler(Text(equals='add_dep_' + 'Partner relations'), state=AuthState.department)
async def callback_button_partner_rel(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.PARTNER_RELATIONS in user_data['department']:
                user_data['department'].remove(DEPARTMENT.PARTNER_RELATIONS)
            else:
                user_data['department'].add(DEPARTMENT.PARTNER_RELATIONS)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.PARTNER_RELATIONS)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)


@dp.callback_query_handler(Text(equals='add_dep_' + "Media"), state=AuthState.department)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.MEDIA in user_data['department']:
                user_data['department'].remove(DEPARTMENT.MEDIA)
            else:
                user_data['department'].add(DEPARTMENT.MEDIA)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.MEDIA)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)


@dp.callback_query_handler(Text(equals='add_dep_' + "Administrative staff"), state=AuthState.department)
async def callback_button_administrative_stuff(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        try:
            if DEPARTMENT.ADMINISTRATIVE_STAFF in user_data['department']:
                user_data['department'].remove(DEPARTMENT.ADMINISTRATIVE_STAFF)
            else:
                user_data['department'].add(DEPARTMENT.ADMINISTRATIVE_STAFF)
        except:
            user_data['department'] = set()
            user_data['department'].add(DEPARTMENT.ADMINISTRATIVE_STAFF)

        department_list = 'Вы выбрали: '
        for department in list(user_data['department']):
            department_list += DEPARTMENT.get_string(department) + ' '
        await query.message.answer(department_list)

#------------------------------------------------------------------------------------


@dp.callback_query_handler(Text(equals='add_dep_' + 'Закончить выбор'), state=AuthState.department)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Напишите о себе:')
    await AuthState.about.set()


@dp.message_handler(state=AuthState.about)
async def auth_dep(message: types.Message, state: FSMContext):
    about = message.text
    _id = get_id()
    data = dict()
    data['id'] = _id
    async with state.proxy() as user_data:
        if about:
            data['about'] = about
        data["coffee_type"] = list(user_data['coffee'])
        data["real_name"] = user_data['name']
        data['department'] = list(user_data['department'])
        data["tg_id"] = user_data['tg_data']['id']
        data["tg_is_bot"] = user_data['tg_data']['is_bot']
        data["tg_first_name"] = user_data['tg_data']['id']
        data["tg_first_name"] = user_data['tg_data']['first_name']
        data["tg_username"] = user_data['tg_data']['username']
        data["tg_language_code"] = user_data['tg_data']['language_code']

    db_users.push(CV(data).to_dict())
    await message.answer('Отлично! профиль успешно создан', reply_markup=main_keyboard(message.from_user.id))
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
    _object = SelectionAlgorithm()
    await message.answer('Пригласить на кофе?', reply_markup=markup)
    for user in _object.get_selection(CV.from_dict(db_users.find_one('tg_id', message.from_user.id))):
        coffee_list = ''
        department_list = ''
        for coffee in user.coffee_type:
            coffee_list += COFFEE.get_string(coffee) + ' '
        for department in user.department:
            department_list += DEPARTMENT.get_string(department) + ' '

        await bot.send_message(message.chat.id,
                               md.text(
                                    md.text("Меня зовут: ", user.real_name +'\n'),
                                    md.text("Мои любимые кофе: ", coffee_list + '\n'),
                                    md.text("Я работаю в отделе(-ax): ", department_list + '\n'),
                                    md.text("Обо мне: ", user.about + '\n'),
                                    md.text("Дата регистрации: ", user.register_date.strftime('%d/%m/%Y') + '\n'),
                                    md.text("Мой рейтинг: ", str(user.rating) + '\n'),
                                      )
                              )
        async with state.proxy() as user_data:
            user_data['select_user'] = user.id
        break

    await MainState.selection.set()


@dp.message_handler(Text(equals='Да'), state=MainState.selection)
async def get_random_user(message: types.Message, state: FSMContext):
    time = reply_submit_keyboard()
    await message.answer('Выберите дату и время когда хотите встретится', reply_markup=time)
    await MainState.set_time.set()


@dp.callback_query_handler(Text(equals='Через час'), state=MainState.set_time)
async def callback_button_media(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_data:
        select_user = user_data['select_user']

    db_meetings.push({'tg_id': query.from_user.id,
                      'meetings': {'target': select_user,
                                    'time':  datetime.datetime.fromtimestamp(time.time() // 1000 + 3600)}})
    await query.message.answer('Встреча записана!')


@dp.message_handler(Text(equals='->'), state=MainState.selection)
async def get_random_user(message: types.Message, state: FSMContext):
    await MainState.main.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('Предложить собеседника')
    await message.answer('Предложить нового собеседника?', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
