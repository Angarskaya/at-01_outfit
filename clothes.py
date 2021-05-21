class Clothes():
	"""Модель одежды"""

	def __init__(self, name, group, price, photo, link):
		self.name = name
		self.group = group
		self.price = price
		self.photo = photo
		self.link = link

	def change_price(price):
		self.price = price