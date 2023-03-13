from telebot import TeleBot
from telebot import types
from components.database import DB
from eth_account import Account
import secrets
from web3 import Web3
from components import settings
from components.start import createWallet
import config
from components import start
import pprint
web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))

def middlewareMainHandler(message: types.CallbackQuery, bot: TeleBot):
    command = message.data.split("_")[1]
    if command == "main": return mainHandler(message, bot)
    if command == "list": return listHandler(message, bot)
    if command == "add": return addHandler(message, bot)
    if command == "remove": return removeHandler(message, bot)
    if command == "statistic": return statisticHandler(message, bot)
    if command == "backToMenu": return backStarthandler(message, bot)


def mainHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="👥 List Admin", callback_data="admin_list"),
    )
    markup.add(
        types.InlineKeyboardButton(text="➕ Add Admin", callback_data="admin_add"),
        types.InlineKeyboardButton(text="❌ Remove Admin", callback_data="admin_remove"),
    )
    markup.add(
        types.InlineKeyboardButton(text="📊 Bot Statistic", callback_data="admin_statistic"),
    )
    markup.add(
        types.InlineKeyboardButton(text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>Bot Owner Menu :</i>

    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def deleteHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    user_id = message.data.split("_")[2]
    print(user_id)
    DB['admins'].delete_one({"_id": int(user_id)})
    markup = markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="👥 List Admin", callback_data="admin_list"),
    )
    markup.add(
        types.InlineKeyboardButton(text="➕ Add Admin", callback_data="admin_add"),
        types.InlineKeyboardButton(text="❌ Remove Admin", callback_data="admin_remove"),
    )
    markup.add(
        types.InlineKeyboardButton(text="📊 Bot Statistic", callback_data="admin_statistic"),
    )
    markup.add(
        types.InlineKeyboardButton(text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>Bot Owner Menu :</i>

    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def statisticHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = markup = types.InlineKeyboardMarkup()
    statistic = DB['statistic'].find_one({"_id":1})
    # print(statistic)

    markup.add(
        types.InlineKeyboardButton(text="🔙 Back To Admin Menu", callback_data="admin_main"),
        types.InlineKeyboardButton(text="🔙 Back To Main Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
BOT STATUS:
🟢 (LIVE)

<b>🤖 Bot Analysis:</b> 
• <i>Total Subscriptions:|</i> <b>{statistic["total_subscriptions"]}</b>
• <i>Total Groups Installed:|</i> <b>{statistic["total_groups_installed"]}</b>
• <i>Total channels installed:|</i> <b>{statistic["total_channel_installed"]}</b>
• <i>Total Telegram Members:|</i> <b>{statistic["total_telegram_members"]}</b>

<b>📊 User Finances:</b>
• <i>Total Paid Out:|</i> $ <b>{statistic["total_paid_out"]}</b>
• <i>24 Hour Bot Volume:|</i> $ <b>{statistic["bot_volume"]}</b>
• <i>Total BNB paid out:|</i> <b>{statistic["total_bnb_paid"]} BNB</b>
• <i>Total TTN paid out:|</i> <b>{statistic["total_ttn_paid"]} TTN</b>
• <i>Total USDT Paid out:|</i> <b>{statistic["total_busd_paid"]} USDT</b>

<b>📈 TeleTreon Finances:</b>
• <i>Total Earned 4% Fees:|</i> $ <b>{statistic["total_fee_earned"]}</b>
• <i>Total BNB Earned:|</i> <b>{statistic["total_bnb_earned"]} BNB</b>
• <i>Total TTN Earned:|</i> <b>{statistic["total_ttn_earned"]} TTN</b>
• <i>Total USDT Earned:|</i> <b>{statistic["total_busd_earned"]} USDT</b>

<b>🗂 Total Amount of Categories:</b>
• <i>Business:|</i> <b>{statistic["business"]}</b> 
• <i>Crypto:|</i> <b>{statistic["crypto"]}</b> 
• <i>Finance:|</i> <b>{statistic["finance"]}</b> 
• <i>Sports:|</i> <b>{statistic["sports"]}</b>   
• <i>Media:|</i> <b>{statistic["media"]}</b> 
• <i>Influencer:|</i> <b>{statistic["influencer"]}</b> 
• <i>Actor:|</i> <b>{statistic["actor"]}</b> 
• <i>Baking:|</i> <b>{statistic["baking"]}</b>    
• <i>Cooking:|</i> <b>{statistic["cooking"]}</b>   
• <i>Nature:|</i> <b>{statistic["nature"]}</b>     
• <i>DIY:|</i> <b>{statistic["diy"]}</b>     
• <i>Celebrity:|</i> <b>{statistic["celebrity"]}</b>  

<i>ℹ️ (Statistics Updates Every 10 Minutes)</i>
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def listHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = markup = types.InlineKeyboardMarkup()
    admin_list = DB['admins'].find({})

    for admins in admin_list :
        markup.add(
            types.InlineKeyboardButton(text=admins["name"], callback_data="nothing"),
        )


    markup.add(
        types.InlineKeyboardButton(text="🔙 Back To Admin Menu", callback_data="admin_main"),
        types.InlineKeyboardButton(text="🔙 Back To Main Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>List Admin :</i>
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def removeHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = markup = types.InlineKeyboardMarkup()
    admin_list = DB['admins'].find({})

    for admins in admin_list :
        cb = f"""remove_admin_{admins["_id"]}"""
        markup.add(
            types.InlineKeyboardButton(text=admins["name"], callback_data=cb),
        )


    markup.add(
        types.InlineKeyboardButton(text="🔙 Back To Admin Menu", callback_data="admin_main"),
        types.InlineKeyboardButton(text="🔙 Back To Main Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>Select Admin / Owner below to remove :</i>
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def addHandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("cancel")
    text_to_send = f"""
<b>Please input telegram user id : </b>
    """
    bot.send_message(message.from_user.id, text_to_send, parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(message.message, emailHandlerCallback, bot)


def backStarthandler(message: types.CallbackQuery, bot:TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    print(message.message)
    return start.startNoReply(message.message, bot)

## Callbacks
def emailHandlerCallback(message: types.Message, bot:TeleBot):
    user_id = message.text
    if user_id.lower() == "cancel": return start.start(message, bot)

    userInfo = DB['users'].find_one({"_id": int(user_id)})

    if not userInfo:
        bot.register_next_step_handler(message, emailHandlerCallback, bot)
        return bot.send_message(message.chat.id, "<b>Invalid user id, Please Try Again</b>", parse_mode='HTML')

    DB['admins'].insert_one({"_id": userInfo["_id"], "name": userInfo["name"]})
    bot.send_message(message.chat.id, "<b>Admin Added Successfully</b>", parse_mode='HTML')
    return start.start(message, bot)