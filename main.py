# -*- coding: utf-8 -*-
# test file

import time
from WechatScraper import WechatScraper
from db import DB
import utils
import re

ws = WechatScraper()

'''
to custom your databse config , add db_config as a named parameter like:
	db_config = {
		'host': '127.0.0.1',    # host
		'port': 3306,           # port
		'user': 'root',         # database username
		'password': '123456',   # database password
		'db': 'DATABASE',       # database name
	}
'''

db = DB()

from ImgHandler import ImageHandler

ih = ImageHandler() 

# scrap 10 page articles related to one keyword.
# images will be put oin imgs folder

keyword_list = [{
	'keyword': '漫威',
	'page': 10
}, {
	'keyword': 'DC',
	'page': 10
}]

def digest_article(msg, **kwargs):
	col = kwargs.get('col', 'mycol')
	url = msg['url'].replace('amp;', '')
	effect_rows = db.check_exist(msg['title'])
	if(effect_rows>0):
		print(msg['title'] + ' alrady exist')
		return
	article = ws.get_article_by_url(url)
	article = utils.merge(article, msg)
	article['col'] = col
	article['content'] = ih.withdraw_content_imgs(article['content'])
	if(article['poster'] and len(article['poster']) > 0):
		article['poster'] = ih.write_image(article['poster'][0])
	print('article get')
	db.store_article(article)
	print('article stored')
	time.sleep(3)

for item in keyword_list:
	for i in range(item['page']):
		try:
			article_list = ws.get_article_list_by_keyword(item['keyword'], page=i)
			[digest_article(article, col=article['gzh']) for article in article_list]
		except Exception as e:
			print(e)
			continue
		






















	


