import random
import sys
import smtplib
import time
from getpass import getpass

#File of the form,
# name1, email1, blocked_name|another_blocked_name
# name2, email2, blocked_name|another_blocked_name
# not checked in to hide email addresses. 
cousins = []
with open('cousin_names_and_emails.txt', 'r') as name_email_pairs_in:
    for line in name_email_pairs_in.readlines():
        cousins.append(tuple(line.strip('\n').split(',')))

def pick(cousin):
    '''
        Randomly select a cousin from the list that is same as the 'cousin' argument. 
        This will prevent pairing people with themselves.
    '''
    rand_cousin = cousin
    while rand_cousin == cousin:
        n = random.randint(0, len(cousins)-1)
        rand_cousin = cousins[n]
    return rand_cousin
    
def generate_email(giver, receiver):
    '''
        Programatically build the email message and return it as a string. 
    '''
    (giver_name, giver_email, blocked1) = giver
    (receiver_name, receiver_email, blocked2) = receiver
    msg = '''Subject: Here's your assigned cousin!\n
    
    Hello {giver_name},
 
    Your 2015 gift exchange recipient: {receiver_name}
 
    Email address to help you reach him/her: {receiver_email}
 
    The names were randomly drawn using a computer program I wrote that randomly paired cousins with other cousins. It was designed to avoid selecting yourself or people in your immediate family. So for example Joseph would not be paired with himself or Anna or Christopher.
 
    See you at the farm!
    '''.format(giver_name=giver_name, receiver_name=receiver_name, receiver_email=receiver_email)
    return (giver_email, msg)

cousins_copy = [c for c in cousins]
emails_to_send = []

i = 0
for c in cousins_copy:
    pair_next_cousin = True
    while pair_next_cousin: 
        rand_cousin = pick(c)
        (giver_name, giver_email, giver_blocked) = c
        (receipiant_name, receipiant_email, receipiant_blocked) = rand_cousin
        pair_next_cousin = receipiant_name in set(giver_blocked.strip(' ').split('|'))
        i += 1
        if i > 100000:
            print 'Cousin blocked list made pairings impossible this round, considering losing some of the blocked names per cousin and try again.'
            sys.exit(0)
    print '%s --> %s' % (giver_name, receipiant_name)
    cousins.remove(rand_cousin)
    emails_to_send.append(generate_email(c, rand_cousin))

contin = raw_input("Do you approve of the list? (Only 'Y' will continue)")
if contin != 'Y':
    print 'Aborting'
    sys.exit(0)
fastmail_server = 'mail.messagingengine.com:587'
username = 'bfemiano@fastmail.com'
password = getpass("password please ")

try:  #email out all the cousins using the prepared message.
    server = smtplib.SMTP(fastmail_server)
    server.starttls()    
    server.login(username,password)
    for (giver_email, msg) in emails_to_send:
        print 'sending email to %s' % giver_email
        server.sendmail(username, giver_email, msg)
        time.sleep(3) #rate limit to avoid being flagged as spam, just as a precaution.  
    print 'Success!'  
finally:
    server.quit()
