# coding: utf-8
from __future__ import unicode_literals
from collections import defaultdict,Counter
from nltk.stem.porter import *

import string,sys

stemmer = PorterStemmer()
f=open('linkdist.txt','r')
punct=set(string.punctuation)

artikeldist=defaultdict(list)
for line in f:
    line=line.split('\t',2)
    artikelname=line[1].strip()
    linktext=line[2].strip()
    artikeldist[artikelname].append(linktext)


def inhalt_des_documents(v):
    l = list(map(lambda x: x.lower(),v))
    s= [''. join(x for x in s if x not in punct)for s in l ]
    vi = [term for linktext in s for term in linktext.split(' ')]
    singles = [stemmer.stem(x) for x in vi]
    return singles


d=dict()
for document, inhalt in artikeldist.items():
    singles = inhalt_des_documents(inhalt)
    d[document]=singles

# d.items() --> artikeldist.txt
Number_of_all_Documents= len(d.keys())


#number of documents that contain term.
def number_of_documents_contain_term(t):
    count = 0
    for v in d.values():
        if t in v:
            count+=1
    return count



def idf(term):
    import math
    return math.log((Number_of_all_Documents+1)/(number_of_documents_contain_term(term)+1))

def idf_csv():
    termset=set()
    for v in d.values():
        termset.update(v)
    with open('idf.csv','w') as f:
        sys.stdout=f
        for term in termset:
            print(term,'\t',idf(term))

def tf_csv():
    tfdict = defaultdict(list)
    for k, v in d.items():
        counts = Counter(v)
        maxvalue = max(counts.values())
        innerdict=dict()
        for t in v:
            tf = (counts[t] / maxvalue)
            innerdict[t]=tf
        tfdict[k] = innerdict
    with open('tf.csv','w') as file:
        sys.stdout=file
        for k,v in tfdict.items():
             print(k,'\t',v)



#tf_csv()
idf_csv()
