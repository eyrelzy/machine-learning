'''
Created on Apr 13, 2015

@author: zhiyuel
'''
import sys

import math
from math import *

state_dict={1:"PR",2:"VB",3:"RB",4:"NN",5:"PC",6:"JJ",7:"DT",8:"OT"}
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

def viterbi(priors, trans_table, emit_table, obs_seq):
    N=len(priors)
    T=len(obs_seq)
    vp_table=[[0.0]*T for i in range(N)]
    opt_seq=[[""]*T for i in range(N)]
    
    for row in xrange(N):
        b=emit_table[row][obs_seq[0]]
        pi=priors[row]
        vp_table[row][0]=math.log(b)+math.log(pi)
        opt_seq[row][0]=str(row)
    
    for col in xrange(1,T):
        for row in xrange(N):
            max=-float("inf")
            bb=emit_table[row][obs_seq[col]]
            for r in xrange(N):
                tran=trans_table[r][row]
                vp=vp_table[r][col-1]
                mul=math.log(tran)+math.log(bb)+vp
                if mul>max:
                    max=mul
                    opt_seq[row][col]=opt_seq[r][col-1]+str(row)
            vp_table[row][col]=max
    last=-float('inf')
    seq=""
    for row in xrange(N):
       if(last < vp_table[row][T-1]):
           last=vp_table[row][T-1]
           seq=opt_seq[row][T-1]
#     print last
    token=[]
    for index in seq:
        token.append(state_dict[int(index)+1])
    ret=""  
    for i in xrange(T):
        ret+=obs_seq[i]+"_"+token[i]+" "
    print ret
        
    
                
                

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
        viterbi(priors, trans_table, emit_table,obslist[i])
    
    
    