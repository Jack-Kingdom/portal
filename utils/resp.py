from utils.code import StatusOk, code2msg
from tornado import escape


def gen_suc_resp(data):
    return escape.json_encode({
        'code': StatusOk,
        'message': code2msg(StatusOk),
        'data': data
    })


def gen_err_resp(code: int):
    return escape.json_encode({
        'code': code,
        'message': code2msg(code)
    })
