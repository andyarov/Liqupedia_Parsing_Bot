import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot("telegram.token")
# create buttons
category = types.ReplyKeyboardMarkup(resize_keyboard=True)
apex_button = types.KeyboardButton('Apex Legends')
valorant_button = types.KeyboardButton('Valorant')
category.add(apex_button, valorant_button)

@bot.message_handler(commands = ["start"])
# get start
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.chat.username}, choose a category", reply_markup=category)

@bot.message_handler(content_types = 'text')
# get category and send answer
def get_category(message):
    # parsing url, write in a dictionary key = title, value = href
    # and display website redirect buttons
    if message.text == 'Apex Legends':
        url = 'https://liquipedia.net/valorant/S-Tier_Tournaments'
        tournaments = {}
        page = requests.get(url)
        # print(page.status_code)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            all_tournaments = soup.findAll('div', class_="gridCell Tournament Header")

            for tag in all_tournaments:
                tournaments[tag.find_all('a')[1]['title']] = tag.find_all('a')[1]['href']

            markup = types.InlineKeyboardMarkup(row_width=1)
            button_list = [types.InlineKeyboardButton(f'{key.replace("/", " ", 3)}',
                                                      url=f"http://liquipedia.net{tournaments[key]}") for key in
                           tournaments]
            markup.add(*button_list)
            bot.send_message(message.chat.id, 'tournaments', reply_markup=markup)
    elif message.text == 'Valorant':
        url = 'https://liquipedia.net/apexlegends/S-Tier_Tournaments'
        tournaments = {}
        page = requests.get(url)
        # print(page.status_code)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            all_tournaments = soup.findAll('div', class_="divCell Tournament Header-Premier")

            for tag in all_tournaments:
                tournaments[tag.find_all('a')[1]['title']] = tag.find_all('a')[1]['href']

            markup = types.InlineKeyboardMarkup(row_width=1)
            button_list = [types.InlineKeyboardButton(f'{key.replace("/", " ", 3)}',
                                                      url=f"http://liquipedia.net{tournaments[key]}") for key in
                           tournaments]
            markup.add(*button_list)
            bot.send_message(message.chat.id, 'tournaments', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"{message.chat.username}, choose a category", reply_markup=category)



bot.polling(none_stop=True, interval=0)