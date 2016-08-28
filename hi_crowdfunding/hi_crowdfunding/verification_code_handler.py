#!/usr/bin/env python

from tornado import (ioloop, web)
from bson.objectid import ObjectId
import json

from error_code_message import *
from verification_code import VerificationCode
from util import *

class VerificationCodeHandler(web.RequestHandler):
    def initialize(self, db, resource_type):
        self.db = db
        self.database_name = resource_type
    
    def get(self):
        resource_id = self.get_query_argument('id', '')
        telephone_number = ''

        if not resource_id:
            telephone_number = self.get_query_argument('telephone_number', '')
            if not telephone_number:
                response = RESOURCE_NOT_FOUND
                self.write(json.dumps(response))
                return
        query = {'id': resource_id}
        if telephone_number:
            query = {'telephone_number': telephone_number}

        resource = self.db.get_one_customized(self.database_name, query)
        if not resource:
            response = RESOURCE_NOT_FOUND
            self.write(json.dumps(response))
         
        else:
            if 'code' in resource:
                resource['code'] = '1111'
            self.set_status(200)
            response = {
                "code": 0,
                "message": "",
                "result": resource
            }
            self.write(json.dumps(response))

    def put(self):
        options = parse_request_body(self.request.body_arguments)
        if not isinstance(options, dict):
            self.set_status(200)
            self.write(json.dumps(INVALID_JSON_FORMAT))
            return

        v_code = VerificationCode(options)
        if not v_code.is_code_ok():
            self.set_status(200)
            response = {
                "code": login_session.get_code(),
                "message": login_session.get_message(),
                "result": {
                }
            }
            self.write(json.dumps(response))
            return

        telephone_number = v_code.getattr('telephone_number')
        query = {
            'telephone_number': telephone_number
        }

        resource = self.db.list(self.database_name, query)
        if not resource:
            resource_id = generate_resource_id(self.database_name)
            v_code.setattr('id', resource_id)
            internal_id = self.db.insert(self.database_name, v_code.to_dict())

            sLogger.warn(u'internal_id:{0}, resource_id:{1},  v_code:{2}'.format(
               internal_id, resource_id, v_code))
        else:
            resource = resource[0]
            resource_id = resource.get('id', '')

        response = {
            "code": 0,
            "message": "",
            "result": {
                "id": resource_id
            }
        }
        self.set_status(201)
        self.write(json.dumps(response))
