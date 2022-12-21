from random import choice
import telebot
from telebot import types

def getting_name(id):
    with open("wish.txt", encoding="utf-8") as wish_file:
        wishes = wish_file.readlines()
        for elem in wishes:
            if id in elem:
                elem = elem.split()
                return elem[1]

bot = telebot.TeleBot('token')
with open("wish.txt", encoding="utf-8") as wish_file:
    wishes = wish_file.readlines()
with open("workers.txt", encoding="utf-8") as workers_file:
    workers = workers_file.readlines()

name = ""
wish = ""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Напиши свою фамилию:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    with open("s.txt", encoding="utf-8") as s_file:
        s_list = s_file.readlines()
        for elem in s_list:
            if name.lower() in elem.lower():
                bot.send_message(message.from_user.id, "Напиши свое пожелание на подарок:")
                bot.register_next_step_handler(message, get_wish)
                break
        else:
            bot.send_message(message.from_user.id, "Не могу найти вас в списке, напишите свою фамилию верно")
            bot.register_next_step_handler(message, get_name_again)

def get_name_again(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Напиши свое пожелание на подарок:")
    bot.register_next_step_handler(message, get_wish)

def get_wish(message):
    global wish
    wish = message.text
    user_id = str(message.from_user.id)
    wishes.append(user_id + " " + name + " " + wish + "\n")
    wish_file = open("wish.txt", "a", encoding="utf-8")
    wish_file.write(user_id + " " + name + " " + wish + "\n")
    wish_file.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список пожеланий")
    btn2 = types.KeyboardButton("Стать Сантой")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text=f"{message.from_user.first_name}! Выбери, что бы ты хотел сделать: ", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    user_id = str(message.from_user.id)
    if message.text == "Стать Сантой":
        id_file = open("ids.txt", "r")
        ids = id_file.readlines()
        id_file.close()
        if user_id in ids[0]:
            bot.send_message(message.chat.id, text="Ты уже участвуешь")
        else:
            your_santa = choice(workers)
            name = getting_name(user_id)
            while name.lower() in your_santa.lower():
                your_santa = choice(workers)
            bot.send_message(message.chat.id, text=f"Ты секретный Cанта для: {your_santa}")

            workers.remove(your_santa)
            workers_file = open("workers.txt", "w", encoding="utf-8")
            for elem in workers:
                workers_file.write(elem)

            ids.append(user_id)
            id_file = open("ids.txt", "w")
            ids = " ".join(ids)
            id_file.write(ids)
            id_file.close()

    if message.text == "Список пожеланий":
        wishes_result = ""
        for elem in wishes:
            elem = elem.split()
            new_wish = " ".join(elem[2:])
            wishes_result += elem[1] + " - " + new_wish + "\n"
        bot.send_message(message.from_user.id, wishes_result)

bot.polling(none_stop=True)
