#!/usr/bin/python
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
# line = lines[0]

tokens=line.split(" ")
# print tokens
# for token in tokens:
# 	print token
ntokens=[]
for token in tokens:
	ntokens.append(token.lower())
res=list(sorted(set(ntokens)))
sys.stdout.write(','.join(res))