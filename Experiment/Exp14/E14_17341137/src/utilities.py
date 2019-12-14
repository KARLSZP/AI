# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:03:51 2019

@author: Karl
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nn import NN
from sklearn.preprocessing import StandardScaler


def load_data(path, sep=','):
    return pd.read_csv(path, sep=sep)


def placeholder(input, label):
    placeholder = {}
    placeholder['X'] = input
    placeholder['Y'] = label
    return placeholder


def Scaler():
    return StandardScaler()


def GridSearch(epochs, trainloader, testloader, num_sample, input_dim, OUTPUT_DIM, HIDDEN_DIMS, LRS, L2_LAMBD):
    best_params = {}
    best_acc = -1
    for hidden_dim in HIDDEN_DIMS:
        for LR in LRS:
            for lambd in L2_LAMBD:
                model = NN(num_sample, input_dim, hidden_dim,
                           OUTPUT_DIM, init_method='He')
                costs = model.train(trainloader, LR, lambd, epochs)
                acc = Accuracy(model.predict(
                    testloader['X']), testloader['Y'])
                if acc > best_acc:
                    best_acc = acc
                    best_params['hidden_dim'] = hidden_dim
                    best_params['learning_rate'] = LR
                    best_params['L2_lambd'] = lambd
                    best_params['costs'] = costs
                    best_params['params'] = model.params
                print('GridSearching: Hidden_dim: {:d}, Learning Rate: {:f}, L2 lambda: {:f} ---> Accuracy: {:f}.'.format(
                    hidden_dim, LR, lambd, acc))
    return best_params


def Accuracy(predictions, labels):
    # @ predictions, labels: (3 x num_samples)
    # @ Strategy:
    # Since the result should be a single '1' in one of 
    # the three vertical axes, the rest two of which should
    # be '0'. So, add up the predictions by axis = 1(vertically)
    # can tell us whether the classifier do a good job or not:
    #   - 1: good job, the classifier predict a class for the sample.
    #   - 2: bad, the classifier predict 2 classes for 1 sample.
    #   - 0/3: bad, the classifier didn't predict.
    # To ensure the accuracy to be fair enough, for those miss-predicted
    # situations, randomly place a '1' in one of the possible classes. 
    predicts = np.int64(predictions[0]) + predictions[1] + predictions[2]
    _class = -1

    # Go through and check for miss-predicted samples
    for idx, i in enumerate(predicts):
        # No selected possible class, randomly choose 1
        if i == 0 or i == 3:
            _class = np.random.randint(0, 3)
            predictions[:, idx] = 0
            predictions[_class, idx] = 1
        # Two selected possible classes, randomly choose 1
        elif i == 2:
            candidate = [0, 1, 2]
            for idy, j in enumerate(predictions):
                # The 'False' valued one is impossible class
                if j[idx] == False:
                    # remove from candidate list
                    candidate.remove(idy)
                    _class = candidate[np.random.randint(0, 2)]
                    candidate.remove(_class)
                    predictions[candidate[0], idx] = 0
                    predictions[_class, idx] = 1
                    break
    
    # SUM UP fixed predictions and labels, if:
    #   - correctly labeled: 0 + 0 = 0 or 1 + 1 = 2
    #   - incorrectly labeled: 0 + 1 = 1 or 1 + 0 = 1
    # so half of a total of '1' denote the miss-predicted
    # samples' number.
    res = list((predictions + labels).flatten())
    return (1 - (res.count(1) / (2 * len(labels[0]))))


def plot_costs_epoch(costs):
    plt.title('Costs - 100 Epochs')
    plt.xlabel('*100 Epochs')
    plt.ylabel('Costs')
    plt.plot(range(len(costs)), costs)
    plt.show()