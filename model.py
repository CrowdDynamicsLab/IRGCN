import torch
import torch.nn as nn

import torch.nn.functional as F
import torch.nn.utils
from torch.nn.parameter import Parameter
from layers import GraphConvolution, SparseMM
import numpy as np
from scipy import sparse
import math
import os

def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(np.vstack((sparse_mx.row,
                                          sparse_mx.col))).long()
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)


class GCN_adaboost(nn.Module):
    def __init__(self, nFeat, nhid1, nhid2, nhid3, nhid4, nclass, dropout=0.5):
        super(GCN_adaboost, self).__init__()

        self.gc1 = GraphConvolution(nFeat, nhid2, bias=True)
        self.gc2 = GraphConvolution(nhid2, nhid3, bias=True)
        self.gc3 = GraphConvolution(nhid3, nhid4, bias=True)
        self.gc4 = GraphConvolution(nFeat, nhid2, bias=True)
        self.gc5 = GraphConvolution(nhid2, nhid3, bias=True)
        self.gc6 = GraphConvolution(nhid3, nhid4, bias=True)
        # self.gc7 = GraphConvolution(nFeat, nhid2, bias=True)
        # self.gc8 = GraphConvolution(nhid2, nhid3, bias=True)
        # self.gc9 = GraphConvolution(nhid3, nhid4, bias=True)
        self.gc10 = GraphConvolution(nFeat, nhid2, bias=True)
        self.gc11 = GraphConvolution(nhid2, nhid3, bias=True)
        self.gc12 = GraphConvolution(nhid3, nhid4, bias=True)
        self.nhid4 = nhid4
        self.dropout = dropout
        # self.epoch = epoch
        self.dense1 = nn.Linear(nhid4, nclass, bias=1)
        self.dense2 = nn.Linear(nhid4, nclass, bias=1)
        self.dense3 = nn.Linear(nhid4, nclass, bias=1)
        self.dense4 = nn.Linear(nhid4, nclass, bias=1)
        self.simdense = nn.Linear(2 * nhid4, nclass, bias=1)
        self.linear1 = nn.Linear(nhid4, 15, bias=1)
        self.linear2 = nn.Linear(nhid4, 5, bias=1)
        self.linear3 = nn.Linear(nhid4, 15, bias=1)
        self.aggre1 = nn.Linear(nhid2, nclass, bias=1)
        self.aggre = nn.Linear(nhid3, nclass, bias=1)
        print("Adaboost model")

    def forward(self, x, adj1, adj2, adj3, adj4, adj5, y, index):
        # adj1: Identity
        # adj2: something we try before
        # adj3: Arrival-similarity
        # adj4: TrueSkill-similarity
        # adj5: Contrastive GCN
        # Identity
        x1 = F.relu(self.gc1(x, adj5))
        x1 = F.dropout(x1, self.dropout, training=self.training)
        x1 = F.relu(self.gc2(x1, adj5))
        x1 = self.gc3(x1, adj5)
        x1_dense = F.relu(x1)
        x1_dense = self.dense1(x1_dense)

        # TS-Similarity
        x2 = F.relu(self.gc4(x, adj4))
        x2 = F.dropout(x2, self.dropout, training=self.training)
        x2 = F.relu(self.gc5(x2, adj4))
        x2 = self.gc6(x2, adj4)
        x2_dense = F.relu(x2)
        x2_dense = self.dense2(x2_dense)

        # A-Similarity
        x3 = F.relu(self.gc4(x, adj3))
        x3 = F.dropout(x3, self.dropout, training=self.training)
        x3 = F.relu(self.gc5(x3, adj3))
        x3 = self.gc6(x3, adj3)
        x3_dense = F.relu(x3)
        x3_dense = self.dense3(x3_dense)

        sim_dense = self.simdense(torch.cat((x2, x3), 1))
        """
        #alpha1, sub-adaboost
        temp1 = torch.exp(-torch.mul(x2_dense[index],y[index]))
        temp2 = torch.mul(x3_dense[index],y[index])
        sum1 = torch.sum(torch.masked_select(temp1,temp2.ge(0)))
        sum2 = torch.sum(temp1) - sum1
        alpha1 = 0.5*torch.log(torch.div(sum2,sum1))
        sim_dense = torch.add(x2_dense,torch.mul(x3_dense,alpha1))
        """
        # Contrastive
        x4 = F.relu(self.gc10(x, adj1))
        x4 = F.dropout(x4, self.dropout, training=self.training)
        x4 = F.relu(self.gc11(x4, adj1))
        x4 = self.gc12(x4, adj1)
        x4_dense = F.relu(x4)
        x4_dense = self.dense4(x4_dense)

        # alpha2, top-adaboost
        temp3 = torch.exp(-torch.mul(x4_dense[index], y[index]))
        temp4 = torch.mul(sim_dense[index], y[index])
        sum3 = torch.sum(torch.masked_select(temp3, temp4.ge(0)))
        sum4 = torch.sum(temp3) - sum3
        alpha2 = 0.5 * torch.log(torch.div(sum3, sum4))

        part1_dense = torch.add(x4_dense, torch.mul(sim_dense, alpha2))

        # alpha3, top-adaboost
        temp5 = torch.exp(-torch.mul(part1_dense[index], y[index]))
        temp6 = torch.mul(x1_dense[index], y[index])
        sum5 = torch.sum(torch.masked_select(temp5, temp6.ge(0)))
        sum6 = torch.sum(temp5) - sum5
        alpha3 = 0.5 * torch.log(torch.div(sum5, sum6))

        part2_dense = torch.add(part1_dense, torch.mul(x1_dense, alpha3))
        return x2_dense, x3_dense, part2_dense
