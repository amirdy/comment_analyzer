import torch
import torch.cuda as cuda

batch_size = 1

class decoder(torch.nn.Module):
  def  __init__(self, encoder_hidden_size, num_enc_direction, decoder_hidden_size, num_layer_dec, num_classes, dec_bidirectional):
    super().__init__() 

    self.lstm = torch.nn.LSTM(encoder_hidden_size*num_enc_direction, decoder_hidden_size, num_layers = num_layer_dec, bidirectional = dec_bidirectional)
    self.attn_alpha = torch.nn.Linear(decoder_hidden_size*2 + encoder_hidden_size * num_enc_direction, 1) # For generating alphas
    self.softmax = torch.nn.Softmax(dim = 1) 
    self.fc = torch.nn.Linear(decoder_hidden_size, num_classes)
 
    
  def forward(self, encoder_hiddens, hidden, c): # seq_lenght is 1 here (in decoder)

    # hidden shape :   torch.Size([1, batch_size, decoder_hidden_size]) 
    # c shape :   torch.Size([1, batch_size, decoder_hidden_size]) 
    # encoder_hiddens shape : torch.Size([encoder_seq_lenght, batch_size, encoder_hidden_size  * num_enc_directions]) | seq_lenght of encoder is 194

    encoder_seq_lenght = encoder_hiddens.shape[0]

    attn_weights = torch.zeros((batch_size, encoder_seq_lenght)) # [(batch_size, encoder_seq_lenght)]
    for i in range(encoder_seq_lenght):
      input = torch.cat((hidden[0,:,:],c[0,:,:],encoder_hiddens[i]),dim=1) # input : [(batch_size, decoder_hidden_size*2 + encoder_hidden_size  * num_directions_enc )]
      attn_weight = self.attn_alpha(input) # attn_weight : [(batch_size,1)]
      attn_weight = self.softmax(attn_weight)
      attn_weights[:,i] = attn_weight.squeeze(1)

    attn_weights = attn_weights.unsqueeze(2).double() # [(batch_size, encoder_seq_lenght, 1)]

    enc_hiddens = torch.transpose(encoder_hiddens, 1, 0) # ([batch_size, encoder_seq_lenght, encoder_hidden_size  * num_directions_enc])
    enc_hiddens = torch.transpose(enc_hiddens, 1, 2) # ([batch_size, encoder_hidden_size  * num_directions_enc, encoder_seq_lenght])
    
    if cuda.is_available():
       attn_weights = attn_weights.cuda()

    attn_applied = torch.bmm(enc_hiddens.double(), attn_weights)  # [(batch_size, encoder_hidden_size*num_directions_enc, 1)]  | alpha1 * h1 + alph2 * h2 + .... 
    attn_applied = attn_applied.squeeze(2) # [(batch_size, encoder_hidden_size*num_directions_enc)]
    attn_applied = attn_applied.unsqueeze(0) ## [(1, batch_size, encoder_hidden_size*num_directions_enc)] | 1 : decoder_seq_lenght
    
    x = attn_applied # [(1, batch_size, encoder_hidden_size*num_directions_enc)] | 1 : decoder_seq_lenght

    out, (hidden, c) = self.lstm(x, (hidden.double(), c.double()) ) #  out = the toppest  hidden layer for all time steps #  out = the toppest  hidden layer for all time steps |  hidden = contains all hiddens of last time step  |  c = contains all C of last time step
    # out shape :  torch.Size([seq_lenght, batch_size, dec_hidden_size  * num_dec_directions]) | 1 : decoder_seq_lenght 
    # hidden shape : torch.Size([num_dec_layers * num_dec_directions, batch_size, dec_hidden_size])
    # c shape : torch.Size([num_dec_layers * num_dec_directions, batch_size, dec_hidden_size])
    output = out.view(out.size(0)* out.size(1),out.size(2))  # shape:  torch.Size([seq_lenght * batch_size, dec_hidden_size  * num_dec_directions])    
    output = self.fc(output) # torch.Size([seq_lenght * batch_size, num_classes]) | seq_lenght = 1

    
    return output