#-*- coding: utf-8 -*-
# vim: set bg=dark noet sw=4 ts=4 fdm=indent :

import os
import sys
import time
import logging
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser
import simplejson as json
from celery import Celery

from abc import ABCMeta, abstractmethod

from weixin_api.store import WeixinTokenFileStorage
from weixin_api.token import WeixinToken
from weixin_api.api import WeixinApi, WeixinResponse


basepath = sys.path[0]
confpath = os.path.join(basepath, 'conf/wx.conf')
conf = ConfigParser.RawConfigParser()
conf.read(confpath)

logging.basicConfig(filename=os.path.join(basepath, 'logs/wx.log'), level=logging.INFO,
	format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
	datefmt = '%a, %d %b %Y %H:%M:%S'
	)
logger = logging.getLogger('WxManager')

#host = 'redis://HOST' # i.e redis://10.0.0.0
#port = 'PORT' # i.e 1234
host = 'redis://localhost' # i.e redis://10.0.0.0
port = '6379' # i.e 1234
db = '0'
app = Celery('task_info', broker=host+':'+port+'/'+db)


class WxBasicSender(object):
	""" Responsible for WX API call
	"""
	__metaclass__ = ABCMeta

	def __init__(self, conf):
		self.app_id = conf.get('common', 'app_id')
		self.app_secret = conf.get('common', 'app_secret')
		self.token_file = conf.get('common', 'token_file')
		self.token_node = 'gettoken'

		self._admin_user_ids = []
		self._api = None
		self.weixin_url = ""
		self.qiye_flag = False

	@property
	def admin_user_ids(self):
		return self._admin_user_ids

	@admin_user_ids.setter
	def admin_user_ids(self, value):
		self._admin_user_ids = value

	def init(self, logger):
		WeixinTokenFileStorage.init(self.token_file, logger)
		WeixinToken.init(self.app_id, self.app_secret, WeixinTokenFileStorage, self.weixin_url, self.qiye_flag, self.token_node)
		access_token = WeixinToken.get_access_token(logger)
		WeixinApi.init(self.app_id, self.app_secret, access_token)

		self._api = WeixinApi.get_weixin_api()

	@abstractmethod
	def send(self, agent_id, user_id, wx_message, now, logger):
		pass


class WxQiyeSender(WxBasicSender):
	""" Responsible for WX Qiye API call
	"""
	def __init__(self, conf):
		super(WxQiyeSender, self).__init__(conf)

		self.weixin_url = 'https://qyapi.weixin.qq.com/cgi-bin' 
		self.qiye_flag = True

	def get_qiye_ids_by_task_user_id(self, task_user_id, now, logger):
		TASK_USER_QIYEID_MAPPING = {
			1: [ 'chutong' ],
		}

		if int(task_user_id) not in TASK_USER_QIYEID_MAPPING:
			logger.warning('task_user_id[%d] dont have related qiye weixin' % int(task_user_id))
			return self.admin_user_ids
		else:
			return self.admin_user_ids + [ TASK_USER_QIYEID_MAPPING[int(task_user_id)] ]

	def get_user_name_by_task_user_id(self, task_user_id, logger):
		TASK_USER_QIYEID_MAPPING = {
			1: 'user_name',
		}
		return TASK_USER_QIYEID_MAPPING[int(task_user_id)] if int(task_user_id) in TASK_USER_QIYEID_MAPPING else 'unknown'

	def send(self, agent_id, user_id, wx_message, now, logger):
		try:
			method = 'POST'
			node = 'message'
			operator = 'send'
			msgtype = 'text'
			path = '/'.join([self.weixin_url, node, operator])
			params = {
				"agentid": agent_id,
				"touser": user_id,
				"msgtype": msgtype,
				"text": {
					"content": wx_message,
				}
			}
			weixin_response = self._api.call(method, path, params)
			send_result = weixin_response.jsonify_body()
			logger.info('send message to user[%s] params[%s] response[%s]' % (str(user_id), str(params), str(send_result)))
		except Exception as e:
			logger.exception(e)


@app.task
def send_message(task_user_id, message_dict):
	wx_qiye_sender = WxQiyeSender(conf)
	wx_qiye_sender.init(logger)
	#wx_qiye_sender.admin_user_ids = ['chutong']

	now = time.localtime()
	agent_id = "1"

	user_qiye_ids = []
	try:
		user_qiye_ids = wx_qiye_sender.get_qiye_ids_by_task_user_id(int(task_user_id), now, logger)
		if not user_qiye_ids:
			logger.warning("task_user_id[%d] has no related qiye_users" % int(task_user_id))
		else:
			logger.info("task_user_id[%d] send message to qiye_users %s" % (int(task_user_id), str(user_qiye_ids)))

		user_name = wx_qiye_sender.get_user_name_by_task_user_id(task_user_id, logger)
		message_body = message_dict['body']
		object = message_dict['object']
		wx_message = ':'.join([user_name, object, message_body])
	except Exception as e:
		logger.exception(e)
	else:
		[ wx_qiye_sender.send(agent_id, user_qiye_id, wx_message, now, logger) for user_qiye_id in user_qiye_ids ]


if __name__ == '__main__':

	wx_qiye_sender = WxQiyeSender(conf)
	wx_qiye_sender.init(logger)

	now = time.localtime()
	agent_id = "1"

	# test
	user_qiye_id = "chutong"
	wx_message = u"test"
	wx_qiye_sender.send(agent_id, user_qiye_id, wx_message, now, logger)
