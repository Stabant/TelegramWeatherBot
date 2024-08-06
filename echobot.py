#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import requests
from dotenv import load_dotenv
import os

load_dotenv()

Weather_API_KEY = os.getenv('Weather_API_KEY')
Tele_Bot_Key = os.getenv('Tele_Bot_Key')

bot = telebot.TeleBot(Tele_Bot_Key)


def getWeather(city):
    url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={Weather_API_KEY}"
    response = requests.get(url)
    WeatherDict = response.json()
    print(response.status_code)
    condition = WeatherDict["current"]['condition']["text"]
    temp = WeatherDict["current"]["feelslike_c"]
    gust = WeatherDict["current"]['gust_kph']
    print(str(url))
    return f"It is currently {condition}, it feels like {temp}C, and the gust speed is {gust}kph"
    

# Handle '/start' and '/help'a
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you! who\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(commands=['weather'])
def echo_message(message):
    cityname = message.text
    cityname = cityname.split()
    cityname.pop(0)
    print(len(cityname))
    if len(cityname) == 0:
        bot.reply_to(message,"Please enter a real city in the format /weather (city_name)")
    else:
        weatherReport = getWeather(cityname)
        bot.reply_to(message,weatherReport)
        

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    initial_message = """
    This bot can tell you the weather in any city. Just send /weather and then your city name
    \U0001F923
    """
    bot.send_message(message.chat.id, initial_message)
bot.infinity_polling()