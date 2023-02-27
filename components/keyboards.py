from telebot import TeleBot, types
import config

def settingPrivateMarkup(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="🗓 Set Monthly Fee", callback_data=f"fees_m_{chat_id}"),
        types.InlineKeyboardButton(text="🎉 Set One Time Entry", callback_data=f"fees_p_{chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text="🗂 Set Category", callback_data=f"category {chat_id}"),
        types.InlineKeyboardButton(text="📝 Set Group Name", callback_data=f"groupname {chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text="💵 Set Owner Wallets", callback_data=f"setownerwallet {chat_id}")
    )
    markup.add(
        types.InlineKeyboardButton(text="🌐 Portal Link", callback_data=f"portal {chat_id}")
    )

    return markup

def settingCategoryMarkup(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=f"Business", callback_data=f"setcategory_Business_{chat_id}"),
        types.InlineKeyboardButton(text=f"Crypto", callback_data=f"setcategory_Crypto_{chat_id}"),
        types.InlineKeyboardButton(text=f"Finance", callback_data=f"setcategory_Finance_{chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text=f"Sports", callback_data=f"setcategory_Sports_{chat_id}"),
        types.InlineKeyboardButton(text=f"Media", callback_data=f"setcategory_Media_{chat_id}"),
        types.InlineKeyboardButton(text=f"Influencer", callback_data=f"setcategory_Influencer_{chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text=f"Actor", callback_data=f"setcategory_Actor_{chat_id}"),
        types.InlineKeyboardButton(text=f"Cooking", callback_data=f"setcategory_Cooking_{chat_id}"),
        types.InlineKeyboardButton(text=f"Nature", callback_data=f"setcategory_Nature_{chat_id}"),
    )
    markup.add(
        types.InlineKeyboardButton(text=f"DIY", callback_data=f"setcategory_DIY_{chat_id}"),
        types.InlineKeyboardButton(text=f"Celebrity", callback_data=f"setcategory_Celebrity_{chat_id}"),
    )
    
    markup.add(
        types.InlineKeyboardButton(text="🔙 Back", callback_data=f"community_{chat_id}"),
    )
    return markup
    

def backCommunityMarkup(chat_id):
    markup = types.InlineKeyboardMarkup()
    
    markup.add(
        types.InlineKeyboardButton(text="🔙 Back", callback_data=f"community_{chat_id}"),
    )
    return markup
