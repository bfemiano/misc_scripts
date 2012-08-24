import csv

countries = set(['Australia', 'New Zealand', 'United States', 'Canada', 
'Ireland', 'Great Britain'])

def inCountry(country):
	return country in countries
	
def main():
	smartReader = csv.reader(open('start-1990-2010.csv', 'rb'), delimiter='\t')
	smartWriter = csv.writer(open('filtered_start.csv', 'wb'), delimiter=',', quoting=csv.QUOTE_MINIMAL)
	for row in smartReader:
		country = row[2]
		fatalities = row[5]
		if ((fatalities != '0' and inCountry(country)) or country == 'COUNTRY'):
			smartWriter.writerow(row)

if __name__ == "__main__":
	main()			