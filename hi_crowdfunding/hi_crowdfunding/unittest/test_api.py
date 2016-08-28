#!/usr/bin/env python

import httplib
import urllib
import json
from bson.objectid import ObjectId

class ResourceClient():
    def __init__(self, host = '139.224.29.217', port = 8888, resource_type = 'users'):
        self.conn = httplib.HTTPConnection(host, port)
        self.default_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
            'Connection': 'keep-alive'
        }
        self.resource_type = resource_type

    def test_get(self, user_id):
        #self.conn.request('GET', url = '/api/v1/{0}/?id={1}'.format(self.resource_type, user_id))
        self.conn.request('GET', url = '/api/v1/user_login_session/?username=xxxx')
        return self.conn.getresponse().read()

    def test_create(self, data):
        body = urllib.quote(json.dumps(data))
        #body = 'age=18&city=chengshi&crowdfunding_number=zhongchou&head_portrait=touxiang&id=uid&job=zhiye&password=111111&provinces=shengfen&registration_time=zhuceshijian&telephone_number=18501360496&username=liupeng'
        self.conn.debuglevel = 100
        self.conn.request('POST', url = '/api/v1/{0}/'.format(self.resource_type), headers = self.default_headers, body = body)
        data = self.conn.getresponse().read()
        print data
        res = json.loads(data)
        return res['result']['id']

    def test_put(self, user_id, body):
        body = urllib.quote(json.dumps(body))
        self.conn.request('PUT', url = '/api/v1/{0}/?id={1}'.format(self.resource_type, user_id), headers = self.default_headers, body = body)
        return self.conn.getresponse().read()
    
    def test_put_without_id(self, body):
        body = urllib.quote(json.dumps(body))
        self.conn.debuglevel = 100
        self.conn.request('PUT', url = '/api/v1/{0}/'.format(self.resource_type), headers = self.default_headers, body = body)
        data = self.conn.getresponse().read()
        res = json.loads(data)
        return res['result']['id']


if __name__ == '__main__':
    client = ResourceClient(resource_type = 'user_login_session')
    data = {
        "username": "xxxx",
        "password": "xxxx"
    }
    session_id = client.test_create(data)
    print session_id
    print client.test_get(session_id)

    client = ResourceClient(resource_type = 'verification_code')

    data = {
        "telephone_number": "01234567891"
    }
    user_id = client.test_put_without_id(data)
    print user_id
    print client.test_get(user_id)
    # test user resource.
    client = ResourceClient(resource_type = 'users')
    data = {
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
    client = ResourceClient(resource_type = 'users')
    client.test_get('')


    user_id = client.test_create(data)
    print user_id
    
    print client.test_get(user_id)
    print 'put___', client.test_put(user_id, {'username': 'zyf'})
    print client.test_get(user_id)


    # test user_statistics
    client = ResourceClient(resource_type = 'user_statistics')
    data = {
        "username": "",
        "last_login_time": "",
        "login_infomation": [
            {
                "login_time": "",
                "logout_time": "",
                "login_addr": ""
            }
        ],
        "donation_history": [
            {
                "person": "",
                "project_name": "",
                "money": 0,
                "donation_time": ""
            }
        ],
        "receive_donation_history": [
            {
                "project_name": "",
                "contributor_name": "",
                "contribute_time": "",
                "contribute_money": 0
            }
        ],
        "friends": [
            {
                "friend_name": "",
                "be_friend_time": "",
                "nice_value": 0
            }
        ],
        "idol": [
            {
                "idol_name": "",
                "focus_on_time": "",
                "focus_on_degree": 0
            }
        ]
    }

    user_id = client.test_create(data)
    print user_id
    print client.test_get(user_id)
    print 'put___', client.test_put(user_id, {'username': 'zyf'})
    print client.test_get(user_id)
    
    data = {
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

    user_id = client.test_create(data)
    print user_id
    print client.test_get(user_id)
    print 'put___', client.test_put(user_id, {'project_name': 'hahahaha'})
    print client.test_get(user_id)

    data = {
        "article_name": "",
        "publish_time": "",
        "publish_person": "",
        "publish_terminal": "",
        "publish_content": "",
        "pictures": [
            {
                "picture_name": {}
            }
        ],
        "all_comments": [
            {
                "comment_person": {
                    "comment_time": "",
                    "at": False,
                    "at_person_name": "",
                    "content": "",
                    "is_read": False
                }
            }
        ],
        "is_placed_at_the_top": False,
        "placed_at_top_time": ""
    }
    

    user_id = client.test_create(data)
    print user_id
    print client.test_get(user_id)
    print 'put___', client.test_put(user_id, {'username': 'hahahaha'})
    print client.test_get(user_id)
