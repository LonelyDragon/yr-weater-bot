from asyncio.windows_events import NULL
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.core.management.base import BaseCommand


import logging

import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class Command(BaseCommand):
    help = "Start telegram bot"




    def handle(self, *args, **kwargs):
        
        #API_TOKEN = str(os.getenv('BOT_KEY'))
        API_TOKEN = "1682438195:AAERPpit2Ny4BGMRF6IZBc2B5m5Gbmonq68"
        # Initialize bot and dispatcher
        bot = Bot(token=API_TOKEN)
        dp = Dispatcher(bot, storage=MemoryStorage())
        logging.basicConfig(level=logging.INFO)
        '''
        Конечный автомат для настроек:
        Если пользователь новый:
        #/start -> menu -> button-geo -> set_geolocation -> menu -> button-time -> set_sendtime ->  menu
        Если пользователь сущесвует:
        #/settings -> menu -> button-geo/button-time -> add -> set_geolocation/set_sendtime
        #/settings -> menu -> button-geo/button-time -> delete -> delete_geolocation/delete_sendtime
        #
        '''
        class Settings(StatesGroup):
            show_menu_settings = State()
            set_location = State()
            set_time = State()
            

        @dp.message_handler(commands=['start'])
        #при нажатии кнопки, информация о пользователе должна падать в логи и создавать в моделях запись о юзере
        async def send_welcome(message: types.Message):
            """
            This handler will be called when user sends `/start`
            """
            logging.info(f"User: {message.from_user.first_name}")
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            geo_button = KeyboardButton(text='Geolocation')
            alert_time = KeyboardButton(text='Time')
            buttons = [geo_button, alert_time]
            keyboard.add(*buttons)
            await message.answer("Welcome to the weather app!\nPlease, set your location and alert time", reply_markup=keyboard)
            await Settings.show_menu_settings.set()

        @dp.message_handler(state=Settings.show_menu_settings)
        async def settings_menu(message:types.Message, state: FSMContext):        
            async with state.proxy():
                if message.text == "Geolocation":
                    message.answer(f"Please, send your location, {message.from_user}")
                    await message.reply("Please, send your location")
                    await Settings.set_location.set()
                elif message.answer == "Time":
                    await message.answer("Does not support")



        @dp.message_handler(lambda message: message.text == "Geolocation")
        async def send_location(message: types.Message):
            if message.location != NULL:
                await message.answer(f'Your location is: {message.location}')


        @dp.message_handler(commands=["settings"])
        async def settings(message: types.Message):
            """
            This handler allows you to change user preferences
            """
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            geo_button = KeyboardButton(text='Geolocation')
            alert_time = KeyboardButton(text='Time')
            buttons = [geo_button, alert_time]
            keyboard.add(*buttons)
            await message.answer("Settings are updated")



        

        executor.start_polling(dp, skip_updates=True)