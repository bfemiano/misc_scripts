import random
import smtplib
from getpass import getpass


#File of the form,
# (name1, email1)
# (name2, email2)
# not checked in to hide email addresses. 
cousins = load_from_file

def pick(cousin):
    rand_cousin = cousin
    while rand_cousin == cousin:
        n = random.randint(0, len(cousins)-1)
        rand_cousin = cousins[n]
    return rand_cousin
    

cousins_copy = [c for c in cousins]
assignments = {}
for c in cousins_copy:
    choice = 'N'
    while choice == 'N':
        rand_cousin = pick(c)
        choice = raw_input("Accept %s -> %s? Enter (Y/N) " % (c, rand_cousin))
    cousins.remove(rand_cousin)
    assignments[c] = rand_cousin
    
fastmail_server = 'mail.messagingengine.com:587'

fromaddr = 'bfemiano@fastmail.com'
toaddrs  = 'bfemiano@gmail.com'
username = 'bfemiano@fastmail.com'
password = getpass("password please ")

server = smtplib.SMTP(fastmail_server)
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()