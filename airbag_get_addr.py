import requests
from bs4 import BeautifulSoup
from MaltegoTransform import *

me = MaltegoTransform()
me.parseArguments(sys.argv)
name = sys.argv[1]
firstname = name.split(' ')[0]
lastname =  name.split(' ')[1]
r = requests.post('http://vin.place/search.php', data = {'first':firstname,'last':lastname})

# Grab all the results from vin.place
vins = BeautifulSoup(r.content).body.findAll('div', attrs={'class':'search-content'})

# For each result, grab the links and car details
results = []
for vin in vins:
	soup = BeautifulSoup(str(vin))
	results.append(str(soup.find_all('a')[0]).split('=')[1].split('>')[0].strip('"'))

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

address = ''
city = ''
state = ''
zipcode = ''

for person in dic:
	details = dic[person][0].split(',')
	for i in details:
		if 'Address' in i:
			test = BeautifulSoup(i).body.findAll('b')
			for node in test:	
				address = ''.join(node.findAll(text=True))
		elif 'City' in i:
			test = BeautifulSoup(i).body.findAll('b')
			for node in test:	
				city = ''.join(node.findAll(text=True))
		elif 'State' in i:
			test = BeautifulSoup(i).body.findAll('b')
			for node in test:	
				state = ''.join(node.findAll(text=True))
		elif 'Zip' in i:
			test = BeautifulSoup(i).body.findAll('b')
			for node in test:	
				zipcode = ''.join(node.findAll(text=True))
						
	ent = me.addEntity("maltego.Home",address + '\n' + city + ', ' + state + ' ' + zipcode)
	ent.addAdditionalFields('fullname','fullname','',name)
me.returnOutput()