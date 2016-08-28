#!/usr/bin/env python

RESOURCE_NOT_FOUND = {
    "code": 404,
    "message": "Resource not found.",
    "result": {
    }
}

INVALID_JSON_FORMAT = {
    "code": 400,
    "message": "Invalid json format.",
    "result": {
    }
}

INVALID_PARAMETER_TYPE = {
    "code": 400,
    "message": "The type of '%s' is invalid, what we expected is '%s'!",
    "result": {
    }
}

INVALID_PARAMETER = {
    "code": 400,
    "message": "The '%s' is invalid.%s!",
    "result": {
    }
}

INVALID_TOKEN = {
    "code": 401,
    "message": "Invalid token!",
    "result": {
    }
}
