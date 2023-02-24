import config
from telebot import TeleBot, types, util, apihelper
from components import start, register, help, ownerHandler, communitiesHandler, change, buyPlan, pay, setOwnerWallet, settings, portal, userMainHandler, groupMainHandler
from components.database import DB
bot = TeleBot(config.BOT_TOKEN, parse_mode='HTML')



# Message Handler
bot.register_message_handler(register.register, commands=['register'], chat_types=['group', 'supergroup'], pass_bot=True)
bot.register_message_handler(help.help, commands=['help'], chat_types=['private','group', 'supergroup'], pass_bot=True)
bot.register_message_handler(groupMainHandler.start, content_types=['new_chat_members', 'left_chat_member'],  pass_bot=True, func= lambda message: message)
bot.register_message_handler(start.joinStart, pass_bot=True, func= lambda message: len(message.text.split("/start ")) == 2)
# bot.register_message_handler(groupMainHandler.start, chat_types=['group', 'supergroup'], pass_bot=True, func= lambda message: message)
bot.register_message_handler(start.start, commands=['start'],chat_types=['private'], pass_bot=True)
# bot.register_message_handler(start.start, commands=['start'],chat_types=['group', 'supergroup'], pass_bot=True)
bot.register_message_handler(settings.settings, commands=['setting'], pass_bot=True, chat_types=['group', 'supergroup'])
bot.register_message_handler(settings.settings, commands=['setting'], pass_bot=True, chat_types=['group', 'supergroup'])
# bot.register_message_handler(setOwnerWallet.setOwnerWallet, commands=['setOwnerWallet'], pass_bot=True, chat_types=['private'])

# Callback Handler
bot.register_callback_query_handler(userMainHandler.middlewareMainHandler, pass_bot=True, func= lambda message: message.data.startswith("main_"))
bot.register_callback_query_handler(ownerHandler.middlewareMainHandler, pass_bot=True, func= lambda message: message.data.startswith("admin_"))
bot.register_callback_query_handler(ownerHandler.deleteHandler, pass_bot=True, func= lambda message: message.data.startswith("remove_admin_"))
bot.register_callback_query_handler(communitiesHandler.middlewareHandler, pass_bot=True, func= lambda message: message.data.startswith("community_"))
bot.register_callback_query_handler(communitiesHandler.categoryHandler, pass_bot=True, func= lambda message: message.data.startswith("category "))
bot.register_callback_query_handler(communitiesHandler.updateCategoryHandler, pass_bot=True, func= lambda message: message.data.startswith("setcategory_"))
bot.register_callback_query_handler(communitiesHandler.groupNameHandler, pass_bot=True, func= lambda message: message.data.startswith("groupname"))
bot.register_callback_query_handler(change.changeStart, pass_bot=True, func= lambda message: message.data.startswith("change"))
bot.register_callback_query_handler(setOwnerWallet.changeWalletStart, pass_bot=True, func= lambda message: message.data.startswith("setownerwallet"))
bot.register_callback_query_handler(buyPlan.buyPlan, func= lambda message: message.data.startswith("buy"), pass_bot=True)
bot.register_callback_query_handler(pay.pay, func= lambda message: message.data.startswith("pay"), pass_bot=True)
bot.register_callback_query_handler(pay.upgrade, func= lambda message: message.data.startswith("upgrade"), pass_bot=True)
bot.register_callback_query_handler(change.changeStart, func= lambda message: message.data.startswith("fees"), pass_bot=True)
bot.register_callback_query_handler(portal.portalStart, func= lambda message: message.data.startswith("portal"), pass_bot=True)


@bot.my_chat_member_handler()
def my_chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,"Config Message") # Welcome message, if bot was added to group



bot.infinity_polling(allowed_updates=util.update_types)

