import time

import telebot
from django.conf import settings

from .models import TelegramUser
from .tokens import match_token


# Init bot
bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'], content_types=['text'])
def start_token(message):
    token = message.text.replace('/start ', '', 1)

    if match_token(token):
        chat_user = TelegramUser.objects.filter(token=token).first()

        if chat_user is None:
            bot.send_message(message.chat.id, "Token is invalid")

        else:
            chat_user.chat_id = message.chat.id
            chat_user.save()
            bot.send_message(message.chat.id, "Token is valid")
    else:
        bot.send_message(message.chat.id, "Please follow {register link}")


@bot.message_handler(commands=['message'], content_types=['text'])
def test_message(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(func=lambda m: True, content_types=['text'])
def test_echo(message):
    bot.send_message(message.chat.id, message.text)


# Setup webhook
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=f'{settings.BOT_BASE}{settings.BOT_PATH}')


def bot_update(request):
    """
    Update bot
    """

    update = telebot.types.Update.de_json(request.data)
    bot.process_new_updates([update])


def bot_notify(user, text):
    """
    Find chat_id of specified user and telegram it with 'text'
    Return True if message is sent or false if it's not
    """

    chat_user = TelegramUser.objects.filter(user=user).first()

    if chat_user is not None:
        bot.send_message(chat_user.chat_id, text)
        return True

    return False
