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

bot = Bot(token='5129253555:AAFQJvLH0Uvrnpbd77ukEITU2E8R3SN27to')
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

def apply_for_hour(day, hour):
    for el in schedule_list:
        if el.day == day and el.hour==hour:
            if el.isTaken:
                return False
            el.isTaken = True
            return True


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1)

    btns_text = ('Записатись на розклад', '')
   
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    await message.reply("Hi!\nWhat do you want to do?", reply_markup=keyboard_markup)

@dp.message_handler(text="Записатись на розклад")
async def math_functions_menu(message: types.Message):

    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    keyboard_markup.row(*(types.KeyboardButton(day) for day in days))
    choosing_day = True
    await message.answer("Choose day", reply_markup=keyboard_markup)

@dp.message_handler(lambda message: message.text and message.text in days)
async def hours_menu(message: types.Message):
    temp[0] = message.text
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