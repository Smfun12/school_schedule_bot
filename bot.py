import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
from constant import TOKEN
from model import Group, User
from SheetsProcessor import get_login_password, upd_data, fetch_user_with_groups

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot) 
admin_telegram_username = ['serdyuuuk','sasha_reshetar']
groups = [Group(1, '01/03 15:00-17:00', 'https://us02web.zoom.us/j/88456997619?pwd=V0ZKNk5zSnZMb2s5UG1wOWxJSktGZz09', 25, [])]
users= []
commands = ('Записатись', 'Аккаунт з Minecraft', 'Вести дані')

writeName = False

def find_user_by_id(id):
    for user in users:
        if user.id == id:
            return user

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user

def is_admin(username):
    return username in admin_telegram_username

def user_in_group(group, user):
    for us in group.users:
        if us.id == user.id:
            return True
    return False

def fetch_data():
    usernames, ids, fetch_groups = fetch_user_with_groups()
    users_copy = []
    new_groups = [Group(1, '28/02 10:00-10:30', 'link', 1, []), Group(2, '28/02 9:00-9:30', 'link', 10, []), Group(3, '29/02 11:00-11:30', 'link', 30, [])]

    for i in range(0, len(usernames)):
        user = User(ids[i], usernames[i], fetch_groups[i])
        users_copy.append(user)
        for el in new_groups:
            el.users = []
            if str(el.id) in fetch_groups[i] and not user_in_group(el, user):
                el.users.append(user)
                el.available_place -= 1
    groups = new_groups


@dp.message_handler(commands='upd_data')
async def do_upd_data(message: types.Message):
    if is_admin(message.from_user.username):
        upd_data()
        #upd_group_data()
        #fetch_data()
        await message.answer('Оновлено!')


@dp.message_handler(commands='start') 
async def start_handler(message: types.Message):
    id = message.from_user.id
    user = find_user_by_id(id)
    if user is None:
        users.append(User(id, message.from_user.username))
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)

    
@dp.message_handler(text='Назад')
async def back_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)

@dp.message_handler(text='Вести дані')
async def setname_handler(message: types.Message):
    global writeName 
    writeName = True
    await message.answer("Ведіть ім'я та вік дитини: ", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(regexp = '^Група:*') 
async def start_handler(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer('Недостатньо прав')
    else:
        requested_group = None
        for group in groups:
            if group.description.split('.')[1] == message.text:
                requested_group = group
                break
        group_users = requested_group.users
        for user_id in group_users:
            await bot.send_message(user_id, group.link)
        await message.answer('Розсилаю...')
    
@dp.message_handler(commands='send') 
async def start_handler(message: types.Message):
    if not is_admin(message.from_user.username):
        await message.answer('Недостатньо прав')
    else:
        available_groups = []
        for group in groups:
            available_groups.append(group.description.split('.')[1])
        available_groups.append('Назад')
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for group in available_groups:
            keyboard_markup.add(types.KeyboardButton(group))
        await message.answer('Виберіть групу для розсилки:', reply_markup=keyboard_markup)   

    
@dp.message_handler(commands='request_account')
async def give_or_request_account(message: types.Message):
    curr_user = find_user_by_id(message.from_user.id)
    if curr_user is None:
        curr_user = User(message.from_user.id, message.from_user.username)
    login, password = get_login_password(curr_user.id, curr_user.username)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')

@dp.message_handler(text='Аккаунт з Minecraft')
async def update_account(message: types.Message):
    curr_user = find_user_by_id(message.from_user.id)
    if curr_user is None:
        curr_user = User(message.from_user.id, message.from_user.username)
    login, password = get_login_password(curr_user.id, curr_user.username, groups)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')



@dp.message_handler(text="Записатись")
async def signup_handler(message: types.Message):
    available_groups = []
    for i, group in enumerate(groups):
        if group.remains() > 0:
            available_groups.append(group.description + ' Місця:' + str(group.remains()))
    available_groups.append('Назад')
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in available_groups:
        keyboard_markup.add(types.KeyboardButton(group))
    await message.answer('Виберіть групу:', reply_markup=keyboard_markup)
    
@dp.message_handler(regexp = '^[0-9]+\.Група:*')
async def group_handler(message: types.Message):
    index = int(message.text.split('.')[0])

    if message.from_user.id not in groups[index-1].users:
        groups[index-1].addUser(message.from_user.id)
        for user in users:
            if user.username == message.from_user.username:
                user.groups.append(groups[index-1].id)
                break
        await message.answer('Вас записано в ' + groups[index-1].description + '. Лінк: ' + groups[index-1].link)
    else :
        await message.answer('Ви вже записані')
    

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
    
@dp.message_handler()
async def anyText_handler(message: types.Message):
    global writeName
    if writeName:
        id = message.from_user.id
        user = find_user_by_id(id)
        if user is None:
            users.append(User(id, message.from_user.username, message.text))
        else:
            user.description = message.text
        writeName = False
        await message.answer('Дані успішно змінено. ' + str(user))
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
        await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
    else:
        await message.answer("Я попугай, ви сказали: " + str(message.text)) 

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


