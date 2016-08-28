#!/usr/bin/env python

from tornado import (ioloop, web)
from bson.objectid import ObjectId

import user_login import UserLoginSession

class UserLoginHandler(web.RequestHandler):
    def initialize(self, db, resource_type):
        self.db = db
        self.database_name = resource_type
        
    def post(self):
        pass
