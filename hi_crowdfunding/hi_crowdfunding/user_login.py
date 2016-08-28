#!/usr/bin/env python

from meta_class import *

class UserLoginSession(MetaClass):
    def __init__(self, options = {}):
        # the id is generate by system.
        _options = {
            "id": "",
            "user_id": "",
            "username": "",
            "password": "",
            "last_login_time": 0,
            "session_expire_time": 24 * 3600
        }

        super(UserLoginSession, self).__init__(_options)
        self.check_element_required(options)
        if self.is_code_ok():
            self.merge(options)

    def get_required_element_list(self):
        required = [
            "username",
            "password"
        ]
        return required
