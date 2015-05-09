'''
Created on Apr 4, 2015

@author: zhiyuel
'''
import math
import sys


def learnNBText(examples, freq_words):
    NUM_CON=0
    NUM_LIB=0
    NUM_VOC=0
    flag=""
    prob={}
    tempCon={}
    tempLib={}
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
    
#     print NUM_VOC
#     print N
#     print len(prob)
    for token_key in prob:
        tempCon[token_key]=(float(prob[token_key]['con']+1))/(N['con']+NUM_VOC)
        tempLib[token_key]=(float(prob[token_key]['lib']+1))/(N['lib']+NUM_VOC)
    
    sortProb(tempCon,tempLib, freq_words, prob, N)
    NUM_VOC-=freq_words
        
    for token_key in prob:
        prob[token_key]['con']=(float(prob[token_key]['con']+1))/(float(N['con']+NUM_VOC))
        prob[token_key]['lib']=(float(prob[token_key]['lib']+1))/(float(N['lib']+NUM_VOC))
#     print len(prob)
    return (prob, NUM_CON, NUM_LIB)


def sortProb(tempCon, tempLib, freq_words, prob, N):
    all_dict={}
    for token_key in tempCon:
        all_dict[token_key]=tempCon[token_key]+tempLib[token_key]
    for token in sorted(all_dict, key=all_dict.get, reverse=True)[:freq_words]:
        N['con']-=prob[token]['con']
        N['lib']-=prob[token]['lib']
        prob.pop(token, None)

#         print token + " %.04f" % all_dict[token]




def classifyNBText(doc,NUM_CON, NUM_LIB, prob):
    flag=''
    doc_nums=0
    cnt=0
    cprior=math.log(float(NUM_CON)/(NUM_CON+NUM_LIB))
    lprior=math.log(float(NUM_LIB)/(NUM_CON+NUM_LIB))
    with open(doc, 'r') as inputFileObj:
        for sfile in inputFileObj:
            doc_nums+=1
            sfile=sfile.strip('\n')
            if sfile[0:3]=="con":
                flag='con'
            else:
                flag='lib'
            final_prob={'con':cprior,'lib':lprior}
            for token in open(sfile):
                token=token.strip('\n').lower()
                if prob.has_key(token):
                    if prob[token].has_key('con'):
                        final_prob['con']+=math.log(prob[token]['con'])
                    if prob[token].has_key('lib'):
                        final_prob['lib']+=math.log(prob[token]['lib'])

            if final_prob['con']>final_prob['lib']:
                print 'C'
                if flag =='con':
                    cnt+=1
            else:
                print 'L'
                if flag =='lib':
                    cnt+=1
                
        precision=float(cnt)/doc_nums
        print "Accuracy: %.04f" % precision
#             print final_prob['con']
#             print final_prob['lib']


def writeToFile(text):
    with open('temp/myfile.test', 'w') as the_file:
        the_file.write(str(text))

if __name__=="__main__":
    train_file=sys.argv[1]
    test_file=sys.argv[2]
    freq_words=int(sys.argv[3])
    (prob, NUM_CON, NUM_LIB)=learnNBText(train_file, freq_words)

    classifyNBText(test_file, NUM_CON, NUM_LIB, prob)
            
