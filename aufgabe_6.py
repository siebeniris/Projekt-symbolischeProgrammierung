from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
from collections import defaultdict,Counter

from nltk.stem.porter import *
import string

stemmer = PorterStemmer()
punct=set(string.punctuation)

def combine2dict():
    f=open('combine2dist.csv','r')
    combine2dist=dict()
    for line in f:
        line=eval(line)
        link, artikelset=line[0],line[1]
        combine2dist[link]=artikelset
    return combine2dist

combine2dist= combine2dict()

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

def ranking(inhalts_der_inquiry):
    tfdist = inquiry_dict(inhalts_der_inquiry)
    document_vector_dict = document_vector_dist(inhalts_der_inquiry)
    cosinedict = dict()
    for k, v in document_vector_dict.items():
        v1, v2 = tobevector(tfdist, v)
        cosinedict[k] = cossim(v1, v2)
    maxcosine_article = max(cosinedict, key=cosinedict.get)
    return (maxcosine_article,cosinedict[maxcosine_article])

def search(userinput):
    try:
        artikellst = []
        append = artikellst.append
        for k in combine2dist.keys():
                try:
                    if userinput in k:
                        append(combine2dist[k])
                except IndexError:
                    print(' ')
                    pass
        l = ([(x, y) for (x, y) in artikellst if not len(x) == 0 if not x =='{{FULLPAGENAME}}'])
        #find the most frequntly occured three article names.
        matchedarticle = (sorted(l, key=lambda x: x[1]))[-3:]
        articles=[x for (x,y) in matchedarticle]
        return articles
    except IndexError:
        return (userinput)
        pass

import sys
def interactive_Modie():
    s = input("Please input Your Query: ")
    if s=='':sys.exit()
    else:
        lst=st.tag(s.split())
        #[('Trump','P')....]
        for (x, y) in lst:
            if not y == 'O':
                try:
                    searched = search(x)
                    print(searched)
                    #[article1,article2,article3]
                    #['United States presidential election, 2008', 'Obama administration', 'Charles I of England']
                    resultls=[]
                    #speed up!
                    append=resultls.append
                    #iterate the found article list.
                    for x in searched:
                        inhalts_der_inqury = inhalt_des_documents(x.split())
                        articletuple=ranking(inhalts_der_inqury)
                        print(articletuple)
                        append(articletuple)
                    #[('Donald Rumsfeld ', '0.9806'),('Case citation ', '0.9939'),('Kurt Cobain ', '0.9978')]
                    resultls.sort(key=lambda x: float(x[1]))
                    print((resultls[-1])[0])
                    interactive_Modie()
                except Exception:
                    print('No match found!')
                    pass
                    interactive_Modie()


def batch_Modie(f,s):
    f1=open(f,'r')
    for line in f1:
        f2=open(s,'a+')
        sys.stdout=f2
        lst = st.tag(line.split())
        for (x, y) in lst:
            if not y == 'O':
                try:
                    searched = search(x)
                    resultls = []
                    append = resultls.append
                    for art in searched:
                        inhalts_der_inqury = inhalt_des_documents(art.split())
                        articletuple = ranking(inhalts_der_inqury)
                        append(articletuple)
                    resultls.sort(key=lambda x: float(x[1]))
                    print('[[',(resultls[-1])[0],'|',x,']]')
                except Exception:
                    print(x)
                    pass


if(len(sys.argv)==3):
    f,s=sys.argv[1],sys.argv[2]
    batch_Modie(f,s)
else:
    interactive_Modie()