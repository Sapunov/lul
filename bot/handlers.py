import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from telegram.ext.dispatcher import run_async
import telegram

from phrases import Phrases
import common
import logulife
import settings


log = common.mini_log(__name__)

phrases = Phrases()


@run_async
def start(bot, update):

    log.debug('Handling `start` command. Update: %s')

    update.message.reply_text(phrases.start)


@run_async
def help(bot, update):

    log.debug('Handling `help` command. Update: %s')

    update.message.reply_text(phrases.help)


@run_async
def unknown(bot, update):

    update.message.reply_text(phrases.unknown)


def confirm(bot, update):

    log.debug('Handling `confirm` command. Update: %s')

    if update.message.text.lower() == 'нет':
        msg = 'Спасибо. Учтем.'
    else:
        msg = 'OK!'

    update.message.reply_text(msg, reply_markup=ReplyKeyboardRemove())

    return 'text'


def text(bot, update):

    log.debug('Handling `text` command. Update: %s')

    if update.message is None:
        status = logulife.update_record(
            update.edited_message.text,
            update.edited_message.message_id)

        if status < 0:
            msg = 'Во время сохранения произошло исключение 😫'
        elif status == 0:
            msg = phrases.edit
        else:
            msg = 'Во время сохранения что-то пошло не так. Код: {0}'.format(status)

        update.edited_message.reply_text(msg)
        return 'text'
    else:
        status = logulife.make_record(
            update.message.text,
            update.message.message_id,
            update.message.date)

        reply_keyboard = None

        if status < 0:
            msg = 'Во время сохранения произошло исключение 😫'
        elif status == 0:
            msg = 'Ваше сообщение обработано. Все верно?'
            reply_keyboard = [['Да', 'Нет']]
        else:
            msg = 'Во время сохранения что-то пошло не так. Код: {0}'.format(status)

        if reply_keyboard is None:
            update.message.reply_text(msg)
            return 'text'
        else:
            update.message.reply_text(
                msg,
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return 'confirm'


def cancel(bot, update):

    log.debug('Handling `cancel` command. Update: %s')

    return ConversationHandler.END
