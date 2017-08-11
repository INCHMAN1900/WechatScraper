# -*- coding: utf-8 -*- 

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import re
import json

import config
import utils

# if you want to make this word on a system with no GUI, install Xvfb first and then uncomment these lines.

# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(1366, 768))
# display.start()
# print('Display start')

browser = webdriver.Firefox()

class WechatScraper():

	def __init__(self, **kwargs):
		self.config = config

	"""
		query: keyword
		page: the page you want to scrap, useful when you use a keyword to scrap many articles
	"""

	def get_article_list_by_keyword(self, query, page=1):
		query = 'query=' + query
		page = 'page=' + str(page)
		built_url = self._build_url(self.config.article_search_url, ['query', 'page'], [query, page])
		article_list = []
		browser.get(built_url)

		times = self._withdraw_time(browser.page_source)

		news_list = browser.find_elements_by_css_selector('.news-list li')
		for i in range(len(news_list)):
			news = news_list[i]
			title = news.find_element_by_tag_name('h3').text
			url = news.find_element_by_css_selector('h3 a').get_attribute('href')
			description = news.find_element_by_css_selector('.txt-box>p').text
			gzh = news.find_element_by_css_selector('.account').text
			gzh_url = news.find_element_by_css_selector('.account').get_attribute('href')
			# time_re = re.compile(r'\d{10}')
			# bs_obj = BeautifulSoup(browser.page_source, 'html.parser')

			# time = re.search(time_re, news.find_element_by_tag_name('script').text).group(0)
			imgs = map(self._withdraw_image, news.find_elements_by_tag_name('img'))
			news_unit = {
				'title': title,
				'url': url,
				'gzh': gzh,
				'gzh_url': gzh_url,
				'description': description,
				'updateTime': times[i],
				'poster': imgs
			}
			article_list.append(news_unit)
		return article_list

	def get_article_by_url(self, url):
		browser.get(url)
		avatar_re = re.compile(r'ori_head_img_url[^;]+;')
		raw_avatar = avatar_re.findall(browser.page_source)
		avatar = ''
		if(raw_avatar):
			avatar = re.sub(re.compile(r'[^"]+"'), '', raw_avatar[0], 1).replace('";', '')
		page_content = browser.find_element_by_id('img-content')
		ems = page_content.find_elements_by_css_selector('.rich_media_meta_list>em')
		author = ''
		if(len(ems)>1):
			author = ems[1].text
		content = page_content.find_element_by_id('js_content').get_attribute('innerHTML')
		article = {
			'authorName': author,
			'authorAvatar': avatar,
			'content': content
		}
		return article

	# scrap gzh list at the page
	def search_gzh_by_keyword(self, query, **kwargs):
		page = kwargs.get('page', 1)
		query = 'query=' + query
		page = 'page=' + str(page)
		built_url = self._build_url(self.config.gzh_search_url, ['query', 'page'], [query, page])
		browser.get(built_url)
		gzh_list = browser.find_elements_by_css_selector('.news-list2 li')
		for i in range(len(gzh_list)):
			gzh = gzh_list[i]
			avatar = gzh.find_element_by_css_selector('.img-box img').get_attribute('src')
			title = gzh.find_element_by_class_name('tit').text
			wechatid = gzh.find_element_by_name('em_weixinhao').text
			qrcode = gzh.find_element_by_css_selector('.ew-pop .pop img').get_attribute('src')
			gzh_info = {
				'title': title,
				'wechatid': wechatid,
				'avatar': avatar,
				'qrcode': qrcode
			}
			dls = gzh.find_elements_by_tag_name('dl')
			for k in range(len(dls)):
				dl = dls[k]
				if(dl.text[0:4] == u'功能介绍'[0:4]):
					gzh_info['introduction'] = dl.find_element_by_tag_name('dd').text
				if(dl.text[0:4] == u'微信认证'[0:4]):
					gzh_info['verification'] = dl.find_element_by_tag_name('dd').text
			gzh_list[i] = gzh_info
		return gzh_list

	# get gzh message by wechatid
	def get_gzh_message(self, wechatid):
		query = 'query=' + str(wechatid)
		page = 'page=' + str(1)
		built_url = self._build_url(self.config.gzh_search_url, ['query', 'page'], [query, page])
		browser.get(built_url)
		gzh_list = browser.find_elements_by_css_selector('.news-list2 li')
		gzh_url = gzh_list[0].find_element_by_css_selector('.img-box a').get_attribute('href')
		browser.get(gzh_url)

		# get msg within the script
		source_re = re.compile(r'{"list":.+}}]}')
		msg_list_string = source_re.findall(browser.page_source)[0]
		msg_list = json.loads(msg_list_string.encode('utf-8'))['list']
		for i in range(len(msg_list)):
			msg = msg_list[i]
			f = msg['app_msg_ext_info']
			s = msg['comm_msg_info']
			msg_list[i] = {
				'title': f['title'],
				'url': 'http://mp.weixin.qq.com' + f['content_url'],
				'poster': f['cover'],
				'authorName': f['author'],
				'description': f['digest'],
				'updateTime': s['datetime']
			}
		return msg_list

		# get msg list through DOM tree
		# msg_list = browser.find_elements_by_class_name('weui_msg_card')
		# for i in range(len(msg_list)):
		# 	msg = msg_list[i]
		# 	html = msg.find_element_by_css_selector('.weui_media_box').get_attribute('innerHTML')
		# 	img_re = re.compile(r'http:.*wx_fmt=[a-zA-Z0-9]+')
		# 	poster = img_re.findall(html)
		# 	title = msg.find_element_by_tag_name('h4').text.strip()
		# 	url = 'http://mp.weixin.qq.com' + msg.find_element_by_tag_name('h4').get_attribute('hrefs')
		# 	time = msg.find_element_by_class_name('weui_media_extra_info').text
		# 	msg_list[i] = {
		# 		'title': title,
		# 		'poster': poster,
		# 		'url': url,
		# 		'time': time
		# 	}
		# print(msg_list)
		# return msg_list


	"""
		below here are some common functions

	"""

	# replace url parameters
	def _build_url(self, base, oldVal, newVal):
		if(type(oldVal) == str):
			base = base.replace(oldVal, newVal)
		if(type(oldVal) == list):
			for i in range(len(oldVal)):
				base = base.replace(oldVal[i], str(newVal[i]))
		return base

	# withdraw image url through image element
	def _withdraw_image(self, element):
		return element.get_attribute('src') or element.get_attribute('data-src')

	# withdraw time within script, page source needed
	def _withdraw_time(self, source):
		raw_re = re.compile(r'document\.write\(timeConvert\(\'\d{10}\'\)\)')
		raw_times = raw_re.findall(source)
		exact_re = re.compile(r'\d{10}')
		return [exact_re.findall(time)[0] for time in raw_times]

