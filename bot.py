import logging
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
	print('Вызван /start')
	context.user_data['emoji'] = get_smile(context.user_data)
	update.message.reply_text(f'Привет, пользователь {context.user_data["emoji"]}')


def get_smile(user_data):
	if 'emoji' not in user_data:
		smile = choice(settings.USER_EMOJI)
		return smile
	return user_data['emoji']


def talk_to_me(update, context):
	user_text = update.message.text
	print(user_text)
	context.user_data['emoji'] = get_smile(context.user_data)
	update.message.reply_text(f'Пока я только повторяю тебя {user_text}{context.user_data["emoji"]}')


def play_random_number(user_number):
	bot_number = randint(user_number - 10, user_number + 10)
	if user_number > bot_number:
		message = f"Ваше число {user_number}, мое число {bot_number}, вы выиграли"
	elif user_number == bot_number:
		message = f"Ваше число {user_number}, мое число {bot_number}, ничья"
	else:
		message = f"Ваше число {user_number}, мое число {bot_number}, вы проиграли"
	return message


def guess_number(update, context):
	print(context.args)
	if context.args:
		try:
			user_number = int(context.args[0])
			message = play_random_number(user_number)
		except (TypeError, ValueError):
			message = "Введите целое число"
	else:
		message = "Введите число"
	update.message.reply_text(message)


def main():
	mybot = Updater(settings.API_KEY, use_context=True)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(CommandHandler("guess", guess_number))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))

	logging.info("Бот стартовал")
	mybot.start_polling()
	mybot.idle()


if __name__ == "__main__":
	main()
