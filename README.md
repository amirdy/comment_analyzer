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

# Details
## Dataset 

- [Amazon Reviews for Sentiment Analysis](https://www.kaggle.com/bittlingmayer/amazonreviews/)

This dataset consists of a ~4 million Amazon customer reviews.

It has 2 labels: 

- <b>Label 1 </b> : for comments corresponds to 1 and 2 star reviews (<b>Negative</b>)

- <b>label 2 </b> : for comments corresponds to 3 and 4 star reviews (<b>Positive</b>)

## Hyperparameters
- #### Batch size: 
   - 64 
- #### Optimizer: 
   - ADAM
- #### Learning rate: 
   - 0.0001
- #### Loss: 
   - Cross entropy
- #### Train vs Validation Split: 
   - Approximately : 0.8 | 0.2 
- #### Tools: 
   - Python - Pytorch ( Using Google Colab Pro )

# Network
#### The network consists of 3 parts:
###### 1. Encoder (2 layers and Bidirectional - LSTM)
###### 2. Encoder2Decoder (MLP)
###### 3. Decoder (wih Attention - LSTM)

## 1. Encoder
####  Word indexes 1 to 194 are given to a 2 layer bidirectional LSTM (Encoder).

|<img src="README_Files/L2R.JPG" >|
|:--:| 
|Left to Right Direction|

|<img src="README_Files/R2L.JPG"  >|
|:--:| 
|Right to Left Direction|

#### 2. Encoder2Decoder

The hiddens af last layer was given to the Encoder2Decoder Network(MLP) to obtain the decoder hiddens.

This network receives hiddens of the last time step in the encoder (every two layers for both directions) and then generates decoder hiddens.

|<img src="README_Files/E2D.jpg"   width = "622"> |
|:--:| 
|Encoder to Decoder Network|


#### 2. Decoder

|<img src="README_Files/Decoder.JPG"  > |
|:--:| 
|Decoder Network|

# Hyperparameters

# Results

# References

# Useful Resources
