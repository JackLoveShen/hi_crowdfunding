#!/usr/bin/env python

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

if __name__ == '__main__':
    register_openers()
    datagen, headers = multipart_encode({"image1": open("/root/123456", "rb"), "image1": open("/root/123456", "rb")})
    request = urllib2.Request("http://localhost:8888/api/v1/crowdfunding/", datagen, headers)
    print urllib2.urlopen(request).read()
