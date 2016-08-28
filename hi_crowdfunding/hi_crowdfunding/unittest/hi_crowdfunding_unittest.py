#!/usr/bin/env python

import urllib
import httplib
import json
import time

import sys
sys.path.append('../')
sys.path.append('./')
from util import *
from bson.objectid import ObjectId

import unittest
from config import *
from mongodb_client import db_client

sLogger = get_logger('unittest')

G_USERNAME = '123456'
G_PASSWORD = '123456'

class LoginUtil():
    def __init__(self):
        self.conn = httplib.HTTPConnection('139.224.29.217', 8888)
        self.conn.debuglevel = 10
        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        username = G_USERNAME
        password = G_PASSWORD
        
        self.user_body = {
            "username": username,
            "telephone_number": "",
            "password": password,
            "crowdfunding_number": "",
            "provinces": "",
            "city": "",
            "age": 0,
            "job": "",
            "head_portrait": "",
            "registration_time": ""
        }

        self.login_body = {
            "username": username,
            "password": password
        }

    def get_id(self, url, body):
        sLogger.warn(u'url:{0}, body:{1}'.format(url, body))

        self.conn.request('POST', url = url, headers = self.default_headers, body = json.dumps(body))
        data = self.conn.getresponse().read()

        sLogger.warn(u'url:{0}, data:{1}'.format(url, data))
        res = json.loads(data)
        return res.get('result', {}).get('id', '')
    
    def create_user(self):
        return self.get_id('/api/v1/users/', self.user_body)

    def create_login(self):
        return self.get_id('/api/v1/user_login_session/', self.login_body)

    def create_user_and_login(self):
        user_id = self.get_id('/api/v1/users/', self.user_body)
        if user_id:
            return self.get_id('/api/v1/user_login_session/', self.login_body)
        return ''

class UserLoginUnittest(unittest.TestCase):
    def setUp(self):
        self.conn = httplib.HTTPConnection('139.224.29.217', 8888)
        self.conn.debuglevel = 10
        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        self.util = LoginUtil()
        user_id = self.util.create_user()
        sLogger.warn(u'user_id:{0}'.format(user_id))

        self.url = '/api/v1/user_login_session/'
        self.default_body = {
            "id": "",
            "username": G_USERNAME,
            "password": G_PASSWORD,
            "last_login_time": "",
            "session_expire_time": 3600
        }

    def tearDown(self):
        pass

    def to_json(self, string):
        try:
            detail = json.loads(string)
        except Exception, e:
            print 'Exception, ', str(e)
            self.assertTrue(False, 'The response is not a json format, what the detail is:{0}'.format(string))
       
        return detail

    def create_user_login(self):
        body = self.default_body
        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()

        sLogger.warn(u'url:{0}, response:{1}'.format(self.url, response))
        detail = self.to_json(response)

        self.assertEqual(0, detail['code'])
        return detail.get('result', {}).get('id', '')

    def test_get(self):
        login_session_id = self.create_user_login()
        tmp_login_session_id = self.create_user_login()
        
        sLogger.warn(u'login_session_id:{0}, tmp_login_session_id:{1}'.format(login_session_id, tmp_login_session_id))

        self.assertTrue(login_session_id != tmp_login_session_id)
        sLogger.warn(u'login_session_id:{0}'.format(login_session_id))

        url = '{0}?id={1}'.format(self.url, login_session_id)
        self.conn.request('GET', url = url, headers = self.default_headers)

        response = self.conn.getresponse().read()
        detail = self.to_json(response)

        sLogger.warn(u'url:{0}, response:{1}'.format(url, response))

        self.assertEqual(0, detail['code'])

        result = detail['result']
        sLogger.warn(u'result:{0}'.format(result)) 

        self.assertEqual(login_session_id, result['id'])
 
    def test_post(self):
        body = {
            "username": "",
        }

        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        self.assertEqual(detail['code'], 400)

class CrowdfundingUnittest(unittest.TestCase):
    def setUp(self):
        self.conn = httplib.HTTPConnection('139.224.29.217', 8888)
        self.conn.debuglevel = 10

        login_util = LoginUtil() 
        login_id = login_util.create_user_and_login()
        sLogger.warn(u'login_id:{0}'.format(login_id))

        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            REQUEST_TOKEN_KEY: login_id 
        }
        self.url = '/api/v1/crowdfunding/'
        self.body = {
            "project_name": "",
            "project_type": "",
            "publish_person": "",
            "publish_time": "",
            "publish_terminal": "",
            "publish_content": "",
            "pictures": [
                {
                    "picture_name": {}
                }
            ],
            "expected_raise_money": 0,
            "total_raise_money": 0,
            "contributors": [
                { 
                    "contributor_name": {
                        "contribute_time": "",
                        "last_contribute_time": "",
                        "contribute_money": 0,
                        "contribute_time": 0
                    }
                }
            ],
            "thumb_up_people": [
                {
                    "name": {
                        "thumb_up_time": "",
                    }
                }
            ],
            "is_placed_at_the_top": False,
            "placed_at_top_time": ""
        }
    
    def tearDown(self):
        pass

    def to_json(self, string):
        try:
            detail = json.loads(string)
        except Exception, e:
            sLogger.exception('string:{0}, exception:{1}'.format(string, str(e)))
            self.assertTrue(False, 'The response is not a json format, what the detail is:{0}'.format(string))
       
        return detail

    def create(self):
        body = self.body
        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        detail = self.to_json(response)

        self.assertEqual(detail['code'], 0)
        return detail['result']['id'] 

    def test_post(self):
        # test the telephone_number is not exists.
        body = self.body
        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        sLogger.warn('detail:{0}'.format(detail))
        self.assertEqual(detail['code'], 0)

    def test_get(self):
        c_id = self.create()
        self.conn.request('GET', url = '{0}?id={1}'.format(self.url, c_id), headers = self.default_headers)

        response = self.conn.getresponse().read()
        detail = self.to_json(response)

        sLogger.warn('detail:{0}'.format(detail))
       
        self.assertEqual(0, detail['code'])

class UserResourceUnittest(unittest.TestCase):
    def setUp(self):
        self.db = db_client
        self.conn = httplib.HTTPConnection('139.224.29.217', 8888)
        self.conn.debuglevel = 10
        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.url = '/api/v1/users/'
        self.user_body = {
            "id": "",
            "username": "",
            "telephone_number": "",
            "password": "",
            "crowdfunding_number": "",
            "provinces": "",
            "city": "",
            "age": 0,
            "job": "",
            "head_portrait": "",
            "registration_time": ""
        }
       
        # clear
        self.clear()

    def clear(self):
        user_collection_name = MONGO_DB_USER_NAME
        while True:
            delete_result = db_client.find_and_remove(user_collection_name)
            if not delete_result:
                break

    def tearDown(self):
        self.clear()

    def to_json(self, string):
        try:
            detail = json.loads(string)
        except Exception, e:
            sLogger.exception(u'string:{0}, exception:{1}'.format(string, str(e)))
            self.assertTrue(False, 'The response is not a json format, what the detail is:{0}'.format(string))
       
        return detail

    def create_user(self):
        # a normal case
        body = self.user_body
        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        
        try:
            detail = json.loads(response)
            self.assertTrue(detail['code'] == 0)
            user_id = detail['result']['id']
        except Exception, e:
            print str(e)
            self.assertTrue(False, 'The response is not a json format, what the detail is:{0}'.format(response))

        self.assertTrue(len(user_id))
        return user_id

    def test_post(self):
        # test the telephone_number is not exists.
        body = {
            "username": "",
            "password": ""
        }
        self.conn.request('POST', url = self.url, headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        self.assertEqual(detail['code'], 400)

    def test_delete(self):
        user_list = []
        for i in range(10):
            user_list.append(self.create_user())

        self.conn.request('GET', url = self.url, headers = self.default_headers) 
        response = self.conn.getresponse().read()

        detail = self.to_json(response)
        sLogger.warn(u'xxxx, detail:{0}'.format(detail))

        self.assertEqual(0, detail['code'])
        result = detail['result']
        exists_user_list = [user['id'] for user in result]

        sLogger.warn(u'exists_user_list:{0}'.format(exists_user_list))

        for user_id in user_list:
            if not user_id in exists_user_list:
                self.assertTrue(False)
        # test delete all
        for user_id in exists_user_list:
            if not user_id:
                continue
            self.conn.request('DELETE', url = '{0}?id={1}'.format(self.url, user_id), headers = self.default_headers)
            response = self.conn.getresponse().read()
            detail = self.to_json(response)
            self.assertEqual(0, detail['code'])

        self.conn.request('GET', url = self.url, headers = self.default_headers) 
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        self.assertEqual(0, detail['code'])
        result = detail['result']
        exists_user_list = [user['id'] for user in result if user['id']]
        self.assertEqual([], exists_user_list)

    def test_get(self):
        user_id = self.create_user()
        self.conn.request('GET', url = '{0}?id={1}'.format(self.url, user_id), headers = self.default_headers)  
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        self.assertEqual(0, detail['code'])

    def test_put(self):
        user_id = self.create_user()
        body = {'username': 'zyf'}
        self.conn.request('PUT', url = '{0}?id={1}'.format(self.url, user_id), headers = self.default_headers, body = json.dumps(body))
        response = self.conn.getresponse().read()
        detail = self.to_json(response)

        self.assertEqual(0, detail['code'])
        self.assertEqual(user_id, detail['result']['id'])
         
        self.conn.request('GET', url = '{0}?id={1}'.format(self.url, user_id), headers = self.default_headers)  
        response = self.conn.getresponse().read()
        detail = self.to_json(response)
        result = detail['result']
    
        self.assertEqual('zyf', result['username'])

    def test_put(self):
        user_id = self.create_user()
        body = {'username': 'zyf'}
        self.conn.request('PUT', url = '{0}?id={1}'.format(self.url, user_id), headers = self.default_headers, body = json.dumps(body))
    
if __name__ == '__main__':
    unittest.main()
