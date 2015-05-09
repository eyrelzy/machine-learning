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

    for token_key in prob:
        prob[token_key]['con']=(float(prob[token_key]['con']+q))/(float(N['con']+q*NUM_VOC))
        prob[token_key]['lib']=(float(prob[token_key]['lib']+q))/(float(N['lib']+q*NUM_VOC))

    # writeToFile(prob) ##
    return prob, NUM_CON, NUM_LIB

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
                    if prob[token]['con']!=0:
                        final_prob['con']+=math.log(prob[token]['con'])
                    if prob[token]['lib']!=0:
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
    q=float(sys.argv[3])
    
    (prob,NUM_CON, NUM_LIB)=learnNBText(train_file, q)
    classifyNBText(test_file, NUM_CON, NUM_LIB, prob)
            
