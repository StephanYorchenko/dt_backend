from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Updater, Filters
from .transport.bot.handlers import start, set_up_command, phone_handler, me
from config.settings import TOKEN

from .transport.bot.states import StatesConversation


def setup_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('set_phone', set_up_command)
        ],
        states={
            StatesConversation.PHONE_NUMBER: [
                MessageHandler(Filters.all, phone_handler, pass_user_data=True)
            ]
        },
        fallbacks=[]
    ))
    dp.add_handler(CommandHandler('me', me))
    updater.start_polling()
    updater.idle()
