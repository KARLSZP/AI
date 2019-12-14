# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:40:39 2019

@author: Karl
"""

import numpy as np


class NN(object):
    # DEBUGGING
    np.random.seed(1)

    # __init__()
    # ================================================================
    # @ func:
    #     class initialization
    # @ args:
    #   - num_sample: number of samples.
    #   - input_dim:  dimension of each sample, A.K.A.
    #                 number of features/attributes.
    #   - hidden_dim: dimension of the hidden layer.
    #   - output_dim: dimension of output.
    # ================================================================
    def __init__(
        self, num_sample,
        input_dim,
        hidden_dim,
        output_dim,
        init_method='He'
    ):
        self.num_sample = num_sample
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        self.params = self.init_params(
            input_dim, hidden_dim, output_dim, init_method)

    # ================================================================
    #   __m__         ___m____          __m___
    #  |     |  W1   |        |   W2   |      |
    # n|input| ---> h| hidden |  ---> y|output|
    #  |     |       |        |        |      |
    #   -----         --------          ------
    # ----------------------------------------------------------------
    # Accordingly:
    #   - input: (n x m)
    #   - W1:    (h x n)
    #     W1 x input + bias = hidden  --> (h x n) x (n x m) -> (h x m)
    #
    #   - hidden:(h x m)
    #   - W2:    (y x h)
    #     W2 x hidden + bias = output --> (y x h) x (h x m) -> (y x m)
    #
    #   - output:(y x m)
    # ----------------------------------------------------------------
    # Params:
    #   - W1:    (h x n)
    #   - W2:    (y x h)
    #   - bias1: (h x 1) (broadcast by numpy)
    #   - bias2: (y x 1) (broadcast by numpy)
    # ================================================================
    def init_params(self, n_input, n_hidden, n_output, method):

        # Init with np.randaom.randn(), which can be
        # reproduce with a fixed random seed.
        if method == 'Random':
            W1 = np.random.randn(n_hidden, n_input) * np.sqrt(2.0 / n_input)
            W2 = np.random.randn(n_output, n_hidden) * np.sqrt(2.0 / n_hidden)
            bias1 = np.random.randn(n_hidden, 1)
            bias2 = np.random.randn(n_output, 1)
        elif method == 'He':
            W1 = np.random.randn(n_hidden, n_input) * np.sqrt(2.0 / n_input)
            W2 = np.random.randn(n_output, n_hidden) * np.sqrt(2.0 / n_hidden)
            bias1 = np.random.randn(n_hidden, 1)
            bias2 = np.random.randn(n_output, 1)
        else:
            raise Exception("MethodError")

        params = {
            'W1': W1,
            'W2': W2,
            'b1': bias1,
            'b2': bias2
        }

        return params

    # forward_propagation()
    # ================================================================
    # @ func:
    #     forward propagation
    # @ args:
    #   - Input: Input matrix of shape (input_dim x num_sample).
    # @ return:
    #   - scaled_out: scaled output through activation (sigmoid).
    #   - cache:      cached middle outputs for following calculations.
    # ================================================================
    def forward_propagation(self, Input):

        # Retrieve parameters
        W1 = self.params['W1']
        W2 = self.params['W2']
        b1 = self.params['b1']
        b2 = self.params['b2']

        # Calculations

        # hidden layer
        hidden_net_out = np.dot(W1, Input) + b1
        hidden_scaled_out = np.tanh(hidden_net_out)

        # output
        net_out = np.dot(W2, hidden_scaled_out) + b2
        scaled_out = NN.sigmoid(net_out)

        cache = {
            'hidden_net_out':    hidden_net_out,
            'hidden_scaled_out': hidden_scaled_out,
            'net_out':           net_out,
            'scaled_out':        scaled_out
        }

        return scaled_out, cache


    # ================================================================
    # In binary classification problem, outputs are consider to be
    # {0, 1}, in this case, with MLE(maximum likelihood estimate),
    # the cost func. for one sample can be written in the form:
    #       J_i = output^label * (1 - output)^(1 - label)
    # Apply ln() func. on both side:
    #       J_i = label * ln(output) + (1-label) * ln(1-output)
    #
    # Actually, this kinda cost func. is also known as:
    # >>> Cross Entropy
    # ================================================================

    # compute_cost()
    # ================================================================
    # @ func:
    #     compute cost with cross entropy
    # @ args:
    #   - output: result of the last layer.
    #   - label:  actual value of the sample.
    #   - lambd:  L2 regularizer.
    # @ return:
    #   - cost:   corresponding cost.
    # ================================================================
    def compute_cost(self, output, label, lambd):

        # Get number of samples
        m = self.num_sample

        # compute cross entropy (Vectorized)
        cross_entropy = label*np.log(output) + (1-label)*np.log(1-output)

        # compute cost
        cost = - 1.0/m * np.sum(cross_entropy / self.output_dim)

        # To transfer rank-1 array into np.float64
        # E.g.: [[cost]] --> cost
        cost = np.squeeze(cost)

        # L2 Regularization
        W1 = self.params['W1']
        W2 = self.params['W2']
        L2_cost = 1.0 / m * lambd / 2 * \
            (np.sum(np.square(W1))+np.sum(np.square(W2)))
        cost += L2_cost

        return cost

    # backward_propagation()
    # ================================================================
    # @ func:
    #     compute gradients of each layer with backward steps
    # @ args:
    #   - cache: cache of results.
    #   - input: input data.
    #   - label: labels of samples.
    #   - lambd: L2 regularizer.
    # @ return:
    #   - grads: a dictionary of gradients.
    # ================================================================
    def backward_propagation(self, cache, input, label, lambd):

        # Get number of samples
        m = self.num_sample

        # Retrieve parameters
        W1 = self.params['W1']
        W2 = self.params['W2']

        # Retrieve middle outputs
        hidden_scaled_out = cache['hidden_scaled_out']
        scaled_out = cache['scaled_out']

        # Compute Partial Derivatives
        d_net_out = scaled_out - label
        d_W2 = 1.0/m * np.dot(d_net_out, hidden_scaled_out.T) + lambd / m * W2
        d_bias2 = 1.0/m * np.sum(d_net_out, axis=1, keepdims=True)
        # d_net_hidden = np.dot(W2.T, d_net_out) * NN.d_sigmoid(hidden_net_out)
        d_net_hidden = np.dot(W2.T, d_net_out) * \
            (1 - np.power(hidden_scaled_out, 2))
        d_W1 = 1.0/m * np.dot(d_net_hidden, input.T) + lambd / m * W1
        d_bias1 = 1.0/m * np.sum(d_net_hidden, axis=1, keepdims=True)

        grads = {
            'dW1': d_W1,
            'dW2': d_W2,
            'db1': d_bias1,
            'db2': d_bias2
        }

        return grads

    # update_params()
    # ================================================================
    # @ func:
    #     update parameters(weights and bias)
    # @ args:
    #   - grads: gradient dict. generated by backward propagation.
    #   - learning_rate: the rate for params. to decent by.
    # ================================================================
    def update_params(self, grads, learning_rate):

        # Retrieve parameters
        W1 = self.params['W1']
        b1 = self.params['b1']
        W2 = self.params['W2']
        b2 = self.params['b2']

        # Retrieve gradients
        dW1 = grads['dW1']
        db1 = grads['db1']
        dW2 = grads['dW2']
        db2 = grads['db2']

        # Gradient Desent
        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2

        # Update params
        self.params['W1'] = W1
        self.params['b1'] = b1
        self.params['W2'] = W2
        self.params['b2'] = b2

    # train()
    # ================================================================
    # @ func:
    #     train model with given hyperparameters
    # @ args:
    #   - trainloader: data loader.
    #   - learning_rate: the rate for params. to decent by.
    #   - L2_lambd: L2 regularizer.
    #   - epochs: the total epochs expected to train.
    #   - print_per_epoch: print results per [input] epoch(s).
    # @ return:
    #   - costs: a track of costs during the training precess.
    # ================================================================
    def train(self, trainloader, learning_rate=0.1,
              L2_lambd=0.1, epochs=1000, print_per_epoch=0):

        # Track the cost
        costs = []

        # Retrieve X: input, Y: label
        X = trainloader['X']
        Y = trainloader['Y']

        for epoch in range(epochs):
            # Forward propagation
            output, cache = self.forward_propagation(X)

            # Compute cost
            cost = self.compute_cost(output, Y, L2_lambd)

            # Backward propagation
            grads = self.backward_propagation(cache, X, Y, L2_lambd)

            # Update parameters
            self.update_params(grads, learning_rate)

            if print_per_epoch and epoch % print_per_epoch == 0:
                print("Cost after epoch: {:d}: {:5f}".format(epoch, cost))

            # Track the cost
            costs.append(cost)

        return costs

    # predict()
    # ================================================================
    # @ func:
    #     predict a new sample with trained params.
    # @ args:
    #   - input: new sample.
    #   - threshold: as a classifier, to classify sample by 
    #                judging the result with a threshold(default=0.5)
    #                into 0 or 1.
    # @ return:
    #   - predictions: the shape of the predictions: 
    #                   (output_dim, num_sample), 
    #                   where $output_dim actually stands for 
    #                   the number of  classes.
    # ================================================================
    def predict(self, input, threshold=0.5):
        # predictions is provided by forward_propagation
        # with trained parameters.
        output, _ = self.forward_propagation(input)

        # In binary classification problem, judge
        # if the output is larger than threshold.
        predictions = (output > threshold)
        return predictions.squeeze()

    # compute sigmoid function
    @staticmethod
    def sigmoid(x):
        return 1.0 / (1 + np.exp(-x))
