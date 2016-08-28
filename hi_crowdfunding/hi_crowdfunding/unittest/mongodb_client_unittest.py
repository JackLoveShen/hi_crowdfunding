#!/usr/bin/env python

import unittest
import urllib
import httplib
import json
import time
import sys
sys.path.append('../')
sys.path.append('./')
from bson.objectid import ObjectId

from config import *
from util import *
from mongodb_client import MongoDBClient

sLogger = get_logger('unittest')

class MongoDBClientUnittest(unittest.TestCase):
    def setUp(self):
        self.client = MongoDBClient()
        self.collection_name = 'users'
        self.clear()

    def clear(self):
        while True:
            delete_result = self.client.find_and_remove(
                self.collection_name, {})
            sLogger.warn(u'delete_result:{0}'.format(delete_result))
            
            if not delete_result:
                return

    def tearDown(self):
        self.clear()


    def test_insert(self):
        # create one document
        doc_or_docs = {
            'name': 'zyf'
        }
        spec_or_id = self.client.insert(self.collection_name, doc_or_docs)
        sLogger.warn(u'spec_or_id:{0}'.format(spec_or_id))
        self.assertTrue(len(str(spec_or_id)))

        # find one by spec_or_id
        document = self.client.find_one(self.collection_name, spec_or_id)
        sLogger.warn(u'document:{0}'.format(document))

        self.assertEqual(spec_or_id, document['_id'])
        self.assertEqual(doc_or_docs['name'], document['name'])        

        # find
        documents = self.client.find(self.collection_name, doc_or_docs)
        self.assertTrue(1, documents.count())
        for doc in documents:
            sLogger.warn(u'doc:{0}, doc_type:{1}'.format(doc, type(doc)))
            self.assertEqual(document['name'], doc['name'])

        # find_and_update
        update = {'name': 'kq'}
        update_result = self.client.find_and_update(
            self.collection_name, query = doc_or_docs, update = update)
        sLogger.warn(u'update_result:{0}'.format(update_result))

        tmp = self.client.find(self.collection_name, doc_or_docs)
        self.assertEqual(0, tmp.count())

        tmp = self.client.find_one(self.collection_name, spec_or_id)
        self.assertEqual(spec_or_id, tmp['_id']) 
        self.assertEqual(update['name'], tmp['name'])

        # find_and_remove
        delete_result = self.client.find_and_remove(
            self.collection_name, update)

        sLogger.warn(u'delete_result:{0}'.format(delete_result))

        # find one
        tmp = self.client.find_one(self.collection_name, spec_or_id)
        self.assertTrue(tmp is None)

        tmp = self.client.find(self.collection_name)
        self.assertEqual(0, tmp.count())

if __name__ == '__main__':
    unittest.main() 
