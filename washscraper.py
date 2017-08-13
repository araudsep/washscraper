from lxml import html
import requests
import csv

def washerScrape(source):
	page = requests.get(source)
	tree = html.fromstring(page.content)
	fulltab = list()

	MachineID = tree.xpath('//table[@id="machine-grid"]/tbody/tr[position() > 1]/td[position() = 1]/text()')
	
	#Scrapes a Washstation site for washing machine rows
	for i in range(2, len(MachineID)+2):
		TabRow = tree.xpath('//table[@id="machine-grid"]/tbody/tr[position() = %s]//text()' %i)
		#Removes empty values from the scrape data
		for n in range(len(TabRow)-1, 0, -1):
			if TabRow[n] == '\n\t\t\t  ':
				del(TabRow[n])
		fulltab.append(list(TabRow))

	#Fills in missing time values that XPATH doesn't catch from tables
	for x in fulltab:
		if len(x) < 3:
			x.append('No data')
	return(fulltab)

def washerExport(data):
	with open("washscraperdata.csv", "w", newline='') as outputcsv:
	  fieldnames = ['Machine', 'Status', 'Remaining']
	  writer = csv.DictWriter(outputcsv, fieldnames=fieldnames)

	  writer.writeheader()
	  for i in range(0, len(data)):
	  	writer.writerow({'Machine': data[i][0], 'Status': data[i][1], 'Remaining': data[i][2]})
	print('washer data exported into csv!')

washerExport(washerScrape('http://readytowash.com/?id=22878&locid=90'))