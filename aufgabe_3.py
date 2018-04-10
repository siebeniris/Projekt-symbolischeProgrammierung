# source : combine2dist.csv
# two modus: batch and interactive.
import sys
import time
start_time=time.time()

def combine2dist():
    f=open('combine2dist.csv','r')
    combine2dist=dict()
    for line in f:
        line=eval(line)
        link, artikelset=line[0],line[1]
        combine2dist[link]=artikelset
    return combine2dist

combine2dist=combine2dist()

def interactive_Modus():
    s = input('please input to search: ')
    if s=='':sys.exit()
    else:
        search(s)
    interactive_Modus()

def search(userinput):
    try:
        artikellst = []
        append = artikellst.append
        for k in combine2dist.keys():
            if userinput in k:
                        append(combine2dist[k])
        l = ([(x, y) for (x, y) in artikellst if not len(x) == 0 if not x =='{{FULLPAGENAME}}'])
        matchedarticle = (sorted(l, key=lambda x: x[1]))[-1][0]
        print(matchedarticle)

    except IndexError:
        print(' ')
        pass


def batch_modus(f,s):
    f1=open(f,'r')
    lst = [line.strip('\n') for line in f1]
    print(lst)
    for word in lst:
        f2 = open(s, 'a+')
        sys.stdout = f2
        search(word)


if(len(sys.argv)==4):
    f,s=sys.argv[2],sys.argv[3]
    batch_modus(f,s)
else: interactive_Modus()

print("---%s seconds---" % (time.time()-start_time))
