# -*- coding: utf-8 -*-
# test file

import time
from WechatScraper import WechatScraper
from db import DB
import utils

ws = WechatScraper()

for i in range(3):
	gzh_list = ws.search_gzh_by_keyword('manwei', page=i + 1)
	db.store_gzh_list(gzh_list)
	time.sleep(3)


# scrap 10 page articles related to one keyword

keyword_list = [{
	'keyword': 'manwei',
	'page': 10
}, {
	'keyword': 'marvel',
	'page': 10
}]

def digest_article(msg, **kwargs):
	col = kwargs.get('col', '过山车')
	url = msg['url'].replace('amp;', '')
	effect_rows = db.check_exist(msg['title'])
	if(effect_rows>0):
		print(msg['title'] + ' alrady exist')
		return
	article = ws.get_article_by_url(url)
	article = utils.merge(article, msg)
	article['col'] = col
	db.store_article(article)
	time.sleep(5)

for item in keyword_list:
	for i in range(item['page']):
		try:
			article_list = ws.get_article_list_by_keyword(item['keyword'], page=i)
			[digest_article(article, col=article['gzh']) for article in article_list]
		except Exception as e:
			print(e)
			continue
		






















	


