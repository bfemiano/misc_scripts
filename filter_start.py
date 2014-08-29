import csv
#still better
countries = set(['Australia', 'New Zealand', 'United States', 'Canada', 
'Ireland', 'Great Britain'])
#test
def inCountry(country):
	return country in countries
	
def main():
	smartReader = csv.reader(open('start-1970-2010.csv', 'rb'), delimiter='\t')
	smartWriter = csv.writer(open('start_1970-2010_without_fats.csv', 'wb'), delimiter=',', quoting=csv.QUOTE_MINIMAL)
	for row in smartReader:
		country = row[2]
		fatalities = row[5]
		if ((fatalities == '0' and inCountry(country)) or country == 'COUNTRY'):
			smartWriter.writerow(row)

if __name__ == "__main__":
	main()			
