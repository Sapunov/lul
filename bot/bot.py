from telegram.error import (TelegramError, TimedOut)
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import telegram

import common
import handlers
import settings


log = common.mini_log(__name__)


HANDLERS = [
    MessageHandler(Filters.command, handlers.unknown)
]


def exception_handler(bot, update, error):

    try:
        raise error
    except TimedOut:
        return
    except TelegramError as exc:
        log.exception(exc)


def main():

    updater = Updater(token=settings.TELEGRAM_TOKEN, workers=10)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, handlers.text, edited_updates=True)],
        states={
            'text': [
                MessageHandler(Filters.text, handlers.text, edited_updates=True)
            ],
            'confirm': [
                RegexHandler(settings.CONFIRM_CHOICE_OPTION_REXP, handlers.confirm)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, handlers.text, edited_updates=True)]
    )

    dispatcher.add_handler(CommandHandler('start', handlers.start))
    dispatcher.add_handler(CommandHandler('help', handlers.help))
    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(exception_handler)

    log.debug('Start polling...')

    updater.start_polling()
    updater.idle()

    log.debug('Polling ended.')


if __name__ == '__main__':

    main()
