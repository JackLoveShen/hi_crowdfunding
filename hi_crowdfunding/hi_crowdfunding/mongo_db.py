#!/usr/bin/env python

from pymongo import MongoClient
from bson.objectid import ObjectId

from util import *

sLogger = get_logger()

class MongoDBClient():
    def __init__(self, host = '127.0.0.1', port = 27017):
        self.client = MongoClient(host, port)

    def __get_database(self, name, codec_options = None, read_preference = None,
                     write_concern = None, read_concern = None):
        return self.client.name

    def __get_collection(self, name):
        return self.client[name].posts

    def get_obj_filter_id(self, obj):
        if isinstance(obj, dict):
            if '_id' in obj:
                del obj['_id']
        elif isinstance(obj, list):
            for element in obj:
                if '_id' in element:
                    del element['_id']
        return obj

    def insert(self, name, obj = {}):
        return self.__get_collection(name).insert(obj)

    def get_many(self, name, query = {}):
        return self.get_obj_filter_id(self.__get_collection(name).find(query))

    def get_one_customized(self, name, query = {}):
        return self.get_obj_filter_id(self.__get_collection(name).find_one(query))

    def get(self, name, resource_id):
        if not resource_id:
            return None
        return self.get_obj_filter_id(self.__get_collection(name).find_one({'_id': resource_id}))
        #return self.get_obj_filter_id(self.__get_collection(name).find_one({'id': resource_id}))

    def list(self, name):
        return self.get_obj_filter_id([col for col in self.__get_collection(name).find()])

    def put(self, name, resource_id, update = {}):
        return self.get_obj_filter_id(self.__get_collection(name).find_and_modify({'_id': resource_id}, update = {'$set': update}))
        #return self.get_obj_filter_id(self.__get_collection(name).find_and_modify({'_id': resource_id}, updata = True))

    def delete(self, name, resource_id):
        #delete_result = self.__get_collection(name).delete_one({'_id': resource_id})
        #return delete_result.deleted_count == 1
        delete_result = self.__get_collection(name).find_and_modify({'_id': resource_id}, remove = True)
        return delete_result

    def delete_many(self, name, filter = {}):
        #return self.__get_collection(name).find_and_modify(filter, remove = True)
        return self.__get_collection(name).remove({'zyf': 'kq'})

db_client = MongoDBClient()

if __name__ == '__main__':
    db = MongoDBClient()
    user_id = db.insert('users', {'zyf':'kq'}, manipulate = False)
    print user_id
