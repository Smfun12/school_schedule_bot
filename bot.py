import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
from constant import TOKEN, groups, admin_telegram_ids, commands
from model import Group, User, BotObject
from SheetsProcessor import get_login_password, upd_data,upd_group_data, fetch_user_with_groups
from util import *


logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot) 


botObject = BotObject(groups=groups, users=[], admin_telegram_ids=admin_telegram_ids, writeName=False)


@dp.message_handler(commands='upd_data')
async def do_upd_data(message: types.Message):
    if is_admin(message.from_user.id, botObject.admin_telegram_ids):
        #upd_data()
        upd_group_data()
        botObject.groups, botObject.users = fetch_data()
        await message.answer('Оновлено!')


@dp.message_handler(commands='start') 
async def start_handler(message: types.Message):
    id = message.from_user.id
    user = find_user_by_id(id, botObject.users)
    if user is None:
        print('user is none')
        botObject.users.append(User(id, message.from_user.username))
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)

    
@dp.message_handler(text='Назад')
async def back_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)

@dp.message_handler(text='Ввести дані')
async def setname_handler(message: types.Message):
    botObject.writeName = True
    await message.answer("Введіть ім'я та вік дитини: ", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(regexp = '^Група:*') 
async def send_links(message: types.Message):
    if not is_admin(message.from_user.username, botObject.admin_telegram_ids):
        await message.answer('Недостатньо прав')
    else:
        requested_group = None
        for group in botObject.groups:
            if group.description.split('.')[1] == message.text:
                requested_group = group
                break
        group_users = requested_group.users
        for user_id in group_users:
            await bot.send_message(user_id, requested_group.link)
        await message.answer('Розсилаю...')
    
@dp.message_handler(commands='send') 
async def send_handler(message: types.Message):
    if not is_admin(message.from_user.username, botObject.admin_telegram_ids):
        await message.answer('Недостатньо прав')
    else:
        available_groups = []
        for group in botObject.groups:
            available_groups.append(group.description.split('.')[1])
        available_groups.append('Назад')
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for group in available_groups:
            keyboard_markup.add(types.KeyboardButton(group))
        await message.answer('Виберіть групу для розсилки:', reply_markup=keyboard_markup)   

    
@dp.message_handler(commands='request_account')
async def give_or_request_account(message: types.Message):
    curr_user = find_user_by_id(message.from_user.id, botObject.users)
    if curr_user is None:
        curr_user = User(message.from_user.id, message.from_user.username, groups=[])
    
    login, password = get_login_password(curr_user.id, curr_user.username,curr_user.groups)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')

@dp.message_handler(text='Аккаунт з Minecraft')
async def update_account(message: types.Message):
    curr_user = find_user_by_id(message.from_user.id, botObject.users)
    print('Curr user=' +  str(curr_user))
    if curr_user is None:
        curr_user = User(message.from_user.id, message.from_user.username, groups=[])
    login, password = get_login_password(curr_user.id, curr_user.username, curr_user.groups)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')



@dp.message_handler(text="Записатись")
async def signup_handler(message: types.Message):
    available_groups = []
    for i, group in enumerate(botObject.groups):
        if group.remains() > 0:
            available_groups.append(group.description + ' Місця:' + str(group.remains()))
    available_groups.append('Назад')
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in available_groups:
        keyboard_markup.add(types.KeyboardButton(group))
    
    await message.answer('Виберіть групу:', reply_markup=keyboard_markup)
    
@dp.message_handler(regexp = '^[0-9]+\.Група:*')
async def group_handler(message: types.Message):
    group_id = int(message.text.split('.')[0])
    if not user_is_in_group(message.from_user.id, group_id, botObject.users):
        botObject.groups[group_id-1].addUser(message.from_user.id)
        for user in botObject.users:
            if user.id == message.from_user.id:
                user.groups.append(botObject.groups[group_id-1].id)
                break
        await message.answer('Вас записано в ' + botObject.groups[group_id-1].description + '. Лінк: ' + botObject.groups[group_id-1].link)
    else :
        await message.answer('Ви вже записані')
    

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
    
@dp.message_handler()
async def anyText_handler(message: types.Message):
    if botObject.writeName:
        id = message.from_user.id
        user = find_user_by_id(id, botObject.users)
        if user is None:
            botObject.users.append(User(id, message.from_user.username, message.text))
        else:
            user.description = message.text
        botObject.writeName = False
        await message.answer('Дані успішно змінено. ' + str(user))
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
        await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
    else:
        await message.answer("Я попугай, ви сказали: " + str(message.text)) 

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


