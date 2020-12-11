from pathlib import Path
import os
import sys
import pickle
import re 
from nltk.tokenize import RegexpTokenizer
from gensim.models import Word2Vec

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
device = torch.device('cpu')

w2v_path = Path('trained/food_w2v_300.w2v')
w2tag_path = Path('trained/w2tag.pkl')
lstm_title_ingr_path = Path('trained/best_lstm_title_ingr.pth')
lstm_steps_path = Path('trained/best_lstm_steps.pth')

with open(w2tag_path,"rb") as file:
  word_to_tag = pickle.load(file)

model_w2v = Word2Vec.load(str(w2v_path))

def text_to_w2v_embeddings(text, model=model_w2v, word2tag=word_to_tag):
    # text = re.sub(r'[^\w\s]+|[\d]+', r'',text.lower()).strip()
    text = re.sub(r'[^\w\t\v\f]+|[\d]+', r' ',text.lower()).strip()
    embds = []
    for word in text.split(' '):
        try:
            tag = word2tag[word]
            emb = model.wv[tag]
        except KeyError:
            continue
        embds.append(emb)
    return np.array(embds)

class SelfAttention(nn.Module):
    def __init__(self, hid_dim):
        super().__init__()
        self.attn = nn.Linear(hid_dim, 1, bias=False)

    def forward(self, encoder_outputs):
        # encoder_outputs = [t * batch_size * hid_dim]
        # Let's permute to [batch_size * t * hid_dim]
        encoder_outputs = encoder_outputs.permute(1, 0, 2)
    
        e = self.attn(encoder_outputs) # [batch_size * t * 1]

        # Calculate alpha = softmax(e)
        alpha = F.softmax(e, dim=1)

        attention = (alpha * encoder_outputs).sum(1).unsqueeze(-1)
        return attention.permute(2, 0, 1)

class Encoder(nn.Module):
    def __init__(self, emb_dim, hid_dim, n_layers, dropout, food_space_dim=1024):
        super().__init__()
        
        self.emb_dim = emb_dim
        self.hid_dim = hid_dim
        self.n_layers = n_layers
        
        self.rnn = nn.LSTM(
            input_size=emb_dim,
            hidden_size=hid_dim,
            num_layers=n_layers,
            dropout=dropout,
            bidirectional=True
        )

        self.attn = SelfAttention(self.hid_dim * 2)
        self.fc = nn.Linear(hid_dim * 2, food_space_dim)
        
    def forward(self, src):
        
        #src = [batch size, sent len, embd]
        src = src.permute(1, 0, 2)
        
        output, (hidden, cell) = self.rnn(src)
        #output = [sent len, batch, 2*hidden_dim]
        
        output = self.attn(output)
        output = self.fc(output)

        return output.squeeze(0)


w2v_emb_dim = 300
hidden_dimm = 300
num_layers = 1
dropout = 0
food_space_dim = 256
lstm_title_ingr = Encoder(w2v_emb_dim, hidden_dimm, num_layers, dropout, food_space_dim=food_space_dim)
lstm_steps = Encoder(w2v_emb_dim, hidden_dimm, num_layers, dropout, food_space_dim=food_space_dim)

lstm_title_ingr.load_state_dict(torch.load(lstm_title_ingr_path,map_location=torch.device(device)))
lstm_steps.load_state_dict(torch.load(lstm_steps_path,map_location=torch.device(device)))
lstm_title_ingr.to(device)
lstm_title_ingr.eval()
lstm_steps.to(device)
lstm_steps.eval()

def title_ingr_to_emb(title,ingr):
  emb = text_to_w2v_embeddings(title+" "+ingr,model_w2v,word_to_tag)
  emb = torch.tensor(emb).unsqueeze(0).to(device)
  return lstm_title_ingr(emb)

def steps_to_emb(steps):
  emb = text_to_w2v_embeddings(steps,model_w2v,word_to_tag)
  emb = torch.tensor(emb).unsqueeze(0).to(device)
  return lstm_steps(emb)

def transform(title,ingr,steps):    
    return title_ingr_to_emb(title,ingr).cpu().detach(),steps_to_emb(steps).cpu().detach()
