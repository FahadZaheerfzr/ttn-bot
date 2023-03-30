import config
from telebot import TeleBot
from telebot import types
from components.database import DB
from web3 import Web3
from datetime import datetime, timedelta
import config


web3 = Web3(Web3.HTTPProvider(config.RPC_ADDRESS))

def getTokenAllowanceAmount(token_address, owner_address):
    """
    returns amount in wei
    """
    token = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=config.TTN_CONTRACT_ABI)
    allowance = token.functions.allowance(web3.toChecksumAddress(owner_address), web3.toChecksumAddress(config.PAYMENT_CONTRACT)).call()
    return allowance

def approveTokens(token_address, owner_address, PRIVATE_KEY):
    token = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=config.TTN_CONTRACT_ABI)
    swap_func = token.functions.approve(config.PAYMENT_CONTRACT, 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        'from': owner_address,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    signedTx = web3.eth.account.sign_transaction(swap_func, private_key=PRIVATE_KEY)
    broadcastedTx = web3.eth.send_raw_transaction(signedTx.rawTransaction)

    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    return result.status, broadcastedTx.hex()


def approveStakingTokens(token_address, owner_address, PRIVATE_KEY):
    token = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=config.TTN_CONTRACT_ABI)
    swap_func = token.functions.approve(config.STAKING_CONTRACT, 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        'from': owner_address,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(owner_address),
    })
    signedTx = web3.eth.account.sign_transaction(swap_func, private_key=PRIVATE_KEY)
    broadcastedTx = web3.eth.send_raw_transaction(signedTx.rawTransaction)

    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    return result.status, broadcastedTx.hex()

def acceptPaymentTTN(recepient_address, amount_token, order_id, PRIVATE_KEY, order_info, currency, message: types.CallbackQuery, bot: TeleBot, membership_info, database_entries=True):
    print(order_id, database_entries, sep='\n')

    payment_contract = web3.eth.contract(address=config.PAYMENT_CONTRACT, abi=config.PAYMENT_CONTRACT_ABI)

    #token_allowance = getTokenAllowanceAmount(config.TTN_CONTRACT, web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address)
    
    if (1000) < float(amount_token):
        bot.send_message(message.message.chat.id, "Approving transaction...")
        try:
            is_approved = approveTokens(
                token_address=config.TTN_CONTRACT, 
                owner_address=web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
                PRIVATE_KEY=PRIVATE_KEY
            )
            is_approvedStaking = approveStakingTokens(
                token_address=config.TTN_CONTRACT, 
                owner_address=web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
                PRIVATE_KEY=PRIVATE_KEY
            )
            bot.send_message(message.message.chat.id, "Tokens Approved, Tx: https://bscscan.com/tx/{}".format(is_approved[1]))
        except Exception as error:
            return bot.answer_callback_query(message.id, "Could not approve tokens, Error: {}".format(error), show_alert=True)

    print(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address, recepient_address)
    try:
        tx = payment_contract.functions.acceptPaymentTTN(
            web3.toChecksumAddress(recepient_address),
            int(amount_token * 10 ** 9),
            # order_id
        ).buildTransaction({
            'chainId': web3.eth.chain_id,
            'gasPrice': web3.eth.gas_price,
            'from': web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
            'gas': 0
        })
    except Exception as error:
        print(error)
        return bot.answer_callback_query(message.id, "Error While Sending TX", show_alert=True)

    try:
        print(tx)
        print(web3.eth.estimate_gas(tx))
        print("Now Sending")
        tx['gas'] = web3.eth.estimate_gas(tx)
        tx['nonce'] = web3.eth.get_transaction_count(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address)
        print(tx)

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        print(signed_tx)
        broadcastedTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(broadcastedTx)
    except Exception as error:
        print("Error is")
        print(error)
        return bot.answer_callback_query(message.id, "Error While Sending After Siging TX, Make Sure You Have Enough Gas Fees!", show_alert=True)


    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    if result.status == 0: return bot.send_message(message.message.chat.id, "<b>Error After Brodcasting TX</b>: Tx Hash: https://bscscan.com/tx/{}".format(broadcastedTx.hex()))

    DB['groups'].update_one(
        {"_id": int(order_info['chat_id'])},
        {"$inc": {"total_earn": float(order_info['price']) }}
    )
    DB['orders'].update_one(
        {"_id": order_id},
        {"$set": {"is_completed": True }}
    )

    if database_entries:
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
            success_text,
            parse_mode='HTML'
        )
    else:
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
            {"$set":{
                "is_one_time": True if order_info['payment_type'] == "permanent" else False,
                "end_time": membership_info['end_time'] + timedelta(days=30)}
            }
        )

        user_info = bot.get_chat_member(chat_id=order_info['chat_id'], user_id=message.from_user.id)
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

        bot.answer_callback_query(message.id, "Membership upgraded successfully!", show_alert=True)

def acceptPaymentBUSD(recepient_address, amount_token, order_id, PRIVATE_KEY, order_info, currency, message: types.CallbackQuery, bot: TeleBot, membership_info, database_entries=True):
    print(recepient_address, amount_token, order_id, PRIVATE_KEY, order_info, currency, sep='\n')

    payment_contract = web3.eth.contract(address=config.PAYMENT_CONTRACT, abi=config.PAYMENT_CONTRACT_ABI)

    token_allowance = getTokenAllowanceAmount(config.BUSD_CONTRACT, web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address)
    # print(token_allowance)
    if (token_allowance / 10 ** 18) < float(amount_token):
        bot.send_message(message.message.chat.id, "Approving transaction...")
        try:
            is_approved = approveTokens(
                token_address=config.BUSD_CONTRACT, 
                owner_address=Web3.toChecksumAddress(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address),
                PRIVATE_KEY=PRIVATE_KEY
            )
            bot.send_message(message.message.chat.id, "Tokens Approved, Tx: https://bscscan.com/tx/{}".format(is_approved[1]))
        except Exception as error:
            print(error)
            return bot.answer_callback_query(message.id, "Could not approve tokens", show_alert=True)

    print(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address, recepient_address)
    try:
        tx = payment_contract.functions.acceptPaymentBUSD(
            web3.toChecksumAddress(recepient_address),
            int(amount_token * 10 ** 18),
            # order_id
        ).buildTransaction({
            'chainId': web3.eth.chain_id,
            'gasPrice': web3.eth.gas_price,
            'from': web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
            'gas': 0
        })
    except Exception as error:
        print(error)
        return bot.answer_callback_query(message.id, "Error While Sending TX: {}".format(error), show_alert=True)

    try:
        tx['gas'] = web3.eth.estimate_gas(tx)
        tx['nonce'] = web3.eth.get_transaction_count(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address)

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        broadcastedTx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    except Exception as error:
        print(error)
        return bot.answer_callback_query(message.id, "Error While Sending After Siging TX, Make Sure You Have Enough Gas Fees!", show_alert=True)


    result = web3.eth.wait_for_transaction_receipt(broadcastedTx)
    if result.status == 0: return bot.send_message(message.message.chat.id, "<b>Error After Brodcasting TX</b>: Tx Hash: https://bscscan.com/tx/{}".format(broadcastedTx.hex()))

    DB['groups'].update_one(
        {"_id": int(order_info['chat_id'])},
        {"$inc": {"total_earn": float(order_info['price']) }}
    )

    if database_entries:
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
    else:
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
            {"$set":{
                "is_one_time": True if order_info['payment_type'] == "permanent" else False,
                "end_time": membership_info['end_time'] + timedelta(days=30)}
            }
        )

        user_info = bot.get_chat_member(chat_id=order_info['chat_id'], user_id=message.from_user.id)
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

        bot.answer_callback_query(message.id, "Membership upgraded successfully!", show_alert=True)