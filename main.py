# -*- coding: utf-8 -*-
# test file

import time
from WechatScraper import WechatScraper
from db import DB
import utils

ws = WechatScraper()
db = DB({
		"password": "203102"
	})

for i in range(3):
	gzh_list = ws.search_gzh_by_keyword('过山车', page=i + 1)
	db.store_gzh_list(gzh_list)
	time.sleep(3)

"""
# get_article:
# 	Args:
# 		keywords: 关键字
# 		pageCount: 所要获取的页数, 因为登录，所以最大为10
# 	**kwargs:
# 		type: 类型（过山车、黑暗乘骑、新闻等等）

# get_gzh_article:
# 	Args:
# 		wechatid: 公众号ID
# 	**kwargs:
# 		type: 类型
"""


# gzh_list = [{'gzh': 'rcd_china','col': '过山车'},
# 			{'gzh': 'lvjienews','col': '旅界'},
# 			{'gzh': 'happyvalley-bj','col': '北京欢乐谷'},
# 			{'gzh': 'paresearch','col': '道略演艺'},
# 			{'gzh': 'youlejiezazhi','col': '游乐界'},
# 			{'gzh': 'ThemeFlowers','col': '旅游奇葩说'}]

# def digest_article(msg, **kwargs):
# 	col = kwargs.get('col', '过山车')
# 	url = msg['url'].replace('amp;', '')
# 	effect_rows = db.check_exist(msg['title'])
# 	if(effect_rows>0):
# 		print(msg['title'] + ' alrady exist')
# 		return
# 	article = ws.get_article_by_url(url)
# 	article = utils.merge(article, msg)
# 	article['col'] = col
# 	db.store_article(article)
# 	time.sleep(5)

# for gzh in gzh_list:
# 	message_list = ws.get_gzh_message(gzh['gzh'])
# 	[digest_article(i, col=gzh['col']) for i in message_list]

# scrap 10 page articles related to one keyword

# keyword_list = [{
# 	'keyword': 'rcd过山车',
# 	'page': 10
# }, {
# 	'keyword': 'daolueyanyi',
# 	'page': 10
# }, {
# 	'keyword': '旅界',
# 	'page': 10
# }, {
# 	'keyword': 'youlejie',
# 	'page': 10
# }, {
# 	'keyword': 'beijinghuanlegu',
# 	'page': 10
# }, {
# 	'keyword': 'lvyouqipashuo',
# 	'page': 10
# }, {
# 	'keyword': 'heianchengqi',
# 	'page': 10
# }]

# def digest_article(msg, **kwargs):
# 	col = kwargs.get('col', '过山车')
# 	url = msg['url'].replace('amp;', '')
# 	effect_rows = db.check_exist(msg['title'])
# 	if(effect_rows>0):
# 		print(msg['title'] + ' alrady exist')
# 		return
# 	article = ws.get_article_by_url(url)
# 	article = utils.merge(article, msg)
# 	article['col'] = col
# 	db.store_article(article)
# 	time.sleep(5)

# for item in keyword_list:
# 	for i in range(item['page']):
# 		try:
# 			article_list = ws.get_article_list_by_keyword(item['keyword'], page=i)
# 			[digest_article(article, col=article['gzh']) for article in article_list]
# 		except Exception as e:
# 			print(e)
# 			continue
		






















	


