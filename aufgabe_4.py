from nltk.tag import StanfordNERTagger
import sys

st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

def combine2dict():
    f=open('combine2dist.csv','r')
    combine2dist=dict()
    for line in f:
        line=eval(line)
        link, artikelset=line[0],line[1]
        combine2dist[link]=artikelset
    return combine2dist

combine2dist=combine2dict()

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
        matchedarticle = (sorted(l, key=lambda x: x[1]))[-1][0]
        return ("[[%s|%s]]"%(matchedarticle, userinput))

    except IndexError:
        return (userinput)
        pass

def work_on_inqury_line(s):
    lst = st.tag(s.split())
    l = []
    append = l.append
    for (x, y) in lst:
        if not y == 'O':
            searched = search(x)
            append(searched)
        else:
            append(x)
    print(' '.join([word for word in l]))


def interactive_Mode():
    s=input("Please input your Inqury: ")
    if s=='':sys.exit()
    else:
        work_on_inqury_line(s)
    interactive_Mode()

def batch_Mode(f,s):
    f1=open(f,'r')
    for line in f1:
        f2=open(s,'a+')
        sys.stdout = f2
        work_on_inqury_line(line)


if(len(sys.argv)==4):
    f,s=sys.argv[2],sys.argv[3]
    batch_Mode(f,s)
else: interactive_Mode()