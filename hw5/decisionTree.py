'''
Created on Feb 15, 2015

@author: zhiyuel
'''
import math
import sys
import csv
edu=['P2', 'P3', 'P1', 'P4', 'F', 'grade', 'M5', 'M4', 'M1', 'M3', 'M2']
def buildLabelDict(labels):
    label_dict={}
    for i,label in enumerate(labels):
        label_dict[label]=i
    return label_dict

def createDataSet(filename):
    return readfile(filename)
#read csv file
def readfile(filename):
    traindata=[]
    with open(filename,'rb') as f:
        lines=csv.reader(f)
        labels=list(next(lines, None))
        for row in lines:
            traindata.append(row)
    f.close()
    return traindata,labels

def calDistribution(dataset):
    labels={}
    for vec in dataset:
        cur_label=vec[-1]
        if cur_label in labels:
            labels[cur_label]+=1
        else:
            labels[cur_label]=1
    return labels

def calEntropy(dataset):
    num_entry=len(dataset)
    labels={}
    for vec in dataset:
        cur_label=vec[-1]
        if cur_label in labels:
            labels[cur_label]+=1
        else:
            labels[cur_label]=1
    entropy=0.0
    for key in labels:
        prob=float(labels[key])/num_entry
        entropy-=prob*math.log(prob,2)
    return entropy

def splitData(f,i,dataset):
    subdata=[]
    for data in dataset:
        if data[i]==f:
            reduced=data[:i]
            # del col i
            reduced.extend(data[i+1:])
            subdata.append(reduced)
    return subdata

def selAttr(dataset):
    numFeatures=len(dataset[0])-1
    baseEntropy=calEntropy(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featureList=[]
        for instance in dataset:
            featureList.append(instance[i])
        condEntropy=0.0
        for feature in set(featureList):
            subData=splitData(feature, i, dataset)
            prob = float(len(subData))/len(dataset)
            subEntropy=calEntropy(subData);
            condEntropy += prob*subEntropy
        gain=baseEntropy-condEntropy
        if gain>=0.1 and gain>bestInfoGain:
            bestInfoGain=gain
            bestFeature=i
    return bestFeature

def majorityVote(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    if classCount[classCount.keys()[0]]>classCount[classCount.keys()[1]]:
        return classCount.keys()[0]
    else:
        return classCount.keys()[1]

def createTree(dataset, labels, depth):
    classList = [instance[-1] for instance in dataset]
    if classList.count(classList[0]) ==len(classList):
        return classList[0]
    if len(dataset[0])==1:
        return majorityVote(classList)
    if depth==0:# prune branches
        return majorityVote(classList)
    bestFeature = selAttr(dataset)
    if bestFeature==-1: #gain<0.1
        return majorityVote(classList)
    bestFeatureLabel = labels[bestFeature]
    dTree={bestFeatureLabel:{}}
    del(labels[bestFeature])
    featurelist=[]
    for instance in dataset:
        featurelist.append(instance[bestFeature])
    for feature in set(featurelist):
        subLabels = labels[:] # deep copy
        subdata=splitData(feature, bestFeature, dataset)
        dTree[bestFeatureLabel][feature]=createTree(subdata, subLabels, depth-1)
    return dTree

def displayDistribution(dataset):
    classList = [example[-1] for example in dataset]
    index=len(dataset[0])-1
    return "["+str(classList.count(yesNo[index]["yes"]))+"+/"+str(classList.count(yesNo[index]["no"]))+"-]"

def formatOutput(dTree,traindata,label_dict, yesNo):
    print displayDistribution(traindata)
    if isinstance(dTree, dict):
        root=dTree.keys()
        if len(root)==1:
            index=label_dict[root[0]]
            yfeatList = []
            nfeatList = []
#             displayDistribution(traindata)
            for data in traindata:
                if data[index] ==yesNo[index]["yes"]:
                    yfeatList.append(data)
                else:
                    nfeatList.append(data)
            print root[0] +" = " + yesNo[index]["yes"]+": "+ displayDistribution(yfeatList)
            yes=dTree[dTree.keys()[0]][yesNo[index]["yes"]]
            if isinstance(yes, dict):
                child = yes.keys()
                if len(child)==1:
                    cindex=label_dict[child[0]]
                    yc=[]
                    nc=[]
                    for data in yfeatList:
                        if data[cindex] ==yesNo[cindex]["yes"]:
                            yc.append(data)
                        else:
                            nc.append(data)
                    if len(yc)>0:
                        print "| "+child[0]+" = " + yesNo[cindex]["yes"]+": "+ displayDistribution(yc)
                    else:
                        print "| "+child[0]+" = " + yesNo[cindex]["yes"]+": "+ "[0+/0-]"
                    if len(nc)>0:
                        print "| "+child[0]+" = " + yesNo[cindex]["no"]+": "+displayDistribution(nc)
                    else:
                        print "| "+child[0]+" = " + yesNo[cindex]["no"]+": "+"[0+/0-]"
               
            print root[0]+" = " + yesNo[index]["no"]+": "+ displayDistribution(nfeatList)
            no = dTree[dTree.keys()[0]][yesNo[index]["no"]]
            if isinstance(no, dict):
                child = no.keys()
                if len(child)==1:
                    cindex=label_dict[child[0]]
                    yc=[]
                    nc=[]
                    for data in nfeatList:
                        if data[cindex] ==yesNo[cindex]["yes"]:
                            yc.append(data)
                        else:
                            nc.append(data)
                    if len(yc)>0:
                        print "| "+child[0]+" = " + yesNo[cindex]["yes"]+": "+ displayDistribution(yc)
                    else:
                        print "| "+child[0]+" = " + yesNo[cindex]["yes"]+": "+ "[0+/0-]"
                    if len(nc)>0:
                        print "| "+child[0]+" = " + yesNo[cindex]["no"]+": "+ displayDistribution(nc)
                    else:
                        print "| "+child[0]+" = " + yesNo[cindex]["no"]+": "+"[0+/0-]"

def evaluateInstance(dTree,testdata,label_dict, yesNo):
    ans=testdata[-1]
    if isinstance(dTree, dict):
        root=dTree.keys()
        if len(root)==1:
            rlabel=root[0]
            rindex=label_dict[rlabel]
            if isinstance(dTree[rlabel][testdata[rindex]], dict):
                child=dTree[rlabel][testdata[rindex]].keys()
                clabel=child[0]
                cindex=label_dict[clabel]
                pre=dTree[rlabel][testdata[rindex]][clabel][testdata[cindex]]
            else:
                pre=dTree[rlabel][testdata[rindex]]
    else:
        pre=dTree
    return pre==ans 

def evaluate(dTree, testdata,label_dict, yesNo):
    cnt=0
    for data in testdata:
        if evaluateInstance(dTree,data,label_dict,yesNo)==False:
            cnt+=1
    return float(cnt)/len(testdata)

def buildYesNo(labels):
    yesNo={}
    for i,l in enumerate(labels):
        if l in edu:
            yesNo[i]={'yes':"A",'no':"notA"}
        elif l=='year':
            yesNo[i]={'yes':"before1950",'no':"after1950"}
        elif l=='length':
            yesNo[i]={'yes':"morethan3min",'no':"lessthan3min"}
        elif l=='tempo':
            yesNo[i]={'yes':"fast",'no':"no"}
        elif l=='buying':
            yesNo[i]={'yes':"expensive",'no':"cheap"}
        elif l=='maint':
            yesNo[i]={'yes':"high",'no':"low"}
        elif l=='boot':
            yesNo[i]={'yes':"small",'no':"large"}
        elif l=='safety':
            yesNo[i]={'yes':"low",'no':"high"}
        elif l=='doors' or l=='person':
            yesNo[i]={'yes':"Two",'no':"MoreThanTwo"}
        else:
            yesNo[i]={'yes':'yes','no':'no'}
    return yesNo

if __name__ == '__main__':
    traindata,labels=createDataSet(sys.argv[1])
    label_dict=buildLabelDict(labels)
    yesNo = buildYesNo(labels)
    testdata,tlabels=createDataSet(sys.argv[2])
    # create decision tree
    dTree=createTree(traindata, labels, 2)
    formatOutput(dTree,traindata,label_dict, yesNo)
    print "error(train): "+str(evaluate(dTree, traindata,label_dict,yesNo))       
    print "error(test): "+str(evaluate(dTree, testdata,label_dict,yesNo))       