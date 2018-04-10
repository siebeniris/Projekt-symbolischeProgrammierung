from collections import defaultdict
import sys,csv

#create wiki2count dictionary
def wiki2count():
    f=open('linkdist.txt','r')
    wiki2count=defaultdict(int)
    for line in f:
        count, artikel, link = line.split('\t', 2)
        artikel=artikel.strip()
        wiki2count[artikel] += int(count)
    
    with open('wiki2count.csv','w+')as file:
         sys.stdout=file
         for k,v in wiki2count.items():
            print([k,v])
    

def link2article():
    f = open('linkdist.txt', 'r')
    link2article = defaultdict(list)
    for line in f:
        count, artikel, link = line.split('\t', 2)
        artikel = artikel.strip()
        link = link.strip()
        link2article[link].append(artikel)
    with open('link2article.csv','w') as file:
         sys.stdout=file
         for k,v in link2article.items():
            print([k,v])



wiki2count()
link2article()


