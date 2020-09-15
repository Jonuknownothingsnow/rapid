from sanic import Sanic
from sanic import response
from sanic.exceptions import InvalidUsage
from rapid.exception import JosnErrorHandler
from sanic import log
import logging.config

# @app.route("/")
# async def run(request):
#     print(request.headers)
#     return response.text("ok")


class Rapid(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        d = log.LOGGING_CONFIG_DEFAULTS
        d['handlers']["console"]['class'] = 'rapid.logger.InterceptHandler'
        d['handlers']["error_console"]['class'] = 'rapid.logger.InterceptHandler'
        d['handlers']["access_console"]['class'] = 'rapid.logger.InterceptHandler'
        del d['handlers']["console"]["stream"]
        del d['handlers']["error_console"]["stream"]
        del d['handlers']["access_console"]["stream"]
        logging.config.dictConfig(d)
        self.error_handler = JosnErrorHandler

    def register_model(self, model_class):
        pass

