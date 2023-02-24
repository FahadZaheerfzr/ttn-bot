from telebot import TeleBot
from telebot import types
from components.database import DB


def register(message: types.Message, bot: TeleBot):
    try:
        DB['groups'].insert_one({
            "_id": message.chat.id,
            "fees": {
                "monthly": None,
                "permanent": None
            },
            "owner": message.from_user.id,
            "name": message.chat.title,
            "total_earn" : 0
        })
        bot.reply_to(message, "Group Registered, Use /help to manage it")
    except:
        bot.reply_to(message, "Group Already Registered, Use /help to manage it")
    