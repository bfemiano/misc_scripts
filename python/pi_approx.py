import sys
from math import pow, pi, fabs
from datetime import datetime

def main():
	try:
		nLen = sys.argv[1]
		startNumer = int(pow(10, int(nLen))) #if 3 then 99
		endNumer = int(pow(10, int(nLen) -1)) #if 3 then 9
		minDifNumer = startNumer
		minDifDenom = endNumer
		minDifference = fabs(pi - (float(startNumer)/float(endNumer)))
		startTime = datetime.now()
		counter = 0;
		for i in reversed(xrange (endNumer, startNumer)):
			denom = int(i * .35)
			endDenom = int(i * .31)
			if counter % 100 == 0:
				print 'processed: ' + str(counter) + ' numerators.'
			while denom >= endDenom:
				if denom > 0:					
					difference = fabs(pi - (float(i)/float(denom)))
					if difference <= minDifference:
						minDifNumer = i
						minDifDenom = denom
						minDifference = difference
				denom-=1
			counter +=1
		endTime = datetime.now()		
		print 'Most accurate: ' + str(minDifNumer) + '/' + str(minDifDenom) + ": " + str(float(minDifNumer)/float(minDifDenom))
		print 'Runtime: ' + str(((endTime - startTime)))
	except IndexError:
		print 'Enter a number (example: pi_approx.exe 2)'
	

if __name__ == '__main__':
		main()