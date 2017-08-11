# -*- coding: utf-8 -*-
# databse actions

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import json
import pymysql

import config
import utils

class DB(object):
	"""docstring for DB"""
	def __init__(self, **kwargs):
		super(DB, self).__init__()
		db_config = kwargs.get('db_config')
		self._db = utils.merge(db_config, config.db_config)
		print(self._db)

	def store_gzh_list(self, gzhList, **kwargs):
		if(type(gzhList) != list):
			return False
		table = kwargs.get('table', 'gzh')
		[self._store_gzh_info(i, table=table) for i in gzhList]

	def _store_gzh_info(self, info, **kwargs):
		table = kwargs.get('table')
		query = 'insert into ' + table + ' (`title`, `wechatid`, `avatar`, `qrcode`, `introduction`, `verification`) values ("' + info.get('title', '') + '", "' + info.get('wechatid', '') + '", "' + info.get('avatar', '') + '", "' + info.get('qrcode', '') + '", "' + info.get('introduction', '') + '", "' + info.get('verification', '') + '")'
		self._execute(query)

	def store_article(self, article, **kwargs):
		for i in article:
			article[i] = self._escape(article[i])
			
		table = kwargs.get('table', 'articles')
		query = 'insert into ' + table + ' (`title`, `poster`, `authorId`, `authorAvatar`, `authorName`, `col`, `description`, `content`, `updateTime`, `tag`, `likes`, `type`) values ("' + article.get('title', '') + '", "' + article.get('poster', '') + '", NULL, "' + article.get('authorAvatar', '') + '", "' + article.get('authorName', '') + '", "' + article.get('col', '') + '", "' + article.get('description', '') + '", "' + article.get('content', '').strip() + '", DATE_ADD(\'1970-01-01 00:00:00\', INTERVAL ' + str(article.get('updateTime', '')) + ' SECOND), 0, 0, 0)'
		self._execute(query)
		print(article['title'] + ' inserted')

	def check_exist(self, title, **kwargs):
		print('checking exist')
		query = 'select * from ' + kwargs.get('table', 'articles') + ' where title="' + self._escape(title) + '"'
		effect_rows = self._execute(query)
		return effect_rows


	def _execute(self, query):
		conn = pymysql.connect(**self._db)
		cursor = conn.cursor()
		effect_rows = cursor.execute(query)
		conn.commit()
		cursor.close()
		conn.close()
		print('connection closed')
		return effect_rows

	def _escape(self, string):
		if(type(string) == list):
			return ','.join(string)
		if(type(string) == int):
			return str(string)
		return string.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;')








		
