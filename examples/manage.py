from rapid import Rapid
from rapid.models import RapidModel


class HelloModel(RapidModel):
    def load(self):
        # 根据需要实现load方法
        return None

    def predict(self, inputs):
        # 根据需要实现推断方法
        return f"Hello {self.name}"

    def metrics(self, y_pre, y):
        # 根据需要实现模型评测方法
        return "xxx"


app = Rapid()
hm = HelloModel("hello")
app.register_model(hm)
app.run()

if __name__ == "__main__":
    app.run()
