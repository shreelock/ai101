#CSE 537
#Clickstream Mining with Decision Trees
#Group 29
# Richard Sicol
# Haotian Wang

import csv
import argparse
import pickle as pkl
import math
from scipy import stats

'''
TreeNode represents a node in your decision tree
TreeNode can be:
    - A non-leaf node: 
        - data: contains the feature number this node is using to split the data
        - children[0]-children[4]: Each correspond to one of the values that the feature can take

    - A leaf node:
        - data: 'T' or 'F' 
        - children[0]-children[4]: Doesn't matter, you can leave them the same or cast to None.

'''


# DO NOT CHANGE THIS CLASS
class TreeNode():
    def __init__(self, data='T', children=[-1] * 5):
        self.nodes = list(children)
        self.data = data

    def save_tree(self, filename):
        obj = open(filename, 'w')
        pkl.dump(self, obj)


# loads Train and Test data
def load_data(ftrain, ftest):
    Xtrain, Ytrain, Xtest = [], [], []
    with open(ftrain, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int, row[0].split())
            Xtrain.append(rw)

    with open(ftest, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = map(int, row[0].split())
            Xtest.append(rw)

    ftrain_label = ftrain.split('.')[0] + '_label.csv'
    with open(ftrain_label, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rw = int(row[0])
            Ytrain.append(rw)

    print('Data Loading: done')
    return Xtrain, Ytrain, Xtest



# *** Load data from CSV files. ***
parser = argparse.ArgumentParser()
parser.add_argument('-p', required=True)
parser.add_argument('-f1', help='training file in csv format', required=True)
parser.add_argument('-f2', help='test file in csv format', required=True)
parser.add_argument('-o', help='output labels for the test dataset', required=True)
parser.add_argument('-t', help='output tree filename', required=True)

args = vars(parser.parse_args())

pval = args['p']
Xtrain_name = args['f1']
Ytrain_name = args['f1'].split('.')[0]+ '_labels.csv' #labels filename will be the same as training file name but with _label at the end

Xtest_name = args['f2']
Ytest_predict_name = args['o']

tree_name = args['t']

Xtrain, Ytrain, Xtest = load_data(Xtrain_name, Xtest_name)
initAttributes = [i for i in range(0,len(Xtrain[0]))]
initPartition = [x for x in range(0,len(Xtrain))]

# *** ID3 Algorithm Methods ***

#Get entropy given attribute.
def getAttributeEntropy(attribute, X, Y, partition):
    entropy = 0
    #Assume attribute can be 5 values.
    for value in range(1,6):
        numValues = 0
        numTrues = 0
        numFalses = 0
        #Check only the attribute in the current partition.
        for r in partition:
            if X[r][attribute] == value:
                numValues += 1
            if X[r][attribute] == value and Y[r] == 1:
                numTrues += 1
            if X[r][attribute] == value and Y[r] == 0:
                numFalses += 1

        if numValues == 0:
            continue
        #Calculate probability
        p = float(numValues)/len(partition)
        #Get target entropy.
        e = getTargetEntropy(numTrues, numFalses)
        #Sum entropy for this value.
        entropy += p*e

    return entropy

#Get entropy wrt target.
def getTargetEntropy(numTrues, numFalses):
    total = numTrues+numFalses
    pTrue = float(numTrues)/total
    pFalse = float(numFalses)/total
    if pTrue == 0 or pFalse == 0:
        return 0
    #Entropy calculation
    entropy = (- pTrue * math.log(pTrue,2)) + (- pFalse * math.log(pFalse,2))
    return entropy

#Calculates information gain (entropy loss) for each attribute and returns them all in a dictionary.
def getGains(attributes,X,Y, partition):
    if len(partition) == 0:
        return  {}
    t, f = countLabels(Y, partition)
    #First get current target entropy, this is the 'before' entropy.
    entropyBefore = getTargetEntropy(t, f)
    gains = {}
    for i in attributes:
        #Then get 'after' entropy for each attribute.
        entropyAfter = getAttributeEntropy(i, X, Y, partition)
        gains[i] = (entropyBefore - entropyAfter)
    return gains

#Splits the dataset into multiple partitions for each value.
def splitDataset(attribute, attributes, X, partition):
    #Make copy to avoid referencing.
    attributes = list(attributes)
    #Remove the attribute which we split on.
    index = attributes.index(attribute)
    attributes.pop(index)

    #Build the partitions for each value of the attribute.
    partitions = []
    for value in range(1, 6):
        partitions.append([r for r in partition if X[r][attribute] == value])
    return attributes, partitions

#Chi Split Stop test. We compute pValue for the current split and compare it to pValue threshold.
#If our pValue exceeds the threshold we stop the split which results in the tree being pruned.
def chiStop(Y,partitions):
    m = 0
    S = 0.0
    
    p = float(0)
    n = float(0)

    for partition in partitions:
        temp_p, temp_n = countLabels(Y, partition)
        p += temp_p
        n += temp_n
    Num = n + p

    #Calculate the statistic, S using Chi Squared
    for partition in partitions:
        if len(partition) == 0:
            continue
        m+=1
        pi, ni = countLabels(Y, partition)
        pi = float(pi)
        ni = float(ni)
        Ti = len(partition)
        pi_ = p * Ti / Num
        ni_ = n * Ti / Num
        #Chi Squared
        S += (pow((pi_-pi),2)/pi_ + pow((ni_-ni),2)/ni_)

    #Calculate observed pValue from statistic with m-1 degrees of freedom.
    pValue = 1.0-stats.chi2.cdf(S , m-1)

    #If our pValue is > the pval threshold we stop split.
    #When the pval threshold is 1, the entire tree will be generated.
    return pValue > float(pval)

#Count true/false negative labels given a partition.
def countLabels(Y,partition):
    t = 0
    f = 0
    for p in partition:
        if Y[p] == 1:
            t += 1
        else:
            f += 1
    return t,f

#The recursive ID3 Algorithm.
#Note: X and Y don't change. They represent the data (X) and the target labels (Y)
#We use 'partition' to decide which rows in X and Y are important when splitting.
#Lastly, attributes represents the currently available attributes.
def ID3(attributes, X,Y, partition):
    #First count current labels.
    t,f = countLabels(Y,partition)

    # If no data left.
    if len(partition) == 0:
        return TreeNode(data='F')

    #If branch is all 1s.
    if f == 0:
        return TreeNode(data='T')

    # If branch is all 0s
    if t == 0:
        return TreeNode(data='F')

    # If no attributes left.
    if len(attributes)==0:
        if (t > f):
            return TreeNode(data='T')
        else:
            return TreeNode(data='F')


    #Calculate the gains for each attribute.
    gains = getGains(attributes, X, Y, partition)
    #print(gains)
    
    #pick best attribute
    attribute = max(gains, key=gains.get)
    #Prune for the case where there was no information gain.
    if (gains[attribute] == 0):
        if (t > f):
            return TreeNode(data='T')
        else:
            return TreeNode(data='F')
    
    #split data and remove attribute.
    newAttributes, partitions = splitDataset(attribute, attributes, X, partition)

    #Check chi stop split condition.
    if chiStop(Y, partitions):
        if (t > f):
            return TreeNode(data='T')
        else:
            return TreeNode(data='F')

    #Create a node with attribute.
    #Recurse down partitions.
    newNode = TreeNode(data=attribute)
    for i in range(0, len(partitions)):
        newNode.nodes[i] = ID3(newAttributes, X, Y,partitions[i])
    return newNode


#Utility method for printing tree.
def displayTree(node, i):

    string = '   '*i+str(node.data)+'\n'
    size = 1
    if node.data == 'T' or node.data == 'F':
        return string,size

    for child in node.nodes:
        st, sz = displayTree(child,i+1)
        string += st
        size += sz
    return string, size


#Predicts label of the feature vector.
def evaluate_datapoint(root,datapoint):
    if root.data == 'T': return 1
    if root.data =='F': return 0
    return evaluate_datapoint(root.nodes[datapoint[int(root.data)-1]-1], datapoint)

print("Training...")

s = ID3(initAttributes, Xtrain, Ytrain, initPartition)
#treeShape, treeSize = displayTree(s,0)
#print(treeShape)
#print('Size: '+str(treeSize))

s.save_tree(tree_name)


print("Testing...")
Ypredict = []
for i in range(0,len(Xtest)):
    Ypredict.append([evaluate_datapoint(s, Xtest[i])])


with open(Ytest_predict_name, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(Ypredict)
print("Output files generated")