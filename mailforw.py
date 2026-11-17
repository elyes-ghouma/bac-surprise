import imaplib
import email
from search import verif

def nbligne(ch):
    s=0
    for i in range(len(ch)):
        if ch[i]=='\n':
            s+=1
    return s

def check_mail():

    EMAIL = "elyesghouma15@gmail.com"
    APP_PASSWORD = "qivi pkmo chqm oikd"

    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    mail.select("inbox")

    # Search unread messages
    result,data = mail.search(None, "UNSEEN")
    ids = data[0].split()
    for i in ids:
        result,msg_data = mail.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject = msg["Subject"]
        if subject.find('[SMSFW]')!=-1 and subject.find('85005')==-1:
            # Get plain text content
            body = msg.get_payload(decode=True).decode()+'\n'
            n=nbligne(body)
            for i in range(n):
                ch=body[0:body.find('\n')]
                if verif(ch):
                    f=open('msg.txt','a')
                    f.write(ch+'\n')
                    f.close()
                    break
                else:
                    body=body[body.find('\n')+1:]
            return True
        else:
            return False
