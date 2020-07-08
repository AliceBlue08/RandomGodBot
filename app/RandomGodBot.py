import telebot
import requests
import uuid
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ParseMode
from app.models import User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

RECEIVED, CANCEL = 0, 1

TEXT = "Hi! This bot gives you random image by your command! Run /menu to start."


class RandomGodBot:
    def __init__(self, token, database_url):
        self.token = token
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        start_handler = CommandHandler('start', self.start)
        menu_handler = CommandHandler('menu', self.menu)
        random_image_handler = CommandHandler('random_image', self.random_image)

        handlers = [start_handler,
                    menu_handler,
                    random_image_handler
                    ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def random_image(self, bot, update):
        user_id = update.message.chat.id
        self.update_user_in_database(user_id)
        url = "https://picsum.photos/700/700?random=" + str(uuid.uuid4())
        bot.sendPhoto(chat_id=update.message.chat_id, photo=url)

    def menu(self, bot, update):
        u = """Choose a command:

        */random_image* - completely random image

        */menu* - show this message."""

        self.display_menu_keyboard(bot, update, u)

    def update_user_in_database(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        time = datetime.now()
        if user is None:
            user = User(id=user_id, date_started=time, date_last_used=time)
        else:
            user.update_time(time)

        self.session.add(user)
        self.session.commit()

    def cancel_conversation(self, bot, update):
        self.display_menu_keyboard(bot, update, TEXT)
        return ConversationHandler.END

    def start(self, bot, update):
        user_id = update.message.chat.id
        self.update_user_in_database(user_id)

        self.display_menu_keyboard(bot, update, TEXT)

    def display_menu_keyboard(self, bot, update, text):
        menu_options = [
            [KeyboardButton('/random_image')],
            [KeyboardButton('/menu')]
        ]

        keyboard = ReplyKeyboardMarkup(menu_options, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=keyboard)

    def start_webhook(self, url, port):
        self.updater.start_webhook(listen="0.0.0.0",
                                   port=port,
                                   url_path=self.token)
        self.updater.bot.set_webhook(url + self.token)
        self.updater.idle()

    def start_local(self):
        self.updater.start_polling()
        self.updater.idle()
