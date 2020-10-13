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


app = Rapid("trans")
app.register_model(TransModel(name="albert", model_path="voidful/albert_chinese_tiny"))
app.run(port=8088)
