#!/usr/bin/env python

import os
from tornado import (ioloop, web, gen)

class PictureHandler(web.RequestHandler):
    def get_default_picture_dir(self):
        return 'picture'

    def get(self):
        picture = self.get_query_argument('id', '')
        path = os.path.join(self.get_default_picture_dir(), picture)
        if picture and os.path.exists(path):
            self.set_status(200)
            with open(path, 'rb+') as f:
                content = f.read()
            self.write(content)
