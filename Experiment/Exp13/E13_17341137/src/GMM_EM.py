# -*- coding: utf-8 -*-
"""
GMM-EM

Classifier with Gaussian Mixture Model(GMM),
using Expectation-Maximization algorithm(EM).

Name: Zhenpeng Song
ID:   17341137
Data:  Chinese Football Dataset wrt. 16 AFC football teams(2005-2018).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 1 LOAD DATA
# =============================================================================

## 
# Data_loader
# @Func:   Load data from file
# @params: file_path, seperator
# @return: train_data, convert_Dict
##
def Data_loader(path, sep=','):
    train_data = pd.read_csv(path, sep=' ')
    # map id to country name
    id2country = {idx: train_data['Country'][idx] for idx in train_data.index}
    # dataframe -> ndarrary
    train_data = np.array(train_data.drop('Country', 1))
    # Strategies:
    # 1. Obeserving the data, I found that the smaller the score was,
    #    the better the team played.
    # 2. In order to lower the dimension from 7 to 2,
    #    I took the two average scores as the final evaluation
    #    features(one for World Cup and one for Asian Cup).
    # 3. As a result, the X_train dataset will be of shape(16, 2).
    X_train = np.hstack(((np.sum(train_data[:, 0:3]/4, axis=1).reshape(-1, 1)),
                         (np.sum(train_data[:, 4:]/3, axis=1).reshape(-1, 1))))
    return X_train, id2country

# =============================================================================
# 2 GMM Definition
# =============================================================================


class EM(object):
    
    # __init__
    # @Func:   Initiate the model.
    # @params: Dataset, class number to classify to, sigma_regularizer
    # @return: NO RETURN
    def __init__(self, Data, num_class, sigma_reg=1):
        self.Data = Data
        self.num_class = num_class
        self.params = self.Init_params(sigma_reg)

    # mvGaussian
    # @Func:   Calculate the multivariate Gaussian probability.
    # @params: Data x, Average value mu, Covariance sigma
    # @return: The multivariate Gaussian probability.
    def mvGaussian(self, x, mu, sigma):
        # import dot() for multiplication between matrices,
        # power() for power calculation,
        # inv() for inverse calculation of sigma,
        # det() for determinant calculation of sigma.
        from numpy import dot, power
        from numpy.linalg import inv, det
        
        # n is the dimension of the features space,
        # in this case, n = 2
        n = x.shape[1]
        # nume denotes for numerator and deno denotes for denominator,
        # corresponding to the equation.
        nume = np.exp(-0.5*dot(dot((x-mu), inv(sigma)), (x-mu).T))
        deno = power(2 * np.pi, n / 2) * power(det(sigma), 0.5)
        return nume / deno

    # Init_params
    # @Func:   Initialize the parameters.
    # @params: sigma_regularizer
    # @return: Initialized parameters.
    def Init_params(self, sigma_reg):
        # m is the number of samples, n is the demension of features
        m, n = self.Data.shape
        num_class = self.num_class
        
        # Parameters:
        # alpha: the mixing coef. in GMM
        # mu   : the average vector.
        # sigma: the covariance matrix.
        # gamma: Of shape(m, k), represent the probability for sample m
        #        to be of category k.
        alpha = np.array([1.0/num_class for i in range(num_class)])
        mu = np.array([self.Data[i*(m//num_class)] for i in range(num_class)])
        sigma = np.array([sigma_reg*np.eye(n) for i in range(num_class)])
        gamma = np.zeros((m, num_class))
        return alpha, mu, sigma, gamma

    # E_step
    # @Func:   E step of EM algorithm.
    # @params: NO Parms.
    # @return: NO RETURN        
    def E_step(self):
        # m is the number of samples, n is the demension of features
        m, n = self.Data.shape
        num_class = self.num_class
        alpha, mu, sigma, gamma = self.params
        
        # Go through samples, calculate gamma
        # using bayes theory.
        for j in range(m):
            x = self.Data[j].reshape(1, n)
            deno = np.sum([alpha[i]*self.mvGaussian(x,mu[i],sigma[i]) for i in range(num_class)])
            for i in range(num_class):
                nume = alpha[i] * self.mvGaussian(x, mu[i], sigma[i])
                gamma[j][i] = nume / deno
        # Update parameters
        self.params = alpha, mu, sigma, gamma

    # M_step
    # @Func:   M step of EM algorithm.
    # @params: NO Parms.
    # @return: NO RETURN   
    def M_step(self):
        # m is the number of samples, n is the demension of features
        m, n = self.Data.shape
        x = self.Data
        num_class = self.num_class
        alpha, mu, sigma, gamma = self.params
        
        # Regularizer to avoid sigma becoming singular.
        regularizer = 0.1 * np.eye(n)
        
        # sum up gamma as the denominator in following calculations
        sum_gamma = np.sum(gamma, axis=0)
        # Go through classes, update parameters step by step.
        for i in range(num_class):
            # Since numpy will defaultly
            # set (x, 1)-like ndarray to (x,),
            # which is known as 'rank 1 array'
            # and does not support numpy broadcast,
            # use reshape() to fix it.
            tmp_gamma = gamma[:, i].reshape(-1,1)
            
            # Parameters Updating
            # mu
            mu[i] = np.sum(tmp_gamma*x, axis=0) / sum_gamma[i]
            # sigma
            nume_sigma = 0
            for j in range(m):
                nume_sigma += gamma[j, i] * (x[j] - mu[i]).T * (x[j] - mu[i])
            sigma[i] = nume_sigma / sum_gamma[i] + regularizer
            # alpha
            alpha[i] = sum_gamma[i] / m
        # Update parameters
        # (This step is not necessary since ndarray is passed by reference)
        self.params = alpha, mu, sigma, gamma

    # Norm_diff
    # @Func:   Calculate the norm-difference between two iters.
    # @params: pre: params in last iter., cur: params in current iter.
    # @return: the norm-difference.
    def Norm_diff(self, pre, cur):
        norm_diff = [np.linalg.norm(pre[i]-cur[i]) for i in range(len(pre))]
        return np.average(norm_diff)

    # clusteror
    # @Func:   Cluster the dataset by gamma
    # @params: gamma
    # @return: The clustered result as a dict.
    def clusteror(self, gamma):
        m, n = self.Data.shape
        # Initialize C as the clustered dictionary
        # C: sample_id: (sample_id, sample_class)
        C = {}
        # Simply, use np.argmax() to 
        # find the index of the largest element.
        for j in range(m):
            C[j] = (j, np.argmax(gamma[j]))
        return C
        
    # EM_method
    # @Func:   EM algorithm.
    # @params: Epsilon as a threshold for norm-difference, 
    #          MaxIter to limit the max epochs.
    # @return: Clustered result as a dictionary, final mu.
    def EM_method(self, Epsilon=5, MaxIter=500):
        # Track the params for debugging
        pre_params = []
        pre_params.append([attr.copy() for attr in self.params])
        norm_diff = np.inf
        
        while (norm_diff > Epsilon and MaxIter):
            MaxIter -= 1
            self.E_step()
            self.M_step()
            norm_diff = self.Norm_diff(pre_params[-1], list(self.params))
            pre_params.append([attr.copy() for attr in self.params])
            # print(norm_diff)
        return self.clusteror(self.params[-1]), self.params


# =============================================================================
# 3 Utilities
# =============================================================================

def plotter(ClusterDict, Centers, Data, convert_dict, num_class):
    colorset = ['red', 'blue', 'yellow', 'black', 'green']
    color = {i:colorset[i] for i in range(num_class)}
    fig = plt.figure(figsize=(9,6))
    ax = fig.add_subplot(111)
    for i in Centers:
        ax.scatter(i[0], i[1], s=100, c='green', marker='D')
    for i in ClusterDict:
        ax.scatter(Data[i][0], Data[i][1], color=color[ClusterDict[i][1]])
        ax.annotate(convert_dict[ClusterDict[i][0]],
                    xy=(Data[i][0], Data[i][1]),
                    xytext=(Data[i][0]+0.1, Data[i][1]+0.1))

    plt.title('Clustered Result')
    plt.xlim(10, 45)
    plt.ylim(0, 20)
    ax.set_xlabel('Appearance in WorldCup')
    ax.set_ylabel('Appearance in AsianCup')
    plt.show()


def displayParams(params):
    print("="*10+"Parameters:"+"="*10)
    print("Mu:")
    for idx, i in enumerate(params[1]):
        print("Mu[{:d}]: ".format(idx), i)
    print("Sigma:")
    for idx, i in enumerate(params[2]):
        print("Sigma[{:d}]:\n".format(idx), i)
    print("Gamma:")
    for idx, i in enumerate(params[3]):
        print("Gamma[{:2d}]: ".format(idx), i)
        

# =============================================================================
# 4 Run the model
# =============================================================================

FILE_PATH = './E13_dataset.csv'
SEP = ' '
NUM_CLASS = 3
SIGMA_REG = 1000
EPSILON = 5

if __name__ == '__main__':    
    X_train, id2country = Data_loader(FILE_PATH, SEP)
    Em = EM(X_train, NUM_CLASS, SIGMA_REG)
    ClusteredDict, params = Em.EM_method(EPSILON)
    plotter(ClusteredDict, params[1], X_train, id2country, NUM_CLASS)
    displayParams(params)
    