import random
import sys
import smtplib
import time
from getpass import getpass

def pick(cousins):
    return cousins[random.randint(0, len(cousins)-1)]

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


def select_cousin(cousins, remaining_cousins):
    if len(cousins) == 0:
        return ['done']
    cousin = cousins.pop()
    (giver_name, giver_email, giver_blocked) = cousin
    ignore_cousins = set(giver_blocked.strip(' ').split('|'))
    allowed_cousins = [c for c in remaining_cousins if c[0] not in ignore_cousins and c[0] != cousin[0]]
    pairings = []
    recipient = None
    while len(pairings) == 0:
        if recipient: # Let's try again with a new recipient and free up this recipient for downstream attempt.
            allowed_cousins.remove(recipient)
            remaining_cousins.append(recipient)
        if len(allowed_cousins) == 0:
            return [] #none left to pick from. Notify previous caller it needs to randomly reassign.
        recipient = pick(allowed_cousins)
        remaining_cousins.remove(recipient)
        pairings += select_cousin([c for c in cousins], [c for c in remaining_cousins])
    pairings.append((cousin, recipient))
    return pairings


def get_cousin_pairings():
    #File of the form,
    # name1, email1, blocked_name|another_blocked_name
    # name2, email2, blocked_name|another_blocked_name
    # not checked in to hide email addresses.
    cousins = []
    with open('cousin_names_and_emails.txt', 'r') as name_email_pairs_in:
        for line in name_email_pairs_in.readlines():
            cousins.append(tuple(line.strip('\n').split(',')))
    pairs =  select_cousin([c for c in cousins], [c for c in cousins])
    if len(pairs) == 0:
        raise Exception("Some cousin has everyone else blacklisted.")
    return pairs

def get_blocked_list_for_cousins():
    cousins = []
    blocked_map = {}
    with open('cousin_names_and_emails.txt', 'r') as name_email_pairs_in:
        for line in name_email_pairs_in.readlines():
            cousins.append(tuple(line.strip('\n').split(',')))
    for c in cousins:
        blocked_map[c[0]] = set(c[2].strip(' ').split('|'))
    return blocked_map

blocked_map = get_blocked_list_for_cousins()
emails_to_send = []
results = [r for r in get_cousin_pairings() if r != 'done']
for (giver, recipient) in results:
    print '%s --> %s' % (giver[0], recipient[0])
    emails_to_send.append(generate_email(giver, recipient))

#This is a regression test to make sure the auto-selector is working. Do not approve if you see any output here.
for i in xrange(1000):
    results = get_cousin_pairings()
    output = [(pairing[0][0], pairing[1][0]) for pairing in results if pairing != 'done'] #collect only the names just to test
    for o in output:
       if o[1] in blocked_map[o[0]] or o[0] == o[1]:
           print o[0], 'should not have --> %s ' % o[1]

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
