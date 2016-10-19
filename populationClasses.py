import random, math
import matplotlib.pyplot as plt
import settings
import numpy as np

class Family(object):
	def __init__(self, location, members, direction = 0, immunity = 1.0, development=1, community = None):
		self.location = location #[x,y]
		self.immunity = immunity #float
		self.community = community #object or None
		self.development = development
		self.members = members
		self.waterSteps = 0
		self.direction = direction
		if community:
		       x, y = location
		       mapPoint = map.plot(x, y, 'ro', markersize=4)[0]
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

	def getFamilyEncounters(self, families):
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
				print(community.immunity)

			# if self.community:
			# 	changeOfAlliance(self.community, society)

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
	        
	        if self.community:
	           isiT=goodEnough(self.location)
	           if isiT:
	               community=Community(self.members, self.location, self.immunity, self.development)
	               self.members=[]
	               return True, community
	               
	           else: return False, None
	        else: return False, None


def goodEnough(location):
        Land=isLand(location)
        T=0.025*getTemperature(location[0],location[1])
        badZone=0.1*badzones(location[0],location[1])
        if random.random()<badZone and random.random()<T:
                if Land: return True
        else:
                return False

"""
class Community(object):
	def __init__(self, members, location, immunity, development):#, alliance=None):
		self.members = members #integer
		self.location = location #[x, y]
		self.immunity = immunity #float
		self.development = development #float, starts at 1 in communities
		self.explorers = [] # A special member who scans vicinity for new area. Resposible for spread
		# if alliance: self.alliances = [alliance]
		# else: self.alliances = []

		x, y = location
		mapPoint = map.plot(x, y, 'ro', markersize=4)[0]
		self.mapPoint = mapPoint #visual attribute on the map

	def update(self):
	    pass
	    
        def updateLocation(self):
	    pass
    
	def split(self):
	        half = int(0.5*len(self.members))
		members = self.members
		random.shuffle(members)
		self.members, leaving = members[:half], members[half:]
		return Community(leaving, self.location, self.immunity) # there are aligned to the self community 
"""
"""	
	def waterstep(self):
	    pass



	def getMembers(self):
		return self.members
		
	def getLocation(self):
	    return self.location
	    
	def getImmunity(self):
	    return self.immunity
	    
	def getDevelopment(self):
	    return self.development
	    
	def getDirection(self):
	    return self.direction
	
	def getExplorers(self):
	    return self.explorers
	    
	def getMapPoint(self):
		return self.mapPoint
	
	def setMembers(self, members):
	    return members
	
	
	def setExplorers(self, explorers):
	    return explorers
	
"""	    
	    
	

"""
	def updateAlliances(self):
		for community in self.alliances:
			if community.getSize() > self.population:
				del community

	def getDistance(self, location):
		x1, y1 = self.location
		x2, y2 = location
		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)

	def getRadius(self):
		return DENSITYFACTOR*self.population/self.development

	def getGrowthPossbilities(self):
		return self.development/len(self.members)

"""


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

	return newLon, newLat

def updateLocation(family):
	location = family.getLocation()

	if isLand(family.getLocation()):
		family.resetWater()
		while True:
			direction = 2*math.pi*random.random()
			newLon, newLat = getNewPosition(location, direction)
			#print(newLon,newLat)
                        newLon = math.fabs(newLon)%180*(newLon/(math.fabs(newLon)))-int(math.fabs(newLon)/180)*(180)*(newLon/math.fabs(newLon))			
			newLat = math.fabs(newLat)%90*(newLat/(math.fabs(newLat)))-int(math.fabs(newLat)/90)*(90)*(newLat/math.fabs(newLat))				
			#print(newLon,newLat)
			
			if isLand([newLon, newLat]) or random.random() < settings.WATERCHANCE:
				badZone = badzones(newLon, newLat)
				if random.random()>=badZone: 
					location = [newLon, newLat] # add a extra condition to not make this infinite steps
					continue
				family.setLastDirection(direction)
				break

	else:
		steps = family.addWaterStep()
		development = family.getDevelopment()
		direction = family.getLastDirection()
		if steps < settings.WATERCHANCE*math.sqrt(development):
			newLon, newLat = getNewPosition(location, direction)
			newLon = math.fabs(newLon)%180*(newLon/(math.fabs(newLon)))-int(math.fabs(newLon)/180)*(180)*(newLon/math.fabs(newLon))			
			newLat = math.fabs(newLat)%90*(newLat/(math.fabs(newLat)))-int(math.fabs(newLat)/90)*(90)*(newLat/math.fabs(newLat))				
			
		else:
			direction += math.pi
			newLon, newLat = getNewPosition(location, direction)
			newLon = math.fabs(newLon)%180*(newLon/(math.fabs(newLon)))-int(math.fabs(newLon)/180)*(180)*(newLon/math.fabs(newLon))			
			newLat = math.fabs(newLat)%90*(newLat/(math.fabs(newLat)))-int(math.fabs(newLat)/90)*(90)*(newLat/math.fabs(newLat))				
			

	family.setLocation([newLon, newLat])
	family.getMapPoint().set_data(newLon, newLat)
	return True


def diseaseSpread(family, disease, immunity, dd):
 	#Checks if the individual will get sick
 	if immunity > disease: return dd

 	exponent = (immunity-disease)/(disease/5.0)
 	chanceOfGettingSick = 1/(math.exp(exponent) + 1) # Look at fermi-dirac statistics for shape

	if random.random() < chanceOfGettingSick:
		ratio = immunity/float(disease)
		members = family.getMembers()
		np.random.shuffle(members)
		n = int(round(ratio*len(members)))
		#print(n,len(members))
		temp=len(members)-n
		#print(dd,temp)
		dd=dd+temp
		family.setMembers(members[:n])
		#print(len(family.getMembers()))
 	return dd

def GriDensity(DENSITY,lon,lat):
        j=int((lon+180)/5)
        i=int((90-lat)/5)
        
        return DENSITY[i,j]
    #    normpopulation=(DENSITY[i,j]-0.3)/(18-0.3)
        #print("normpopulation")
        #normpopulation=-normpopulation+1
        #print(DENSITY[i,j],normpopulation)
     #   return normpopulation
     

def getTemperature(x,y):
	if (y<=16 and y>=-20):
		T=27
	else:
		if y>16:
			T=40.76-0.86*y
		else:
			T=39.6-0.63*(math.fabs(y))

	return 1-.01*(T+38)/65.0
	    
# Checking for Malnouttrition Function
#Checks for the amount of calorie per grid and temperature

def getCondition(family,GRIDDENSITY,d):
	[lon,lat]=family.getLocation()    
	value=GriDensity(GRIDDENSITY,lon,lat)*settings.HUNGERDYING
	if family.community: value=value*0.01
	if random.random() < value:
		n = int(round(len(family.getMembers())*(value)))
		d += n

		members = family.getMembers()
		#print(len(family.getMembers()),value,n)
		random.shuffle(members)
		family.setMembers(members[n:])
	return d

#Adds population to the specific GRID        
def modifygrid(x,y,members,GRIDPOPULATION):
	j=int((x-(-180))/5)
	i=int((90-y)/5)
	GRIDPOPULATION[i,j] += members
	#print(members,GRIDPOPULATION[i,j],(i,j))
	#print("here")
	return GRIDPOPULATION

# Calculates population density per GRID                        
def griddensity(GRIDPOPULATION, numPersons): # Calculated by using the formula you suggested
        w=len(np.arange(-180.,181.,5))
        h=len(np.arange(-90.,91.,5))
        
        GRIDDENSITY=np.zeros((h-1,w-1))
        
        mink = math.fabs(3.5*(10**6)*(math.sin(math.radians(5))))/(100000)
        maxValue = 500000/mink

        for i in range(18): 
            pi1=math.radians(90-5*i)
            pi2=math.radians(90-5*(i+1))
            k=math.fabs(3.5*(10**6)*(math.sin(pi1)-math.sin(pi2))) #km^2
            k=k/(100000)                                        # 10^5 km^2
            GRIDDENSITY[i,:]=GRIDPOPULATION[i,:]/(k*maxValue)
            GRIDDENSITY[35-i,:]=GRIDPOPULATION[35-i,:]/(k*maxValue)
            
        return GRIDDENSITY     

# Checking if family is in a bad zones
# Bad zones are those regions where human habitation is not probable (Deserts, Artic Zones, Mountains)         
# 0 means you can't inhabit, 0.5 possible but hard. Migration through these routes possible
# 1 means migration as well as settlement is possible
def badzones(x,y):
        if y<=-60:#Artic Zones
            return 0
        elif (x>=115 and x<=150) and (y>=-30 and y<=-15): #Deserts in Australia
            return 0.6
        elif x>=85 and y>=50: #Parts of Russia and Syberia
            return 0.90
        elif x<=-10 and y>=50: #Alaska, Greeland
            return 0.75
        elif (x>=-120 and x<=-90) and (y>=35 and y<=45): # North American Desert
            return 0.75
        elif (x>=-10 and x<=30) and (y>=15 and y<=30): #Sahara Desert
            return 0.2
        else: # Everywhere else
            return 1 

class Community(object):
	def __init__(self, members, location, immunity, development,community=True):#, alliance=None):
		self.members = members #integer
		self.location = location #[x, y]
		self.immunity = immunity #float
		self.community=community
		self.development = development #float, starts at 1 in communities
		#self.explorers = [] # A special member who scans vicinity for new area. Resposible for spread
		# if alliance: self.alliances = [alliance]
		# else: self.alliances = []

		x, y = location
		mapPoint = map.plot(x, y, 'ro', markersize=4)[0]
		self.mapPoint = mapPoint #visual attribute on the map
		
	def update(self,rate):
	        if random.random()<rate:
	                self.development += 6
	                self.immunity+=6
		else:
		        self.development+=3
		        self.immunity+=3
		if len(self.members) <10:
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
		direction=0
		explorers=Family(self.location, explorers, direction, self.immunity, self.development, self)
		#explorers.update()
		#childCommunity=Community(explorers.members, explorers.location, explorers.immunity, explorers.development)
		#explorers.kill()
		return explorers  # Bounds with community are maintained

	    
	def getMembers(self):
		return self.members
	
	def getImmunity(self):
		return self.immunity
	
	#def growImmunity(self, disease):
	#	if self.immunity > disease: return
	#	growth = settings.IMMUNITYGROWTH*(disease-self.immunity + 1)
	#	self.immunity += growth
	#	return
		
	def getLocation(self):
	        return self.location
	       	
	def setMembers(self, members):
	        self.members=members	
	
	def getDistance(self, location):
		x1, y1 = self.location
		x2, y2 = location
		return math.sqrt((x1-x2)**2 + (y1 - y2)**2)