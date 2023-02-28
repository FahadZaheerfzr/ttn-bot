from telebot import TeleBot
from telebot import types
from components.database import DB
from eth_account import Account
import secrets
from web3 import Web3
from components import settings
import config


web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))


def createWallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key).address
    return [private_key, acct]

def start(message: types.Message, bot: TeleBot):
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

    is_admin = DB['admins'].find_one({"_id": message.from_user.id})

    # if not userInfo: userInfo = DB['users'].find_one({"_id": message.from_user.id})
    bnb_balance = web3.eth.get_balance(userInfo['address']) / 10 ** 18

    ttn_contract = web3.eth.contract(address=web3.toChecksumAddress(config.TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
    busd_contract = web3.eth.contract(address=web3.toChecksumAddress(config.BUSD_CONTRACT), abi=config.TTN_CONTRACT_ABI)

    ttn_balance, busd_balance = (
        round(ttn_contract.functions.balanceOf(userInfo['address']).call()/ 10 ** 9, 4),
        round(busd_contract.functions.balanceOf(userInfo['address']).call()/ 10 ** 18, 4),
    )

    markup = types.InlineKeyboardMarkup()
    

    markup.add(
        types.InlineKeyboardButton(text="💵 Your Wallets", callback_data="main_wallet"),
        types.InlineKeyboardButton(text="📲 Subscriptions", callback_data="main_subscription"),
    )
    markup.add(
        types.InlineKeyboardButton(text="📩 E-mail", callback_data="main_email"),
        types.InlineKeyboardButton(text="🔔 Notifications", callback_data="main_notification"),
    )

    markup.add(
        types.InlineKeyboardButton(text="👥 Your Communities", callback_data="main_communities")
    )

    if is_admin :
        markup.add(
            types.InlineKeyboardButton(text="🔒 Bot Owner Menu", callback_data="admin_main")
        )


    markup.add(
        types.InlineKeyboardButton(text="❓Help", callback_data="main_help"),
    )


    text_to_send = f"""
<i>Welcome to your personal $TTN Account!</i>

<i>• Email:|</i> {"✅ Set" if "email" in userInfo else "❌ Not Set"}
<i>• Telegram Notifications:|</i> {"✅ Unmuted" if "tg_not" in userInfo else "🔇Muted"}
<i>• E-mail Notifications:|</i> {"✅ Unmuted" if "email_not" in userInfo else "🔇Muted"}

<b>💵 Wallet Balance:</b> 
<i>• BNB:|</i> {round(bnb_balance, 4)}
<i>• TTN:|</i> {ttn_balance}
<i>• USDT:|</i> {busd_balance}
    """

    bot.reply_to(
        message,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def startNoReply(message: types.Message, bot: TeleBot):
    userInfo = DB['users'].find_one({"_id": message.chat.id})
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

    ttn_contract = web3.eth.contract(address=web3.toChecksumAddress(config.TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
    busd_contract = web3.eth.contract(address=web3.toChecksumAddress(config.BUSD_CONTRACT), abi=config.TTN_CONTRACT_ABI)

    ttn_balance, busd_balance = (
        round(ttn_contract.functions.balanceOf(userInfo['address']).call()/ 10 ** 9, 4),
        round(busd_contract.functions.balanceOf(userInfo['address']).call()/ 10 ** 18, 4),
    )
    is_admin = DB['admins'].find_one({"_id": message.chat.id})

    markup = types.InlineKeyboardMarkup()
   

    markup.add(
        types.InlineKeyboardButton(text="💵 Your Wallets", callback_data="main_wallet"),
        types.InlineKeyboardButton(text="📲 Subscriptions", callback_data="main_subscription"),
    )
    markup.add(
        types.InlineKeyboardButton(text="📩 E-mail", callback_data="main_email"),
        types.InlineKeyboardButton(text="🔔 Notifications", callback_data="main_notification"),
    )

    markup.add(
        types.InlineKeyboardButton(text="👥 Your Communities", callback_data="main_communities")
    )

    if is_admin :
        markup.add(
            types.InlineKeyboardButton(text="🔒 Bot Owner Menu", callback_data="admin_main")
        )

    markup.add(
        types.InlineKeyboardButton(text="❓Help", callback_data="main_help"),
    )


    text_to_send = f"""
<i>Welcome to your personal $TTN Account!</i>

<i>• Email:|</i> {"✅ Set" if "email" in userInfo else "❌ Not Set"}
<i>• Telegram Notifications:|</i> {"✅ Unmuted" if "tg_not" in userInfo else "🔇Muted"}
<i>• E-mail Notifications:|</i> {"✅ Unmuted" if "email_not" in userInfo else "🔇Muted"}

<b>💵 Wallet Balance:</b> 
<i>• BNB:|</i> {round(bnb_balance, 4)}
<i>• TTN:|</i> {ttn_balance}
<i>• USDT:|</i> {busd_balance}
    """

    bot.send_message(
        message.chat.id,
        text_to_send,
        parse_mode='HTML',
        reply_markup=markup
    )

def joinStart(message: types.Message, bot: TeleBot):
    # print(message)
    commmand, chat_id = message.text.split(" ")

    if(chat_id == None) : return start(message, bot)

    if len(chat_id.split("_")) == 2:
        return settings.settingStart(message, bot)

    try:
        chat_id = int(chat_id)
    except:
        return bot.reply_to(message, "Wrong Chat ID")

    info = DB['groups'].find_one({"_id": chat_id})
    if not info: return bot.reply_to(message, "Chat Not Found!")

    member = DB['memberships'].find_one({"chat_id": chat_id, "user_id" : message.from_user.id})
    # print(member)
    invite_link = bot.create_chat_invite_link(
            chat_id,
            member_limit=1
        )
    if member :
        return bot.send_message(message.chat.id, f"""
<i>Welcome to {info['name']}
You're already subscribed to this community.</i>

 Group Link: {invite_link.invite_link}
""", parse_mode='HTML')


    markup = types.InlineKeyboardMarkup()
    isAdd = False

    if info['fees']['monthly']:
        isAdd = True
        markup.add(types.InlineKeyboardButton(text="🗓 Monthly Subscription", callback_data=f"buy {chat_id} monthly"))
    
    if info['fees']['permanent']:
        isAdd = True
        markup.add(types.InlineKeyboardButton(text="🎉 One Time Entry Fee", callback_data=f"buy {chat_id} permanent"))

    if not isAdd:
        return bot.reply_to(message, "Plans Are Not Setup For This Group!")

    bot.send_message(message.chat.id, "<i>Welcome to {}\nSelect a method to join the community.</i>".format(info['name']), reply_markup=markup, parse_mode='HTML')
    

