import random, math
import matplotlib.pyplot as plt
import settings
import numpy as np

def goodEnough(location):
        onLand=isLand(location)
        T=settings.EXPLORERTRAVEL*getTemperature(location[0],location[1])
        badZone=badzones(location[0],location[1])
        if badZone == 1 and random.random()<T and onLand:
                return True
        else:
                return False

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
	members = [
		random.randint(0, settings.MAXAGE) for i in range(random.randint(1, settings.FAMILYSIZE))
		]

	return Family([lon, lat], members)

def getNewPosition(location, direction):
	size = settings.SIZE
	dist = settings.travelDist
	lon, lat = location

	lonRatio = math.cos(direction)*dist/size
	latRatio = math.sin(direction)*dist/size
	newLon = lon + lonRatio*360
	newLat = lat + latRatio*180
        
        # This allowes people to walk from 180 longitude to -180 longitude
        if abs(newLon) > 180:
                newLon = np.sign(newLon)*(abs(newLon)%180 - 180)

	return newLon, newLat

def updateLocation(family):
	location = family.getLocation()

	if isLand(family.getLocation()):
		family.resetWater()
		limit = 0
		while limit < 100000:
		        limit += 1
			direction = 2*math.pi*random.random()
			newLon, newLat = getNewPosition(location, direction)
			if newLat < -85 or newLat > 85:
			    continue
			
			if (isLand([newLon, newLat]) 
			    or random.random() < settings.WATERCHANCE):
				badZone = badzones(newLon, newLat)
				if random.random() > badZone: 
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
	
# Checks for availabilty at x,y. Returns within 0-1 Scale. 0 being null amount, 1 being high amount(13 Cattles). 
# 0.5 is to be taken as moderate amount
# The return value need to affect the rate of agriculture at each location         
def cattlesavailable(loc):
    x, y = loc
    if (x>=-10 and x<=40) and (y>=35 and y<=75): #Eurasia 1
        return 1
    elif (x>40 and x<50) and (y>=15 and y<=75): #Eurasia 2
        return 1
    elif (x>=50) and (y>=0): #Eurasia 3
        return 1
    elif (x>=-85 and x<=-35) and (y<=10 and y>=-55): # South America
        return 1/13 # or give another value maybe 0.1
    else: #Rest of the continent
        return 0

def diseaseSpread(family, disease, immunity, death):
 	#Checks if the individual will get sick
 	if immunity > disease: return death
 	    
        # Look at fermi-dirac statistics for shape
 	exponent = (immunity-disease)/(disease/5.0)
 	chanceOfGettingSick = 0.1/(math.exp(exponent) + 1)
 
	if random.random() < chanceOfGettingSick:
	        # Kills a portion of the members group in case of sickness
		ratio = immunity/float(disease)
		members = family.getMembers()
		np.random.shuffle(members)
		n = int(round(ratio*len(members)))
                death += len(members)-n
		family.setMembers(members[:n])
	return death

def getTemperature(x,y):
        # Returns a normalised temperature distribution
	if (y<=16 and y>=-20):
		T=27
	else:
		if y>16:
			T=40.76-0.86*y
		else:
			T=39.6-0.63*abs(y)

	return 1 - settings.TEMPNORM*(T+38)/65.0
	    
# Checks for overpopulation in regions
def updateMalnutrition(group, grid, death, isFarmer):
	lon, lat = group.getLocation()    
	value = getGridDensity(grid,lon,lat)*settings.HUNGERDYING
	if isFarmer:
	    value *= settings.COMMUNITYHUNGERDYING
	elif group.getCommunity():
	    value *= settings.COMMUNITYHUNGERDYING
	if random.random() < value:
		n = int(round(len(group.getMembers())*(value)))
		death += n

		members = group.getMembers()
		random.shuffle(members)
		group.setMembers(members[n:])
		
        return death

# Calculates population density per GRID                        
def setGriddensity(grid, numPersons):
        w=len(np.arange(-180.,181.,5))
        h=len(np.arange(-90.,91.,5))
        griddensity = np.zeros((h-1,w-1))
        
        mink = math.fabs(3.5*(10**6)*(math.sin(math.radians(5))))
        maxValue = 500000/mink

        for i in range(36):
            for j in range(72):
                pi1=math.radians(90-5*i)
                pi2=math.radians(90-5*(i+1))
                k=math.fabs(3.5*(10**6)*(math.sin(pi1)-math.sin(pi2))) #km^2
                n = sum([sum(group.getMembers()) for group in grid[i][j]])
                griddensity[i,j] += n/(k*maxValue)
            
        return griddensity

def getGridDensity(grid, lon, lat):
        # Returns the normalised population density at a grid point
        j=int((lon+180)/5)
        i=int((90-lat)/5)
        
        return grid[i][j]   
        
# Checking if family is in a bad zones
# Bad zones are those regions where human habitation is not probable (Deserts, Artic Zones, Mountains)         
# 0 means you can't inhabit, 1 means migration as well as settlement is possible
def badzones(x,y):
        if y<=-60:#Artic Zones
            return 0
        elif (x>=115 and x<=150) and (y>=-30 and y<=-15): #Deserts in Australia
            return 0.6
        elif x>=85 and y>=50: #Parts of Russia and Syberia
            return 0.9
        elif x<=-10 and y>=50: #Alaska, Greeland
            return 0.75
        elif (x>=-120 and x<=-90) and (y>=35 and y<=45): # North American Desert
            return 0.75
        elif (x>=-10 and x<=30) and (y>=15 and y<=30): #Sahara Desert
            return 0.2
        else: # Everywhere else
            return 1 
            
class Family(object):
	def __init__(self, location, members, immunity = 1.0, development=1, community = None):
		self.location = location #[x,y]
		self.immunity = immunity #float
		self.community = community #object or None
		self.development = development
		self.members = members
		self.waterSteps = 0
		self.direction = 0
		if community:
		       x, y = location
		       mapPoint = map.plot(x, y, 'ro', markersize=6)[0]
		       self.mapPoint = mapPoint #visual attribute on the map
                else:
		       x, y = location
		       mapPoint = map.plot(x, y, 'bo', markersize=2)[0]
		       self.mapPoint = mapPoint #visual attribute on the map

	def update(self):
		self.development += 1
		if len(self.members) < 2:
			self.mapPoint.remove()
			isAlive = False
			return isAlive
			
		isAlive = updateLocation(self)
		return isAlive

	def split(self):
		half = int(0.5*len(self.members))
		members = self.members
		random.shuffle(members)
		self.members, leaving = members[:half], members[half:]
		return Family(self.location, leaving, self.direction, self.immunity) # No bounds with community are maintained

	def getEncounters(self, grid):
	        lon, lat = self.location
	        j=int((lon+180)/5)
                i=int((90-lat)/5)
	        families = grid[i][j]
		encounters = []
		for family in families:
			if (family != self and 
				family.getDistance(self.location) < settings.ENCOUNTERDIST):
				encounters.append(family)
		return encounters

	def getCommunityEncounters(self, communities):
		encounters = []
		for community in communities:
			if (community.getDistance(self.location) < settings.ENCOUNTERDIST):
				encounters.append(community)
		return encounters

	def getDistance(self, location):
		x1, y1 = self.location
		x2, y2 = location
		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

	def growImmunity(self, disease):
		if self.immunity > disease: return
		growth = settings.IMMUNITYGROWTH*(disease-self.immunity + 1)
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

	def getWaterSteps(self):
		return self.waterSteps

	def setLastDirection(self, direction):
		self.direction = direction

	def getLastDirection(self):
		return self.direction
	
	def startCommunity(self):
	        # Explorer families from farming communities can start a new
	        # community
	        if self.community and goodEnough(self.location):
	               community = Community(self.members, self.location, self.immunity, self.development)
	               self.members = []
	               return community
	               
	        else: return None


class Community(object):
	def __init__(self, members, location, immunity, development):
		self.members = members # integer
		self.location = location # [x, y]
		self.immunity = immunity # float
		self.development = development # float

		x, y = location
		mapPoint = map.plot(x, y, 'ro', markersize=4)[0]
		self.mapPoint = mapPoint # visual attribute on the map
		
	def update(self):
	        cattleRate = cattlesavailable(self.location)
	        if random.random() < cattleRate: self.development += 6
		else: self.development += 3
		
		if len(self.members) < 10:
			self.mapPoint.remove()
			isAlive = False
			return isAlive
			
		isAlive = True
		return isAlive
			
	def splitexplorers(self):
	        half = int(0.5*len(self.members))
		members = self.members
		random.shuffle(members)
		self.members, explorers = members[:half], members[half:]
		explorers=Family(self.location, explorers, self.immunity, self.development, self)
		return explorers  # Bounds with community are maintained
	    
	def getMembers(self):
		return self.members
	
	def getImmunity(self):
		return self.immunity
	
	def growImmunity(self, disease):
	        growth = settings.IMMUNITYGROWTH*(disease-self.immunity + 1)
		if self.immunity < disease:
		        self.immunity += growth
		growth = 5*growth*cattlesavailable(self.location)
		self.immunity += growth
		return
		
	def getDevelopment(self):
	        return self.development
		
	def growDevelopment(self):
	        self.development += 2
		
	def getLocation(self):
	        return self.location
	       	
	def setMembers(self, members):
	        self.members=members	
	
	def getDistance(self, location):
		x1, y1 = self.location
		x2, y2 = location
		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)