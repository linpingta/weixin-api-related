__author__ = 'linpingta@163.com'

import os, sys
basepath = os.path.abspath(os.path.dirname(sys.path[0]))
sys.path.append(basepath)
import unittest
import logging
import time

from weixin_api.api import WeixinApi
from weixin_api.token import WeixinToken 
from weixin_api.store import WeixinTokenStorage, WeixinTokenFileStorage
from weixin_api.objects import WeixinUser, WeixinUserGroup


class WeixinObjectTest(unittest.TestCase):
    def setUp(self):
    	logging.basicConfig(filename=os.path.join(basepath, 'logs/test.log'), level=logging.DEBUG,
            format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
            datefmt = '%a, %d %b %Y %H:%M:%S'
        )
	self.logger = logging.getLogger('WeixinUserTest')
	logger = self.logger

	app_id = 'YOUR_APP_ID'
	app_secret = 'YOUR_APP_SECRET'

    	token_filename = 'tests/token_info'
    	WeixinTokenFileStorage.init(token_filename, logger)
    	WeixinToken.init(app_id, app_secret, WeixinTokenFileStorage)

    	access_token = WeixinToken.get_access_token(logger)
    	WeixinApi.init(app_id, app_secret, access_token)
    	self.api = WeixinApi.get_weixin_api()

    def tearDown(self):
	pass


class WeixinUserTest(WeixinObjectTest):
    def setUp(self):
	super(WeixinUserTest, self).setUp()

    def test_get_user_info(self):
	test_open_id = "o37kwuH3w6mUNTfHXyypmEdM5jLU"
	user = WeixinUser(self.api, test_open_id)
	user.get_info_from_wx(test_open_id, self.logger)

class WeixinUserGroupTest(WeixinObjectTest):
    def setUp(self):
	super(WeixinUserGroupTest, self).setUp()

    @unittest.skip('skip')
    def test_get_users(self):
	user_group = WeixinUserGroup(self.api)
	wx_users = user_group.get_users(self.logger, True)


if __name__ == '__main__':
    unittest.main()

