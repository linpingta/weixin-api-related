from api import WeixinApi, WeixinResponse
from store import WeixinDbStorage, WeixinMySQLDbStorage


WEIXIN_URL = 'https://api.weixin.qq.com/cgi-bin'


class WeixinObject(object):
    ''' Base Weixin Object
    '''
    def __init__(self, api, node='', operator=''):
	self.api = api
	self.node = node
	self.operator = operator

    def _get_path(self):
	return '/'.join([WEIXIN_URL, self.node, self.operator])


class WeixinUser(WeixinObject):
    ''' User
    '''
    def __init__(self, api, open_id='', node='user', operator='info'):
	super(WeixinUser, self).__init__(api, node, operator)

	self.open_id = open_id
	self.nickname = ''
	self.sex = 0
	self.open_id = ''
	self.language = ''

    def get_info_from_wx(self, open_id, logger):
	try:
	    print open_id
	    self.open_id = open_id
	    method = 'GET'
	    path = self._get_path()
	    params = {
		"openid": open_id,
	    }

	    weixin_response = self.api.call(method, path, params)
	    print weixin_response.body()
	except Exception as e:
	    logger.exception(e)


class WeixinUserGroup(WeixinObject):
    ''' User Group
    '''
    def __init__(self, api, node='user', operator='get'):
	super(WeixinUserGroup, self).__init__(api, node, operator)
	self.wx_users = []

    def _wrap_wx_user(self, user_open_id, logger):
	wx_user = WeixinUser(self.api, user_open_id)
	wx_user.get_info_from_wx(user_open_id, logger)
	return wx_user

    def _wrap_db_user(self, user, logger):
	return user

    def get_users(self, logger, force_from_wx=False, storage=None):
	''' get users of platform
	as call limit exists, only force_from_wx=True will lead to call in wx server
	otherwise use local info
	'''
	if force_from_wx:
	    method = 'GET'
	    path = self._get_path()
	    params = {}
	    weixin_response = self.api.call(method, path, params)
    	    user_group = weixin_response.jsonify_body()
    	    user_open_ids = user_group['data']['openid']
	    [ self.wx_users.append(self._wrap_wx_user(user_open_id, logger)) for user_open_id in user_open_ids ]
	else:
	    db_users = storage.get_users(logger)
	    [ self.wx_users.append(self._wrap_db_user(db_user)) for db_user in db_users ]
	return self.wx_users
	    
	    
	    



