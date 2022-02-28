import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
from constant import TOKEN
from model import Group
from SheetsProcessor import get_login_password

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot) 
admin_telegram_username = ['serdyuuuk','sasha_reshetar']
groups = [Group(1, '28/02 10:00-10:30', 'link', 1), Group(2, '28/02 9:00-9:30', 'link', 10), Group(3, '29/02 11:00-11:30', 'link', 30)]
users= []
commands = ('Записатись', 'Обновити акаунт')
 
@dp.message_handler(commands='start') 
async def start_handler(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:' + message.from_user.username, reply_markup=keyboard_markup)

@dp.message_handler(regexp = '^Група:*') 
async def start_handler(message: types.Message):
    if message.from_user.username not in admin_telegram_username:
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
    if message.from_user.username not in admin_telegram_username:
        await message.answer('Недостатньо прав')
    else:
        available_groups = []
        for group in groups:
            if group.remains() > 0:
                available_groups.append(group.description.split('.')[1])
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for group in available_groups:
            keyboard_markup.add(types.KeyboardButton(group))
        await message.answer('Виберіть групу для розсилки:', reply_markup=keyboard_markup)   

    
@dp.message_handler(commands='request_account')
async def give_or_request_account(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name + ' ' + message.from_user.last_name
    login, password = get_login_password(user_id, user_name)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')
 
@dp.message_handler(text='Оновити аккаунт')
async def give_or_request_account(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name + ' ' + message.from_user.last_name
    login, password = get_login_password(user_id, user_name)
    await message.answer('Успішно записаний, аккаунт:\n' + login + ' ' + password + '\nЯкщо не вдається зайти, напиши @serdyuuuk для отримання нового аккаунта')
  

@dp.message_handler(text="Записатись")
async def signup_handler(message: types.Message):
    available_groups = []
    for group in groups:
        if group.remains() > 0:
            available_groups.append(group.description + ' Місця:' + str(group.remains()))
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in available_groups:
        keyboard_markup.add(types.KeyboardButton(group))
    await message.answer('Виберіть групу:', reply_markup=keyboard_markup)
    
@dp.message_handler(regexp = '^[0-9]+\.Група:*')
async def group_handler(message: types.Message):
    index = 0
    for i, g in enumerate(groups):
        if g.id == message.text.split('.')[0]:
            index = i
            break
    if message.from_user.id not in groups[index].users :
        groups[index].addUser(message.from_user.id)
        await message.answer('Вас записано в ' + groups[index].description + '. Лінк: ' + groups[index].link)
    else :
        await message.answer('Ви вже записані')
    for el in groups:
        print(el.users)
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(command) for command in commands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
 
@dp.message_handler() 
async def hello(message: types.Message):
    await message.answer("Your text: " + str(message.text)) 

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


