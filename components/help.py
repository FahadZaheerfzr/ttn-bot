from telebot import TeleBot
from telebot import types

def help(message: types.Message, bot: TeleBot):
    bot.reply_to(
        message,
        """
<b>Welcome To Help Section!</b>

<b>👨‍💻Commands in-bot:</b>
• /start = Go to your TeleTreon account.
• /help = Receive TeleTreon info.
<b>👨‍💻Commands in Group/ Channel:</b>
• /setting = Go to settings menu to configure your private chat.
        """,
        parse_mode="HTML"
    )
    