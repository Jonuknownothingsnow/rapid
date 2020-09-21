from sanic.exceptions import SanicException, InvalidUsage

class RapidException(SanicException):
    pass

class ModelNotExists(InvalidUsage):
    pass

class ModelPredictError(RapidException):
    pass
