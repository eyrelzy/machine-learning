'''
Created on Feb 15, 2015

@author: zhiyuel
'''
import csv
import math
import sys
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
def inspect(filename):
    dataset=[]
    with open(filename,'rb') as f:
        lines=csv.reader(f)
        next(lines,None)
        ycnt=0
        for row in lines:
            dataset.append(row)
            if row[-1]=='yes' or row[-1]=='A':
                ycnt+=1
        print 'entropy: '+str(round(calEntropy(dataset),3))
        error_rate=float(min(ycnt,len(dataset)-ycnt))/len(dataset)
        print 'error: '+str(round(error_rate,2))

if __name__ == '__main__':
    inspect(sys.argv[1])        
