#!/usr/bin/env python

from meta_class import *

class DonationHistoryItem():
    def __init__(self, person, project_name, money_count, donation_time): 
        self.person = person
        self.project_name = project_name
        self.money_count = money_count
        self.donation_time = donation_time

    def get(self):
        return {
            "person": self.person,
            "project_name": self.project_name,
            "money_count": self.money_count,
            "donation_time": self.donation_time
        }

class ReceiveDonationHistoryItem():
    def __init__(self, project_name, contributor_name, contribute_time, contribute_money):
        self.project_name = project_name
        self.contributor_name = contributor_name
        self.contribute_time = contribute_time
        self.contribute_money = contribute_money

    def get(self):
        return {
            "project_name": self.project_name,
            "contributor_name": self.contributor_name,
            "contribute_time": self.contribute_time,
            "contribute_money": self.contribute_money
        }

class Friend():
    def __init__(self, friend_id, be_friend_time, nice_value):
        self.friend_id = friend_id
        self.be_friend_time = be_friend_time
        self.nice_value = nice_value
  
    def get(self):
        return {
            "friend_id": self.friend_id,
            "be_friend_time": self.be_friend_time,
            "nice_value": self.nice_value
        }

class Idol():
    def __init__(self, idol_id, focus_on_time, focus_on_degree):
        self.idol_id = idol_id
        self.focus_on_time = focus_on_time
        self.focus_on_degree = focus_on_degree

    def get(self):
        return {
            "idol_id": self.idol_id,
            "focus_on_time": self.focus_on_time,
            "focus_on_degree": self.focus_on_degree
        }
        

class UserMeta(MetaClass):
    def __init__(self, options = {}):
        # the id is generate by system.
        _options = {
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
            "registration_time": "",
            "metrics": {
                "donation_history": [],
                "receive_donation_history": [],
                "friends": [],
                "idol": []
            }
        }

        super(UserMeta, self).__init__(_options)

        self.check_element_required(options)
        if self.is_code_ok():
            self.merge(options)

    def get_required_element_list(self):
        required = [
            "username",
            "password",
            "telephone_number"
        ]
        return required
