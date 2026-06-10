import telebot
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! I'm your English buddy! 👋")

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def echo(message):
    bot.send_message(message.chat.id, f"You said: {message.text}")

bot.polling()

