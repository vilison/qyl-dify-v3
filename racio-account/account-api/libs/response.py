def response_json(code, msg=None, data=None):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }
