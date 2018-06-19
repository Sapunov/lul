import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from telegram.ext.dispatcher import run_async
import telegram

from logulife import LogulifeClient
from logulife import exceptions as lul_exceptions

import common
import messages
import settings
import misc


log = common.mini_log(__name__)

lul_clients = {}


@run_async
def start(bot, update):

    log.debug('Handling `start` command. Update: %s')

    update.message.reply_text(messages.START)


@run_async
def help(bot, update):

    log.debug('Handling `help` command. Update: %s')

    update.message.reply_text(messages.HELP)


@run_async
def unknown(bot, update):

    update.message.reply_text(messages.UNKNOWN)


def text(bot, update):

    log.debug('Handling `text` command. Update: %s', update)

    from_id = str(update.effective_user.id)
    token = settings.USERS.get(from_id, None)

    if token is None:
        update.message.reply_text('Извините, вы не наш клиент :(')
        return

    if from_id not in lul_clients:
        lul_clients[from_id] = LogulifeClient(token=token)

    client = lul_clients[from_id]

    if update.message is None: # this is update
        try:
            client.records.update_by_ext_id(
                settings.SOURCE_NAME,
                update.edited_message.message_id,
                update.edited_message.text)
            update.edited_message.reply_text(messages.OK_UPDATE)
        except lul_exceptions.NotFoundException as exc:
            log.debug(exc)
            update.edited_message.reply_text(messages.NOT_FOUND)
        except Exception as exc:
            log.error(exc)
            save_msg = '{0}\n{1}'.format(str(exc), update.to_json())
            misc.save_json(update.update_id, save_msg)
            update.edited_message.reply_text(messages.OK_UPDATE)
            # Сообщение админу
            bot.send_message(
                settings.ADMIN_ACCOUNT,
                'Запись с id={0} у пользователя {1} не была ' \
                'обновлена. Ошибка: {2}'.format(
                    update.update_id,
                    update.effective_user.username,
                    str(exc)))
    else:
        try:
            client.records.create(
                update.message.text,
                settings.SOURCE_NAME,
                update.message.message_id,
                update.message.date)
        except Exception as exc:
            log.error(exc)
            save_msg = '{0}\n{1}'.format(str(exc), update.to_json())
            misc.save_json(update.update_id, save_msg)
            # Сообщение админу
            bot.send_message(
                settings.ADMIN_ACCOUNT,
                'Запись с id={0} у пользователя {1} не была ' \
                'сохранена. Ошибка: {2}'.format(
                    update.update_id,
                    update.effective_user.username,
                    str(exc)))

        update.message.reply_text(messages.OK)
