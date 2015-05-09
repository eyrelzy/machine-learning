'''
Created on Apr 4, 2015

@author: zhiyuel
'''
import math
import sys


def learnNBText(examples, q):
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
#                     N[flag]+=1

#     print NUM_CON
#     print NUM_LIB
#     print NUM_VOC
#     writeToFile(prob)
#     print N['con']
#     print N['lib']
#     print N['lib']+N['con']==NUM_VOC
    for token_key in prob:
        prob[token_key]['con']=calMap(prob[token_key]['con'], q, N['con'], NUM_VOC)
        prob[token_key]['lib']=calMap(prob[token_key]['lib'], q, N['lib'], NUM_VOC)

#     writeToFile(prob) ##
    return prob, NUM_CON, NUM_LIB


def calMap(pr,smoothing,n, voc):
    return float(pr+smoothing)/(n+voc)


def classifyNBText(doc,NUM_CON, NUM_LIB, prob):
    flag=''
    doc_nums=0
    cnt=0
    cprior=(float(NUM_CON)/(NUM_CON+NUM_LIB))
    lprior=(float(NUM_LIB)/(NUM_CON+NUM_LIB))
    with open(doc, 'r') as inputFileObj:
        for sfile in inputFileObj:
            doc_nums+=1
            sfile=sfile.strip('\n')
            if "con" in sfile:
                flag='con'
            else:
                flag='lib'
#             print sfile
            final_prob={'con':cprior,'lib':lprior}
            for token in open(sfile):
                token=token.strip('\n').lower()
                if prob.has_key(token):
                    final_prob['con']+=math.log(prob[token]['con'])
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


# def writeToFile(text):
#     with open('temp/myfile.test', 'w') as the_file:
#         the_file.write(str(text))

if __name__=="__main__":
    train_file=sys.argv[1]
    test_file=sys.argv[2]
    q=1
    (prob,NUM_CON, NUM_LIB)=learnNBText(train_file, q)
    classifyNBText(test_file, NUM_CON, NUM_LIB, prob)
            
