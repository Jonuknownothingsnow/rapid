from rapid import Rapid
from rapid.models import RapidModel

class HelloModel(RapidModel):
    def load(self):
        return None

    def predict(self, inputs):
        return f"Hello {self.name}"

app = Rapid()
hm = HelloModel("hello")
app.register_model(hm)
app.run()