from collections import defaultdict,Counter
from nltk.stem.porter import *
import string

stemmer = PorterStemmer()
punct=set(string.punctuation)

def idf(term):
    idfdist = dict()
    with open('idf.csv', 'r') as infile:
        for line in infile:
            try:
                term, idf = line.split('\t')
                idfdist[term] = float(idf)
            except Exception:
                pass
    return idfdist[term]

#tf: {article:{'term1',:10.2039202,'term2':10.023930},article2:{...}...}
def tf():
    tfdist=defaultdict(dict)
    with open('tf.csv','r') as infile:
        for line in infile:
            artikel,termdist=line.split('\t')
            termdist=eval(termdist)
            tfdist[artikel]=termdist
    return tfdist

tfdist=tf()

#v: a list of words.
def inhalt_des_documents(v):
    l = list(map(lambda x: x.lower(),v))
    s= [''. join(x for x in s if x not in punct)for s in l ]
    vi = [term for linktext in s for term in linktext.split(' ')]
    singles = [stemmer.stem(x) for x in vi]
    return singles

def inquiry_dict(inhalts_der_inqury):
    counter_inqury=Counter(inhalts_der_inqury)
    maxoccurences = max(counter_inqury.values())
    tfidf_inqury=dict()
    for k,v in counter_inqury.items():
        tfidf_inqury[k]=(v/maxoccurences)*idf(k)
    return tfidf_inqury

# ('obama', 'United States presidential election, 2008 ') 0.09803921568627451
def document_vector_dist(inhalts_der_inquiry):
    documentlst=[]
    for k, v in tfdist.items():
        for k1, v1 in tfdist[k].items():
            for term in inhalts_der_inquiry:
                    newdict = dict() # (term,doc) as key, tf as value.
                    if term == k1 and not k==' ':
                       newdict[(term,k)]=v1
                    documentlst.append(newdict)

    #documentlst=[{(term1,doc1):tf_term1},{(term2,doc2):tf_term2}...}
    tfidfdict=dict()
    for termdist in documentlst:
            for k,v in termdist.items():
                idf_x=idf(k[0]) # x of (x,y)
                tfidf=idf_x*termdist[k]
                tfidfdict[k]=tfidf
    #tfidfdict={document: [{obama,0.9834398},{trump,0.34839}....]}
    document_vector_dict=defaultdict(list)
    for k,v in tfidfdict.items():
        newdict=dict()
        newdict[k[0]]=v
        document_vector_dict[k[1]].append(newdict)

    #concatenate the dictionaries in document_vector_dict
    newdist=dict()
    for k,v in document_vector_dict.items():
        result={}
        for v1 in v:
            result.update(v1)
        newdist[k]=result
    return newdist


def tobevector(dict1,dict2):
    all_items=set(dict1.keys()).union(dict2.keys())
    vector1 = [dict1.get(k, 0) for k in all_items]
    vector2 = [dict2.get(k, 0) for k in all_items]
    return vector1,vector2


def cossim(v1,v2):
    import math
    dot_product=sum(n1*n2 for n1,n2 in zip(v1,v2))
    m1=math.sqrt(sum(n**2 for n in v1))
    m2=math.sqrt(sum(n**2 for n in v2))
    return '%.4f'% (dot_product/(m1*m2))

def ranking(inhalts_der_inqury):
    tfdist = inquiry_dict(inhalts_der_inqury)
    document_vector_dict = document_vector_dist(inhalts_der_inqury)
    cosinedict = dict()
    for k, v in document_vector_dict.items():
        v1, v2 = tobevector(tfdist, v)
        cosinedict[k] = cossim(v1, v2)
    maxcosine_article = max(cosinedict, key=cosinedict.get)
    return maxcosine_article

import sys
def interactive_Mode():
    s = input("Please input Your Query: ")
    if s=='':sys.exit()
    else:
        ls = s.split()
        inhalts_der_inquiry = inhalt_des_documents(ls)
        try:
            article=ranking(inhalts_der_inquiry)
            print(article)
        except Exception:
            print('No match found!')
            pass

    interactive_Mode()

def batch_Mode(f,s):
    f1=open(f,'r')
    lst = [line.split() for line in f1]
    for inquiry in lst:
        f2 = open(s, 'a+')
        sys.stdout = f2
        inquiry_content=inhalt_des_documents(inquiry)
        try:
            article=ranking(inquiry_content)
            print(inquiry,':',article)
        except Exception:
             print(inquiry,': None Matched')
             pass


if(len(sys.argv)==3):
    f,s = sys.argv[1],sys.argv[2]
    batch_Mode(f,s)
else: interactive_Mode()

