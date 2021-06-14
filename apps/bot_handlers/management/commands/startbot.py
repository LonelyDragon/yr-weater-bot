from asyncio.windows_events import NULL
from typing import Set
from aiogram.types import location
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
        
        API_TOKEN = str(os.getenv('BOT_TOKEN'))
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

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        geo_button = KeyboardButton(text='Geolocation')
        alert_time = KeyboardButton(text='Time')
        buttons = [geo_button, alert_time]
        keyboard.add(*buttons)
        
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

            await message.answer(f"Welcome to the weather app, {message.from_user.username}!\nPlease, set your location and alert time", reply_markup=keyboard)
            await Settings.show_menu_settings.set()

        @dp.message_handler(state=Settings.show_menu_settings)
        async def settings_menu(message:types.Message, state: FSMContext):        
            async with state.proxy():
                if message.text == "Geolocation":
                    await Settings.set_location.set()
                    await message.answer(f"Please, send your location:", reply_markup=ReplyKeyboardRemove())
                elif message.text == "Time":
                    await message.answer("Does not support")


        @dp.message_handler(state=Settings.set_location, content_types=types.ContentType.LOCATION)
        async def send_location(message: types.Message):
            if message.location:
                await message.answer(f'Your location is: {message.location}')
                await Settings.show_menu_settings.set()
            else:
                await message.answer(f"Please, send your location:")


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