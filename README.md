# Comment analyzer
This is a sentiment analysis project. A Deep learning model which can detect the comment given for a product is positive or negative !


<ins>[Preview](#preview)</ins>&nbsp;&nbsp;&nbsp;
<ins>[Details](#Details)</ins>&nbsp;&nbsp;&nbsp;
<ins>[Network](#Network)</ins>&nbsp;&nbsp;&nbsp;
<ins>[Hyperparameters](#Hyperparameters)</ins>&nbsp;&nbsp;&nbsp;
<ins>[Results](#Results)</ins>&nbsp;&nbsp;&nbsp;
<ins>[References](#References)</ins>&nbsp;&nbsp;&nbsp;
<ins>[Useful Resources](#Useful-Resources)</ins>

# Preview

# Details of Implementation
## Dataset 

- [Amazon Reviews for Sentiment Analysis](https://www.kaggle.com/bittlingmayer/amazonreviews/)

This dataset consists of a ~4 million Amazon customer reviews(~3.6Milion for training and 0.4milion for testing).

It has 2 labels: 

- <b>Label 1 </b> : for comments corresponds to 1 and 2 star reviews (<b>Negative</b>)

- <b>label 2 </b> : for comments corresponds to 3 and 4 star reviews (<b>Positive</b>)

## Prerpocessing

I just used 1 million samples for training(validationg) and 400000 samples for testing.

Thus:
 ###### Train set : 800000 samples.
 ###### Validation set : 200000 samples.
 ###### Test set : 400000 samples.

Each sample(which is sequnece of sentences) became a sequence of vocabs(tokens).

The length of each sample is considered the size of this sequence.

The length of samples are different. For batch(mini batch) gradient descent we need to have samples with same lenght.

##### So what is the solution?
###### We can only consider the first N Vocabs(Tokens) for each sample.

###### Then, we can add enough <pad> token to samples with a length of less than N to reach a length of N.
 
##### But, what is the value of N?
###### Lets assume the lenght of samples in the train set is a random variable X with a Normal distribution.
###### The average length of the samples in the training set is 92.78 and the standard deviation is 50.22.

<img src="README_Files/MuSigma.png"   >

###### We know in the noraml distribution we have : 

<img src="README_Files/Prob1.png"   >

###### So, here we have : 

<img src="README_Files/Prob2.png"   >

##### Thus, considering *N = 194* can be a good choice !




# Network
#### The network consists of 3 parts:
###### 1. Encoder (2-layer and Bidirectional - LSTM)
###### 2. Encoder2Decoder (MLP)
###### 3. Decoder (wih Attention - LSTM)

## 1. Encoder
####  Word indexes 1 to 194 are given to a 2 layer bidirectional LSTM (Encoder).

|<img src="README_Files/L2R.JPG"  width = "622" >|
|:--:| 
|Left to Right Direction|

|<img src="README_Files/R2L.JPG"  width = "622" >|
|:--:| 
|Right to Left Direction|

#### 2. Encoder2Decoder

The hiddens af last layer was given to the Encoder2Decoder Network(MLP) to obtain the decoder hiddens.

This network receives hiddens of the last time step in the encoder (every two layers for both directions) and then generates decoder hiddens.

|<img src="README_Files/E2D.jpg"   width = "622"> |
|:--:| 
|Encoder to Decoder Network|


#### 2. Decoder
For better result, I used attention mechanism which is a simple MLP.
|<img src="README_Files/Attention.jpg"  width = "622"  > |
|:--:| 
|Attention|

Then, I used the output of attention for create the input of the decoder.
|<img src="README_Files/Decoder.JPG"  width = "622"  > |
|:--:| 
|Decoder Network|

# Hyperparameters and Tools
- #### Batch size: 
   - 64 
- #### Optimizer: 
   - ADAM
- #### Learning rate: 
   - 0.0001
- #### Loss: 
   - Cross entropy
- #### Encoder sequence lenght
   - 194 
- #### Decoder sequence lenght
   - 1
- #### Train vs Validation Split: 
   - Approximately : 0.8 | 0.2 
- #### Tools: 
   - Python - Pytorch ( Using Google Colab Pro )

# Results

# References

# Useful Resources
