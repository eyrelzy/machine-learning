'''
Created on Jan 27, 2015

@author: zhiyuel
'''
#!/usr/bin/python
# counting words
import sys
# for i in range(len(sys.argv)):
#     print(sys.argv[i])

#read file could be wrapped into a function
devfile = sys.argv[1]
riskdict={"Gender":"","Age":"","Student?":"","PreviouslyDeclined?":"",
         "HairLength":"","Employed?":"","TypeOfColateral":"","FirstLoan":"","LifeInsurance":"","Risk":""}
risklist=["Gender","Age","Student?","PreviouslyDeclined?","HairLength",
          "Employed?","TypeOfColateral","FirstLoan","LifeInsurance","Risk"]
devdata=[]
uniquedev=[]
for line in open(devfile):
    line=line[:-2]
    attrs=line.split("\t")
    ndev={"Gender":"","Age":"","Student?":"","PreviouslyDeclined?":"",
         "HairLength":"","Employed?":"","TypeOfColateral":"","FirstLoan":"","LifeInsurance":"","Risk":""}
    for pair in attrs:
        pairs=pair.split(" ")
        ndev[pairs[0]]=pairs[1]
    if ndev not in devdata:
        uniquedev.append(ndev)
    devdata.append(ndev)


trainfile="9Cat-Train.labeled"
traindata=[]
uniquetrain=[]
for line in open(trainfile):
    line=line[:-2]
    attrs=line.split("\t")
    ntrain={"Gender":"","Age":"","Student?":"","PreviouslyDeclined?":"",
         "HairLength":"","Employed?":"","TypeOfColateral":"","FirstLoan":"","LifeInsurance":"","Risk":""}
    for pair in attrs:
        pairs=pair.split(" ")
        ntrain[pairs[0]]=pairs[1]
    if ntrain not in traindata:
        uniquetrain.append(ntrain)
    traindata.append(ntrain)
#step 1:
input_space=pow(2,len(riskdict.keys())-1)
print input_space
# print concept_space 
#step 2:2^512
# print len(str(pow(2,9)))
print len(str(pow(2,input_space)))

#step 3:
hypothesis_space=pow(3,len(riskdict.keys())-1)+1
print hypothesis_space


#step 4:
#say yes to null
hypothesis_file=open("partA4.txt","w")
hypothesis=["null","null","null","null","null",
            "null","null","null","null","null"]
for i,atrain in enumerate(traindata):
    #skip no
    if atrain[risklist[9]]=="high":
        index=0
        while(index<10):
            if(hypothesis[index]=="null"):
                if(atrain[risklist[index]] !="null"):
                    hypothesis[index]=atrain[risklist[index]]
            else:
                if(hypothesis[index]!="?" and hypothesis[index]!=atrain[risklist[index]]):
                    hypothesis[index]="?"
            index=index+1
#     print hypothesis
    if i%30==29 and i>0:
        #write into file
        index=0
        hypothesis_str=""
        while(index<9):
            hypothesis_str+=hypothesis[index]+"\t"
            index=index+1;
        hypothesis_str=hypothesis_str[:-1]
        hypothesis_file.write(hypothesis_str+"\n")        

misclassification_rate=0.0
classification_result=[]
for adev in devdata:
    index=0
    flag=False
    while(index<9):
        if hypothesis[index]=="?" or adev[risklist[index]]==hypothesis[index]:
            index=index+1
            continue
        else:
            flag=True
            break
    if flag==True:
        #print "low"
        classification_result.append("low")
        if adev[risklist[9]]!="low":
            misclassification_rate=misclassification_rate+1/float(len(devdata))
    else:
        #print "high"
        classification_result.append("high")
        if adev[risklist[9]]!="high":
            misclassification_rate=misclassification_rate+1/float(len(devdata))
print misclassification_rate
for result in classification_result:
    print result
