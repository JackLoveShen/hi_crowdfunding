#!/usr/bin/env python

from pymongo import MongoClient
from bson.objectid import ObjectId

from util import *

sLogger = get_logger('mongodb_client')

class MongoDBClient():
    def __init__(self, host = '127.0.0.1', port = 27017):
        self.db_client = MongoClient(host, port)
        self.database_name = self.get_default_database_name()

    def get_default_database_name(self):
        return self.db_client['hi_crowdfunding']

    def get_collection(self, collection_name):
        try:
            return self.database_name[collection_name]
        except Exception, e:
            sLogger.exception('collection_name:{0}, exception:{1}'.format(
                collection_name, str(e)))
            raise
    
    def insert(self, collection_name, doc_or_docs = {}):
        collection = self.get_collection(collection_name)
        obj_id = collection.insert(doc_or_docs)
        
        sLogger.warn(u'collection_name:{0}, doc_or_docs:{1}, obj_id:{2}'.format(
            collection_name, doc_or_docs, obj_id))

        return obj_id

    # user internal filed id: spec_or_id.
    def find_one(self, collection_name, spec_or_id = None):
        collection = self.get_collection(collection_name)
        find_result = collection.find_one(spec_or_id)

        sLogger.warn(u'collection_name:{0}, spec_or_id:{1}, find_result:{2}'.format(
            collection_name, spec_or_id, find_result))

        return find_result

    # XXX exclude filed _id in my result
    def find(self, collection_name, query = {}):
        collection = self.get_collection(collection_name)
        # XXX we will exclude _id filed in my result
        find_result = collection.find(query, fields = {'_id': False})

        sLogger.warn(u'collection_name:{0}, query:{1}, find_result:{2}'.format(
            collection_name, query, find_result))

        return find_result

    # remove document which id equal to spec_or_id
    def remove(self, collection_name, spec_or_id):
        collection = self.get_collection(collection_name)
        remove_result = collection.remove(spec_or_id)
        
        sLogger.warn(u'collection_name:{0}, spec_or_id:{1}, remove_result:{2}'.format(
            collection_name, spec_or_id, remove_result))

        return remove_result

    def find_and_update(self, collection_name, query = {}, update = {}, sort = {'_id', 1}):
        collection = self.get_collection(collection_name)
        update_result = collection.find_and_modify(query, update = {'$set': update})

        sLogger.warn(u'collection_name:{0}, query:{1}, update:{2}, update_result:{3}'.format(
            collection_name, query, update, update_result))

        return update_result

    def find_and_remove(self, collection_name, query = {}, sort = {'_id': 1}):
        collection = self.get_collection(collection_name)
        # the method will only select one document to modify
        delete_result = collection.find_and_modify(query, remove = True, sort = sort)

        sLogger.warn(u'collection_name:{0}, query:{1}, delete_result:{2}'.format(collection_name, query, delete_result))

        return delete_result

    def generate_query(self, resource_id):
        return {'id': resource_id}

    def list(self, collection_name, query = {}):
        sLogger.warn(u'collection_name:{0}, query:{1}'.format(
            collection_name, query))

        find_result = self.find(collection_name, query)
        list_result = [doc for doc in find_result]
   
        sLogger.warn(u'list_result:{0}'.format(list_result))
        return list_result

    def get(self, collection_name, resource_id):
        sLogger.warn(u'collection_name:{0}, resource_id:{1}'.format(
            collection_name, resource_id))

        query = self.generate_query(resource_id)
        list_result = self.find(collection_name, query)
     
        sLogger.warn(u'list_result:{0}'.format(list_result))

        for result in list_result:
            return result
        return None

    def post(self, collection_name, doc_or_docs = {}):
        return self.insert(collection_name, doc_or_docs)

    def put(self, collection_name, resource_id, update = {}):
        query = self.generate_query(resource_id)
        update_result = self.find_and_update(query, update)

        sLogger.warn(u'collection_name:{0}, resource_id:{1}, update_result:{2}'.format(
            collection_name, resource_id, update_result))

        return update_result

    def delete(self, collection_name, resource_id):
        query = self.generate_query(resource_id)
        delete_result = self.find_and_remove(collection_name, query)

        sLogger.warn(u'collection_name:{0}, resource_id:{1}, delete_result:{2}'.format(
            collection_name, resource_id, delete_result))

        return delete_result

db_client = MongoDBClient()

if __name__ == '__main__':
    db_client = MongoDBClient()

    # delete all
    while True:
        delete_result = db_client.find_and_remove('users', {'zyf': 'kq'})
        print 'find_and_remove', delete_result
        if not delete_result:
            break

    obj_id = db_client.insert('users', {'zyf': 'kq'})
    print 'insert, obj_id:{0}'.format(obj_id)

    find_result = db_client.find_one('users', obj_id)
    print 'find_result:{0}'.format(find_result)

    all_objects = db_client.find('users', {'zyf': 'kq'})
    for cur in all_objects:
        print cur

    list_result = db_client.list('users', {'zyf': 'kq'})
    print 'list_result, ', list_result 

    update_result = db_client.find_and_update('users', query = {'zyf': 'kq'}, update = {'zyf': 'zyf'})
    print update_result

    all_objects = db_client.find('users', {'zyf': 'zyf'})
    for cur in all_objects:
        print cur
    
    delete_result = db_client.find_and_remove('users', {'zyf': 'kq'})
    print 'find_and_remove', delete_result
    
    all_objects = db_client.find('users')
    for cur in all_objects:
        print 'find', cur, type(cur)
