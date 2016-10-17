import requests
from bs4 import BeautifulSoup
from MaltegoTransform import *

me = MaltegoTransform()
me.parseArguments(sys.argv)

fullname = sys.argv[2].split('fullname=')[1].split('#')[0]
firstname = fullname.split(' ')[0]
lastname = fullname.split(' ')[1]

car = sys.argv[1]
addr = sys.argv[2].split('addr=')[1].split('#')[0]

r = requests.post('http://vin.place/search.php', data = {'first':firstname,'last':lastname})

# Grab all the results from vin.place
vins = BeautifulSoup(r.content).body.findAll('div', attrs={'class':'search-content'})

# For each result, grab the links and car details
results = []
for vin in vins:
	soup = BeautifulSoup(str(vin))
	results.append(str(soup.find_all('a')[0]).split('=')[1].split('>')[0].strip('"'))

# dic has a key of the link, and value of the results, i.e. make, model, year 
dic = {}
for result in results:
	deets = []
	r = requests.get(result)
	soup = BeautifulSoup(r.content)
	details = soup.body.findAll('ul', attrs={'class':'list'})
	soup = BeautifulSoup(str(details))
	li = soup.findAll('li')
	deets.append(str(li))
	dic[result] = deets 

year = ''
make = ''
model = ''
vin = ''

for person in dic:
	details = dic[person][0].split(',')
	for i in details:
		if 'Address' in i:
			soup = BeautifulSoup(i).body.findAll('b')
			for node in soup:	
				address = ''.join(node.findAll(text=True))
		elif 'Year' in i:
			soup = BeautifulSoup(i).body.findAll('b')
			for node in soup:	
				year = ''.join(node.findAll(text=True))
		elif 'Make' in i:
			soup = BeautifulSoup(i).body.findAll('b')
			for node in soup:	
				make = ''.join(node.findAll(text=True))
		elif 'Model' in i:
			soup = BeautifulSoup(i).body.findAll('b')
			for node in soup:	
				model = ''.join(node.findAll(text=True))
		elif 'VIN' in i:
			if 'Lookup' in i:
				pass
			else:
				soup = BeautifulSoup(i).body.findAll('b')
				for node in soup:	
					vin = ''.join(node.findAll(text=True))
	if addr == address:
		returncar = year + ' ' + make + ' ' + model
		if car == returncar:
			ent = me.addEntity("maltego.VinNumber", vin)
		
me.returnOutput()