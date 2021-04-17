import torch
batch_size = 1
class encoder2decoder(torch.nn.Module):
  def  __init__(self, encoder_hidden_size, decoder_hidden_size, num_layer_enc, num_enc_directions):
    super().__init__()  
    self.fc = torch.nn.Linear(encoder_hidden_size * num_layer_enc * num_enc_directions, decoder_hidden_size)
    
    
  def forward(self, hidden): 
    # hidden shape :   torch.Size([num_enc_direction * num_layer_enc, batch_size, encoder_hidden_size]) 
    
    hidden = torch.transpose(hidden, 0, 1)
    # hidden shape :   torch.Size([batch_size, num_enc_direction * num_layer_enc, encoder_hidden_size]) 

    hidden = hidden.reshape(batch_size, hidden.shape[1] * hidden.shape[2])    
    # hidden shape : torch.Size([batch_size, encoder_hidden_size * num_layer_enc * num_enc_directions]) 

    out= self.fc(hidden) 
    # out shape : torch.Size([batch_size, decoder_hidden_size])

    out =out.unsqueeze(0)
    # out shape : torch.Size([1, batch_size, decoder_hidden_size])

    return out