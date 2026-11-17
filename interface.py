import tkinter as tk
from pickle import load,dump

#-------------------------------------

enr=dict(INS=int,Res=str,Moye=float,Algo=float,Math=float,STI=float,ScPh=float,Angl=float,Fran=float,Arab=float,Phil=float,EdPh=float,Opt=float)

def taille(f):
    s=0
    while f.readline()[:-1]!='':
        s+=1
    return s

def pos_option(ch):
    i=len(ch)-1
    while i>-1 and ch[i]!='=':
        i-=1
    return i

def extract(ch,t,n):
    ch+=''
    e=dict(enr)
    for i in range(n-1):
        d=ch.find(t[i])+len(t[i])+1
        e[t[i]]=ch[d:ch[d:].find(' ')+d]
    p=ch.find(' ')
    if ch[p+1]=='A':
        e['Res']='ADMIS'
    elif ch[p+1]=='C':
        e['Res']='CONTROLE'
    else:
        e['Res']='REFUSE'
    e['Opt']=ch[pos_option(ch)+1:]
    f=open('data.dat','wb')
    dump(e,f)
    f.close()

def remplir_data(t,nt):
    f=open('msg.txt','r')
    n=taille(f)
    f.close()
    f=open('msg.txt','r')
    for i in range(n):
        extract(f.readline()[:-1],t,nt)
    f.close()
    
def initialisation():
    global t,nt
    
    f=open('inst.txt','r')
    nt=taille(f)
    f.close()
    t=['']*nt
    
    f=open('inst.txt','r')
    for i in range(nt):
        t[i]=f.readline()[:-1]
    f.close()

def conv10_16(n):
    chx='0123456789ABCDEF'
    ch=''
    ch=chx[n%16]+ch
    n=n//16
    while n!=0:
        ch=chx[n%16]+ch
        n=n//16
    if len(ch)==2:
        return ch
    elif len(ch)==1:
        return '0'+ch
    
def rgb_to_hex(r,g,b):
    return '#'+conv10_16(r)+conv10_16(g)+conv10_16(b)

def animate():
    global n
    n+=1
    if n<lim:
        mr=(n/lim)*moy
        moyenne.config(text=str(round(mr,2)))
        color=rgb_to_hex(0,n,0)
        root.configure(bg=color)
        moyenne.config(bg=rgb_to_hex(0,0,n))
        root.after(15, animate)
    else:
        moyenne.config(text=str(moy))

def get_info():
    initialisation()
    remplir_data(t,nt)

def showdown():
    global lim,moyenne,moy,f,fd,n
    f.close()

    for widget in root.winfo_children():
        widget.destroy()

    labeling() 

    f=open('data.dat','rb')
    e=load(f)
    f.close()

    moy=float(e['Moye'])
    coef=moy/20
    lim=round(coef*255)
    n=0
    
    moyenne=tk.Label(root,text='',font=('Arial',30))
    moyenne.grid(row=2,column=1,sticky='nsew',pady=5)

    animate()

    loading()

def labeling():
    f=open('inst.txt','r')
    n=taille(f)
    f.close()

    f=open('inst.txt','r')
    for i in range(n):
        tk.Label(root,text=f.readline()[:-1],font=('Arial',30)).grid(row=i,column=0,padx=415,pady=5,sticky='nsew')
    f.close()

def loading():
    f=open('inst.txt','r')
    n=taille(f)
    f.close()

    fd=open('data.dat','rb')
    e=load(fd)
    fd.close()

    f=open('inst.txt','r')
    for i in range(n):
        if i==2:
            f.readline()
        else:
            tk.Label(root,text=e[f.readline()[:-1]],font=('Arial',30)).grid(row=i,column=1,sticky='nsew',pady=5)
    f.close()

def play():
    global label,f,fd,phase,ch,e,skip_button,button,inp,notif
    root.unbind('<Key>')
    guide.destroy()

    f=open('inst.txt','r')
    phase=taille(f)+1
    f.close()
    
    fd=open('data.dat','rb')
    e=load(fd)
    fd.close()

    f=open('inst.txt','r')

    #burn INS
    phase=phase-2
    for _ in range(2):
        res=f.readline()[:-1]

    if e[res]!='ADMIS':
        msg='Malhereusement Vous Etes '+e[res]
        resultat=tk.Label(root,text=msg,font=('Serif',25),bg='red')
        resultat.pack(expand=True)
        sleep(2)
    else:
        resultat=tk.Label(root,text=e[res],font=('Serif',80),bg=root['bg'])
        resultat.pack(pady=20)

        label=tk.Label(root,text='Guess',font=('Arial',30),bg=root['bg'])
        label.pack(pady=17.5)

        inp=tk.Entry(root,font=('Arial',30))
        inp.pack(pady=15)

        button=tk.Button(root,text=' Check ',command=lambda :check_guess(inp.get(),e[ch]),font=('Arial',20))
        button.pack(pady=15)

        skip_button=tk.Button(root,text='  Skip  ',command=lambda :show_next(),font=('Arial',20))
        skip_button.pack(pady=15)

        skip_all_button=tk.Button(root,text='Skip All',command=lambda :showdown(),font=('Arial',20))
        skip_all_button.pack(pady=15)

        notif=tk.Label(root,text='The hint will be shown here',font=('Serif',20),bg=root['bg'])
        notif.pack(pady=17.5)

        show_next()

def show_next():
    global phase,ch
    
    inp.delete(0,len(inp.get()))
    button.config(state='active')
    skip_button.config(text='Skip')
    notif.config(text='The hint will be shown here')

    phase=phase-1
    if phase>0:
        ch=f.readline()[:-1]
        label.config(text='Guess '+ch)
    else:
        showdown()

def bg_color_animation(diff):
    if diff==0:
        r,b=255//2,255//2
    elif diff<=1:
        b,r=0,255
    elif diff>1:
        b,r=255,0
    root.configure(bg=rgb_to_hex(r,0,b))

def check_guess(guess,value):
    try:
        guess=float(guess)
        value=float(value)

        bg_color_animation(abs(guess-value))
        
        if guess>value:
            msg=str(guess)+' is HIGHER'
        elif guess<value:
            msg=str(guess)+' is LOWER'
        else:
            msg=str(guess)+' is CORRECT'
            skip_button.config(text='Continue')
            button.config(state='disabled')
    except:
        msg='Validate your guess'

    notif.config(text=msg)

def start_interface():
    global guide
    root.bind('<Key>',lambda e:play())

    guide=tk.Label(root,text='Press any key to continue..',font=('Serif',20),bg=root['bg'])
    guide.pack(expand=True)

#-------------------------------------

if __name__=='__main__':
    root=tk.Tk()
    root.attributes('-fullscreen',True)
    root.title('APP')
    root.bind('<Escape>',lambda e:root.destroy())

    get_info()

    fd=open('data.dat','rb')
    e=load(fd)
    fd.close()

    fm=open('moy.txt','r')
    moy=fm.read()
    fm.close()

    diff=float(e['Moye'])-float(moy)
    if diff>=3:
        color='gold'
    elif diff>=2:
        color='cyan'
    elif diff>=1:
        color='pink'
    elif diff>=0:
        color='white'
    else:
        color='black'
    root.configure(bg=color)
    if color=='black':
        root.destroy()
    else:
        start_interface()
    root.mainloop()
