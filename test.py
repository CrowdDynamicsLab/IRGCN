from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix


def repackage_hidden(h):
    """Wraps hidden states in new Variables, to detach them from their history."""
    if type(h) == Variable:
        return Variable(h.data)
    else:
        return tuple(repackage_hidden(v) for v in h)


def evaluate_adaboost(gcn_model, test_loader, Adj, Adj2, Adj3, Adj4, Adj5, Features, rowsum, X, epoch, Target):
    for i, (X_test_1, Y_test_1) in enumerate(test_loader):
        X_test = torch.tensor(X[X["QuestionId"].isin(X_test_1)]['PairId'].values)
        Y_test = torch.tensor(X[X["QuestionId"].isin(Y_test_1)]['Credible'].values)
        gcn_model.eval()
        _, _, user_gcn_embed2 = gcn_model(Features, Adj, Adj2, Adj3, Adj4, Adj5, Target, X_test)
        user_gcn_embed2.squeeze_()
        predicted2 = user_gcn_embed2[X_test] > 0
    acc = accuracy_score(Y_test, predicted2.cpu())

    return acc
