
f0=open('linkdist.txt','r')
lstInput=[]
for line in f0:
    try:
        lstLine=line.replace('\n','').split('\t')
    except Exception as e:
        print(e)
        pass

    lstInput.append(lstLine)
f0.close()

#end of the loop
f1=open('linkdist.csv','w')
for line in lstInput:
    szWriteLine= ",".join(line)
    f1.write(szWriteLine+"\n")

f1.close()