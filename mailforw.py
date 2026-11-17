import imaplib
import os
import email
import email.policy
from search import verif

def load_env(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env')):
    # tiny KEY=VALUE reader so no python-dotenv dependency; real env vars win
    if os.path.exists(path):
        for line in open(path):
            k,_,v=line.strip().partition('=')
            if k and not k.startswith('#'):
                os.environ.setdefault(k,v.strip('"\''))

def check_mail():

    load_env()
    EMAIL = os.environ["EMAIL"]
    APP_PASSWORD = os.environ["APP_PASSWORD"]

    # Connect to Gmail
    with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        # Search unread messages
        result,data = mail.search(None, "UNSEEN")
        ids = data[0].split()
        for i in ids:
            result,msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email, policy=email.policy.default)
            subject = msg["Subject"] or ""
            if subject.find('[SMSFW]')!=-1 and subject.find('97754430')!=-1:
                # plain part of a (possibly multipart) mail; the SMS text follows the ***** line and may be hard-wrapped
                body = msg.get_body(preferencelist=('plain',)).get_content()
                ch = ' '.join(body.rsplit('************',1)[-1].split())
                if verif(ch):
                    with open('msg.txt','a') as f:
                        f.write(ch+chr(10))
                return True
            else:
                return False
