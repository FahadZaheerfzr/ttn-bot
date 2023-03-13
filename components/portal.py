from telebot import TeleBot
from telebot import types
from components.database import DB
import string, random
from web3 import Web3
import config, os
from components import keyboards


def backSettings(message: types.Message, bot: TeleBot, chat_id):
    group_info = DB['groups'].find_one({"_id": int(chat_id)})
    owner_info = DB['users'].find_one({"_id": group_info['owner']})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.send_message(message.chat.id, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")
    
    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id): is_admin = True
    if not is_admin: return bot.reply_to(message, "You are not admin!")

    text_to_send = f"""
Owner Wallet: <code>{owner_info['owner_wallet']}</code>
Monthly Fees: <code>{group_info['fees']['monthly']}</code>
One Time Fees: <code>{group_info['fees']['permanent']}</code>
    """

    bot.send_message(message.chat.id, "Back to settings", reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(
        message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.settingPrivateMarkup(chat_id)
    )


def portalStart(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    chat_id = message.data.split(" ")[1]

    # bot.delete_message(message.message.chat.id, message.message.id)
    # print(os.getcwd())

    photo = open('./media/portal.jpg', 'rb')
    bot.send_photo(
        message.message.chat.id,
        photo,
        caption="Portal Link: {}".format(f"https://t.me/{bot.get_me().username}?start={chat_id}"),
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.send_message(message.message.chat.id, "<i>Send the message above to a channel in order to create a public portal, or share the link with your community on other social media outlets.</i>", parse_mode="HTML")
    backSettings(message, bot, chat_id)
