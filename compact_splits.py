import sys
r = open('splits.txt', 'rb')
w = open('compact_splits.txt', 'wb')
counter = 0
for line in r:
	if counter % 10 == 0:
		w.write(line)
	counter += 1
w.write('105000006')
w.close()
r.close()