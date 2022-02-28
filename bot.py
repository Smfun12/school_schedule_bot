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

schedule_list = [] 
days = ['Monday', 'Tuesday','Wednesday', 'Thursday','Friday', 'Saturday','Sunday'] 
hours = ['9:00-9:30','10:00-10:30', '11:00-11:30'] 
zoomlinks = ['', '', ''];
groups = [Group('28/02/2022', '10:00-10:30', 'link', 10), Group('28/02/2022', '9:00-9:30', 'link', 10), Group('28/02/2022', '11:00-11:30', 'link', 10)]
dates = ['28/02/2022', '01/03/2022','02/03/2022', '03/03/2022']
temp = ['',''] 
 
        

def getDates(groups):
    dates = []
    for group in groups:
        if group.date not in dates:
            dates.append(group.date)
    return dates
    
def getHours(groups, date):
    hours = []
    for group in groups:
        if group.date == date and group.time not in hours:
            hours.append(group.time + ",місць=" + str(group.available_place))
    return hours

 
@dp.message_handler(commands='start') 
async def start_cmd_handler(message: types.Message): 
     
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1) 
 
    btns_text = ('Записатись', '') 
    
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text)) 
    
    await message.reply("Привіт!\nЩо ви хочете робити?", reply_markup=keyboard_markup) 
 
@dp.message_handler(text="Записатись") 
async def start(message: types.Message):
    dates = getDates(groups)
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3) 
    keyboard_markup.row(*(types.KeyboardButton(date) for date in dates)) 
    await message.answer("Виберіть дату:", reply_markup=keyboard_markup) 
 
@dp.message_handler(lambda message: message.text and message.text in dates) 
async def hours_menu(message: types.Message): 
    temp[0] = message.text
    hours = getHours(groups, temp[0])
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    keyboard_markup.row(*(types.KeyboardButton(str(hour)) for hour in hours)) 
    await message.answer("Виберіть години", reply_markup=keyboard_markup) 
  
@dp.message_handler(lambda message: message.text and message.text.split(',')[0] in hours) 
async def create_schedule(message: types.Message):
    temp[1] = message.text.split(',')[0]
    found_schedule = False
    for group in groups:
        if group.date == temp[0] and group.time == temp[1]:
            group.available_place -= 1
            break
            
    for schedule in schedule_list:
        if schedule.day == temp[0] and schedule.hour == temp[1]:
            schedule.number_of_people += 1
            found_schedule = True
            break
    if not found_schedule:
        el = Schedule(temp[0], temp[1], 1) 
        schedule_list.append(el) 
    await message.answer("Applied, list=" + str([str(el) for el in schedule_list])) 
     
 
@dp.message_handler() 
async def hello(message: types.Message):
    await message.answer("Your text: " + str(message.text)) 
 
 
if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


