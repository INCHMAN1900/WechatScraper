# -*- coding: utf-8 -*-
# config file

import pymysql.cursors

article_search_url = 'http://weixin.sogou.com/weixin?oq=&query&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=17&_sug_=n&type=2&sst0=1499142762773&page&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'

gzh_search_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=10144&sst0=1500528877030&lkt=1%2C1500528876895%2C1500528876895&page'

db_config = {
	'host': '127.0.0.1',    # host
	'port': 3306,           # port
	'user': 'root',         # database username
	'password': '123456',   # database password
	'db': 'HUANLEYE',       # database name
	'charset': 'utf8mb4',   # database charset
	'cursorclass': pymysql.cursors.DictCursor
}