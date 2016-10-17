import requests
from bs4 import BeautifulSoup
from MaltegoTransform import *
import random

me = MaltegoTransform()
me.parseArguments(sys.argv)

transform = sys.argv[1]

if transform == 'addr':
	name = sys.argv[2]
	firstname = name.split(' ')[0]
	lastname =  name.split(' ')[1]
	address = ''
	city = ''
	state = ''
	zipcode = ''

	def create_dictionary(vins):
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
		return dic

	def create_entities(dic):
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

	r = requests.post('http://vin.place/search.php', data = {'first':firstname,'last':lastname})

	vins = BeautifulSoup(r.content).body.findAll('div', attrs={'class':'search-content'})

	dic = create_dictionary(vins)
	create_entities(dic)

	me.returnOutput()

if transform == 'vehicles':
	addr = sys.argv[2].split('\n')[0]
	fullname = sys.argv[3].split('fullname=')[1]
	firstname = fullname.split(' ')[0]
	lastname = fullname.split(' ')[1]

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

	address = ''
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
				soup = BeautifulSoup(i).body.findAll('b')
				for node in soup:	
					vin = ''.join(node.findAll(text=True))
		if address == addr:
			ent = me.addEntity("maltego.Car", year + ' ' + make + ' ' + model)
			ent.addAdditionalFields('fullname','fullname','strict',fullname)
			uuid = random.getrandbits(128)
			ent.addAdditionalFields('uuid','uuid','strict',uuid)
			ent.addAdditionalFields('addr','addr','strict',addr)
		
	me.returnOutput()

if transform == 'vins':
	fullname = sys.argv[3].split('fullname=')[1].split('#')[0]
	firstname = fullname.split(' ')[0]
	lastname = fullname.split(' ')[1]

	car = sys.argv[2]
	addr = sys.argv[3].split('addr=')[1].split('#')[0]

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