from sanic.exceptions import SanicException

class RapidException(SanicException):
    pass

class ModelNotExists(RapidException):
    pass

class ModelPredictError(RapidException):
    pass