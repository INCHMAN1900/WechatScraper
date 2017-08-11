# -*- coding: utf-8 -*-

import config
import re
import math
import json
import random
import requests
import time

class ImageHandler(object):
	"""docstring for ImageHandler"""
	def __init__(self, **kwargs):
		super(ImageHandler, self).__init__()
		self.path = kwargs.get('path', config.img_base_path)

	def withdraw_content_imgs(self, content):
		img_re = re.compile(r'<img[^>]+data\-src\=\"http[^"]+\"')
		images = img_re.findall(content)
		for j in range(len(images)):
			images[j] = re.sub('<img.+data\-src=', '', images[j]).replace('"', '')
			newPath = self.write_image(images[j])
			content = content.replace(images[j], newPath, 2)
		return content

	def write_image(self, image):
		if(image):
			_id = self._generate_image_id()
			_type_re = re.compile(r'wx_fmt=\w+')
			_types = _type_re.findall(image)
			end = ''
			print(image)
			if(len(_types) == 0 or _types[0] == 'wx_fmt=1'):
				end = '.png'
				path = self.path + str(_id) + end
			else:
				end = '.' + re.sub('wx_fmt=', '', _types[0])
				path = self.path + str(_id) + end
			f_img = open(path, 'w')
			r = requests.get(image)
			f_img.write(r.content)
			f_img.close()
			time.sleep(3)
			# if you want to change the path where the images will be put, change config file and this path config.
			path = '/imgs' + str(_id) + end
			return path
		else:
			return ''


	def _generate_image_id(self):
		chars = 'QWERTYUPLKJHGFDSAZXCVBNMqwertyuplkjhgfdsazxcvbnm123456789'
		length = len(chars)
		_id = ''
		for i in range(15):
			_id = _id + chars[math.trunc(random.random()*length)]
		return _id
