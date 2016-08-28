#!/usr/bin/env python

from tornado import (ioloop, web, httpserver)

from resource_handler import ResourceHandler
from verification_code_handler import VerificationCodeHandler
from user_login_handler import UserLoginHandler
from crowdfunding_project_handler import CrowdfundingProjectHandler
from picture_handler import PictureHandler

from mongodb_client import db_client
from config import *

def generate_app():
    return web.Application([
        (r'/api/v1/users/', ResourceHandler, dict(db = db_client, resource_type = MONGO_DB_USER_NAME)),
        (r'/api/v1/crowdfunding/', CrowdfundingProjectHandler, dict(db = db_client, resource_type = MONGO_DB_CROWDFUNDING_NAME)),
        (r'/api/v1/community/', ResourceHandler, dict(db = db_client, resource_type = MONGO_DB_COMMUNITY_NAME)),
        (r'/api/v1/verification_code/', VerificationCodeHandler, dict(db = db_client, resource_type = MONGO_DB_VERIFICATION_CODE)),
        (r'/api/v1/user_login_session/', UserLoginHandler, dict(db = db_client, resource_type = MONGO_DB_USER_LOGIN_NAME)),
        (r'/api/v1/picture/', PictureHandler)
    ])

if __name__ == '__main__':
    application = generate_app()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8888)
    ioloop.IOLoop.current().start()
