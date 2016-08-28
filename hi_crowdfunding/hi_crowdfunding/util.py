#!/usr/bin/env python

import json
import os
import time
import random
from logging import *
from logging.handlers import RotatingFileHandler

from config import *

DEFAULT_LOGGER_NAME = 'admin'

def get_logger(name = DEFAULT_LOGGER_NAME):
    filename = '{0}.LOG'.format(name)
    formatter = Formatter('%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s', '%Y-%m-%d %H:%M:%S')
    handler = RotatingFileHandler(filename, maxBytes = 10 * 1024 * 1024, backupCount = 5)
    handler.setLevel(DEBUG)
    handler.setFormatter(formatter)
    logger = getLogger(filename)
    logger.addHandler(handler)
    return logger

sLogger = get_logger()

def get_userid(username, password):
    query = {
        'username': username,
        'password': password
    }
    from mongo_db import db_client
    user = db_client.get_one_customized(MONGO_DB_USER_NAME, query)

    sLogger.warn(u'query:{0}, database:{1}, user:{2}'.format(query, MONGO_DB_USER_NAME, user))

    if not user:
        return user

    return user.get('id', '')

def generate_resource_id(resource_type):
    return '{0}_{1}_{2}_{3}'.format(
        resource_type, os.getpid(), time.time(), random.random())

def parse_request_body(body):
    if not isinstance(body, dict):
        return body

    if len(body.keys()) == 1: 
        key = body.keys()[0]
        try:
            key = json.loads(key)
            return key
        except Exception, e:
            print str(e)

    return body
    

if __name__ == '__main__':
    code = {'{"telephone_number": "01234567890"}': ['']}
    print parse_request_body(code)
    
    code = {'username': ['liupeng'], 'city': ['chengshi'], 'provinces': ['shengfen'], 'registration_time': ['zhuceshijian'], 'age': ['18'], 'telephone_number': ['18501360496'], 'head_portrait': ['touxiang'], 'job': ['zhiye'], 'crowdfunding_number': ['zhongchou'], 'password': ['111111'], 'id': ['uid']}
    print parse_request_body(code)
