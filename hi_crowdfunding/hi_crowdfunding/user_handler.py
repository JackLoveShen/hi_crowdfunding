#!/usr/bin/env python

import json
from tornado import (ioloop, web)
from bson.objectid import ObjectId

from user_meta import UserMeta
from error_code_message import *
from util import *
from resource_handler import ResourceHandler

sLogger = get_logger()

class UserHandler(ResourceHandler):
    def get(self):
        resource_id = self.get_query_argument('id', '')
        if not resource_id:
            resource = self.db.list(self.database_name)
            self.set_status(200)
            response = {
                "code": 0,
                "message": "",
                "result": resource
            }
            self.write(json.dumps(response))
        else:
            resource = self.db.get(self.database_name, resource_id)
            if not resource:
                self.set_status(200)
                response = RESOURCE_NOT_FOUND
                self.write(json.dumps(response))
            else:
                self.set_status(200)
                response = {
                    "code": 0,
                    "message": "",
                    "result": resource
                }
                self.write(json.dumps(response))
