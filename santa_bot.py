from random import choice
import telebot
from telebot import types
import os

bot = telebot.TeleBot('token bot')
with open("workers.txt", encoding="utf-8") as workers_file:
    workers = workers_file.readlines()
with open("ids.txt", encoding="utf-8") as id_file:
    ids = id_file.readlines()
    print(ids)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Стать Сантой")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}! Выбери, что бы ты хотел сделать: ", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    user_id = message.from_user.id
    print(user_id)
    if message.text == "Стать Сантой":
        if str(user_id) + "\n" not in ids:
            your_santa = choice(workers)
            bot.send_message(message.chat.id, text=f"Ты даришь подарок: {your_santa}")
            workers.remove(your_santa)
            workers_file = open("workers.txt", "w", encoding="utf-8")
            for elem in workers:
                workers_file.write(elem)

            id_file = open("ids.txt", "a")
            id_file.write(str(user_id) + "\n")
            id_file.close()
        else:
            bot.send_message(message.chat.id, text="Ты уже выбирал")

bot.polling(none_stop=True)
