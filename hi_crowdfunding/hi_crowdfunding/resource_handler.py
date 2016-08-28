#!/usr/bin/env python

import json
import tornado
from tornado import (ioloop, web, gen)
from bson.objectid import ObjectId

from user_meta import UserMeta
from crowdfunding_project import CrowdfundingProject
from community_project import CommunityProject
from user_statistics import UserStatistics
from error_code_message import *
from util import *
from config import *

sLogger = get_logger()

RESOURCE_TYPE_TO_CLASS = {
    'users': UserMeta,
    'crowdfunding': CrowdfundingProject,
    'community': CommunityProject,
    'user_statistics': UserStatistics
}

class ResourceHandler(web.RequestHandler):
    def initialize(self, db, resource_type):
        self.db = db
        self.database_name = resource_type
        self.resource_type = resource_type

    def generate_picture_access(self, path): 
        return '/api/v1/picture/?id={0}'.format(path) 

    def get_db(self):
        return self.db

    def get_default_picture_dir(self):
        return 'picture'

    def get_database_name(self):
        return self.database_name

    def validate_token(self, token):
        login_session = self.db.get(MONGO_DB_USER_LOGIN_NAME, token)
        sLogger.warn(u'token:{0}, login_session:{1}'.format(token, login_session))

        if not login_session:
            return False

        user_id = login_session.get('user_id', '')
        last_login_time = login_session.get('last_login_time', 0)

        query = {
            'user_id': user_id
        }

        history_login = self.get_many(MONGO_DB_USER_LOGIN_NAME, query = query)

        sLogger.warn(u'history_login:{0}'.format(history_login))

        if not history_login:
            return False

        for login in history_login:
            login_time = login.get('last_login_time', 0)
            if login_time > last_login_time:
                return False

        return True

    def class_type(self):
        return RESOURCE_TYPE_TO_CLASS[self.resource_type]

    def get(self):
        resource_id = self.get_query_argument('id', '')
        if not resource_id:
            resource = self.db.list(self.database_name)

            sLogger.warn(u'list, database_name:{0}, resource:{1}'.format(
                self.database_name, resource))

            self.set_status(200)
            response = {
                "code": 0,
                "message": "",
                "result": resource
            }
            self.write(json.dumps(response))
        else:
            resource = self.db.get(self.database_name, resource_id)
            sLogger.warn(u'database_name:{0}, resource_id:{1}'.format(
                self.database_name, resource_id))

            if not resource:
                response = RESOURCE_NOT_FOUND
                self.set_status(200)
                self.write(json.dumps(response))
            else:
                self.set_status(200)
                response = {
                    "code": 0,
                    "message": "",
                    "result": resource
                }
                self.write(json.dumps(response))

    def post(self):
        options = parse_request_body(self.request.body_arguments)
        if not isinstance(options, dict):
            self.set_status(201)
            self.write(json.dumps(INVALID_JSON_FORMAT))
            return

        user_meta = self.class_type()(options)
        if not user_meta.is_code_ok():
            self.set_status(200)
            response = {
                "code": user_meta.get_code(),
                "message": user_meta.get_message(),
                "result": {
                }
            }
            self.write(json.dumps(response))
            return

        resource_id = generate_resource_id(self.database_name)

        if user_meta.is_valid():
            user_meta.setattr('id', resource_id)
            internal_id = str(self.db.insert(self.database_name, user_meta.to_dict()))
            sLogger.warn(u'id:{0}, internal_id:{1}, user_meta:{2}'.format(
                resource_id, internal_id, user_meta))

        response = {
            "code": 0,
            "message": "",
            "result": {
                "id": resource_id
            }
        }
        self.set_status(201)
        self.write(json.dumps(response))

    def put(self):
        resource_id = self.get_query_argument('id', '')
        resource = self.db.get(self.database_name, resource_id)

        sLogger.warn(u'resource_id:{0}, resource:{1}, database_name:{2}'.format(
            resource_id, resource, self.database_name))

        if not resource:
            response = RESOURCE_NOT_FOUND
            self.set_status(200)
            self.write(json.dumps(response))
            return 
        else:
            options = self.request.body_arguments
            sLogger.warn(u'options:{0}'.format(options))
            if not isinstance(options, dict):
                self.set_status(200)
                self.write(json.dumps(INVALID_JSON_FORMAT))
                return 

            user_meta = self.class_type()(resource)
            user_meta.merge(options)

            self.db.put(self.database_name, resource_id, options)
            response = {
                "code": 0,
                "message": "",
                "result": {
                    "id": resource_id
                }
            }
        self.set_status(200)
        self.write(json.dumps(response))

    def delete(self):
        resource_id = self.get_query_argument('id', '')

        sLogger.warn(u'database_name:{0}, resource_id:{1}'.format( 
            self.database_name, resource_id))

        delete_result = self.db.delete(self.database_name, resource_id)

        sLogger.warn(u'resource_id:{0}, delete_result:{1}'.format(
            resource_id, delete_result))

        response = {}
        response['code'] = 0
        response['message'] = ''
        response['result'] = {
            'id': resource_id
        }
            
        self.set_status(200)
        self.write(json.dumps(response))
