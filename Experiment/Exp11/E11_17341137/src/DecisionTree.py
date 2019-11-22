import pickle as pk
import treePlotter as tp
import seaborn as sns
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

# Load Training set, Test set.
train_data_path = 'dataset/adult.data'
test_data_path = 'dataset/adult.test'

header = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
          'marital-status', 'occupation', 'relationship', 'race', 'sex',
          'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'Salaries']

train_data = pd.read_csv(train_data_path, names=header)
test_data = pd.read_csv(test_data_path, names=header)
test_data.drop(0, inplace=True)
test_data.reset_index(drop=True, inplace=True)

train_data.replace(' ?', np.nan, inplace=True)
train_data.fillna(train_data.mode().iloc[0], inplace=True)

test_data.replace(' ?', np.nan, inplace=True)
test_data.fillna(test_data.mode().iloc[0], inplace=True)


continuous_cols = ['age', 'fnlwgt', 'education-num',
                   'capital-gain', 'capital-loss', 'hours-per-week']

f, axes = plt.subplots(3, 2, figsize=(12, 9))
sns.kdeplot(train_data['age'], shade=True, ax=axes[0, 0])
sns.kdeplot(train_data['fnlwgt'], shade=True, ax=axes[0, 1])
sns.kdeplot(train_data['education-num'], shade=True, ax=axes[1, 0])
sns.kdeplot(train_data['hours-per-week'], shade=True, ax=axes[1, 1])
sns.kdeplot(train_data['capital-gain'], shade=True, ax=axes[2, 0])
sns.kdeplot(train_data['capital-loss'], shade=True, ax=axes[2, 1])
plt.show()

pos1 = int(len(train_data)/3)
pos2 = 2 * pos1
intervals = {}

for col in continuous_cols:
    print('Col:', col)
    i1 = sorted(train_data[col])[pos1]
    i2 = sorted(train_data[col])[pos2]
    intervals[col] = (range(0, i1+1), range(i1+1, i2+1),
                      range(i2+1, sorted(train_data[col])[len(train_data)-1]+1))
    print('Sections: [0 %d] [%d %d] [%d %d]' % (i1, i1+1, i2,
                                                i2+1, sorted(train_data[col])[len(train_data)-1]+1))


rev_intervals = {}
for k, v in intervals.items():
    tmp = {}
    for idx, r in enumerate(v):
        for i in r:
            tmp[i] = idx
    rev_intervals[k] = tmp

dsp_dict = {
    1: ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'],
    3: ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'],
    5: ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'],
    6: ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'],
    7: ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    8: ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'],
    9: ['Female', 'Male'],
    13: ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands']
}


def dsp2numlist(idx):
    return list(range(len(dsp_dict[idx])))


AttrSet = [
    (0, [0, 1, 2], 'age'),
    (1, dsp2numlist(1), 'workclass'),
    (2, [0, 1, 2], 'fnlwgt'),
    (3, dsp2numlist(3), 'education'),
    (4, [0, 1, 2], 'education-num'),
    (5, dsp2numlist(5), 'marital-status'),
    (6, dsp2numlist(6), 'occupation'),
    (7, dsp2numlist(7), 'relationship'),
    (8, dsp2numlist(8), 'race'),
    (9, dsp2numlist(9), 'sex'),
    (10, [0, 1, 2], 'capital-gain'),
    (11, [0, 1, 2], 'capital-loss'),
    (12, [0, 1, 2], 'hours-per-week'),
    (13, dsp2numlist(13), 'native-country')
]


train_label = [1 if val == ' >50K' else 0 for val in train_data['Salaries']]
train_input = []

for idx in range(len(train_data)):
    tmp = [dsp_dict[i].index(val.strip()) if int(i) in dsp_dict.keys()
           else rev_intervals[train_data.columns[i]].get(val, 2) for i, val in enumerate(train_data.iloc[idx][:-1])]
    train_input.append(tmp)

test_label = [1 if val == ' >50K.' else 0 for val in test_data['Salaries']]
test_input = []

for idx in range(len(test_data)):
    tmp = [dsp_dict[i].index(val.strip()) if int(i) in dsp_dict.keys()
           else rev_intervals[test_data.columns[i]].get(val, 2) for i, val in enumerate(test_data.iloc[idx][:-1])]
    test_input.append(tmp)


print(len(train_label))
print(len(train_input))
print(train_input[:2])

print(len(test_label))
print(len(test_input))
print(test_input[:2])


def Entropy(Data):
    # Labels were stored at tail of the data set.
    labels = [sample[-1] for sample in Data]
    # Use set() to remove duplicates
    types = set(labels)
    # To calculate Pr by Pr = sample_num / total_num
    types_counts = [labels.count(type) for type in types]
    probs = [prob/len(Data) for prob in types_counts]
    # Calculate final result
    return -np.sum(probs*np.log2(probs))


def Gain(Data, attr):
    # Get Entropy of current data
    entropy = Entropy(Data)
    # Get the position of current attribute
    attr_num = attr[0]
    # Get all possible values for current attribute
    attr_vals = attr[1]
    # Calculate weights and entropy for each branches
    entropys = [0 for val in attr_vals]
    weights = [0 for val in attr_vals]
    # Enumerates attr_vals
    for idx, val in enumerate(attr_vals):
        # for each value, general an subset to
        # help calculate its entropy.
        sub_data = []
        for sample in Data:
            # when the value on attr_num of a sample
            # equals to val, this sample should be
            # a member of set 'D^v'
            if sample[attr_num] == val:
                sub_data.append(sample)
                weights[idx] += 1
        entropys[idx] = Entropy(sub_data)
        weights[idx] /= len(Data)
    # Calculate the final result
    return entropy - np.sum(np.multiply(weights, entropys))


def Gini(Data):
    # Labels were stored at tail of the data set.
    labels = [sample[-1] for sample in Data]
    # Use set() to remove duplicates
    types = set(labels)
    # To calculate Pr by Pr = sample_num / total_num
    types_counts = [labels.count(type) for type in types]
    probs = [prob/len(Data) for prob in types_counts]
    # Calculate final result
    return 1 - np.sum(np.power(probs, 2))


def Gini_index(Data, attr):
    # Get Gini value of current data
    gini = Gini(Data)
    # Get the position of current attribute
    attr_num = attr[0]
    # Get all possible values for current attribute
    attr_vals = attr[1]
    # Calculate weights and entropy for each branches
    ginis = [0 for val in attr_vals]
    weights = [0 for val in attr_vals]
    # Enumerates attr_vals
    for idx, val in enumerate(attr_vals):
        # for each value, general an subset to
        # help calculate its entropy.
        sub_data = []
        for sample in Data:
            # when the value on attr_num of a sample
            # equals to val, this sample should be
            # a member of set 'D^v'
            if sample[attr_num] == val:
                sub_data.append(sample)
                weights[idx] += 1
        ginis[idx] = Gini(sub_data)
        weights[idx] /= len(Data)
    # Calculate the final result
    return np.sum(np.multiply(weights, ginis))


def chooseBestAttr(Data, Attrset, method='ID3'):
    # Initialization
    # Mind that for:
    # Gain info.: find arg_max, init to -1
    # Gini index: find arg_min, init to infinity.
    best_attr = Attrset[0]
    best_gain = -1
    best_gini = np.Inf
    # When 'ID3' is assigned or using default method
    if method == 'ID3':
        for attr_tuple in Attrset:
            gain = Gain(Data, attr_tuple)
            best_attr = attr_tuple if gain > best_gain else best_attr
            best_gain = gain if gain > best_gain else best_gain
        return best_attr
    # When 'CART' is assigned
    elif method == 'CART':
        for attr_tuple in Attrset:
            gini = Gini_index(Data, attr_tuple)
            best_attr = attr_tuple if gini < best_gini else best_attr
            best_gini = gini if gini < best_gini else best_gini
        return best_attr
    else:
        print('Unknown method!')
        return None


def splitData(Data, attr_num, attr_val):
    # Initialization
    sub_data = []
    # Enumerate Data
    for sample in Data:
        # When the value of sample equals to attr_val,
        # add the sample to sub_data
        if sample[attr_num] == attr_val:
            # new sub_data should not contain the chosen attribute
            sub_data.append(sample[:attr_num] + sample[attr_num+1:])
    return sub_data


def getMajority(Data):
    # Labels were stored at tail of the data set.
    labels = [sample[-1] for sample in Data]
    # Use set() to remove duplicates
    types = list(set(labels))
    # Counts each type.
    types_counts = [labels.count(type) for type in types]
    # Enumerate to find major label
    major = 0
    max_count = 0
    for idx, type_count in enumerate(types_counts):
        major = types[idx] if max_count < type_count else major
        max_count = type_count if max_count < type_count else max_count
    # Return the type which counts most.
    return str(major)

def GenerateTree(Data, Attrset, method='ID3'):
        # Labels were stored at tail of the data set.
    labels = [sample[-1] for sample in Data]

    # ================ Terminals Check =================
    # The following IF sentences will
    # determine if the node if a leaf.

    # 1# ALL the SAME labels
    if len(set(labels)) == 1:
        # LEAF node | value = any one of the same labels
        return str(labels[0])

    # 2# No Attributes left
    if len(Attrset) == 0:
        # LEAF node | value = the major label
        return getMajority(Data)

    # 3# Samples behave the same on Attrset
    flag = False
    for attr_tuple in Attrset:
        if len(set([sample[attr_tuple[0]] for sample in Data])) != 1:
            flag = True
            break
    if not flag:
        return getMajority(Data)

    # ============== Terminals Check Ends ===============

    # Choose the best attribute to split the data set by
    best_attr = chooseBestAttr(Data, Attrset, method)
    attr_num = best_attr[0]
    attr_vals = best_attr[1]
    attr_name = best_attr[2]
    for idx, attr in enumerate(Attrset):
        if attr[0] > attr_num:
            Attrset[idx] = (attr[0]-1, attr[1], attr[2])
    del(Attrset[Attrset.index(best_attr)])
    # Initialzation
    # Current Node is named with attr_num;
    # The empty dict., as its child,
    # will be fill in following steps.
    Node = {attr_name: {}}

    # Enumerate values of the best attributes
    for val in attr_vals:
        sub_data = splitData(Data, attr_num, val)
        if len(sub_data) == 0:
            return getMajority(Data)
        else:
            Node[attr_name][val] = GenerateTree(sub_data, Attrset[:], method)

    # Return the Node as the result
    return Node


def Classifier(DecisionTree, AttrSet, SampleData):
    root = list(DecisionTree.keys())[0]
    for attr_tuple in AttrSet:
        if root == attr_tuple[2]:
            key = SampleData[attr_tuple[0]]
    succ = DecisionTree[root][key]
    if isinstance(succ, dict):
        return Classifier(succ, AttrSet, SampleData)
    else:
        return succ

def Benchmarker(DecisionTree, AttrSet, testing_data, log=False):
    labels = [sample[-1] for sample in testing_data]
    res = []
    for sample in testing_data:
        res.append(Classifier(DecisionTree, AttrSet, sample[:-1]))
    check = [labels[idx] + int(res[idx]) for idx in range(len(testing_data))]
    if log:
        for idx in range(len(testing_data)):
            if idx % 1000 == 0:
                print(" T ", end='') if labels[idx] == int(
                    res[idx]) else print(" F ", end='')
                print('%5d: expected %d, classified to %d.' %
                      (idx, labels[idx], int(res[idx])))
        print("Total Accuracy: %.5f" % (1-check.count(1)/len(testing_data)))
    else:
        return 1 - check.count(1)/len(testing_data)


testing_data = [
    [0, 1, 1, 1],
    [1, 3, 5, 1],
    [3, 3, 3, 1],
    [3, 2, 2, 1],
    [2, 1, 6, 1],
    [0, 3, 3, 1],
    [1, 2, 4, 1],
    [1, 2, 2, 1],

    [0, 1, 6, 0],
    [1, 3, 4, 0],
    [1, 3, 3, 0],
    [0, 2, 3, 0],
    [2, 2, 2, 0],
    [0, 0, 1, 0],
    [1, 2, 3, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 1]
]

testing_attrset = [(0, [0, 1, 2, 3], '2nd'), (1, [0, 1, 2, 3],
                                              '3rd'), (2, [0, 1, 2, 3, 4, 5, 6], '4th')]

print('\n'+"*"*10+' Testing with ID3 '+"*"*10)
dt = GenerateTree(testing_data, testing_attrset[:])
tp.createPlot(dt)
Benchmarker(dt, testing_attrset, testing_data, True)

print('\n'+"*"*10+' Testing with CART '+"*"*10)
dt = GenerateTree(testing_data, testing_attrset[:], 'CART')
tp.createPlot(dt)
Benchmarker(dt, testing_attrset, testing_data, True)


# training data
print("Training Inputs:", train_input[:2])
print("Training Labels:", train_label[:2])
# combined
X_train = [data + [train_label[idx]] for idx, data in enumerate(train_input)]
print("Combined Training data:", X_train[:2], '\n')

# testing data
print("Testing Inputs:", test_input[:2])
print("Testing Labels:", test_label[:2])
# combined
X_test = [data + [test_label[idx]] for idx, data in enumerate(test_input)]
print("Combined Testing data:", X_test[:2], '\n')

# Attribute Set
print("Attribute Set:[index, domain, name]")

print('\n'+"*"*10+' Salary Data with ID3 '+"*"*10)
SalaryPredict_DT_ID3 = GenerateTree(X_train, AttrSet[:])
plt.subplots(figsize=(14, 12))
tp.createPlot(SalaryPredict_DT_ID3)
Benchmarker(SalaryPredict_DT_ID3, AttrSet, X_train, True)


print('\n'+"*"*10+' Salary Data with CART '+"*"*10)
SalaryPredict_DT_CART = GenerateTree(X_train, AttrSet[:], 'CART')
plt.subplots(figsize=(14, 12))
tp.createPlot(SalaryPredict_DT_CART)
Benchmarker(SalaryPredict_DT_CART, AttrSet, X_train, True)

print('\n'+"*"*10+' Testing Salary Data with ID3 '+"*"*10)
Benchmarker(SalaryPredict_DT_ID3, AttrSet, X_test, True)


with open('./DTmodel/SalaryPredict_DT_ID3.pkl', 'wb') as pkl:
    pk.dump(SalaryPredict_DT_ID3, pkl)

with open('./DTmodel/SalaryPredict_DT_CART.pkl', 'wb') as pkl:
    pk.dump(SalaryPredict_DT_CART, pkl)


with open('./DTmodel/SalaryPredict_DT_ID3.pkl', 'rb') as pkl:
    SalaryPredict_DT_ID3 = pk.load(pkl)

with open('./DTmodel/SalaryPredict_DT_CART.pkl', 'rb') as pkl:
    SalaryPredict_DT_CART = pk.load(pkl)

print('\n'+"*"*10+' Testing Salary Data with ID3 '+"*"*10)
Benchmarker(SalaryPredict_DT_ID3, AttrSet, X_test, True)
