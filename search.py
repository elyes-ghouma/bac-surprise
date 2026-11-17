import winsound

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
    
def search(x1,x2,y1,y2):
    text=text_of((x1,y1,x2,y2))
    while not(verif(text)) and y1>100:
        text=text_of((x1,y1,x2,y2))
        y1-=20
    if y1<=100:
        print('Message Not Found')
    else:
        winsound.MessageBeep()
        print('Message Found')
    return text
