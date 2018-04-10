from collections import defaultdict

f=open('linkdist.txt','r')
wiki2count=defaultdict(int)
for line in f:
    count, artikel, link = line.split('\t', 2)
    wiki2count[artikel] += int(count)
#lst=[k for k in wiki2count.keys() if wiki2count.get(k)>=200]

with open('linkdist.txt','r') as f:
    for line in f:
        count,artikel,link=line.split('\t',2)
        if wiki2count.get(artikel)>=200:
            print(line.strip('\n'))

#output -> linkdist2.txt