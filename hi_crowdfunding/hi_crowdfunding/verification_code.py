#!/usr/bin/env python

from meta_class import *

class VerificationCode(MetaClass):
    def __init__(self, options = {}):
        # the id is generate by system.
        _options = {
            "id": "",
            "telephone_number": "",
            "code": "",
            "last_modify_time": "",
            "valid_interval": 0
        }

        super(VerificationCode, self).__init__(_options)
        self.check_element_required(options)
        if self.is_code_ok():
            self.merge(options)

    def get_required_element_list(self):
        required = [
            "telephone_number"
        ]
        return required
