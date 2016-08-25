#-*- coding: utf-8 -*-
# vim: set bg=dark noet sw=4 ts=4 fdm=indent :

import os, sys
import time
import logging
import ConfigParser
import simplejson as json
from celery import Celery

from weixin_api.store import WeixinTokenFileStorage
from weixin_api.token import WeixinToken
from weixin_api.api import WeixinApi, WeixinResponse


confpath = os.path.join(basepath, 'conf/wx.conf')
conf = ConfigParser.RawConfigParser()
conf.read(confpath)

logging.basicConfig(filename=os.path.join(basepath, 'logs/wx.log'), level=logging.DEBUG,
	format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
	datefmt = '%a, %d %b %Y %H:%M:%S'
	)
logger = logging.getLogger('WxManager')

host = 'redis://HOST' # i.e redis://10.0.0.0
port = 'PORT' # i.e 1234
app = Celery('task_info', broker=host+':'+port)


class WxBasicSender(object):
	''' Responsible for WX API call
	'''
	def __init__(self):
		self.api = None

	def init(self, logger):
		WeixinTokenFileStorage.init(self.token_file, logger)
		WeixinToken.init(self.app_id, self.app_secret, WeixinTokenFileStorage, self.weixin_url, self.qiye_flag, self.token_node)
		access_token = WeixinToken.get_access_token(logger)
		WeixinApi.init(self.app_id, self.app_secret, access_token)

		self.api = WeixinApi.get_weixin_api()


class WxQiyeSender(WxBasicSender):
	''' Responsible for WX Qiye API call
	'''
	def __init__(self, conf):
		super(WxQiyeSender, self).__init__()

		self.token_file = conf.get('wx_qiye_sender', 'token_file')
		self.app_id = conf.get('wx_qiye_sender', 'app_id')
		self.app_secret = conf.get('wx_qiye_sender', 'app_secret')
		self.qiye_flag = True
		self.token_node = 'gettoken'
		self.weixin_url = 'https://qyapi.weixin.qq.com/cgi-bin' 

	def get_qiye_ids_by_task_user_id(self, task_user_id, now, logger):
		TASK_USER_QIYEID_MAPPING = {
			1234: 'weixin_name',
		}

		if int(task_user_id) not in TASK_USER_QIYEID_MAPPING:
		    return [ "your_admin_id" ]
		else:
			return [ "your_admin_id", TASK_USER_QIYEID_MAPPING[int(task_user_id)] ]

	def get_user_name_by_task_user_id(self, task_user_id, logger):
		TASK_USER_QIYEID_MAPPING = {
			1234: 'user_name',
		}
		return TASK_USER_QIYEID_MAPPING[task_user_id] if task_user_id in TASK_USER_QIYEID_MAPPING else 'unknown'

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
			weixin_response = self.api.call(method, path, params)
			send_result = weixin_response.jsonify_body()
			logger.info('send message to user[%s] params[%s] response[%s]' % (str(user_id), str(params), str(send_result)))
		except Exception as e:
			logger.exception(e)


@app.task
def send_message(task_user_id, message_dict):
	wx_qiye_sender = WxQiyeSender(conf)
	wx_qiye_sender.init(logger)

	now = time.localtime()
	agent_id = "1"
	user_qiye_ids = wx_qiye_sender.get_qiye_ids_by_task_user_id(task_user_id, now, logger)
	try:
		user_name = wx_qiye_sender.get_user_name_by_task_user_id(task_user_id, logger)
		message_body = message_dict['body']
		object = message_dict['object']
		wx_message = ':'.join([user_name, object, message_body])
	except Exception as e:
		logger.exception(e)
	else:
		[ wx_qiye_sender.send(agent_id, user_qiye_id, wx_message, now, logger) for user_qiye_id in user_qiye_ids ]
