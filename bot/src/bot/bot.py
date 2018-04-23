from telegram.error import (TelegramError, NetworkError)
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


def exception_handler(bot, update, error):

    try:
        raise error
    except NetworkError as exc:
        log.error('Catch NetworkError: %s', exc)
    except TelegramError as exc:
        log.exception('Catch TelegramError: %s', exc)


def main():

    if settings.USE_PROXY:
        request_kwargs = {
            'proxy_url': settings.PROXY_HOST,
            'urllib3_proxy_kwargs': {
                'username': settings.PROXY_USERNAME,
                'password': settings.PROXY_PASSWORD
            }
        }
    else:
        request_kwargs = {}

    updater = Updater(
        token=settings.TELEGRAM_TOKEN,
        workers=10,
        request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', handlers.start))
    dispatcher.add_handler(CommandHandler('help', handlers.help))
    dispatcher.add_handler(MessageHandler(Filters.text, handlers.text, edited_updates=True))

    dispatcher.add_error_handler(exception_handler)

    log.debug('Start polling...')

    updater.start_polling()
    updater.idle()

    log.debug('Polling ended.')


if __name__ == '__main__':

    main()
