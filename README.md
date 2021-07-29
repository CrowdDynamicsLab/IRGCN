# IRGCN

This repository contains codes of Induced Relational GCN(IR-GCN).

If this code helps you in your research, please cite the following publication: 

[Ranking User-Generated Content via Multi-Relational Graph Convolution](https://dl.acm.org/doi/abs/10.1145/3404835.3462857)

```
@inproceedings{10.1145/3404835.3462857, author = {Narang, Kanika and Krishnan, Adit and Wang, Junting and Yang, Chaoqi and Sundaram, Hari and Sutter, Carolyn}, title = {Ranking User-Generated Content via Multi-Relational Graph Convolution}, year = {2021}, isbn = {9781450380379}, publisher = {Association for Computing Machinery}, address = {New York, NY, USA}, url = {https://doi.org/10.1145/3404835.3462857}, doi = {10.1145/3404835.3462857}, abstract = {The quality variance in user-generated content is a major bottleneck to serving communities on online platforms. Current content ranking methods primarily evaluate text and non-textual content features of each user post in isolation. In this paper, we demonstrate the utility of considering the implicit and explicit relational aspects across user content to assess their quality. First, we develop a modular platform-agnostic framework to represent the contrastive (or competing) and similarity-based relational aspects of user-generated content via independently induced content graphs. Second, we develop two complementary graph convolutional operators that enable feature contrast for competing content and feature smoothing/sharing for similar content. Depending on the edge semantics of each content graph, we embed its nodes via one of the above two mechanisms. We also show that our contrastive operator creates discriminative magnification across the embeddings of competing posts. Third, we show a surprising result-applying classical boosting techniques to combine final-layer embeddings across the content graphs significantly outperforms the typical stacking, fusion, or neighborhood embedding aggregation methods in graph convolutional architectures. We exhaustively validate our method via accepted answer prediction over fifty diverse Stack-Exchange (https://stackexchange.com/) websites with consistent relative gains of over 5% accuracy over state-of-the-art neural, multi-relational and textual baselines.}, booktitle = {Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval}, pages = {470–480}, numpages = {11}, keywords = {multi-relational graphs, graph convolution, user-generated content, multi-view learning, content ranking}, location = {Virtual Event, Canada}, series = {SIGIR '21} }

```

## Getting Started

These instructions will help you setup the proposed model on your local machine.

### Platforms Supported

- Unix, MacOS, Windows (with appropriate Python and PyTorch environment)

### Prerequisites
Our framework can be compiled on Python 3.6+ environments with the following modules installed:
- [tensorflow(1.3+)](https://www.tensorflow.org/)
- [numpy](http://www.numpy.org/)
- [scipy](https://www.scipy.org/)
- [pandas](https://pandas.pydata.org/)
- [sklearn](https://scikit-learn.org)

These requirements may be satisified with an updated Anaconda environment as well - https://www.anaconda.com/

## Input Files

Download [stackexchange dataset](https://archive.org/download/stackexchange). In the preprocess folder, run the following command to preprocess the dataset:

```
$ sh extract.sh <path/to/raw/stackexchange dataset>

```
The preprocessed dataset will be used as input to the model.

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

