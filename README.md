# IRGCN

This repository contains codes of Induced Relational GCN(IR-GCN).

If this code helps you in your research, please cite the following publication: 


## Getting Started

These instructions will help you setup the proposed model on your local machine.

### Platforms Supported

- Unix, MacOS, Windows (with appropriate Python and PyTorch environment)

### Prerequisites
Our framework can be compiled on Python 3.6+ environments with the following modules installed:
- [tensorflow](https://www.tensorflow.org/)
- [numpy](http://www.numpy.org/)
- [scipy](https://www.scipy.org/)
- [pandas](https://pandas.pydata.org/)
- [sklearn](https://scikit-learn.org)

These requirements may be satisified with an updated Anaconda environment as well - https://www.anaconda.com/

## Input Files



## Running the Model

### Configure

The model can be configured using the file [config.ini](Codes/config.ini) present inside the [Codes](Codes/) folder. The parameters h0_size, h1_size, h2_size, and h3_size are the sizes of the hidden layers as defined in the architecture of our discriminator in the GAN framework (see figure).

The other parameters to be configured are:

```
GANLAMBDA:       Weight provided to the Adversary's Loss Term (Default = 1.0)
NUM_EPOCH:       Number of Epochs for training (Default = 80)
BATCH_SIZE:      Size of each batch (Default = 100)
LEARNING_RATE:   Learning Rate of the Model (Default = 0.0001)
model_name:      Name by which model is saved (Default = "LT_GAN")
```


### Train

For training the model, run the following command: 

```
$ python2.7 train.py <path/to/input/folder>
```

