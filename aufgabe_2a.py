import nltk
import sys



f=open('output.txt','r')

# wichtig: dist!!!!!*******************
dist = dict() #{linktext:{wikipediaartikelname:vorkommen}}
fdist=nltk.FreqDist()
fdist.update(f)
#pprint(fdist)

for k, v in fdist.items():
    k = k.rsplit('\t', 1)
    k[-1] = k[-1].strip('\n')
    #k[0] = k[0].strip()
    dist[k[-1]] = dict()
    dist[k[-1]][k[0]] = v

#aufgabe 2 a)
with open('linkdist.txt','w+') as file:
     sys.stdout = file
     for k,v in dist.items():
          for k1,v1 in dist[k].items():
              print(v1,'\t',k1,'\t',k)



# txt for linktext
# {linktext: vorkommen}
# linktextDist!
