import time
#!/usr/bin/env python

from tornado import (ioloop, web)
from bson.objectid import ObjectId
import json
import time

from error_code_message import *
from user_login import UserLoginSession
from util import *


class UserLoginHandler(web.RequestHandler):
    def initialize(self, db, resource_type):
        self.db = db
        self.database_name = resource_type
        self.resource_type = resource_type

    def get_user_meta(self, username, password):
        collection_name = MONGO_DB_USER_NAME 
        query = {
            'username': username,
            'password': password
        }
        list_result = self.db.list(collection_name, query)
        
        sLogger.warn(u'query:{0}, list_result:{1}'.format(
            query, list_result)) 

        for user_meta in list_result:
            return user_meta
        else:
            return {}

    def get(self):
        '''
        we now only have one filter, which is username.
        In the future, we will have token, which can represent a login session.
        '''
        login_id = self.get_query_argument('id', '')

        sLogger.warn(u'login_id:{0}, database_name:{1}'.format(
            login_id, self.database_name))

        resource = self.db.get(self.database_name, login_id)
        
        sLogger.warn(u'login_id:{0}, resource:{1}'.format(login_id, resource))
        if not resource:
            response = RESOURCE_NOT_FOUND
            self.set_status(200)
            self.write(json.dumps(response))
        else:
            response = {
                "code": 0,
                "message": "",
                "result": resource
            }
            self.write(json.dumps(response))

    def post(self):
        options = parse_request_body(self.request.body_arguments)
        sLogger.warn(u'options:{0}'.format(options))
        if not isinstance(options, dict):
            self.set_status(201)
            self.write(json.dumps(INVALID_JSON_FORMAT))
            return

        login_session = UserLoginSession(options)
        if not login_session.is_code_ok():
            response = {
                "code": login_session.get_code(),
                "message": login_session.get_message(),
                "result": {
                }
            }
            self.set_status(200)
            self.write(json.dumps(response))
        else:
            username = login_session.getattr('username')
            password = login_session.getattr('password')
            user_meta = self.get_user_meta(username, password)

            sLogger.warn(u'username:{0}, password:{1}, user_meta:{2}'.format(
                username, password, user_meta))

            if not user_meta:
                self.set_status(200)
                self.write(json.dumps(INVALID_TOKEN))
                return

            # we will always create a new object.
            resource_id = generate_resource_id(self.database_name)
            options = {
                'id': resource_id,
                'user_id': user_meta.get('id', ''),
                'username': username,
                'password': password,
                'last_login_time': int(time.time())
            }

            user_login_session = UserLoginSession(options)
            internal_id = self.db.insert(self.database_name, user_login_session.to_dict())
            sLogger.warn(u'options:{0}, internal_id:{1}'.format(
                user_login_session, internal_id))

            response = {
                "code": 0,
                "message": "",
                "result": {
                    "id": resource_id
                }
            }
            self.set_status(201)
            self.write(json.dumps(response))
