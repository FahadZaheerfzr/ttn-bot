from telebot import TeleBot
from telebot import types
from components.database import DB



def isNumber(num):
    try:
        float(num)
        return True
    except:
        return False

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

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="Set Monthly Fees", callback_data=f"fees_m_{chat_id}"),
        types.InlineKeyboardButton(text="Set One Time Fees", callback_data=f"fees_p_{chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text="Set Owner Wallet", callback_data=f"setownerwallet {chat_id}")
    )

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
        reply_markup=markup
    )

def changeStart(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    fees_type, chat_id = message.data.split("_")[1], int(message.data.split("_")[2])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("cancel")

    bot.send_message(message.from_user.id, "Please enter the amount in $ USD.", reply_markup=markup)
    bot.register_next_step_handler(message.message, updateFees, bot, fees_type, chat_id)

def updateFees(message: types.Message, bot: TeleBot, fees_type, chat_id):
    if message.text == "cancel": return backSettings(message, bot, chat_id)
    fees_struct = {
        "m": "monthly",
        "p": "permanent"
    }

    try:
        fees_amount = float(message.text)
    except:
        bot.reply_to(message, "Fees must be a number, try again")
        return bot.register_next_step_handler(message, updateFees, bot, fees_type, chat_id)
    
    all_admins = bot.get_chat_administrators(chat_id)
    is_admin = False
    
    for x in all_admins:
        if x.user.id == message.from_user.id: is_admin = True

    if not is_admin: return bot.reply_to(message, "This Command Is Only For Admins", reply_markup=types.ReplyKeyboardRemove())

    DB['groups'].update_one(
        {"_id": chat_id},
        { "$set": { f"fees.{fees_struct[fees_type]}": float(fees_amount)} }
    )

    bot.send_message(message.chat.id, "Fees Updated", reply_markup=types.ReplyKeyboardRemove())
    backSettings(message, bot, chat_id)
