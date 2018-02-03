import telegram

from phrases import Phrases


phrases = Phrases()


def start(bot, update):

    update.message.reply_text(phrases.start)


def help(bot, update):

    update.message.reply_text(phrases.help)


def unknown(bot, update):

    update.message.reply_text(phrases.unknown)


def text(bot, update):

    if update.message is None:
        update.edited_message.reply_text(phrases.edit)
        # And call edit routine
    else:
        update.message.reply_text(phrases.wait)
