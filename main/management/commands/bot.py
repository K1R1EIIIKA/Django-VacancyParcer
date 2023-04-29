import time
from django.core.management.base import BaseCommand

import requests
import telebot

TOKEN = '6150513881:AAG6Mqg9JYNlShhX_hJU1VTOPQ6irEq7l1c'
URL = 'https://api.telegram.org/bot'
file_log_bot = open('log_bot.txt', 'w', encoding='utf-8')
updates = []

bot = telebot.TeleBot('6150513881:AAG6Mqg9JYNlShhX_hJU1VTOPQ6irEq7l1c')


@bot.message_handler(commands=['huy'])
def huy(message):
    bot.send_message(message.chat.id, 'asd')


def send_message_to_user(username, vacancy, city, data_hhru, data_superjob, data_zarplataru):
    updates = get_updates()

    for update in updates:
        if update['message']['chat']['username'] == username:

            bot.send_message(update['message']['chat']['id'],
                             'Привет, ' + username
                             + '. Вакансии ' + str(vacancy.capitalize())
                             + ' в городе ' + str(city.capitalize()) + ' \n\n\n'
                             + form_data(data_hhru, data_superjob, data_zarplataru))
            break


def form_data(data_hhru, data_superjob, data_zarplataru):
    data = ''
    data += 'Вакансии с hh.ru: \n\n'
    data += form_data_piece(data_hhru)

    data += '\n\nВакансии с superjob.ru: \n\n'
    data += form_data_piece(data_superjob)

    data += '\n\nВакансии с zarplata.ru: \n\n'
    data += form_data_piece(data_zarplataru)

    return data


def form_data_piece(data_site):
    data = ''
    for data_piece in data_site:
        data += f'Название: {data_piece["name"]}\n'

        if data_piece['address']:
            data += f'Адрес: {data_piece["address"]}\n'
        else:
            data += f'Адрес: Не указан\n'

        if data_piece.get("is_salary"):
            if data_piece['salary_from']:
                if data_piece['salary_to']:
                    data += f'Зарплата: От {data_piece["salary_from"]} до {data_piece["salary_to"]}\n'
                else:
                    data += f'Зарплата: От {data_piece["salary_from"]}\n'

            else:
                data += f'Зарплата: До {data_piece["salary_to"]}\n'

        else:
            data += f'Зарплата: Не указана\n'

        data += f'Ссылка: {data_piece["link"]}\n\n'

    return data


def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result'] if 'result' in result else []


def start(updates):
    updates = get_updates()

    while True:
        time.sleep(2)
        updates = get_updates()


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        start(updates)
        bot.infinity_polling()
