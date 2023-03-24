from telebot import TeleBot
from telebot import types
from components.database import DB
from web3 import Web3
from datetime import datetime, timedelta
import config
from components import token_functions


web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))


def isMembershipMarkup(order_id, currency):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text="📲 Upgrade", callback_data=f"upgrade {order_id} {currency}"),
        types.InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    )
    return markup


def sameSection(message: types.CallbackQuery, bot: TeleBot, order_id, currency):
    order_info = DB['orders'].find_one({"_id": order_id})
    user_info = DB['users'].find_one({"_id": message.from_user.id})
    group_info = DB['groups'].find_one({"_id": int(order_info['chat_id'])})
    owner_info = DB['users'].find_one({"_id": int(group_info['owner'])})
    prices = DB['panel'].find_one({"_id": 1})

    if not user_info:
        bot.reply_to(message.message.chat.id,
                     "You are not registered with bot yet, Press /start to register!")

    # if currency == "ttn":
    #     bot.answer_callback_query(message.id, "TTN Payments Are Currently Not Avilable", show_alert=True)
    #     return None

    bnb_price, ttn_price = prices['bnb_price'], prices['ttn_price']
    newPrices = {"bnb": bnb_price, "ttn": ttn_price,
                 "busd": prices['busd_price']}
    new_price_type = order_info['price'] / newPrices[currency]

    payment_contract = web3.eth.contract(
        address=config.PAYMENT_CONTRACT, abi=config.PAYMENT_CONTRACT_ABI)
    balance = None

    if currency == "bnb":
        balance = web3.eth.get_balance(user_info['address']) / 10 ** 18
    elif currency == "ttn":
        token = web3.eth.contract(address=web3.toChecksumAddress(
            config.TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
        balance = token.functions.balanceOf(
            user_info['address']).call() / 10 ** 9
    elif currency == "busd":
        token = web3.eth.contract(address=web3.toChecksumAddress(
            config.BUSD_CONTRACT), abi=config.TTN_CONTRACT_ABI)
        balance = token.functions.balanceOf(
            user_info['address']).call() / 10 ** 18
    else:
        bot.answer_callback_query(message.id, "Currency 404", show_alert=True)
        return None

    if balance < new_price_type:
        if currency == "busd":
            bot.answer_callback_query(message.id, "You Only Have {balance} USDT, But According To Current Subscription Price The Amount Is {sub_amount} USDT".format(
                balance=round(balance, 4),
                currency=currency,
                sub_amount=round(new_price_type, 4)
            ), show_alert=True)
            return None

        bot.answer_callback_query(message.id, "You Only Have {balance} {currency}, But According To Current Subscription Price The Amount Is {sub_amount} {currency}".format(
            balance=round(balance, 4),
            currency=currency,
            sub_amount=round(new_price_type, 4)
        ), show_alert=True)
        return None

    if not 'owner_wallet' in owner_info:
        bot.answer_callback_query(
            message.id, "This Group Owner Didn't Set His/Her Address To Receive Payment, Please Contact Them & Ask To Set", show_alert=True)
        return None

    if not owner_info['owner_wallet']:
        bot.answer_callback_query(
            message.id, "This Group Owner Didn't Set His/Her Address To Receive Payment, Please Contact Them & Ask To Set", show_alert=True)
        None

    return order_info, payment_contract, owner_info, new_price_type, user_info


def upgrade(message: types.CallbackQuery, bot: TeleBot):
    command, order_id, currency = message.data.split(" ")
    function_output = sameSection(message, bot, order_id, currency)
    if not function_output:
        pass
    order_info, payment_contract, owner_info, new_price_type, user_info = function_output

    membership_info = DB['memberships'].find_one(
        {"chat_id": int(order_info['chat_id']), "user_id": message.from_user.id})

    if currency == "ttn":
        return token_functions.acceptPaymentTTN(
            recepient_address=owner_info['owner_wallet'],
            amount_token=new_price_type,
            order_id=order_id,
            PRIVATE_KEY=user_info['private_key'],
            order_info=order_info,
            currency=currency,
            message=message,
            bot=bot,
            database_entries=False,
            membership_info=membership_info
        )

    if currency == "busd":
        return token_functions.acceptPaymentBUSD(
            recepient_address=owner_info['owner_wallet'],
            amount_token=new_price_type,
            order_id=order_id,
            PRIVATE_KEY=user_info['private_key'],
            order_info=order_info,
            currency=currency,
            message=message,
            bot=bot,
            database_entries=False,
            membership_info=membership_info
        )

    buyFunc = payment_contract.functions.acceptPaymentBNB(
        owner_info['owner_wallet'],
        order_id
    )

    tx = buyFunc.buildTransaction({
        "from": web3.eth.account.privateKeyToAccount(user_info['private_key']).address,
        "chainId": web3.eth.chain_id,
        "gasPrice": web3.eth.gas_price,
        "value": int(new_price_type * 10 ** 18),
        "gas": 0
    })

    try:
        tx['gas'] = web3.eth.estimate_gas(tx)
        tx['nonce'] = web3.eth.getTransactionCount(
            web3.eth.account.privateKeyToAccount(user_info['private_key']).address)

        signedTx = web3.eth.account.sign_transaction(
            tx, private_key=user_info['private_key'])
        broadcastedTx = web3.eth.send_raw_transaction(signedTx.rawTransaction)
    except Exception as err:
        return bot.send_message(message.message.chat.id, "<b>Error While Sending TX</b>: <code>{}</code>".format(err), parse_mode='HTML')

    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    if result.status == 0:
        return bot.send_message(message.message.chat.id, "<b>Error After Brodcasting TX</b>: Tx Hash: https://bscscan.com/tx/{}".format(broadcastedTx.hex()))

    DB['payment_infos'].insert_one({
        "amount": order_info['price'],
        "date": datetime.utcnow(),
        "currency": currency
    })

    DB['memberships'].update_one(
        {
            "chat_id": int(order_info['chat_id']),
            "user_id": message.from_user.id
        },
        {"$set": {
            "is_one_time": True if order_info['payment_type'] == "permanent" else False,
            "end_time": membership_info['end_time'] + timedelta(days=30)}
         }
    )

    user_info = bot.get_chat_member(
        chat_id=order_info['chat_id'], user_id=message.from_user.id)
    # print(user_info)
    if user_info.status == "left":
        invite_link = bot.create_chat_invite_link(
            order_info['chat_id'],
            member_limit=1
        )

        success_text = f"""
<b>✅ Membership Upgraded! </b>
• Tx link: <a href='https://bscscan.com/tx/{broadcastedTx.hex()}'>Click Here</a>
• Group Link: {invite_link.invite_link}
        """

        bot.send_message(
            message.message.chat.id,
            success_text
        )

    bot.edit_message_text(message_id=message.message.id, chat_id=message.message.chat.id,
                          text="Membership Upgraded Successfully", reply_markup=None)


def pay(message: types.CallbackQuery, bot: TeleBot):
    command, order_id, currency = message.data.split(" ")
    print(currency)
    function_output = sameSection(message, bot, order_id, currency)
    # print(function_output)
    if not function_output:
        return
    order_info, payment_contract, owner_info, new_price_type, user_info = function_output

    is_membership = DB['memberships'].find_one(
        {"chat_id": int(order_info['chat_id']), "user_id": message.from_user.id})
    if is_membership:
        if is_membership['is_one_time']:
            return bot.answer_callback_query(message.id, "You already have purchase lifetime susbcription", show_alert=True)
        return bot.edit_message_text(
            text="<i>You already subscribed to this community, do you want to upgrade?</i>",
            chat_id=message.message.chat.id,
            message_id=message.message.id,
            reply_markup=isMembershipMarkup(order_id, currency),
            parse_mode='HTML'
        )

    if currency == "ttn":
        return token_functions.acceptPaymentTTN(
            recepient_address=owner_info['owner_wallet'],
            amount_token=new_price_type,
            order_id=order_id,
            PRIVATE_KEY=user_info['private_key'],
            order_info=order_info,
            currency=currency,
            message=message,
            bot=bot,
            database_entries=False if is_membership else True,
            membership_info=None
        )

    if currency == "busd":
        return token_functions.acceptPaymentBUSD(
            recepient_address=owner_info['owner_wallet'],
            amount_token=new_price_type,
            order_id=order_id,
            PRIVATE_KEY=user_info['private_key'],
            order_info=order_info,
            currency=currency,
            message=message,
            bot=bot,
            database_entries=False if is_membership else True,
            membership_info=None
        )

    buyFunc = payment_contract.functions.acceptPaymentBNB(
        owner_info['owner_wallet'],
        order_id
    )

    tx = buyFunc.buildTransaction({
        "from": web3.eth.account.privateKeyToAccount(user_info['private_key']).address,
        "chainId": web3.eth.chain_id,
        "gasPrice": web3.eth.gas_price,
        "value": int(new_price_type * 10 ** 18),
        "gas": 0
    })

    try:
        tx['gas'] = web3.eth.estimate_gas(tx)
        tx['nonce'] = web3.eth.getTransactionCount(
            web3.eth.account.privateKeyToAccount(user_info['private_key']).address)

        signedTx = web3.eth.account.sign_transaction(
            tx, private_key=user_info['private_key'])
        broadcastedTx = web3.eth.send_raw_transaction(signedTx.rawTransaction)
    except Exception as err:
        return bot.send_message(message.message.chat.id, "<b>Error While Sending TX</b>: <code>{}</code>".format(err), parse_mode='HTML')

    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    if result.status == 0:
        return bot.send_message(message.message.chat.id, "<b>Error After Brodcasting TX</b>: Tx Hash: https://bscscan.com/tx/{}".format(broadcastedTx.hex()))

    DB['groups'].update_one(
        {"_id": int(order_info['chat_id'])},
        {"$inc": {"total_earn": float(order_info['price'])}}
    )

    DB['payment_infos'].insert_one({
        "amount": order_info['price'],
        "date": datetime.utcnow(),
        "currency": currency
    })

    DB['memberships'].insert_one({
        "chat_id": int(order_info['chat_id']),
        "user_id": message.from_user.id,
        "is_one_time": True if order_info['payment_type'] == "permanent" else False,
        "end_time": datetime.utcnow() + timedelta(days=30),
        "tx_hash": broadcastedTx.hex(),
        "currency": currency,
        "is_active": True
    })

    invite_link = bot.create_chat_invite_link(
        order_info['chat_id'],
        member_limit=1
    )

    success_text = f"""
<b>✅ Transaction successfull! </b>
• Tx link: <a href='https://bscscan.com/tx/{broadcastedTx.hex()}'>Click Here</a>
• Group Link: {invite_link.invite_link}
    """

    bot.send_message(
        message.message.chat.id,
        success_text
    )
