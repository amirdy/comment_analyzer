from files.encoder import encoder
from files.decoder import decoder
from files.encoder2decoder import encoder2decoder
from files.functions import *
import numpy as np 
import torch
import os , time
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

import random
import torch.cuda as cuda
import pickle

def r(comment):
    start = time.time()

    cwd = os.getcwd()
    path = os.path.join(cwd, "./models/vocab_new.txt").replace('\\','/')
    with open(path, "rb") as fp:   
        vocab = pickle.load(fp)

    seq_lenght = 244 
    example_test = comment
    example = word_tokenize( example_test.lower().replace(".", " . ") )  
    test_data = [example]
    ## ADD Padding and Cutting the long samples 

    if len(example) < seq_lenght:
        for i in range( seq_lenght -len(example) ):
          test_data[0].append('PAD')
    else :
        test_data[0] = test_data[0][0:seq_lenght]



    ## Convert Vocabs to their indexes in Vocab. 

    for idx_word, word in enumerate(test_data[0]):
        if word not in vocab:
             test_data[0][idx_word] = 0 ## UNK for vocabs that are not in the Vocab.
        else:
            test_data[0][idx_word] = vocab.index(word)    

    num_classes = 2
    batch_size =  1 
    number_of_test_batches = 1
    encoder_hidden_size = 16
    num_layer_enc = 2
    num_enc_direction = 2
    enc_bidirectional = bool(num_enc_direction - 1)
    emb_size = 16
    enc = encoder(encoder_hidden_size, num_layer_enc, enc_bidirectional, emb_size)

    with open("models/vocab.txt", "rb") as fp:   
        vocab = pickle.load(fp)

    decoder_hidden_size = 16
    enc2dec = encoder2decoder(encoder_hidden_size,decoder_hidden_size, num_layer_enc, num_enc_direction)

    num_layer_dec = 1
    num_dec_direction = 1
    dec_bidirectional = bool(num_dec_direction - 1)
    dec = decoder(encoder_hidden_size, num_enc_direction, decoder_hidden_size, num_layer_dec, num_classes, dec_bidirectional)

    enc.double()
    dec.double()
    enc2dec.double()


    enc.load_state_dict(torch.load("models/enco.pth", map_location=torch.device('cpu')))
    dec.load_state_dict(torch.load("models/deco.pth", map_location=torch.device('cpu')))
    enc2dec.load_state_dict(torch.load("models/enco2deco.pth", map_location=torch.device('cpu')))

    enc.eval()
    dec.eval()
    enc2dec.eval()

    X = torch.tensor(test_data)
        ## X shape : torch (batch_size , seq_lenght) 

    X = torch.transpose(X, 0, 1)
        ## X shape : torch (seq_lenght, batch_size) 

    h0 = torch.zeros((num_enc_direction * num_layer_enc, batch_size, encoder_hidden_size)).double()
    c0 = torch.zeros((num_enc_direction * num_layer_enc, batch_size, encoder_hidden_size)).double()

    if cuda.is_available(): 
                X = X.cuda()
                enc = enc.cuda() 
                dec = dec.cuda() 
                enc2dec = enc2dec.cuda() 
                h0 = h0.cuda() 
                c0 = c0.cuda() 


    encoder_hiddens ,encoder_last_h ,encoder_last_c = enc(X, h0, c0) # seq_lenght is 244
        # encoder_hiddens shape :  torch.Size([seq_lenght, batch_size, encoder_hidden_size*num_enc_direction]) | hidden of all time steps
        # encoder_last_h shape :   torch.Size([num_enc_direction * num_layer_enc, batch_size, encoder_hidden_size]) | hidden of last time step
        # encoder_last_c shape :   torch.Size([num_enc_direction * num_layer_enc, batch_size, encoder_hidden_size]) | C of last time step


    h = enc2dec(encoder_last_h)
        # h shape :   torch.Size([1, batch_size, decoder_hidden_size]) 

    c = enc2dec(encoder_last_c)
        # c shape :   torch.Size([1, batch_size, decoder_hidden_size]) 

    output = dec(encoder_hiddens ,h, c)
        # output shape :   torch.Size([batch_size, num_classes]) | num_classes : 2
    
    soft_max = torch.nn.Softmax(dim = 1)
    probabilities = soft_max(output)
    print("Example : ",example_test)
    print("Probability of Negative:  {}  \n \t       Positive:  {}".format(probabilities[0,0],probabilities[0,1]))
    end = time.time()
    print("time: ",end - start)
    print("___________________________________")


   


    return(probabilities[0,0], probabilities[0,1])
  
