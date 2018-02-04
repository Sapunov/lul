import telegram

from phrases import Phrases
import logulife


phrases = Phrases()


def start(bot, update):

    update.message.reply_text(phrases.start)


def help(bot, update):

    update.message.reply_text(phrases.help)


def unknown(bot, update):

    update.message.reply_text(phrases.unknown)


def text(bot, update):

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
    else:
        status = logulife.make_record(
            update.message.text,
            update.message.message_id,
            update.message.date)

        if status < 0:
            msg = 'Во время сохранения произошло исключение 😫'
        elif status == 0:
            msg = phrases.saved
        else:
            msg = 'Во время сохранения что-то пошло не так. Код: {0}'.format(status)

        update.message.reply_text(msg)
