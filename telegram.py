import telebot
from telebot import types
import os
from dotenv import load_dotenv
from db import Database

load_dotenv()
# Токен, который вы получили от BotFather
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
db = Database()
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    msg = bot.reply_to(message, "Привет! "
                          "Я умею показывать погоду. "
                          "Отправь мне название города или своё местоположение.")
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    if message.content_type == 'text':
        city_name = message.text
        coordinates = get_city_coordinates(city_name)
        bot.reply_to(message, f"Координаты города {city_name}: {coordinates}")
    elif message.content_type == 'location':
        longitude = message.location.longitude
        latitude = message.location.latitude
        city_name = reverse_geocode(latitude, longitude)
        bot.send_message(message.chat.id, f"Твои координаты: долгота {longitude}, широта {latitude}, город {city_name}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    coordinates = get_city_coordinates(message.text)
    bot.reply_to(message, f"Ты написал: {message.text}"
                          f"Координаты города {message.text}: {coordinates}")


@bot.message_handler(content_types=['location'])
def handle_location(message):
    longitude = message.location.longitude
    latitude = message.location.latitude
    bot.send_message(message.chat.id, f"Твои координаты: долгота {longitude}, широта {latitude}")


import requests


def get_city_coordinates(city_name):
    # Формирование URL запроса к Nominatim API
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json'
    }

    # Выполнение запроса
    response = requests.get(url, params=params)
    data = response.json()

    if data:
        # Получение координат из первого результата
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return (latitude, longitude)
    else:
        return "Координаты не найдены."


def reverse_geocode(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': latitude,
        'lon': longitude,
        'format': 'json'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data and 'address' in data:
        # Можно настроить, какую часть адреса вы хотите извлечь
        address = data['address']
        # Выведем, например, название города или деревни
        city = address.get('city', '') or address.get('town', '') or address.get('village', '')
        return city
    else:
        return "Название населённого пункта не найдено."
# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
