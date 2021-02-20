import telebot
import config
import fastans


bot = telebot.TeleBot(config.TOKEN)


def get_file(message):
	file_data = bot.get_file(message.photo[-1].file_id)
	file = bot.download_file(file_data.file_path)
	return file


def user_logic(message):
	if message.content_type == "photo":
		bot.send_photo(config.ADMIN_CHAT, get_file(message), message.caption)

	if message.content_type == "video":
		bot.send_video(config.ADMIN_CHAT, get_file(message), message.caption)

	if message.content_type == "document":
		bot.send_document(config.ADMIN_CHAT, get_file(message), message.caption)

	if message.content_type == "text":
		bot.send_message(config.ADMIN_CHAT, message.text)


def admin_logic(message):
	pass


@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.send_message(message.chat.id, fastans.START)


@bot.message_handler(commands=["getchat"])
def handle_getchat(message):
	bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def handle_all(message):
	if message.chat.id == config.ADMIN_CHAT:
		admin_logic(message)
	else:
		user_logic(message)


bot.polling(none_stop=True)
