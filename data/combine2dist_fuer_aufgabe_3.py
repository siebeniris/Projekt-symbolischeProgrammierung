import sys
def link2article():
    f=open('link2article.csv','r')
    mydict=dict()
    for line in f:
        line=eval(line)
        k,v = line[0],line[1]
        mydict[k]=v
    return mydict


def wiki2count():
    f=open('wiki2count.csv','r')
    mydict=dict()
    for line in f:
        line=eval(line)
        k,v = line[0],line[1]
        mydict[k]=v
    return mydict


wiki2countdist=wiki2count()
link2count=link2article()
combine2dist=dict()
for link, articles  in link2count.items():
    combine2dist[link] = dict()
    for v1 in articles:
        combine2dist[link]=(v1,wiki2countdist[v1])

with open('combine2dist.csv','w+') as file:
    sys.stdout=file
    for k,v in combine2dist.items():
        print([k,v])


