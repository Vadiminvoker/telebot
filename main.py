import requests
import json
import telebot
from bs4 import BeautifulSoup
from telebot import types


req = requests.get('https://myfin.by/currency/molodechno')
src = req.text
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)
with open('index.html', 'r', encoding='utf-8') as file:
    src = file.read()
soup = BeautifulSoup(src, 'lxml')
find_table = soup.find(class_='c-best-rates').find_all('td')
prodaza = find_table[2].text
find_table = soup.find_all(class_='c-currency-table__main-row--with-arrow')
money = {}
for item in find_table:
    banks = item.find_all('td')[0].text
    course = item.find_all('td')[2].text
    money[banks] = course
final_course = course


total_banks=[]
total_banks.append([k for k in money if money[k] == prodaza])
qqq = str(total_banks)


bot = telebot.TeleBot('5731510422:AAHJeIxRB_rhwrGmlLE10ENQ-rBTY0OZoz8')


payload = {'from': 'BYN', 'to': 'RUB'}
r = requests.get('https://api.tinkoff.ru/v1/currency_rates?', params=payload)
test = r.text
data = json.loads(test)
for i in data['payload']['rates']:
    if i["category"] == "DebitCardsOperations":
        cour1 = str(i['sell'])


@bot.message_handler(commands=['start'])
def course(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cour2 = types.KeyboardButton('Узнай курс на сегодня')
    button2 = types.KeyboardButton("Купить даляры")
    markup.add(cour2, button2)
    bot.send_message(message.chat.id, text="Привет, чтобы узнать курс или купить даляры, нажми на кнопку ",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text=="Узнай курс на сегодня"):
        bot.send_message(message.chat.id, text="Курс на сегодня"+' '+cour1)
    elif(message.text=="Купить даляры"):
        bot.send_message(message.chat.id, text='Минимальный курс в Молодечно: '+ final_course)
        for i in range(len(total_banks)):
            bot.send_message(message.chat.id, text='Купить можно в ' +qqq)
    else:
        bot.send_message(message.chat.id, text='Нажми на одну из кнопок после команды /start!')


bot.polling(none_stop=True)
