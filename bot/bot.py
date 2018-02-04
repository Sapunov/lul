import logging

from telegram.error import TelegramError
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import telegram

import handlers
import settings


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


HANDLERS = [
    CommandHandler('start', handlers.start),
    CommandHandler('help', handlers.help),
    MessageHandler(Filters.text, handlers.text, edited_updates=True),
    MessageHandler(Filters.command, handlers.unknown)
]


def exception_handler(bot, update, error):

    logging.exception(error)


def main():

    updater = Updater(token=settings.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    for hndler in HANDLERS:
        dispatcher.add_handler(hndler)

    dispatcher.add_error_handler(exception_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    main()
