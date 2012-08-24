import csv
import random

def main():
	firstreader = open('first_name.txt', 'rb')
	lastreader = open('last_name.txt', 'rb')
	names = csv.writer(open('names.txt', 'wb'), delimiter='\t')
	first_names = map(lambda x: x.strip('\n'), firstreader.readlines())
	for line in firstreader:
		print line.strip('\n')
	last_names = map(lambda x: x.strip('\n'), lastreader.readlines())
	already_generated = set([])
	while len(already_generated) < 180000:
		fn = random.randint(0,5492)
		ln = random.randint(0,4476)
		key = str(fn) + str(ln)
		if key not in already_generated:	
			already_generated.add(key)
			names.writerow([first_names[fn], last_names[ln]])

if __name__ == "__main__":
	main()