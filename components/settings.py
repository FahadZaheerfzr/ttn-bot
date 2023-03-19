from telebot import TeleBot
from telebot import types
from components.database import DB
import string, random
from components import keyboards


def settings(message: types.Message, bot: TeleBot):
    chat_id = message.chat.id
    group_info = DB['groups'].find_one({"_id": chat_id})

    if not group_info: return bot.reply_to(message, "Group is not registered!")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="⚙️ Settings", url=f"https://t.me/{bot.get_me().username}?start=setting_{chat_id}")
    )
    bot.send_message(
        message.chat.id,
        "<i>Click on the button below to change chat settings. (Admins only)</i>",
        reply_markup=markup,
        parse_mode='HTML'
    )

def settingStart(message: types.Message, bot: TeleBot):
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
<i>• Current Entry Fee:|</i> ${group_info['fees']['permanent'] if group_info['fees']['permanent'] else "❌ Not Set"}
<i>• Total Earned:|</i> ${group_info['total_earn']}

<b>💵 Current Owner Wallets:</b>
<i>• Bep-20:|</i> <code>{owner_info['owner_wallet'] if "owner_wallet" in owner_info else "❌ Not Set"}</code>
    """

#     text_to_send = f"""
# Owner Wallet: <code>{owner_info['owner_wallet']}</code>
# Monthly Fees: <code>{group_info['fees']['monthly']}</code>
# One Time Fees: <code>{group_info['fees']['permanent']}</code>
#     """
    bot.send_message(
        message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.settingPrivateMarkup(chat_id)
    )

def settingCommunity(message: types.Message, bot: TeleBot, chat_id: int):
    # print(message)
    #commmand, info = message.text.split(" ")
    #info_text, chat_id = info.split("_")

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
<i>• Current Entry Fee:|</i> ${group_info['fees']['permanent'] if group_info['fees']['permanent'] else "❌ Not Set"}
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