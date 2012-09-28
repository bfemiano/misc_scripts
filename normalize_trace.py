import csv
import sys
import os

#Takes a tracefile and expands into multilple lines for each memory-read, memory-write, register read and/or register write per instruction. 
# outputs a tableau ready file to the working directory where the script was executed. 
# requires relative or absolute path to a tracefile.  

def output(writer, fields, offset, seq, dataset):
	for i in range(0, offset):
		fields.pop(0)
	fields.insert(0, seq)
	fields.append(dataset)
	writer.writerow(fields)

def appendBase10ForHexFields(fields, positionsToParse):
	for i in positionsToParse:
		hex = ''
		if fields[i] != '':
			hex = int(fields[i], 0)
		fields.append(hex)
	return fields
		

def writeDataset(basicOut, memReadOut, memWriteOut, regReadOut, regWriteOut, tracefileAbsPath, dataset):
	reader = csv.reader(open(tracefileAbsPath, 'rb'), delimiter='|')
	for row in reader:
		basicOut.writerow([row[0], row[1], row[2], dataset])
		memread = row[5]
		if len(memread) > 0:
			memread= appendBase10ForHexFields([x for x in memread.split(':')], [2,4])
			output(memReadOut, memread, 2, row[0], dataset)
		memwrite = row[6]
		if len(memwrite) > 0:
			fields = memwrite.split(':')
			if len(fields) == 4:
				fields.append('')
			fields = appendBase10ForHexFields([x for x in fields], [2,4])
			output(memWriteOut, fields, 2, row[0], dataset)
		rreads = row[7]
		if len(rreads) > 0:
			for rread in rreads.split(','):
				rread = appendBase10ForHexFields([x for x in rread.split(':')],[2])
				output(regReadOut, rread, 1, row[0], dataset)
		rwrites = row[8]
		if len(rwrites) > 0:
			for rwrite in rwrites.split(','):
				rwrite = appendBase10ForHexFields([x for x in rwrite.split(':')], [2])
				output(regWriteOut, rwrite, 1, row[0], dataset)
		
def main(workingPath):	
	basicOut = csv.writer(open(workingPath + '/tableau_basic_info.txt', 'wb'), delimiter='\t')
	memReadOut = csv.writer(open(workingPath + '/tableau_memread.txt', 'wb'), delimiter='\t')
	memWriteOut = csv.writer(open(workingPath + '/tableau_memwrite.txt', 'wb'), delimiter='\t')
	regReadOut = csv.writer(open(workingPath + '/tableau_regread.txt', 'wb'), delimiter='\t')
	regWriteOut = csv.writer(open(workingPath + '/tableau_regwrite.txt', 'wb'), delimiter='\t')
	basicOut.writerow(['seq', 'td', 'ip', 'dataset']), #base 3 fields
	memReadOut.writerow(['seq', 'mr_addr', 'mr_size', 'mr_value', 'base10_addr', 'base10_value', 'dataset']) #memory read 
	memWriteOut.writerow(['seq', 'mw_addr', 'mw_size', 'mw_value', 'base10_addr', 'base10_value', 'dataset']) #memory write
	regReadOut.writerow(['seq', 'rr_reg', 'rr_val', 'base10_value', 'dataset']) #register read 
	regWriteOut.writerow(['seq', 'wr_reg', 'wr_val', 'base10_value', 'dataset']) #register write
	if not workingPath.endswith('/'):
		workingPath += '/'
	for tracefile in os.listdir(workingPath):
		if tracefile.endswith('final'):
			writeDataset(basicOut, memReadOut, memWriteOut, regReadOut, regWriteOut, workingPath + tracefile, tracefile)

if __name__ == "__main__":
	main(sys.argv[1])