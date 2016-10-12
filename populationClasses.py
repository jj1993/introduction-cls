import random, math
import matplotlib.pyplot as plt
import settings
import numpy as np

class Family(object):
	def __init__(self, location, members, mapPoint, immunity = 1.0, community = None):
		self.location = location #[x,y]
		self.immunity = immunity #float
		self.community = community #object or None
		self.mapPoint = mapPoint #visual attribute on the map
		self.development = 0
		self.sick = 0
		self.members = members

	def update(self):
		self.development += 1

		if len(self.members) == 0:
			self.mapPoint.remove()
			isAlive = False
			return isAlive

		isAlive = updateLocation(self)
		return isAlive
		# self.hasFood = checkForFood(self.location, len(self.members))

		# if doesFoundCommunity(location):
		# 	newCommunity = Community(
		# 		len(self.members), self.location, self.immunity, self.community
		# 		)
		# 	communities.append(newCommunity)

	def split(self):
		half = int(0.5*len(self.members))
		members = self.members
		random.shuffle(members)
		remaining = members[:half]
		leaving =  members[half:]
		self.members = remaining
		x, y = self.location
		newPoint = map.plot(x, y, 'bo', markersize=2)[0]
		return Family([x, y], leaving, newPoint, self.immunity) # No bounds with community are maintained

	def getFamilyEncounters(self):
		encounters = []
		for family in families:
			if (family != self and 
				family.getDistance(self.location) < settings.ENCOUNTERDIST):
				encounters.append(family)
		return encounters

	def getSocietyEncounters(self):
		encounters = []
		for society in societies:
			if (society.getDistance(self.location) < settings.ENCOUNTERDIST):
				encounters.append(society)

			if self.community:
				changeOfAlliance(self.community, society)

		return encounters

	def getDistance(self, location):
		x1, y1 = self.location
		x2, y2 = location
		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

	def growImmunity(self, disease):
		if self.immunity > disease: return
		growth = settings.IMMUNITYGROWTH*(disease-self.immunity)
		self.immunity += growth
		return

	def setLocation(self, location):
		self.location = location

	def getMembers(self):
		return self.members

	def setMembers(self, members):
		self.members = members

	def getDevelopment(self):
		return self.development

	def getImmunity(self):
		return self.immunity

	def getCommunity(self):
		return self.community

	def getLocation(self):
		return self.location

	def getMapPoint(self):
		return self.mapPoint

def isLand(location):
	lon, lat = location
	x = int((lon+180)/360.0*616)
	y = int((-lat+90)/180.0*307)
	if settings.LANDMAP[x,y] == (255, 255, 255):
		return False
	return True

def newFamily(basemap):
	global map
	map = basemap
	minLon, maxLon = settings.LONLAT[0]
	minLat, maxLat = settings.LONLAT[1]

	# Generate initial location on map
	lon = random.choice(range(minLon, maxLon))
	lat = random.choice(range(minLat, maxLat))
	while not isLand([lon, lat]):	
		lon = random.choice(range(minLon, maxLon))
		lat = random.choice(range(minLat, maxLat))

	# Generate initial members population
	members = set([
		random.randint(0, settings.MAXAGE) for i in range(random.randint(1, settings.FAMILYSIZE))
		])

	# Add families to map

	x, y = map(lon, lat)
	p = map.plot(x, y, 'bo', markersize=2)[0]

	return Family([lon, lat], members, p)

def updateLocation(family):
	location = family.getLocation()
	dev = family.getDevelopment()

	dist = settings.travelDist
	lon, lat = location
	size = settings.earthR*2*math.pi

	if isLand(family.getLocation()):
		locationFound = False
		while not locationFound:
			direction = 2*math.pi*random.random()
			lonRatio = math.cos(direction)*dist/size
			latRatio = math.sin(direction)*dist/size
			newLon = (lon + lonRatio*360)
			newLat = lat + latRatio*180
			locationFound = isLand([newLon, newLat])

	else:
		return True

	family.setLocation([newLon, newLat])
	family.getMapPoint().set_data(newLon, newLat)
	return True

def checkForFood(location, nrMembers):
	food = getRainyValue(location)
	food += getTemperature(location)
	food += isRiverClose(location)
	return settings.MINFOOD > food/nrMembers
def getRainyValue(location):
	pass
def getDomesticAnimals(location):
	pass

def doesFoundCommunity(location):
	pass


# class Community(object):
# 	def __init__(self, population, location, immunity, alliance):
# 		self.population = population #integer
# 		self.location = location #[x, y]
# 		self.immunity = immunity #float
# 		self.development = 1 #float, starts at 1 in communities
# 		self.explorers = [] #list of family objects
# 		if alliance: self.alliances = [alliance]
# 		else: self.alliances = []

# 	def getSize(self):
# 		return self.population

# 	def updateAlliances(self):
# 		for community in self.alliances:
# 			if community.getSize() > self.population:
# 				del community

# 	def getDistance(self, location):
# 		x1, y1 = self.location
# 		x2, y2 = location
# 		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

# 	def getRadius(self):
# 		return DENSITYFACTOR*self.population/self.development


# def diseaseSpread(member, disease, immunity):
# 	# Checks if the individual will get sick
# 	if member.getSick() > disease: return

# 	exponent = (immunity-disease)/(disease/5.0)
# 	chanceOfGettingSick = 1/(math.exp(exponent) + 1) # Look at fermi-dirac statistics for shape
# 	if random.random() < chanceOfGettingSick:
# 		member.setSick(disease)
# 	return