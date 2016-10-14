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

"""
SICK FUNCTION

def diseaseSpread(member, disease, immunity):
 	#Checks if the individual will get sick
 	if member.getSick() > disease: return

 	exponent = (immunity-disease)/(disease/5.0)
 	chanceOfGettingSick = 1/(math.exp(exponent) + 1) # Look at fermi-dirac statistics for shape
 	if random.random() < chanceOfGettingSick:
 		member.setSick(disease)
 	return
"""

#Adds population to the specific GRID        
def modifygrid(x,y,members):
        i=int((x-(-180))/5)
        j=int((90-y)/5)
        settings.GRIDPOPULATION[i,j]=+members
        #return GRIDPOPULATION

# Calculates population density per GRID                        
def griddensity(): # Calculated by using the formula you suggested
        w=len(np.arange(-180.,181.,5))
        h=len(np.arange(-90.,91.,5))
        global GRIDDENSITY
        GRIDDENSITY=np.zeros((w-1,h-1))

        for i in range(18): 
            pi1=math.radians(90-5*i)
            pi2=math.radians(90-5*(i+1))
            k=math.fabs(3.5*(10**6)*(math.sin(pi1)-math.sin(pi2))) 
            GRIDDENSITY[i,:]=settings.GRIDPOPULATION[i,:]/k
            GRIDDENSITY[35-i,:]=settings.GRIDPOPULATION[35-i,:]/k         


def isLand(location):
	lon, lat = location
	x = int((lon+180)/360.0*616)
	y = int((-lat+90)/180.0*307)
	if settings.LANDMAP[x,y] == (255, 255, 255):
		return False
	return True

# Checking if family is in a bad zones
# Bad zones are those regions where human habitation is not probable (Deserts, Artic Zones, Mountains)         
# 0 means you can't inhabit, 0.5 possible but hard. Migration through these routes possible
# 1 means migration as well as settlement is possible
def badzones(x,y):
        if y>=60:#Artic Zones
            return 0
        elif (x>=115 and x<=150) and (y>=-30 and y<=-15): #Deserts in Australia
            return 0.5
        elif x>=85 and y>=50: #Parts of Russia and Syberia
            return 0.5
        elif x<=-10 and y>=50: #Alaska, Greeland
            return 0.5
        elif (x>=-120 and x<=-90) and (y>=35 and y<=45): # North American Desert
            return 0.5
        elif (x>=-10 and x<=30) and (y>=15 and y<=30): #Sahara Desert
            return 0.5
        else: # Everywhere else
            return 1 
            
def newFamily(basemap):
	global map
	map = basemap
	#print "I have reached here"
	minLon, maxLon = settings.LONLAT[0]
	#print(minLon,maxLon)
	minLat, maxLat = settings.LONLAT[1]

	# Generate initial location on map
	lon = random.choice(range(minLon, maxLon))
	lat = random.choice(range(minLat, maxLat))
	while not isLand([lon, lat]) or not badzones(lon,lat):	
		lon = random.choice(range(minLon, maxLon))
		lat = random.choice(range(minLat, maxLat))
	

	# Generate initial members population
	members = set([
		random.randint(0, settings.MAXAGE) for i in range(random.randint(1, settings.FAMILYSIZE))
		])

	# Add families to map

	x, y = map(lon, lat)
	#modifygrid(x,y,len(members))
	p = map.plot(x, y, 'bo', markersize=2)[0]

	return Family([lon, lat], members, p)
#def

def updateLocation(family):
	location = family.getLocation()
	dev = family.getDevelopment()

	dist = settings.travelDist
	lon, lat = location
	size = settings.earthR*2*math.pi

	if isLand(family.getLocation()):
		locationFound = False
		badZone=0
		while not locationFound or not badZone :
			direction = 2*math.pi*random.random()
			lonRatio = math.cos(direction)*dist/size
			latRatio = math.sin(direction)*dist/size
			newLon = (lon + lonRatio*360)
			newLat = lat + latRatio*180
			locationFound = isLand([newLon, newLat])
			badZone=badzones(newLon,newLat)
			if badZone==0:
			    badZone=int(badZone) #Reduntant but essential
			elif badZone==0.5:
			    lon,lat=newLon,newLat
		            badZone=int(badZone)

	else:
		return True
	    
	#elif badzones(newLon,newLat)==0:
	    #Change the state to DEAD
	    

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

