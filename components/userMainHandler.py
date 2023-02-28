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
    if command == "help":
        return helpHandler(message, bot)
    if command == "email":
        return emailHandler(message, bot)
    if command == "wallet":
        return walletHandler(message, bot)
    if command == "notification":
        return notificationHandler(message, bot)
    if command == "subscription":
        return subscriptionHandler(message, bot)
    if command == "communities":
        return communitiesHandler(message, bot)
    if command == "toggleEmail":
        return toggleEmailHandler(message, bot)
    if command == "toggleTg":
        return toggleTgHandler(message, bot)
    if command == "backToMenu":
        return backStarthandler(message, bot)


def emailHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    markup.add("cancel")
    userInfo = DB['users'].find_one({"_id": message.from_user.id})

    text_to_send = f"""
<b>Current Email:</b> <code>{"✅ Set" if "email" in userInfo else "❌ Not Set"}</code>
<b>Insert your email to receive notifications when a subscription period ends.</b>
    """
    bot.send_message(message.from_user.id, text_to_send,
                     parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(message.message, emailHandlerCallback, bot)


def helpHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(callback_query_id=message.id)
    bot.send_message(
        message.message.chat.id,
        """
<b>👨‍💻Commands in-bot:</b>
• /start = Go to your TeleTreon account.
• /help = Receive TeleTreon info.
<b>👨‍💻Commands in Group / Channel:</b>
• /setting = Go to settings menu to configure your private chat.
        """,
        parse_mode='HTML'
    )


def notificationHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    userInfo = DB['users'].find_one({"_id": message.from_user.id})

    markup = types.InlineKeyboardMarkup()
    current_mail = f"""{"🔇 Mute Email" if "email_not" in userInfo else "✅ Unmute Email" }"""
    current_tg = f"""{"🔇 Mute Telegram" if "tg_not" in userInfo else "✅ Unmute Telegram"}"""
    markup.add(
        types.InlineKeyboardButton(
            text=current_mail, callback_data="main_toggleEmail"),
        types.InlineKeyboardButton(
            text=current_tg, callback_data="main_toggleTg"),
    )
    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>🔔 Notification Settings</i>
<i>Receive notifications when a subscription period ends.</i>
<i>• Telegram Notifications: </i> {"✅ Unmuted" if "tg_not" in userInfo else "🔇Muted"}
<i>• E-mail Notifications: </i> {"✅ Unmuted" if "email_not" in userInfo else "🔇Muted"}

    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def toggleTgHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    userInfo = DB['users'].find_one({"_id": message.from_user.id})
    if ("tg_not" in userInfo):
        DB['users'].update_one({"_id": message.from_user.id}, {
                               "$unset": {"tg_not": ""}})
    else:
        DB['users'].update_one({"_id": message.from_user.id}, {
                               "$set": {"tg_not": True}})

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
        types.InlineKeyboardButton(
            text="🔙 Back To Notification", callback_data="main_notification"),
    )

    text_to_send = f"""
<b>{"🔇 Mute Telegram" if "tg_not" in userInfo else "✅ Unmute Telegram" } Notification Updated Successfully</b>
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def toggleEmailHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    userInfo = DB['users'].find_one({"_id": message.from_user.id})
    if ("email_not" in userInfo):
        DB['users'].update_one({"_id": message.from_user.id}, {
                               "$unset": {"email_not": ""}})
    else:
        DB['users'].update_one({"_id": message.from_user.id}, {
                               "$set": {"email_not": True}})

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
        types.InlineKeyboardButton(
            text="🔙 Back To Notification", callback_data="main_notification"),
    )

    text_to_send = f"""
<b>{"🔇 Mute Email" if "email_not" in userInfo else "✅ Unmute Email" } Notification Updated Successfully</b>
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def subscriptionHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    memberships = DB['memberships'].find({"user_id": message.from_user.id})
    markup = types.InlineKeyboardMarkup()

    for membership in memberships:
        invite_link = bot.create_chat_invite_link(
            membership['chat_id'],
            member_limit=1
        )
        group_info = DB['groups'].find_one({"_id": membership['chat_id']})
        markup.add(
            types.InlineKeyboardButton(
                text=group_info["name"], url=invite_link.invite_link),
        )

    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>💵 Your Subscription Group :</i>

    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def communitiesHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    communities = DB['groups'].find({"owner": message.from_user.id})
    markup = types.InlineKeyboardMarkup()

    for community in communities:
        markup.add(
            types.InlineKeyboardButton(
                text=f"{community['name']}", callback_data=f"community_{community['_id']}"),
        )

    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    if communities.count() == 0:
        text_to_send = f"""
            <i>You currently don't have private communities. Add the bot to your private community and configure the chat.</i>
            """
    else:
        text_to_send = f"""
        <i>👥 Your Communities :</i>
        """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def walletHandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    userInfo = DB['users'].find_one({"_id": message.from_user.id})
    if not userInfo:
        wallet = createWallet()
        userInfo2 = {
            "_id": message.from_user.id,
            "name": message.from_user.full_name,
            "all_groups": [],
            "private_key": wallet[0],
            "address": wallet[1]
        }
        DB['users'].insert_one(userInfo2)
        userInfo = userInfo2

    # if not userInfo: userInfo = DB['users'].find_one({"_id": message.from_user.id})
    bnb_balance = web3.eth.get_balance(userInfo['address']) / 10 ** 18

    ttn_contract = web3.eth.contract(address=web3.toChecksumAddress(
        config.TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
    busd_contract = web3.eth.contract(address=web3.toChecksumAddress(
        config.BUSD_CONTRACT), abi=config.TTN_CONTRACT_ABI)

    ttn_balance, busd_balance = (
        round(ttn_contract.functions.balanceOf(
            userInfo['address']).call() / 10 ** 9, 4),
        round(busd_contract.functions.balanceOf(
            userInfo['address']).call() / 10 ** 18, 4),
    )

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            text="🔙 Back To Menu", callback_data="main_backToMenu"),
    )

    text_to_send = f"""
<i>💵 Your TeleTreon wallet.</i>

<i>Deposit funds to enter private communities. Keep in mind that you always leave some BNB Bep-20 in your wallet in order to do transactions on the blockchain. (Gas fee)
❌ Deposit only.
</i>
<i>• 💵 Bep-20 Wallet:|</i> ```{userInfo['address']}```

<i>• BNB:|</i> {round(bnb_balance, 4)}
<i>• TTN:|</i> {ttn_balance}
<i>• BUSD:|</i> {busd_balance}
    """

    bot.send_message(
        message.from_user.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )


def backStarthandler(message: types.CallbackQuery, bot: TeleBot):
    bot.delete_message(message.from_user.id, message.message.message_id)
    print(message.message)
    return start.startNoReply(message.message, bot)

# Callbacks


def emailHandlerCallback(message: types.Message, bot: TeleBot):
    email = message.text
    if email.lower() == "cancel":
        return start.start(message, bot)

    if (not "@" in email) or (len(email) < 5):
        bot.register_next_step_handler(message, emailHandlerCallback, bot)
        return bot.send_message(message.chat.id, "<b>Invalid Email, Please Try Again</b>", parse_mode='HTML')

    DB['users'].update_one({"_id": message.from_user.id}, {
                           "$set": {"email": email}})
    bot.send_message(
        message.chat.id, "<b>Email Updated Successfully</b>", parse_mode='HTML')
    return start.start(message, bot)
