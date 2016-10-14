import random, math
import matplotlib.pyplot as plt
import settings
import numpy as np

class Family(object):
	def __init__(self, location, members, direction = 0, immunity = 1.0, community = None):
		self.location = location #[x,y]
		self.immunity = immunity #float
		self.community = community #object or None
		self.development = 1
		self.members = members
		self.waterSteps = 0
		self.direction = direction

		x, y = location
		mapPoint = map.plot(x, y, 'bo', markersize=2)[0]
		self.mapPoint = mapPoint #visual attribute on the map

	def update(self):
		self.development += 1

		if len(self.members) == 0:
			self.mapPoint.remove()
			isAlive = False
			return isAlive

		isAlive = updateLocation(self)
		[lon,lat]=self.location
		getCondition(self)
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
		self.members, leaving = members[:half], members[half:]
		return Family(self.location, leaving, self.direction, self.immunity) # No bounds with community are maintained

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

	def setLocation(self, location):
		self.location = location

	def getMapPoint(self):
		return self.mapPoint

	def resetWater(self):
		self.waterSteps = 0

	def addWaterStep(self):
		self.waterSteps += 1
		return self.waterSteps

	def setLastDirection(self, direction):
		self.direction = direction

	def getLastDirection(self):
		return self.direction

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

	return Family([lon, lat], members)

def getNewPosition(location, direction):
	size = settings.SIZE
	dist = settings.travelDist
	lon, lat = location

	lonRatio = math.cos(direction)*dist/size
	latRatio = math.sin(direction)*dist/size
	newLon = lon + lonRatio*360
	newLat = lat + latRatio*180

	return newLon, newLat

def updateLocation(family):
	location = family.getLocation()

	if isLand(family.getLocation()):
		family.resetWater()
		while True:
			direction = 2*math.pi*random.random()
			newLon, newLat = getNewPosition(location, direction)
			if isLand([newLon, newLat]) or random.random() < settings.WATERCHANCE:
				badZone = badzones(newLon, newLat)
				if badZone == 0:
					continue
				if badZone == 0.5:
					location = [newLon, newLat]
					continue
				family.setLastDirection(direction)
				break

	else:
		steps = family.addWaterStep()
		development = family.getDevelopment()
		direction = family.getLastDirection()
		if steps < settings.WATERCHANCE*math.sqrt(development):
			newLon, newLat = getNewPosition(location, direction)
		else:
			direction += math.pi
			newLon, newLat = getNewPosition(location, direction)		

	family.setLocation([newLon, newLat])
	family.getMapPoint().set_data(newLon, newLat)
	return True


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
def normGriddensity(POPULATION,x,y,numofperson):
        i=int((lon-(-180))/5)
        j=int((90-lat)/5)
        normpopulation=POPULATION[i,j]/numofperson
        normpopulation=-normpopulation+1
        
        return normpopulation
def getTemperature(x,y):
        if (y<=16 and y>=-20):
            T=27
        else:
            if y>16:
                T=40.76-0.86*y
                
            else:
                T=39.6-0.63*(math.fabs(y))
        return (T+36)/63.0    
# Checking for Malnouttrition Function
#Checks for the amount of calorie per grid and temperature
def getCondition(family):
            [lon,lat]=family.getLocation    
            value=normGriddensity(settings.GRIDPOPULATION,lon,lat)*getTemperature(lon,lat)
            value=-value+1
            if random.random() > value:
                n = int(len(family.getMembers()*(value)))
                
                members = family.getMembers()
                np.shuffle(members)
                family.setMembers(members[:n])

        

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

