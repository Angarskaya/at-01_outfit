import telebot
from telebot import types
import os
import packaging

bot = telebot.TeleBot('1789007273:AAFOpqeR6aPQd18zYb1XRT_dLreXbvvfaBg')



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.reply_to(message, "Добрый день")
	keyboard = types.InlineKeyboardMarkup()
	key_headdress = types.InlineKeyboardButton(text='Головные уборы', callback_data='headdress')
	key_glasses = types.InlineKeyboardButton(text='Очки', callback_data='glasses')
	key_hoodie = types.InlineKeyboardButton(text='Худи', callback_data='hoodie')
	keyboard.add(key_headdress, key_glasses, key_hoodie)
	bot.send_message(message.from_user.id, text='Добрый день', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text='Хочу', callback_data='yes')
	keyboard.add(key_yes)
	bot.send_message(message.from_user.id, text='привет)\nхочешь анек?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	keyboard = types.InlineKeyboardMarkup()
	key_add_cart = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add_cart')
	key_next = types.InlineKeyboardButton(text='Следующий товар', callback_data='next')
	key_back = types.InlineKeyboardButton(text='Назад', callback_data='back')
	keyboard.add(key_add_cart, key_next, key_back)
	current_clothes = packaging.clothes_items[0]
	if call.data == 'headdress':
		photo = open(current_clothes.photo, 'rb')
		bot.send_photo(call.message.chat.id, photo)
		bot.send_message(call.message.chat.id, text=current_clothes.name + str(current_clothes.price) + 'р.',
						 reply_markup = keyboard)
	if call.data == 'add_cart':
		packaging.add_cart(current_clothes)
	if call.data == 'back':
		send_welcome('')

	pass
	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text='ещё!', callback_data='yes')
	keyboard.add(key_yes)
	if call.data == 'yes':
		aneck = getAneck.parse()
		bot.send_message(call.message.chat.id, text=aneck, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)