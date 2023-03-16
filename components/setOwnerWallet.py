from telebot import TeleBot
from telebot import types
from components.database import DB
import string, random
from web3 import Web3
import config
from components import settings


web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))

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
    return settings.settingStart(message, bot)

    #bot.send_message(message.chat.id, "Back to settings", reply_markup=types.ReplyKeyboardRemove())
    #return settings.settingStart(message, bot)
    # bot.send_message(
    #     message.chat.id,
    #     text=text_to_send,
    #     parse_mode='HTML',
    #     reply_markup=keyboards.settingPrivateMarkup(chat_id)
    # )

def changeWalletStart(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    chat_id = message.data.split(" ")[1]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id, "Please enter your BNB Bep-20 Wallet Address.", reply_markup=markup)
    bot.register_next_step_handler(message.message, updateWallet, bot, chat_id)

def updateWallet(message: types.Message, bot: TeleBot, chat_id):
    if message.text == "cancel": return backSettings(message, bot, chat_id)
    if not web3.isAddress(message.text): 
        bot.reply_to(message, "Wrong Wallet Address, Please Try Again!")
        return bot.register_next_step_handler(message, updateWallet, bot, chat_id)

    all_admins = bot.get_chat_administrators(chat_id)
    is_admin = False
    
    for x in all_admins:
        if x.user.id == message.from_user.id: is_admin = True

    if not is_admin: return bot.reply_to(message, "This Command Is Only For Admins", reply_markup=types.ReplyKeyboardRemove())

    DB['users'].update_one(
        {"_id": message.from_user.id},
        {"$set": {"owner_wallet": Web3.toChecksumAddress(message.text)}}
    )

    bot.send_message(message.chat.id, "Wallet Updated", reply_markup=types.ReplyKeyboardRemove())
    backSettings(message, bot, chat_id)