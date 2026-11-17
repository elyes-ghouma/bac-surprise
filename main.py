import sys
from subprocess import run
from time import sleep
import winsound
from mailforw import check_mail

def fixe(ch):
    p=ch.find('\n')
    while p!=-1:
        ch=ch[:p]+' '+ch[p+1:]
        p=ch.find('\n')
    return ch

def mail_method():
    while not(check_mail()):
        print('No New SMS...')
        sleep(1)
    winsound.MessageBeep()
    run([sys.executable,'interface.py'])


def saisir_save_zone():
    moy=input('Saisir save moy : ')
    while not(moy.replace('.','',1).isdigit() and 0<float(moy)<21):
        moy=input('Saisir save moy : ')

    f=open('moy.txt','w')
    f.write(str(float(moy)+1))
    f.close()

#-----------------------------------------------------------------------------------------------

if __name__=='__main__':
    saisir_save_zone()
    print('Listening for New SMS')
    mail_method()
