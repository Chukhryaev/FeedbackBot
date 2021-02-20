import telebot
import config
import fastans


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.send_message(message.chat.id, fastans.START)


@bot.message_handler(commands=["getchat"])
def handle_getchat(message):
	bot.send_message(message.chat.id, message.chat.id)


bot.polling(none_stop=True)
