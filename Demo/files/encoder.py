import torch
import pickle
import os 

cwd = os.getcwd()
path = os.path.join(cwd, "./models/vocab.txt").replace('\\','/')
with open(path, "rb") as fp:   
        vocab = pickle.load(fp)

class encoder(torch.nn.Module):
  def  __init__(self, encoder_hidden_size, num_layer_enc, enc_bidirectional, emb_size):
    super().__init__()  
    self.lstm = torch.nn.LSTM(emb_size, encoder_hidden_size, num_layers = num_layer_enc, dropout = 0.4 ,bidirectional = enc_bidirectional)
    self.embedding = torch.nn.Embedding(len(vocab), emb_size)

  def forward(self, x, hidden, c): # seq_lenght is 194

    # x shape : torch.Size([seq_lenght, batch_size]) 
    # hidden shape :torch.Size([num_layers_enc * num_enc_direction, batch_size, hidden_size])
    # c shape :torch.Size([num_layers_enc * num_enc_direction, batch_size, hidden_size])
    
    emb = self.embedding(x.long())
    # emb shape : torch.Size([seq_lenght, batch_size, emb_size]) 

    out, (hidden, c) = self.lstm(emb, (hidden, c)) #  out = the toppest  hidden layer for all time steps |  hidden = contains all hiddens of last time step  |  c = contains all C of last time step
    
    # out shape :  torch.Size([seq_lenght, batch_size, hidden_size  * num_enc_direction])
    # hidden shape : torch.Size([num_layers_enc * num_enc_direction, batch_size, hidden_size])
    # c shape : torch.Size([num_layers_enc * num_enc_direction, batch_size, hidden_size])

    return out, hidden, c
