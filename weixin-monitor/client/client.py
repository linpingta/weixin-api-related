#!/usr/bin/env python
#-*- coding: utf-8 -*-
# vim: set bg=dark noet sw=4 ts=4 fdm=indent : 

''' Task Monitor Client '''
__author__='linpingta@163.com'

import os,sys
import logging
import ConfigParser
from celery import Celery
import celeryconfig


class WxClient(object):
    def __init__(self):
        self.celery_client = None

    def init(self, conf, logger):
        try:
            celery = Celery()
            celery.config_from_object(celeryconfig)
            self.celery_client = celery
        except Exception as e:
            logger.exception(e)

    def release(self, logger):
        try:
			pass
        except Exception as e:
            logger.exception(e)

	def send_your_message(self, id, message, logger, type=1):
		try:
			# wrap object from id, related with business
			# task_user_id is who receive monitor, id is business id
			object = 'id[%d]' % id
			task_user_id = id
            elem_dict = {    
				'object':object,
                'type':type,
                'body':message,
            }
            logger.info('id[%d] send message %s' % (id, message))
            self.celery_client.send_task('wx_task_manager.send_message', [task_user_id, elem_dict])
		except Exception as e:
			logger.exception(e)


if __name__ == '__main__':

    basepath = os.getcwd()
    confpath = os.path.join(basepath, 'conf/wx_client.conf')
    conf = ConfigParser.RawConfigParser()
    conf.read(confpath)

    logging.basicConfig(filename=os.path.join(basepath, 'logs/wx_client.log'), level=logging.DEBUG,
        format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
        datefmt = '%a, %d %b %Y %H:%M:%S'
        )
    logger = logging.getLogger('WxClient')

    try:
        wx_client = WxClient()
        wx_client.init(conf, logger)

        # real use
        wx_client.send_your_message(1, u'中文', logger)    

        wx_client.release(logger)
    except Exception,e:
        logging.exception(e)

