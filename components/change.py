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
    commmand, info = message.text.split(" ")
    info_text, chat_id = info.split("_")

    group_info = DB['groups'].find_one({"_id": int(chat_id)})
    owner_info = DB['users'].find_one({"_id": group_info['owner']})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.reply_to(message, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")
    
    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id): is_admin = True
    if not is_admin: return bot.reply_to(message, "You are not admin!")

    category = "❌ Not Set"
    if "category" in group_info: category = group_info['category']

    total_subs = DB['memberships'].count_documents({"chat_id": int(chat_id)})

    text_to_send = f"""
<i>Welcome to your $TTN Private Community Control Panel.</i>

<b>👥 Community Details:</b>
<i>• Name:|</i> {group_info['name']}
<i>• Category:|</i> {category}
<i>• Total Subscribers:|</i> {total_subs}

<b>📊 Finance:</b>
<i>• Current Monthly Fee:|</i> ${group_info['fees']['monthly']}
<i>• Current Entry Fee:|</i><code> ${group_info['fees']['permanent'] if group_info['fees']['permanent'] else "❌ Not Set"} </code>
<i>• Total Earned:|</i> ${group_info['total_earn']}

<b>💵 Current Owner Wallets:</b>
<i>• Bep-20:|</i> <code>{owner_info['owner_wallet'] if "owner_wallet" in owner_info else "❌ Not Set"}</code>
    """

    bot.send_message(
        message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.settingPrivateMarkup(chat_id)
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
    return backSettings(message, bot, chat_id)
