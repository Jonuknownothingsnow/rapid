# Rapid



rapid用于快速将模型转化为http服务接口，以便于调试、测试部署。



## 安装rapid

通过whl安装：

```shell
pip install rapid-0.1.0-py3-none-any.whl
```





## 使用

### Quick Start

快速运行一个无模型的Rapid服务

```python
# app.py
from rapid import Rapid

if __name__ == '__main__':  
  app = Rapid("trans")
  app.run(port=8088)
```





### 创建自己的模型类

在通过Rapid挂载模型之前，需要将它包装为RapidModel类：

```python
# models.py
from MyProject import MyModel
from rapid.models import RapidModel



class MyRapidModel(RapidModel):
    # RapidModel的__init__方法接受name、model_path两个输入，它们被存储在self.name,和self.model_path中，接着__init__会调用self.load方法。
    def load(self):
        # 实现load方法
        self.model = MyModel.load(self.model_path)

    def predict(self, inputs):
        # 实现predict方法
        results = self.model.predict(inputs)
        return results
      
```





### 注册模型

定义完成自己的Rapid模型类后，可以通过两种方式注册到Rapid服务。

一是直接实例化模型进行挂载：

```python
# app.py
from rapid import Rapid
from models import MyRapidModel



if __name__ == '__main__':  
  app = Rapid("trans")
  app.register_model(MyRapidModel(name="my_model", model_path="./data"))
  app.run(port=8088)
```



另一种方式是注册模型类到服务上，并通过读取config文件实例化模型：

```python
# app.py
from rapid import Rapid
from models import MyRapidModel



if __name__ == '__main__':  
  app = Rapid("trans")
  app.register_model_class(MyRapidModel)
  app.load_config("./config.json")
  app.run(port=8088)
  
"""
config.json:
{
	models:[
		{name:"my_model", model_path:"./data", class:"MyRapidModel"}
		{name:"my_model_2", model_path:"./data", class:"MyRapidModel"}
	]
}

"""
```





### 使用模型预测接口

模型挂载后即可用过服务调用模型:

```python
import requests
data = {"instances":[...]}

r = requests.post("http://127.0.0.1:8088/models/<model_name>/predict", json=data)
r.json()
```







### 使用模型评测接口

使用模型评测接口需要先实现RapidModel中的metrics方法

```python
from MyProject import MyModel
from rapid.models import RapidModel
from sklearn.metrics import f1_score


class MyRapidModel(RapidModel):
    # RapidModel的__init__方法接受name、model_path两个输入，它们被存储在self.name,和self.model_path中，接着__init__会调用self.load方法。
    def load(self):
        # 实现load方法
        self.model = MyModel.load(self.model_path)

    def predict(self, inputs):
        # 实现predict方法
        results = self.model.predict(inputs)
        return results

    def metrics(self, y_pre, y):
        # 选择实现评测指标方法
        return f1_score(y, y_pre)

```



然后通过服务调用：

```python
import requests
data = {"instances":[...], "labels":[1,0,1]}

r = requests.post("http://127.0.0.1:8088/models/<model_name>/valid?return", json=data)
r.json()
```





### 使用实例

使用rapid快速加载transformers模型提供http接口调用。

```python
import torch
from rapid import Rapid, models
from transformers import AutoTokenizer, AutoModel, BertTokenizer

class TransModel(models.RapidModel):
    def load(self):
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        self.model = AutoModel.from_pretrained(self.model_path)

    def predict(self, inputs):
        input_ids = []
        for input_text in inputs:
            input_ids.append(self.tokenizer.encode(input_text))
        input_ids = torch.tensor(input_ids)
        results = self.model(input_ids)[0].tolist()
        return results

      

if __name__ == '__main__':  
  app = Rapid("trans")
  app.register_model(MyRapidModel(name="my_model", model_path="./data"))
  app.run(port=8088)


```

