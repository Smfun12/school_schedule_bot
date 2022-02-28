import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
from constant import TOKEN
from model import Group, Schedule

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot) 
 
groups = [Group('28/02/2022', '10:00-10:30', 'link', 20), Group('28/02/2022', '9:00-9:30', 'link', 10), Group('29/02/2022', '11:00-11:30', 'link', 30)]
users= []
temp = ['','']

 
@dp.message_handler(commands='start') 
async def start_cmd_handler(message: types.Message): 
    users.append([message.from_user.id, message.from_user.username]);
    
 
@dp.message_handler() 
async def hello(message: types.Message):
    await message.answer("Your text: " + str(message.text)) 
 
 
if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


