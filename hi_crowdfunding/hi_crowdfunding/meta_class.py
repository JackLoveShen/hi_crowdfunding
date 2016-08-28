#!/usr/bin/env python

class MetaClass(object):
    def __init__(self, _options):
        self._options = _options
        self.code = 0
        self.message = ''

    def getattr(self, name):
        try:
            return self._options[name]
        except KeyError, e:
            print 'KeyError', str(e)
        return ''

    def get_required_element_list(self):
        raise Exception('you must override it in child class')


    def check_element_required(self, options):
        '''
        The method can be use in create resource.
        '''
        requires = self.get_required_element_list()
        print 'check_element_required', options
        print 'requires', requires
        for k in requires:
            if not k in options:
                self.set_code(400)
                self.set_message('The "%s" is required.' % k)
                return
        self.set_code(0)

    def is_code_ok(self):
        return self.code == 0

    def set_code(self, code):
        self.code = code
    
    def get_code(self):
        return self.code

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def setattr(self, name, value):
        if name in self._options:
            self._options[name] = value

    def to_dict(self):
        if '_id' in self._options:
            del self._options['_id']
        return self._options

    def merge(self, options):
        for (k, v) in options.items():
            if isinstance(v, list):
                self.setattr(k ,v[0])
            else:
                self.setattr(k, v)

    def is_valid(self):
        return True
