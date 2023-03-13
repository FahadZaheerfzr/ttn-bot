from telebot import TeleBot
from telebot import types
from components.database import DB
from eth_account import Account
import secrets
from web3 import Web3
from components import settings, keyboards
from components.start import createWallet
import config
from components import start
import pprint
web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))


def middlewareHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    chat_id = message.data.split("_")[1]
    group_info = DB['groups'].find_one({"_id": int(chat_id)})
    owner_info = DB['users'].find_one({"_id": group_info['owner']})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.reply_to(
            message, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")

    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id):
            is_admin = True
    if not is_admin:
        return bot.reply_to(message, "You are not admin!")

    category = "❌ Not Set"
    if "category" in group_info:
        category = group_info['category']

    total_subs = DB['memberships'].count_documents({"chat_id": int(chat_id)})

    text_to_send = f"""
<i>Welcome to your $TTN Private Community Control Panel.</i>

<b>👥 Community Details:</b>
<i>• Group Name:|</i> {group_info['name']}
<i>• Category:|</i> {category}
<i>• Total Subscribers:|</i> {total_subs}

<b>📊 Finance:</b>
<i>• Current Monthly Fee:|</i> ${group_info['fees']['monthly']}
<i>• Current Entry Fee:|</i> ${group_info['fees']['permanent']}
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
        message.message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.settingPrivateMarkup(chat_id)
    )


def categoryHandler(message: types.CallbackQuery, bot: TeleBot):
    # print(message)
    bot.delete_message(message.from_user.id, message.message.message_id)
    chat_id = message.data.split(" ")[1]
    group_info = DB['groups'].find_one({"_id": int(chat_id)})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.reply_to(
            message, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")

    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id):
            is_admin = True
    if not is_admin:
        return bot.reply_to(message, "You are not admin!")

    category = "❌ Not Set"
    if "category" in group_info:
        category = group_info['category']

    text_to_send = f"""
<b>👥 Community Details:</b>
<i>• Group Name:|</i> {group_info['name']}
<i>• Category:|</i> {category}


<i>Click on the right category that fits your private community. This data is saved for our website search engine in which communities and fans are able to locate and indentify private communities.</i>
    """
    bot.send_message(
        message.message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.settingCategoryMarkup(chat_id)
    )


def updateCategoryHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    chat_id = message.data.split("_")[2]
    selected_category = message.data.split("_")[1]
    group_info = DB['groups'].find_one({"_id": int(chat_id)})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.reply_to(
            message, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")

    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id):
            is_admin = True
    if not is_admin:
        return bot.reply_to(message, "You are not admin!")

    DB['groups'].update_one(
        {"_id": int(chat_id)},
        {"$set": {"category": selected_category}}
    )

    text_to_send = f"""
<b>Categories Successfully Updated </b>
    """
    bot.send_message(
        message.message.chat.id,
        text=text_to_send,
        parse_mode='HTML',
        reply_markup=keyboards.backCommunityMarkup(chat_id)
    )


def groupNameHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    markup.add("cancel")
    chat_id = message.data.split(" ")[1]
    group_info = DB['groups'].find_one({"_id": int(chat_id)})

    try:
        chat_admins = bot.get_chat_administrators(chat_id)
    except:
        bot.reply_to(
            message, "Failed to fetch chat admins to verify you are one of them, please make the bot admin and try again")

    is_admin = False
    for x in chat_admins:
        if int(x.user.id) == int(message.from_user.id):
            is_admin = True
    if not is_admin:
        return bot.reply_to(message, "You are not admin!")

    text_to_send = f"""
<b>Current Group Name:</b> <code> {group_info["name"]} </code>
<i>Enter the name of your community below. This data is saved for our website search engine in which communities and fans are able to locate and indentify your private Group: </i>

    """
    bot.send_message(message.from_user.id, text_to_send,
                     parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(
        message.message, updateGroupNameHandlerCallback, bot, args=chat_id)


def updateGroupNameHandlerCallback(message: types.Message, bot: TeleBot, args):
    # print(args)
    name = message.text
    if name.lower() == "cancel":
        return start.start(message, bot)

    if (len(name) < 5):
        bot.register_next_step_handler(
            message, updateGroupNameHandlerCallback, bot, args)
        return bot.send_message(message.chat.id, "<b>Invalid Group Name, Please Try Again</b>", parse_mode='HTML')

    DB['groups'].update_one({"_id": int(args)}, {"$set": {"name": name}})
    bot.set_chat_title(int(args), name)
    bot.send_message(
        message.chat.id, "<b>Group Name Updated Successfully</b>", parse_mode='HTML')
    return start.start(message, bot)
