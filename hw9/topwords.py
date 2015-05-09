'''
Created on Apr 4, 2015

@author: zhiyuel
'''

import sys

def learnNBText(examples):
    NUM_CON=0
    NUM_LIB=0
    NUM_VOC=0
    flag=""
    prob={}
    N={"con":0,"lib":0}
    with open(examples, 'r') as inputFileObj:
        for sfile in inputFileObj:
            sfile=sfile.strip('\n')
            if "con" in sfile:
                NUM_CON+=1
                flag="con"
            else:
                NUM_LIB+=1
                flag="lib"
            for token in open(sfile):
                token=token.strip('\n').lower()
                N[flag]+=1
                if prob.has_key(token):
                    prob[token][flag]+=1
                else:
                    NUM_VOC+=1
                    prob[token]={}
                    prob[token]['con']=0
                    prob[token]['lib']=0
                    prob[token][flag]=1

    for token_key in prob:
        prob[token_key]['con']=(float(prob[token_key]['con']+1))/(float(N['con']+NUM_VOC))
        prob[token_key]['lib']=(float(prob[token_key]['lib']+1))/(float(N['lib']+NUM_VOC))
    sortProb(prob)

def sortProb(prob):
    cdict={}
    ldict={}
    for token_key in prob:
        if prob[token_key].has_key('con'):
            cdict[token_key]=prob[token_key]['con']
        if prob[token_key].has_key('lib'):
            ldict[token_key]=prob[token_key]['lib']
    for token in sorted(ldict, key=ldict.get, reverse=True)[:20]:
        print token + " %.04f" % ldict[token]
        
    print 
    
    for token in sorted(cdict, key=cdict.get, reverse=True)[:20]:
        print token + " %.04f" % cdict[token]

if __name__=="__main__":
    train_file=sys.argv[1]
    learnNBText(train_file)