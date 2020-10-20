from sanic import Sanic
from sanic.exceptions import SanicException, InvalidUsage
from rapid.logger import LOGGING_CONFIG
import logging.config
import json
from sanic import response

from rapid.models import RapidModel
from rapid.utils import response_data
from rapid.handlers import JosnErrorHandler
from rapid.exceptions import ModelNotExists
from rapid.logger import logger


class Rapid(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.config.dictConfig(LOGGING_CONFIG)
        self.error_handler = JosnErrorHandler()
        self.models = {}
        self.model_classes = {}
        self.set_default_routes()

    def load_config(self, config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        self.load_models_from_config(config["models"])

    def load_models_from_config(self, models):
        for model in models:
            cls = self.model_classes.get(model["class"], None)
            if cls is None:
                raise SanicException(
                    f"not found model class named {model['class']}", 400
                )
            model.pop("class")
            obj = cls(**model)
            self.register_model(obj)

    def register_model_class(self, model_class):
        """
        Register model class to app

        :param model_class: class inherit from RapidModel
        """
        if isinstance(model_class, (list, tuple)):
            for item in model_class:
                self.register_model_class(model_class)
        elif issubclass(model_class, RapidModel):
            self.model_classes[model_class.__name__] = model_class
        else:
            SanicException(
                f"only RapidModel can be registered to server, got {type(model_class)}"
            )

    def register_model(self, model):
        """
        Register single model

        :param model: model instance
        """
        if isinstance(model, (list, tuple)):
            for item in model:
                self.register_model(item)
        elif isinstance(model, RapidModel):
            self.models[model.name] = model
            logger.info(f"success load model '{model.name}' {type(model)}")
        else:
            SanicException(
                f"only RapidModel can be registered to server, got {type(model)}"
            )  # todo


    # -------------------------------------------------------------------- #
    # Model calls
    # -------------------------------------------------------------------- #

    def predict(self, request, name):
        try:
            d = self.models[name].predict(request.json["instances"])
        except Exception as e:
            raise e  # todo
        return response_data(d)

    def model_info(self, request, name):
        model = self.models.get(name, None)
        if model is None:
            raise ModelNotExists(name)
        else:
            return response_data(model.to_dict())

    def valid(self, request, name):

        instances = request.json.get("instances", [])
        labels = request.json.get("labels", [])
        return_detail = request.args.get("return_detail", False)
        try:
            d = self.models[name].valid(instances, labels, return_detail)
        except Exception as e:
            raise e  # todo
        return response_data(d)

    def set_default_routes(self):
        self.add_route(self.predict, "/models/<name>/predict", methods=["POST"])
        self.add_route(self.valid, "/models/<name>/valid", methods=["POST"])
        self.add_route(self.model_info, "/models/<name>/info")
