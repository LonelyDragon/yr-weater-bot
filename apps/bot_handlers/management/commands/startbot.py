from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from django.core.management.base import BaseCommand

import logging

import os

from aiogram import Bot, Dispatcher, executor, types

class Command(BaseCommand):
    help = "Start telegram bot"
    
    def handle(self, *args, **kwargs):
        pass

        #API_TOKEN = str(os.getenv('BOT_KEY'))
        API_TOKEN = "1682438195:AAGf3KyOU_5nx-eYw-OOy5DfJDCw_wNYbrc"
        # Initialize bot and dispatcher
        bot = Bot(token=API_TOKEN)
        dp = Dispatcher(bot)

        @dp.message_handler(commands=['start'])
        async def send_welcome(message: types.Message):
            """
            This handler will be called when user sends `/start`
            """
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            geo_button = KeyboardButton(text='Geolocation')
            keyboard.add(geo_button)

            await message.reply("Welcome to the weather app!\nPlease, send your location", reply_markup=keyboard)


        


        executor.start_polling(dp, skip_updates=True)