import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
from constant import TOKEN
from model import Group

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot) 

groups = [Group(1, '28/02 10:00-10:30', 'link', 1), Group(2, '28/02 9:00-9:30', 'link', 10), Group(3, '29/02 11:00-11:30', 'link', 30)]
users= []

 
@dp.message_handler(commands='start') 
async def start_handler(message: types.Message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
    print(users)
    comands = ('Записатись', 'Обновити акаунт')
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(comand) for comand in comands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
    
@dp.message_handler(text="Записатись")
async def signup_handler(message: types.Message):
    comands = []
    for group in groups:
        if group.remains() > 0:
            comands.append(group.description + ' Місця:' + str(group.remains()))
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for comand in comands:
        keyboard_markup.add(types.KeyboardButton(comand))
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
    print(groups[index])
    comands = ['Записатись', 'Обновити акаунт']
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(*(types.KeyboardButton(comand) for comand in comands))
    await message.answer('Виберіть дію:', reply_markup=keyboard_markup)
 
@dp.message_handler() 
async def hello(message: types.Message):
    await message.answer("Your text: " + str(message.text)) 

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


