import telebot

import misc
import settings
from datetime import datetime


TOKEN = misc.get_token(settings.TOKEN_PATH)

bot = telebot.TeleBot(TOKEN)


def main():

    for update in bot.get_updates():
        print("[{0}] ({1}): {2}".format(
            datetime.fromtimestamp(update.message.date),
            update.message.from_user.username,
            update.message.text))


if __name__ == "__main__":

    main()
