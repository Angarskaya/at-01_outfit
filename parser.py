import bs4
import logging
import json
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')
main_url = 'https://www.wildberries.ru'


class Client:
	def __init__(self):
		self.session = requests.Session()
		self.session.headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
			'Accept-Language': 'ru',
			}
		self.result = []

	def load_page(self):
		url = 'https://www.wildberries.ru/catalog/zhenshchinam/odezhda/verhnyaya-odezhda'
		res = self.session.get(url=url)
		res.raise_for_status()
		# with open('test.txt', 'w', encoding="utf-8") as file:
		# 	file.write(res.text)
		return res.text

	def parse_page(self, text: str):
		soup = bs4.BeautifulSoup(text, 'lxml')
		container = soup.select('div.dtList.i-dtList.j-card-item')
		for block in container:
			self.parse_block(block=block)

	def parse_block(self, block):
		#logger.info(block)
		#logger.info('=' * 100)

		url_block = block.select_one('a.ref_goods_n_p.j-open-full-product-card')
		if not url_block:
			logger.error('no url_block')
			return

		url = url_block.get('href')
		if not url:
			logger.error('not url')
			return
		url = main_url + url

		name = block.select_one('strong.brand-name')
		if not name:
			logger.error('not name')
			return
		name = name.text.replace('/', '').strip()

		price = block.select_one('ins.lower-price')
		if not price:
			logger.error('not price')
			return
		price = price.text[:-1].replace(' ', '')

		link_photo = url_block.select('img.thumbnail')
		if not link_photo:
			logger.error('not link_photo')
			return
		link_photo = 'https:' + link_photo[1].get('src').strip()

		self.result.append([name, 'outerwearwoman', int(price), link_photo, url])

	def run(self):
		text = self.load_page()
		self.parse_page(text=text)
		with open('clothes.json', 'r', encoding="utf-8") as file:
			info = json.load(file)
		info.extend(self.result)
		with open('clothes.json', 'w', encoding="utf-8") as file:
			json.dump(info, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
	parser = Client()
	parser.run()