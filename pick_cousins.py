import random
import smtplib
from getpass import getpass


#File of the form,
# name1, email1
# name2, email2
# not checked in to hide email addresses. 
cousins = []
with open('name_email_file.txt', 'r') as name_email_pairs_in:
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
    (giver_name, giver_email) = giver
    (receiver_name, receiver_email) = receiver
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

for c in cousins_copy:
    choice = 'N'
    while choice == 'N': #Keep picking until we are satisfied with the selection. This is where we can prevent cousins of immediate family from being paired together. 
        rand_cousin = pick(c)
        choice = raw_input("Accept %s -> %s? Enter (Y/N) " % (c, rand_cousin))
    cousins.remove(rand_cousin)
    emails_to_send.append(generate_email(c, rand_cousin))

fastmail_server = 'mail.messagingengine.com:587'
username = 'bfemiano@fastmail.com'
password = getpass("password please ")

try:  #email out all the cousins using the prepared message.
    server = smtplib.SMTP(fastmail_server)
    server.starttls()    
    server.login(username,password)
    for (giver_email, msg) in emails_to_send:   
        server.sendmail(username, giver_email, msg)
finally:
    server.quit()