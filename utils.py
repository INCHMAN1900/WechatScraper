# -*- coding: utf-8 -*-

# merge two different dict object
def merge(new, base):
	for i in new:
		base[i] = new[i]
	return base