import telebot
import json
import requests as r
from telebot import types
import clothes
import packaging

bot = telebot.TeleBot('1789007273:AAFOpqeR9aPQd18zYb1XRT_dLreXbvvfaBg')
menu = telebot.types.ReplyKeyboardMarkup(True)
menu.row('Каталог🏬', 'Корзина🛒')
menu.row('Мой бюджет💵')


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.from_user.id, text='a', reply_markup=menu)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text == 'Каталог🏬':
		choose_gender(message)
		#view_catalog(message)
	if message.text == 'Корзина🛒':
		view_item_cart(str(message.chat.id), 0)
	if message.text == 'Мой бюджет💵':
		with open('users_budget.json', 'r', encoding="utf-8") as file: #чтение
			keyboard = types.InlineKeyboardMarkup()
			key_change_budget = types.InlineKeyboardButton(text='Указать сумму', callback_data='change_budget')
			keyboard.row(key_change_budget)
			users_budget = json.load(file)
			if str(message.chat.id) in users_budget:
				bot.send_message(message.chat.id, 
					text=f'📈 Ваш текущий бюджет:  {users_budget[str(message.chat.id)][0]}р.\n📉 Сумма товара в кашей корзине:  {users_budget[str(message.chat.id)][1]}р.',
					reply_markup=keyboard)
			else:
				bot.send_message(message.chat.id, 
					text='Укажите ваш бюджет, который вы можете на одежду',
					reply_markup=keyboard)
	if message.text.isdigit():
		with open('users_budget.json', 'r', encoding="utf-8") as file: #чтение
			users_budget = json.load(file)
		price_cart = 0
		if str(message.chat.id) in users_budget:
			price_cart = users_budget[str(message.chat.id)][1]
		users_budget[str(message.chat.id)] = [int(message.text), price_cart]
		with open('users_budget.json', 'w', encoding="utf-8") as file: #запись
			json.dump(users_budget, file, indent=2, ensure_ascii=False)
		bot.send_message(message.chat.id, text='Бюджет успешно изменен!')


def choose_gender(message):
	keyboard = types.InlineKeyboardMarkup()
	key_man = types.InlineKeyboardButton(text='Мужская одежда', callback_data='man')
	key_woman = types.InlineKeyboardButton(text='Женская одежда', callback_data='woman')
	keyboard.row(key_man, key_woman)
	bot.send_message(message.from_user.id, text='Выберите категорию одежды:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data.startswith('man'))
def view_man_catalog(call):
	keyboard = types.InlineKeyboardMarkup()
	key_polo = types.InlineKeyboardButton(text='Рубашки/Поло/Футболки', callback_data='next_polo_0')
	key_hoodie = types.InlineKeyboardButton(text='Худи/Толстовки/Свитеры', callback_data='next_hoodie_0')
	key_trousers = types.InlineKeyboardButton(text='Шорты/Брюки/Джинсы', callback_data='next_trousers_0')
	key_outerwear = types.InlineKeyboardButton(text='Верхняя одежда', callback_data='next_outerwear_0')
	keyboard.row(key_polo)
	keyboard.row(key_hoodie)
	keyboard.row(key_trousers)
	keyboard.row(key_outerwear)

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
		text='Мужская одежда\nВыберите категорию одежды:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data.startswith('woman'))
def view_man_catalog(call):
	keyboard = types.InlineKeyboardMarkup()
	key_top = types.InlineKeyboardButton(text='Рубашки/Топы/Футболки', callback_data='next_top_0')
	key_hoodie = types.InlineKeyboardButton(text='Худи/Толстовки/Свитеры', callback_data='next_hoodie_0')
	key_dress = types.InlineKeyboardButton(text='Платья/Комбинезоны', callback_data='next_dress_0')
	key_outerwear = types.InlineKeyboardButton(text='Верхняя одежда', callback_data='next_outerwearwoman_0')
	keyboard.row(key_top)
	keyboard.row(key_hoodie)
	keyboard.row(key_dress)
	keyboard.row(key_outerwear)

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
		text='Женская одежда\nВыберите категорию одежды:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data.startswith('change_'))
def change_budget(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
		text="Напишите сумму в рублях:")


@bot.callback_query_handler(func=lambda c: c.data.startswith('nextcart_'))
def cart_callback_worker(call):
	next_index = int(call.data.split('_')[-1])
	view_item_cart(str(call.message.chat.id), next_index)


def view_item_cart(user_id, index):
	keyboard = types.InlineKeyboardMarkup()
	key_add_cart = types.InlineKeyboardButton(text='🗑 Удалить из корзины 🗑', 
		callback_data=f'delete_cart_{index}')
	key_next = types.InlineKeyboardButton(text='>', 
		callback_data=f'nextcart_{index+1}')
	key_back = types.InlineKeyboardButton(text='<', 
		callback_data=f'nextcart_{index-1}')
	keyboard.row(key_back, key_next)
	keyboard.row(key_add_cart)

	with open('users_data.json', 'r', encoding="utf-8") as file: #чтение
		cart = json.load(file)
		if len(cart[user_id]) == 0:
			bot.send_message(user_id, text='Ваша корзина пуста, добавьте что-нибудь из каталога')
			return
		if index >= len(cart[user_id]):
			index = 0
		elif index < 0:
			index = len(cart[user_id]) - 1
		item = cart[user_id][index]
		send_message_photo(change_item_model(item), keyboard, user_id)


def change_item_model(item):
	return clothes.Clothes(item[0], item[1], item[2], item[3], item[4])


@bot.callback_query_handler(func=lambda c: c.data.startswith('delete_cart_'))
def delete_item_from_cart(call):
	index = int(call.data.split('_')[-1])
	if packaging.delete_cart_user(call.message.chat.id, index):
		bot.send_message(call.message.chat.id, 
					text='🛒 Ваша корзина пуста, добавьте что-нибудь из каталога 🛒')
		return


	keyboard = types.InlineKeyboardMarkup()
	key_back = types.InlineKeyboardButton(text='Вернутся к корзине', 
		callback_data=f'nextcart_{index-1}')
	keyboard.row(key_back)
	bot.send_message(call.message.chat.id, text='🎉 Товар успешно удален из корзины 🎉',
						 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data.startswith('next_'))
def catalog_callback_worker(call):
	next_index = int(call.data.split('_')[-1])
	type_item = call.data.split('_')[-2]
	if next_index >= len(packaging.clothes_items[type_item]):
		next_index = 0
	elif next_index < 0:
		next_index = len(packaging.clothes_items[type_item]) - 1
	current_item = packaging.clothes_items[type_item][next_index]

	keyboard = types.InlineKeyboardMarkup()
	key_add_cart = types.InlineKeyboardButton(text='📥 В корзину 📥', 
		callback_data=f'add_cart_{type_item}_{next_index}')
	key_next = types.InlineKeyboardButton(text='>', 
		callback_data=f'next_{type_item}_{next_index+1}')
	key_back = types.InlineKeyboardButton(text='<', 
		callback_data=f'next_{type_item}_{next_index-1}')
	keyboard.row(key_back, key_next)
	keyboard.row(key_add_cart)

	send_message_photo(current_item, keyboard, call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('add_cart_'))
def add_cart(call):
	index_item = int(call.data.split('_')[-1])
	type_item = call.data.split('_')[-2]
	packaging.add_cart_user(call.message.chat.id, 
		packaging.clothes_items[type_item][index_item])
	keyboard = types.InlineKeyboardMarkup()
	key_back = types.InlineKeyboardButton(text='Вернутся к просмотру', 
		callback_data=f'next_{type_item}_{index_item}')
	keyboard.row(key_back)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
						 text='Товар успешно добавлен в корзину',
						 reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: False)
def callback_worker(call):
	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text='ещё!', callback_data='yes')
	keyboard.add(key_yes)
	if call.data == 'yes':
		aneck = getAneck.parse()
		bot.send_message(call.message.chat.id, text=aneck, reply_markup=keyboard)


def send_message_photo(item, keyboard, user_id):
	bot.send_photo(user_id, r.get(item.photo).content)
	bot.send_message(user_id, text=item.name + ' ' + str(item.price) + 'р.',
					  reply_markup = keyboard)



bot.polling(none_stop=True, interval=0)