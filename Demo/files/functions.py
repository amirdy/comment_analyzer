import torch
import numpy as np
import random

def return_batch(batch_number, mode = 'train'):
  if mode =='train':
      X = torch.zeros((batch_size, seq_lenght))
      X[:,:] = torch.tensor(train_data[batch_size * batch_number : batch_size * (batch_number + 1)])

      Y = torch.zeros((batch_size, 1))
      Y[:,0] = torch.tensor(train_label[batch_size * batch_number : batch_size * (batch_number + 1)])

  elif mode =='test':
      X = torch.zeros((batch_size, seq_lenght))
      X[:,:] = torch.tensor(test_data[batch_size * batch_number : batch_size * (batch_number + 1)])

      Y = torch.zeros((batch_size, 1))
      Y[:,0] = torch.tensor(test_label[batch_size * batch_number : batch_size * (batch_number + 1)])

  else:
      X = torch.zeros((batch_size, seq_lenght))
      X[:,:] = torch.tensor(validation_data[batch_size * batch_number : batch_size * (batch_number + 1)])

      Y = torch.zeros((batch_size, 1))
      Y[:,0] = torch.tensor(validation_label[batch_size * batch_number : batch_size * (batch_number + 1)])

  return X, Y


def shuffling_whole_date(X, Y):
  C = list(zip(X, Y))
  random.shuffle(C)
  X, Y = zip(*C)

  return list(X), list(Y)


def accuracy(output, y):
  #  output shape ->  torch : [batch_size, num_classes]
  #  y shape ->  torch : [batch_size,1]
  
  output = output.cpu().detach().numpy()
  #  output shape ->  numpy : [batch_size, num_classes]

  pred_classes = np.argmax(output, axis = 1) #  pred_classes -> numpy : [batch_size,]
  pred_classes = np.expand_dims(pred_classes, axis=1) #  pred_classes -> numpy : [batch_size,1]

  real_classes = y.cpu().detach().numpy()  #  real_classes  -> numpy : [batch_size,1]

  bool_array = (pred_classes==real_classes) # example: bool_array=[True, False, True, False, True]
  True_pred_counts=np.count_nonzero(bool_array) # count number of Trues in [True, False, True, False, True]
  
  return True_pred_counts/pred_classes.shape[0] # a digit 


