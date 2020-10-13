from sanic.response import text
from rapid import Rapid
from rapid.models import HelloModel
import pytest

@pytest.fixture
def app():
    app = Rapid("test")
    yield app

def test_hello(app):
    @app.get("/")
    def handler(request):
        return text("hello")

    _, response = app.test_client.get("/")
    assert response.status == 200

def test_register_model(app):
    dm = HelloModel(name="dummy", model_path="")
    app.register_model(dm)
    _, response = app.test_client.post("/models/dummy/predict", json={"instances":["aaa"]})
    assert response.status == 200
    assert response.json["data"] == "Hello dummy"