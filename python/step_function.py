import time
import random

i = 0
curr_on = False

def signal_blocked():
    return bool(random.getrandbits(1))

while(True):
    
    if signal_blocked(): #returns either 1 or 0
        change = 1 if i < 10 else 0
    else:
        change = -1 if i > 0 else 0
    i += change          
    if i == 0 and change == -1 and curr_on:     
        print 'Change detected: Object present.'
        curr_on = False
    elif i == 10 and change == 1 and not curr_on:
        print 'Change detected: Coast is clear'
        curr_on = True
    time.sleep(1)
    