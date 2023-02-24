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

def start(message: types.Message, bot: TeleBot):
    command = message.content_type
    if command == 'left_chat_member' : return goodBye(message, bot)
    if command == 'new_chat_members' : return wellcome(message, bot)
    # command = message.data.split("_")[1]
    # print(message)

def goodBye(message: types.Message, bot: TeleBot) :
    bot.delete_message(message.chat.id, message.message_id)

def wellcome(message: types.Message, bot: TeleBot) :
    bot.delete_message(message.chat.id, message.message_id)
    print(message)
    if(message.new_chat_members[0].is_bot == False) : 
        is_subscribe = DB['memberships'].find_one({"chat_id":message.chat.id, "user_id": message.new_chat_members[0].id, "is_active":True })
        print(is_subscribe)
        if not is_subscribe:
            bot.ban_chat_member(chat_id=message.chat.id, user_id=message.new_chat_members[0].id)
        # check subscription
    
