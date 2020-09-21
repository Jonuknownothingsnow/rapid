import datetime

class RapidModel(object):
    def __init__(self, name, model_path, **kwargs):
        self.name = name
        self.model_path = model_path
        self.params = kwargs
        self.model = self.load()
        self.update_time = datetime.datetime.now()

    def load(self):
        raise NotImplementedError("load function is not implemented")

    def predict(self, inputs):
        raise NotImplementedError("predict function is not implemented")

    def to_dict(self):
        return {
            "name":self.name,
            "model_path":self.model_path,
            "params":self.params,
            "update_time":self.update_time
        }


class HelloModel(RapidModel):
    def load(self):
        return None

    def predict(self, inputs):
        return f"Hello {self.name}"