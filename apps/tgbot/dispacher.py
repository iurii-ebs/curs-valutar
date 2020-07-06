from django.conf import settings
import logging
import time
import telebot


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi master")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=f'{settings.BOT_BASE}{settings.BOT_PATH}')


def process_new_updates(request):
    update = telebot.types.Update.de_json(request.data)
    bot.process_new_updates([update])
