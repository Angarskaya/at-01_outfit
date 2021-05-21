import clothes

clothes_items = []
cap = clothes.Clothes('SQUIRTABLE / Кепка / Бейсболка / Бейсболка женская / Кепка женская / Бейсболка чёрная ', 
					  'headdress', 475, 'photos\\cap1.jpg',
			          'https://www.wildberries.ru/catalog/25870950/detail.aspx?targetUrl=XS')
clothes_items.append(cap)
shopping_cart = []

def add_cart(product):
	shopping_cart.append(product)