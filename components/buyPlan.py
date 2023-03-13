from telebot import TeleBot
from telebot import types
from components.database import DB
import string, random, config
from web3 import Web3


web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))


def generateRandomString(length):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    isExists = DB['orders'].find_one({"_id": res})
    if not isExists: return res
    return generateRandomString(length)

def buyPlan(message: types.CallbackQuery, bot: TeleBot):
    command, chat_id, payment_type = message.data.split(" ")

    info = DB['groups'].find_one({"_id": int(chat_id) })
    if not info: return bot.reply_to(message, "Chat Not Found!")

    order_id = None

    is_order = DB['orders'].find_one({"chat_id": chat_id, "user_id": message.from_user.id})

    if is_order:
        order_id = is_order['_id']
        DB['orders'].update_one({
            "_id": order_id
        }, {"$set": { "payment_type": payment_type, "price": info['fees'][payment_type] }})
    else:
        order_id = generateRandomString(7)
        DB['orders'].insert_one({
            "_id": order_id,
            "payment_type": payment_type,
            "price": info['fees'][payment_type],
            "chat_id": chat_id,
            "user_id": message.from_user.id,
            "is_completed": False
        })

    prices = DB['panel'].find_one({"_id": 1})

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="BNB (Bep-20)", callback_data=f"pay {order_id} bnb"),
        types.InlineKeyboardButton(text="TTN (Bep-20)", callback_data=f"pay {order_id} ttn"),
    )
    markup.add(
        types.InlineKeyboardButton(text="💵 Your Wallets", callback_data="main_wallet"),
        types.InlineKeyboardButton(text="USDT (Bep-20)", callback_data=f"pay {order_id} busd")
    )
    user_info = DB['users'].find_one({"_id": message.from_user.id})

    if not user_info:
        return bot.send_message(message.message.chat.id, "You don't have a $TTN account yet. Use /start to configure your account and try again.")

    bnb_balance = web3.eth.get_balance(user_info['address']) / 10 ** 18
    ttn_contract = web3.eth.contract(address=web3.toChecksumAddress(config.TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
    busd_contract = web3.eth.contract(address=web3.toChecksumAddress(config.BUSD_CONTRACT), abi=config.TTN_CONTRACT_ABI)

    ttn_balance, busd_balance = (
        round(ttn_contract.functions.balanceOf(user_info['address']).call()/ 10 ** 9, 4),
        round(busd_contract.functions.balanceOf(user_info['address']).call()/ 10 ** 18, 4),
    )

    text_to_send = f"""
<b>Method accepted, Invoice Generated.
{"🗓 Monthly Fee" if payment_type == "monthly" else "🎉 One Time Entry Fee"} :| ${info['fees'][payment_type]}</b>
__
<i>• Amount in BNB:|</i> {round(info['fees'][payment_type] / prices['bnb_price'], 4)}
<i>• Amount in TTN:|</i> {round(info['fees'][payment_type] / prices['ttn_price'], 4)}
<i>• Amount in USDT:|</i> {round(info['fees'][payment_type] / 1, 4)}
__
*The prices of certain Cryptocurrencies might change when a transaction is delayed due the volatility of the markets.
    """

    bot.edit_message_text(
        text=text_to_send,
        message_id=message.message.id,
        chat_id=message.message.chat.id,
        parse_mode="HTML",
        reply_markup=markup
    )

