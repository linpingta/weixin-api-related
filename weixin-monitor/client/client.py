#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim: set bg=dark noet sw=4 ts=4 fdm=indent : 

""" Task Monitor Client """
__author__='linpingta@163.com'

import os
import sys
import logging
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser
from celery import Celery

import celeryconfig


class WxClient(object):
	""" Weixin Client
	"""
	def __init__(self, name='wx_client'):
		self._name = name
		self._celery_client = None

	@property
	def name(self):
		return self._name

	def init(self, logger):
		celery = Celery()
		celery.config_from_object(celeryconfig)
		self._celery_client = celery

	def release(self, logger):
		pass

	def send_message(self, id, message, logger, type=1):
		try:
			# wrap object from id, related with business
			# id is "business id" who receive monitor 
			object = 'id[%d]' % id
			task_user_id = id
			elem_dict = {	
				'object':object,
				'type':type,
				'body':message,
			}
			logger.info('id[%d] send message %s' % (id, message))
			self._celery_client.send_task('wx_task_manager.send_message', [task_user_id, elem_dict])
		except Exception as e:
			logger.exception(e)


if __name__ == '__main__':

	basepath = os.getcwd()
	confpath = os.path.join(basepath, 'conf/wx_client.conf')
	conf = ConfigParser.RawConfigParser()
	conf.read(confpath)

	logging.basicConfig(filename=os.path.join(basepath, 'logs/wx_client.log'), level=logging.INFO,
		format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
		datefmt = '%a, %d %b %Y %H:%M:%S'
		)
	logger = logging.getLogger('WxClient')

	try:
		name = conf.get('common', 'name')

		wx_client = WxClient(name)
		wx_client.init(logger)

		# real usage
		wx_client.send_message(1, 'test here', logger)	

		wx_client.release(logger)
	except Exception,e:
		logging.exception(e)

