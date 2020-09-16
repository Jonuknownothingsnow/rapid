from sanic import Sanic
from sanic import response
from sanic.exceptions import InvalidUsage
from rapid.handlers import JosnErrorHandler
from sanic.exceptions import SanicException
from rapid.logger import LOGGING_CONFIG
import logging.config
from rapid.models import RapidModel
from rapid.utils import response_data
from copy import deepcopy
# @app.route("/")
# async def run(request):
#     print(request.headers)
#     return response.text("ok")


class Rapid(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.config.dictConfig(LOGGING_CONFIG)
        self.error_handler = JosnErrorHandler()
        self.models = {}
        self.add_route(self.predict, "/models/<name>/predict")

    def register_model(self, model):
        if isinstance(model, (list, tuple)):
            for item in model:
                self.register_model(item)
        elif isinstance(model, RapidModel):
            self.models[model.name] = model
        else:
            SanicException(f"only RapidModel can be registered to server, got {type(model)}")

    def predict(self, request, name):
        try:
            d = self.models[name].predict(request.json)
        except Exception as e:
            raise e # todo
        return response_data(d)


