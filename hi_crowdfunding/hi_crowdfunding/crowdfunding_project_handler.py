#!/usr/bin/env python

import time
import os

from resource_handler import *
from util import *
from config import *

sLogger = get_logger()

class CrowdfundingProjectHandler(ResourceHandler):
    def generate_picture_name(self, token, image_name):
        return 'crowdfunding_{0}_{1}_{2}'.format(token, time.time(), image_name)

    def restore_image(self, images, token):

        sLogger.warn('restore_image, image_names:{0}'.format(images.keys()))

        file_list = []
        for (image_name, image_content) in images.items():
            if len(image_content):
                obj = {}
                try:
                    real_filename = self.generate_picture_name(token, image_name)
                    obj['name'] = image_name
                    obj['access'] = self.generate_picture_access(real_filename)
                    file_list.append(obj)

                    filename = os.path.join(self.get_default_picture_dir(), real_filename)

                    content = image_content[0]['body']
                    with open(filename, 'wb+') as f:
                        f.write(content)
                except Exception, e:
                    sLogger.exception(str(e))

        # sorted it
        file_list = sorted(file_list, cmp = lambda x, y: cmp(x['name'], y['name']))
        return file_list

    def post(self):
        # we will check token
        sLogger.warn(u'request:{0}'.format(self.request))
        sLogger.warn('headers:{0}, body_arguments:{1}'.format(self.request.headers, self.request.body_arguments))

        # check token, only valid token can post project.
        token = self.request.headers.get(REQUEST_TOKEN_KEY, '')

        '''
        if not self.validate_token(token):
            self.set_status(200)
            self.write(json.dumps(INVALID_TOKEN))
            return
        '''

        options = parse_request_body(self.request.body_arguments)
        if not isinstance(options, dict):
            self.set_status(201)
            self.write(json.dumps(INVALID_JSON_FORMAT))
            return

        sLogger.warn(u'class_type:{0}'.format(self.class_type())) 

        crowdfunding_project = self.class_type()(options)
        if not crowdfunding_project.is_code_ok():
            self.set_status(200)
            response = {
                "code": crowdfunding_project.get_code(),
                "message": crowdfunding_project.get_message(),
                "result": {
                }
            }
            self.write(json.dumps(response))
            return

        resource_id = generate_resource_id(self.database_name)
        images = self.request.files 
        file_list = self.restore_image(images, token)

        sLogger.warn(u'resource_id:{0}, file_list:{1}'.format(
            resource_id, file_list))

        crowdfunding_project.setattr('id', resource_id)
        crowdfunding_project.setattr('pictures', file_list)

        internal_id = str(self.db.insert(self.database_name, crowdfunding_project.to_dict()))

        sLogger.warn(u'resource_id:{0}, internal_id:{1}'.format(resource_id, internal_id))

        response = {
            "code": 0,
            "message": "",
            "result": {
                "id": resource_id
            }
        }
        self.set_status(201)
        self.write(json.dumps(response))
