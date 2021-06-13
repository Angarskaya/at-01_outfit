import clothes
import json


clothes_hoodie = []
clothes_trousers = []
clothes_polo = []
clothes_outerwear = []
clothes_outerwearwoman = []
clothes_top = []
clothes_dress = []


clothes_items = {
	 			 'hoodie': clothes_hoodie,
	 			 'trousers': clothes_trousers,
	 			 'polo': clothes_polo,
	 			 'outerwear': clothes_outerwear,
	 			 'outerwearwoman': clothes_outerwearwoman,
	 			 'dress': clothes_dress,
	 			 'top': clothes_top
	 			}



with open('clothes.json', 'r', encoding="utf-8") as file:
	clothes1 = json.load(file)
	for item in clothes1:
		clothes_items[item[1]].append(clothes.Clothes(item[0], item[1], item[2], item[3], item[4]))


def remove_repetitions_cart(cart):
    n = []
    for i in cart:
        if i not in n:
            n.append(i)
    return n


def add_cart_user(user_id, product):
	with open('users_data.json', 'r', encoding="utf-8") as file: #чтение
		cart = json.load(file)
	if str(user_id) in cart:
		cart[str(user_id)].append(product.to_list())
	else:
		tmp = []
		tmp.append(product.to_list())
		cart[str(user_id)] = tmp
	cart[str(user_id)] = remove_repetitions_cart(cart[str(user_id)])
	with open('users_data.json', 'w', encoding="utf-8") as file: #запись
		json.dump(cart, file, indent=2, ensure_ascii=False)
	change_price_cart(user_id)

def delete_cart_user(user_id, index_product):
	with open('users_data.json', 'r', encoding="utf-8") as file: #чтение
		cart = json.load(file)
	cart[str(user_id)].pop(index_product)
	with open('users_data.json', 'w', encoding="utf-8") as file: #запись
		json.dump(cart, file, indent=2, ensure_ascii=False)
	change_price_cart(user_id)
	return len(cart[str(user_id)]) == 0 #возвращает True если корзина пуста

def change_price_cart(user_id):
	with open('users_budget.json', 'r', encoding="utf-8") as file: #чтение
		users_budget = json.load(file)
	budget = 0
	if str(user_id) in users_budget:
		budget = users_budget[str(user_id)][0]
	with open('users_data.json', 'r', encoding="utf-8") as file: #чтение
		cart = json.load(file)
	summ = 0
	for item in cart[str(user_id)]:
		print(item[2])
		summ += item[2]
	users_budget[str(user_id)] = [budget, summ]
	with open('users_budget.json', 'w', encoding="utf-8") as file: #запись
		json.dump(users_budget, file, indent=2, ensure_ascii=False)
