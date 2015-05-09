#!/usr/bin/python
#counting words
import sys
# for i in range(len(sys.argv)):
#     print(sys.argv[i])
filename=sys.argv[1]
file=open(filename)
lines=file.readlines()
file.close()

line=lines[0]
if line[-1]=='\n':
	line=line[:-1]

tokens=line.split(" ")
# for token in tokens:
# 	print token
stopwords=[]
sfile=open(sys.argv[2])
for word in sfile.readlines():
	stopwords.append(word.split("\n")[0])
# for sline in sfile:
# 	stopwords.append(sline)
# print stopwords
ntokens=[]
dict={}

for token in tokens:
	if token.lower() in stopwords:
		continue
	if token.lower() in dict:
		dict[token.lower()]=dict[token.lower()]+1
	else:
		dict[token.lower()]=1
l = sorted(dict.iteritems(),key=lambda d:d[0],reverse=False)
#brown:1,dog:1,fox:1,jumps:1,lazy:1,over:1,quick:1,the:2
strs=''
for item in l:
    strs=strs+item[0]+':'+str(item[1])+','
sys.stdout.write(strs[:-1])
