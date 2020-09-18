from sanic import response

def response_data(data, msg="", err="", success=True, code=200):
    res = dict(
        err=err,
        msg=msg,
        data=data,
        success=success
    )
    code = code
    return response.json(res, code)