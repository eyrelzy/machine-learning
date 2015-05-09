'''
Created on Jan 29, 2015

@author: zhiyuel
'''
#!/usr/bin/python
# counting words
import sys

devfile = sys.argv[1]
riskdict={"Gender":"","Age":"","Student?":"","PreviouslyDeclined?":"","Risk":""}
risklist=["Gender","Age","Student?","PreviouslyDeclined?","Risk"]
attrlist=[["Male","Female"],["Young","old"],["Yes","No"],["Yes","No"]]
devdata=[]
for line in open(devfile):
    line=line[:-2]
    attrs=line.split("\t")
    bitnum=0
    label=""
    for i,pair in enumerate(attrs):
        pairs=pair.split(" ")
        if pairs[0]=="Risk":
            label=pairs[1]
            break;
        if pairs[1]==attrlist[i][0]:
            bitnum=bitnum+(1<<i)
        else:
            bitnum=bitnum+(0<<i)
    devdata.append((bitnum,label))
# print devdata

trainfile="4Cat-Train.labeled"
traindata=[]
for line in open(trainfile):
    line=line[:-2]
    attrs=line.split("\t")
    bitnum=0
    label=""
    for i,pair in enumerate(attrs):
        pairs=pair.split(" ")
        if pairs[0]=="Risk":
            label=pairs[1]
            break;
        if pairs[1]==attrlist[i][0]:
            bitnum=bitnum+(1<<i)
        else:
            bitnum=bitnum+(0<<i)
    traindata.append((bitnum,label))
# print traindata    

counter=0
hightask=[]
lowtask=[]
for (num,risklabel) in traindata:
    counter=counter+1
    if risklabel=="high":
        hightask.append(num)
    else:
        lowtask.append(num)
#input space
print pow(2,4)
#concept space
print pow(2,16)
#version space
vs=pow(2,16-counter)
print vs
for instance in devdata:
    if instance[0] in set(hightask):
        print str(vs) + " " + str(0)
#         instance[1]
    elif instance[0] in set(lowtask):
        print str(0) + " " + str(vs)
    else:
        print str(vs/2) + " " +str(vs/2)



