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

Download [stackexchange dataset](https://archive.org/download/stackexchange). In the preprocess folder, run the following command to preprocess the dataset:

sh extract.sh <path/to/raw/stackexchange dataset>

## Running the Model

### Configure

The other parameters to be configured are:

```
NUM_EPOCH:       Number of Epochs for training (Default = 500)
BATCH_SIZE:      Size of each batch (Default = 400)
LEARNING_RATE:   Learning Rate of the Model (Default = 0.001)
```

### Train

For training and test the model, run the following command: 

```
$ python train.py --dataset <path/to/input/folder>
```

