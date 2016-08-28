#!/usr/bin/env python

from meta_class import *

class CrowdfundingProject(MetaClass):
    def __init__(self, options = {}):
        _options = {
            "id": "",
            "user_id": "",
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
        super(CrowdfundingProject, self).__init__(_options)
        self.check_element_required(options)
        if self.is_code_ok():
            self.merge(options)

    def get_required_element_list(self):
        required = [
            "project_name",
            "project_type",
            "publish_terminal",
            "publish_content",
            "expected_raise_money"
        ]
        return required
