#!/usr/bin/env python

from meta_class import *

class CommunityProject(MetaClass):
    def __init__(self, options = {}):
        _options = {
            "id": "",
            "user_id": "",
            "article_name": "",
            "publish_time": "",
            "publish_person": "",
            "publish_terminal": "",
            "publish_content": "",
            "pictures": [
                {
                    "picture_name": {}
                }
            ],
            "all_comments": [
                {
                    "comment_person": {
                        "comment_time": "",
                        "at": False,
                        "at_person_name": "",
                        "content": "",
                        "is_read": False
                    }
                }
            ],
            "is_placed_at_the_top": False,
            "placed_at_top_time": ""
        }

        super(CommunityProject, self).__init__(_options)
        self.merge(options)
