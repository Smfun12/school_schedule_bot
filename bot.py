import logging 
import math22 
import math 
import requests 
import random 
from aiogram import Bot, Dispatcher, executor, types 
 
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG) 
 
schedule_list = [] 
days = ['Monday', 'Tuesday','Wednesday', 'Thursday','Friday', 'Saturday','Sunday'] 
hours = ['9:00-9:30','10:00-10:30', '11:00-11:30'] 
zoomlinks = ['', '', ''];
 
bot = Bot(token='5253652716:AAEvUly9LXT9-UzP9MxKsCwnNcLW3HiaRH0') 
dp = Dispatcher(bot) 
 
 
temp = ['',''] 
 
class Schedule: 
    def __init__(self, day, hour, isTaken, number_of_people): 
        self.day = day 
        self.hour = hour 
        self.isTaken = False 
        self.number_of_people = number_of_people 
         
    def __str__(self): 
        return 'Day='+ self.day + ', hour='+ self.hour + ', number_of_people='+ str(self.number_of_people) 

 
class Group:
    usersId = []
 
    def __init__(self, date, time, link):
        self.date = date
        self.time = time
        self.link = link
        
    def addUser(userId):
        users.append(userId)
        
    def contains(userId):
        if user in usersId:
            return True
        else:
            return False
        
groups = [Group('28/02/2022', '10:00', 'link')]
dates = []
hours = []

def getDates(groups):
    dates = []
    for group in groups:
        if group.date not in dates:
            dates.append(group.date)
    return dates
    
def getHours(groups, date):
    hours = []
    for group in groups:
        if group.data == date and group.time not in hours:
            hours.append(group.time)
    return hours

 
@dp.message_handler(commands='start') 
async def start_cmd_handler(message: types.Message): 
     
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1) 
 
    btns_text = ('Записатись', '') 
    
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text)) 
    
    await message.reply("Привіт!\nЩо ви хочете робити?", reply_markup=keyboard_markup) 
 
@dp.message_handler(text="Записатись") 
async def math_functions_menu(message: types.Message): 
    dates = getDates(groups)
    print(dates)
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3) 
    keyboard_markup.row(*(types.KeyboardButton(date) for date in dates)) 
    await message.answer("Виберіть дату:", reply_markup=keyboard_markup) 
 
@dp.message_handler(lambda message: message.text and message.text in dates) 
async def hours_menu(message: types.Message): 
    temp[0] = message.text 
    hours = getHours(groups, temp[0])
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3) 
    keyboard_markup.row(*(types.KeyboardButton(hour) for hour in hours)) 
 
    await message.answer("Choose hour", reply_markup=keyboard_markup) 
  
@dp.message_handler(lambda message: message.text and message.text in hours) 
async def createSchedule(message: types.Message): 
    temp[1] = message.text 
    el = Schedule(temp[0], temp[1], False, 1) 
    schedule_list.append(el) 
    await message.answer("Applied, list=" + str([str(el) for el in schedule_list])) 
     
 
@dp.message_handler() 
async def hello(message: types.Message): 
    await message.answer("Your text: " + str(message.text)) 
 
 
if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True)


