## Rapid



```python
from rapid.models import RapidModel

class MyModel(RapidModel):
  def __init__(self, name, model_path):
    super().__init__(name, model_path)
    
  def load(self):
    pass
  
  def predict(self, inputs):
    pass
```

