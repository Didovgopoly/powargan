from transformers import LineByLineTextDataset, DataCollatorForLanguageModeling, BertModel
from transformers import BertTokenizer, BertForPreTraining, BertForMaskedLM, Trainer, TrainingArguments

tokenizer = BertTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
rubert = BertModel.from_pretrained('trained/rubert')
rubert.eval()

def transform(s):
    title_in = tokenizer(s, return_tensors="pt", max_length=512,truncation=True)
    return rubert(**title_in)[0][:, 0, :].cpu().detach()
