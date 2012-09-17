import csv
import sys
import os

def output(writer, outfields, items, index, offset):
	for i in range(0, (len(items)-offset)):
		outfields.pop(index+i)
		outfields.insert(index+i, items[i+offset])
	writer.writerow(outfields)

#Takes a tracefile and expands into multilple lines for each memory-read, memory-write, register read and/or register write per instruction. 
# outputs a tableau ready file to the working directory where the script was executed. 
# requires relative or absolute path to a tracefile.  
def main(filePath):
	workingPath = os.path.dirname(filePath[1])
	reader = csv.reader(open(workingPath + '/trace.final'), delimiter='|')
	writer = csv.writer(open('./tableau_'+ os.path.basename(filePath[1]) + '.tsv', 'wb'), delimiter='\t')
	writer.writerow(['seq', 'td', 'ip', #base 3 fields
	'mr_addr', 'mr_size', 'mr_value', #memory read 
	'mw_addr', 'mw_size', 'mw_value', #memory write
	'rr_reg', 'rr_val', #register read 
	'wr_reg', 'wr_val']) #register write
	for row in reader:
		outfields = [row[0], row[1], row[2]]
		for i in range(0,10):
			outfields.append('')
		memread = row[5]
		if len(memread) > 0:
			items = memread.split(':')
			output(writer, [x for x in outfields], items, 3, 2)
		memwrite = row[6]
		if len(memwrite) > 0:
			items = memwrite.split(':')
			if len(items) == 4:
				items.append('')
			output(writer, [x for x in outfields], items, 6, 2)
		rreads = row[7]
		if len(rreads) > 0:
			for rread in rreads.split(','):
				output(writer, [x for x in outfields], rread.split(':'), 9, 1)
		rwrites = row[8]
		if len(rwrites) > 0:
			for rwrite in rwrites.split(','):
				output(writer, [x for x in outfields], rwrite.split(':'), 11, 1)

if __name__ == "__main__":
	main(sys.argv)