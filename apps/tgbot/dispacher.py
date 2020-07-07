import re
import time
import secrets
import logging
import telebot

from django.conf import settings

from .models import TelegramUser
from .tokens import build_token, match_token


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['build_token'], content_types=['text'])
def build_token_handler(message):
    bot.send_message(message.chat.id, build_token())


@bot.message_handler(commands=['start'], content_types=['text'])
def match_token_handler(message):
    token = message.text.replace('/start ', '', 1)
    chat_id = message.chat.id

    if match_token(token):
        user = TelegramUser.objects.filter(token=token).first()
        user.chat_id = chat_id
        user.save()
        bot.send_message(message.chat.id, "User registred")
    else:
        bot.send_message(chat_id, "User does not registred")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, 'HI')


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=f'{settings.BOT_BASE}{settings.BOT_PATH}')


def process_new_updates(request):
    update = telebot.types.Update.de_json(request.data)
    bot.process_new_updates([update])


def telegram_user(chat_id, text):
    bot.send_message(chat_id, text)


# Telegram message object example
MESSAGE = {
    "content_type": "text",
    "message_id": 50,
    "from_user": {
        "id": 912545219,
        "is_bot": False,
        "first_name": "Artiom",
        "username": "None",
        "last_name": "Rotari",
        "language_code": "en",
        "can_join_groups": "None",
        "can_read_all_group_messages": "None",
        "supports_inline_queries": "None"
    },
    "date": 1594122966,
    "chat": {
        "id": 912545219,
        "type": "private",
        "title": "None",
        "username": "None",
        "first_name": "Artiom",
        "last_name": "Rotari",
        "all_members_are_administrators": "None",
        "photo": "None",
        "description": "None",
        "invite_link": "None",
        "pinned_message": "None",
        "permissions": "None",
        "slow_mode_delay": "None",
        "sticker_set_name": "None",
        "can_set_sticker_set": "None"
    },
    "forward_from": "None",
    "forward_from_chat": "None",
    "forward_from_message_id": "None",
    "forward_signature": "None",
    "forward_date": "None",
    "reply_to_message": "None",
    "edit_date": "None",
    "media_group_id": "None",
    "author_signature": "None",
    "text": "hi",
    "entities": "None",
    "caption_entities": "None",
    "audio": "None",
    "document": "None",
    "photo": "None",
    "sticker": "None",
    "video": "None",
    "video_note": "None",
    "voice": "None",
    "caption": "None",
    "contact": "None",
    "location": "None",
    "venue": "None",
    "animation": "None",
    "dice": "None",
    "new_chat_member": "None",
    "new_chat_members": "None",
    "left_chat_member": "None",
    "new_chat_title": "None",
    "new_chat_photo": "None",
    "delete_chat_photo": "None",
    "group_chat_created": "None",
    "supergroup_chat_created": "None",
    "channel_chat_created": "None",
    "migrate_to_chat_id": "None",
    "migrate_from_chat_id": "None",
    "pinned_message": "None",
    "invoice": "None",
    "successful_payment": "None",
    "connected_website": "None",
    "json": {
        "message_id": 50,
        "from": {
            "id": 912545219,
            "is_bot": False,
            "first_name": "Artiom",
            "last_name": "Rotari",
            "language_code": "en"

        },
        "chat": {
            "id": 912545219,
            "first_name": "Artiom",
            "last_name": "Rotari",
            "type": "private"
        },
        "date": 1594122966,
        "text": "hi"
    }
}
