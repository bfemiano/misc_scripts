import csv
import sys
import os

#Takes a tracefile and expands into multilple lines for each memory-read, memory-write, register read and/or register write per instruction. 
# outputs a tableau ready file to the working directory where the script was executed. 
# requires relative or absolute path to a tracefile.  

def output(writer, fields, offset, seq):
	for i in range(0, offset):
		fields.pop(0)
	fields.insert(0, seq)
	writer.writerow(fields)
	
		
def main(filePath):
	workingPath = os.path.dirname(filePath)
	reader = csv.reader(open(filePath), delimiter='|')
	basicOut = csv.writer(open(workingPath + '/tableau_basic_info.tsv', 'wb'), delimiter='\t')
	memReadOut = csv.writer(open(workingPath + '/tableau_memread.tsv', 'wb'), delimiter='\t')
	memWriteOut = csv.writer(open(workingPath + '/tableau_memwrite.tsv', 'wb'), delimiter='\t')
	regReadOut = csv.writer(open(workingPath + '/tableau_regread.tsv', 'wb'), delimiter='\t')
	regWriteOut = csv.writer(open(workingPath + '/tableau_regwrite.tsv', 'wb'), delimiter='\t')
	basicOut.writerow(['seq', 'td', 'ip']), #base 3 fields
	memReadOut.writerow(['seq', 'mr_addr', 'mr_size', 'mr_value']) #memory read 
	memWriteOut.writerow(['seq', 'mw_addr', 'mw_size', 'mw_value']) #memory write
	regReadOut.writerow(['seq', 'rr_reg', 'rr_val']) #register read 
	regWriteOut.writerow(['seq', 'wr_reg', 'wr_val']) #register write
	for row in reader:
		basicOut.writerow([row[0], row[1], row[2]])
		memread = row[5]
		if len(memread) > 0:
			output(memReadOut, memread.split(':'), 2, row[0])
		memwrite = row[6]
		if len(memwrite) > 0:
			items = memwrite.split(':')
			if len(items) == 4:
				items.append('')
			output(memWriteOut, items, 2, row[0])
		rreads = row[7]
		if len(rreads) > 0:
			for rread in rreads.split(','):
				output(regReadOut, rread.split(':'), 1, row[0])
		rwrites = row[8]
		if len(rwrites) > 0:
			for rwrite in rwrites.split(','):
				output(regWriteOut, rwrite.split(':'), 1, row[0])

if __name__ == "__main__":
	main(sys.argv[1])