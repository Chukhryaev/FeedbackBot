import telebot
from telebot import types
import config
import fastans


bot = telebot.TeleBot(config.TOKEN)


states = {
	"waiting_for_answer": False,
	"answer_chat_id": 0,
}


def get_file(message):
	file_data = bot.get_file(message.photo[-1].file_id)
	file = bot.download_file(file_data.file_path)
	return file


def get_answer_buttons(message):
	buttons = types.InlineKeyboardMarkup()
	buttons.add(*[types.InlineKeyboardButton(text=f"Answer to {message.chat.first_name} ({message.chat.id})",
											 callback_data=f"{message.chat.id}")])
	return buttons


def get_cancel_buttons():
	buttons = types.InlineKeyboardMarkup()
	buttons.add(*[types.InlineKeyboardButton(text=f"Cancel", callback_data=f"cancel")])
	return buttons


def user_logic(message):
	if message.content_type == "photo":
		bot.send_photo(config.ADMIN_CHAT, get_file(message), message.caption, reply_markup=get_answer_buttons(message))

	if message.content_type == "video":
		bot.send_video(config.ADMIN_CHAT, get_file(message), message.caption, reply_markup=get_answer_buttons(message))

	if message.content_type == "document":
		bot.send_document(config.ADMIN_CHAT, get_file(message), message.caption, reply_markup=get_answer_buttons(message))

	if message.content_type == "text":
		bot.send_message(config.ADMIN_CHAT, message.text, reply_markup=get_answer_buttons(message))


def admin_logic(message):
	if states["waiting_for_answer"]:
		states["waiting_for_answer"] = False
		chat = states["answer_chat_id"]
		if message.content_type == "photo":
			bot.send_photo(chat, get_file(message), message.caption)
			bot.send_message(config.ADMIN_CHAT, f"Sent message to {chat}:")
			bot.send_photo(config.ADMIN_CHAT, get_file(message), message.caption)

		if message.content_type == "video":
			bot.send_video(chat, get_file(message), message.caption)
			bot.send_message(config.ADMIN_CHAT, f"Sent message to {chat}:")
			bot.send_video(config.ADMIN_CHAT, get_file(message), message.caption)

		if message.content_type == "document":
			bot.send_document(chat, get_file(message), message.caption)
			bot.send_message(config.ADMIN_CHAT, f"Sent message to {chat}:")
			bot.send_document(config.ADMIN_CHAT, get_file(message), message.caption)

		if message.content_type == "text":
			bot.send_message(chat, message.text)
			bot.send_message(config.ADMIN_CHAT, f"Sent message to {chat}:")
			bot.send_message(config.ADMIN_CHAT, message.text)


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


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def handle_callback(call):
	states["waiting_for_answer"] = False
	bot.send_message(call.message.chat.id, "Canceled")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
	states["waiting_for_answer"] = True
	states["answer_chat_id"] = call.data
	bot.send_message(call.message.chat.id, f"You are answering to {call.data}", reply_markup=get_cancel_buttons())


bot.polling(none_stop=True)
