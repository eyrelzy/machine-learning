'''
Created on Apr 11, 2015

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

def forward(priors, trans_table, emit_table, obs_seq):
    N=len(priors)
    T=len(obs_seq)
    alpha_table=[[0.0]*T for i in range(N)]
#     print alpha_table
    
    for row in xrange(N):
        b=emit_table[row][obs_seq[0]]
        pi=priors[row]
#         alpha_table[row][0]=b*pi
        alpha_table[row][0]=math.log(b)+math.log(pi)
        #??math.log here?
#         print alpha_table[row][0]
#     print '============'+obs_seq[0]
    
    
    for col in xrange(1,T):
        for row in xrange(N):
#             alpha_table[row][col]=0.0
            sum=0.0
            bb=emit_table[row][obs_seq[col]]
            for r in xrange(N):
                tran=trans_table[r][row]
                alp=alpha_table[r][col-1]
#                 print math.log(tran)
#                 print alp #it's negative???
#                 print (math.log(tran)+math.log(alp))
#                 sum+=math.exp(math.log(tran)+alp)
                if r==0:
                    sum=(math.log(tran)+alp)
                else:
                    sum=log_sum(sum, (math.log(tran)+alp))
                
            alpha_table[row][col]=sum+math.log(bb)
#             print alpha_table[row][col]
#         print '============'+obs_seq[col]
    
    pr=0.0
    for row in xrange(N):
        if row==0:
            pr=alpha_table[row][T-1]
        else:
            pr=log_sum(pr,alpha_table[row][T-1])
    print pr
                
                

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
        forward(priors, trans_table, emit_table,obslist[i])
    
    
    