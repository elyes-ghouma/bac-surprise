def taille(f):
    s=0
    while f.readline()[:-1]!='':
        s+=1
    return s

def verif(msg):
    f=open('inst.txt','r')
    n=taille(f)
    f.close()

    test=True
    f=open('inst.txt','r')
    for i in range(n):
        ch=f.readline()[:-1]
        if ch!='Res' and ch!='Opt':
            test=test and (msg.find(ch)!=-1)
    f.close()

    return test 

