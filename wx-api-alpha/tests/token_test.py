__author__ = 'linpingta@163.com'

import os, sys
basepath = os.path.abspath(os.path.dirname(sys.path[0]))
sys.path.append(basepath)
import unittest
import logging
import time

from weixin_api.token import WeixinToken 
from weixin_api.store import WeixinTokenStorage, WeixinTokenFileStorage


class WeixinTokenTest(unittest.TestCase):
    def setUp(self):
    	logging.basicConfig(filename=os.path.join(basepath, 'logs/test.log'), level=logging.DEBUG,
            format = '[%(filename)s:%(lineno)s - %(funcName)s %(asctime)s;%(levelname)s] %(message)s',
            datefmt = '%a, %d %b %Y %H:%M:%S'
        )
	self.logger = logging.getLogger('WeixinTokenTest')
	self.app_id = 'YOUR_APP_ID'
	self.app_secret = 'YOUR_APP_SECRET'

    def tearDown(self):
	pass

    def test_basic_storage(self):
	WeixinTokenStorage.init(self.logger)

	WeixinTokenStorage.load(self.logger)
	WeixinTokenStorage.store(self.logger)

	origin_app_to_token_dict = {1:{2:3, 4:5}}
	WeixinTokenStorage.set_app_to_token_dict(origin_app_to_token_dict)
	new_app_to_token_dict = WeixinTokenStorage.get_app_to_token_dict()
	self.assertEqual(origin_app_to_token_dict, new_app_to_token_dict)
	
    @unittest.skip('skip')
    def test_file_storage(self):
	token_filename = 'tests/token_info_for_file'
	WeixinTokenFileStorage.init(token_filename, self.logger)

	origin_app_to_token_dict = {1:{2:3, 4:5}}
	WeixinTokenFileStorage.set_app_to_token_dict(origin_app_to_token_dict)
	WeixinTokenFileStorage.store(self.logger)
	WeixinTokenFileStorage.load(self.logger)
	new_app_to_token_dict = WeixinTokenStorage.get_app_to_token_dict()

	self.assertEqual(origin_app_to_token_dict, new_app_to_token_dict)

    @unittest.skip('skip')
    def test_update_access_token(self):
	token_filename = 'tests/token_info_for_update'
	WeixinTokenFileStorage.init(token_filename, self.logger)

	WeixinToken.init(self.app_id, self.app_secret, WeixinTokenFileStorage)
	WeixinToken.update_access_token(self.logger)

    def test_get_access_token(self):
	token_filename = 'tests/token_info_for_get'
	WeixinTokenFileStorage.init(token_filename, self.logger)
	
	WeixinToken.init(self.app_id, self.app_secret, WeixinTokenFileStorage)
	new_access_token = WeixinToken.get_access_token(self.logger)

	origin_app_to_token_dict = WeixinTokenFileStorage.get_app_to_token_dict()
	if origin_app_to_token_dict:
	    origin_access_token = origin_app_to_token_dict[self.app_id]['access_token']
	    origin_expires_in = origin_app_to_token_dict[self.app_id]['expires_in']
	    origin_fetch_unix_time = origin_app_to_token_dict[self.app_id]['fetch_unix_time']

	    unix_now = int(time.mktime(time.localtime()))
	    if unix_now - origin_fetch_unix_time < origin_expires_in: 
	        self.assertEqual(new_access_token, origin_access_token)


if __name__ == '__main__':
    unittest.main()

