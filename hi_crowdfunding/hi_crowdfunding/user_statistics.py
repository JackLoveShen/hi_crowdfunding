#!/usr/bin/env python

from meta_class import *

class UserStatistics(MetaClass):
    def __init__(self, options = {}):
        _options = {
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
        super(UserStatistics, self).__init__(_options)
        self.merge(options)
