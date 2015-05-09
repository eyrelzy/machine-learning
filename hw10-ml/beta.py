'''
Created on Apr 13, 2015

@author: zhiyuel
'''
import sys

import math
from math import *


#computes log sum of two exponentiated log numbers efficiently
def log_sum(left,right):
    if right < left:
        return left + log1p(exp(right - left))
    elif left < right:
        return right + log1p(exp(left - right));
    else:
        return left + log1p(1)


def readObsSymbol(filename):
    obslist=[]
    with open(filename, 'r') as f:
        for line in f:
            line=line.strip('\n')
            obs=line.split(' ')
            obslist.append(obs)
    return obslist

def initPrior(filename):
    priors=[]
    with open(filename, 'r') as f:
        for line in f:
            line=line.strip('\n')
            elem=float(line.split(' ')[1])
            priors.append(elem)
    return priors
            
# PR VB RB NN PC JJ DT OT 
def initTransTable(filename, N):
    trans_table = [[0.0]*N for i in range(N)]
    cnt=0
    with open(filename, 'r') as f:
        for line in f:
            line=line.strip('\n')
            elems=line.split(' ')
            for i in xrange(1,len(elems)-1):
                trans_table[cnt][i-1]=float(elems[i].split(':')[1])
            cnt+=1 
    return trans_table   

def initEmitTable(filename, N):
    emit_table = [{} for i in range(N)]
#     print emit_table
    cnt=0
    with open(filename, 'r') as f:
        for line in f:
            line=line.strip('\n')
            elems=line.split(' ')
            for i in xrange(1,len(elems)-1):
                key=elems[i].split(':')[0]
                val=elems[i].split(':')[1]
                emit_table[cnt][key]=float(val)
            cnt+=1 
    return emit_table  

def backward(priors, trans_table, emit_table, obs_seq):
    N=len(priors)
    T=len(obs_seq)
    beta_table=[[math.log(1.0)]*T for i in range(N)]
    for col in xrange(T-2,-1,-1):
        for row in xrange(N):
            sum=0.0
            for r in xrange(N):
                tran=trans_table[row][r]
                bet=beta_table[r][col+1]
                bb=emit_table[r][obs_seq[col+1]]
                if r==0:
                    sum=math.log(tran)+bet+math.log(bb)
                else:
                    sum=log_sum(sum, (math.log(tran)+bet+math.log(bb)))
            beta_table[row][col]=sum
#     print beta_table
    pr=0.0
    for row in xrange(N):
        b=emit_table[row][obs_seq[0]]
        if row==0:
            pr=beta_table[row][0]+math.log(priors[row])+math.log(b)
        else:
            pr=log_sum(pr, beta_table[row][0]+math.log(priors[row])+math.log(b))
    print pr
#     print beta_table[0][1]

# <dev> <hmm-trans> <hmm-emit> <hmm-prior>
if __name__=='__main__':
    obfile=sys.argv[1]#'dev.txt'
    obslist=readObsSymbol(obfile)
    hmm_priorfile=sys.argv[4]#'hmm-prior.txt'
    priors=initPrior(hmm_priorfile)
#     print priors
    N=len(priors)
    hmm_trainfile=sys.argv[2]#'hmm-trans.txt'
    trans_table=initTransTable(hmm_trainfile, N)
#     print trans_table 
    hmm_emitfile=sys.argv[3]#'hmm-emit.txt'
    emit_table=initEmitTable(hmm_emitfile, N)
    
    O=len(obslist)
    for i in xrange(O):
        backward(priors, trans_table, emit_table,obslist[i])
    
    
    