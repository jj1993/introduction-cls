import random, math

DENSITYFACTOR = 0.1 # defines how dense the population in communities is
MAXAGE = 40 # defines a mean year of dying of old age
MAXAGESPREAD = MAXAGE/10.0 # defines the spread in dying of old age
BABYRANGE = [16, 35] # range of ages for getting a baby
BABYCHANCE = 0.125 # chance of heaving a baby each year
MINFOOD = 1.0 #minimal food value for checkForFood()
ENCOUNTERDIST = 1 #km? the distance withing an encounter 'counts'
RECOVERYRATE = 0.5 # the factor the sickness is multiplied by each year
IMMUNITYGROWTH = 1 # factor to define the amount of immunity growth due to encounters with diseases

class Family(Object):
	def __init__(self, location, members, immunity = 1.0, community = None):
		self.location = location #[x,y]
		self.hasFood = True
		self.immunity = immunity #float
		self.community = community #object or None
		self.sick = RECOVERYRATE * self.sick
		self.members = [11, 14, 5, 39]

	def getImmunity(self):
		return self.immunity

	def getCommunity(self):
		return self.community

	def update(self):
		self.hasFood = checkForFood(self.location, len(self.members))
		self.location = locationUpdate(self.location, self.hasFood)
		self.members = updateMembers(m)

		if doesFoundCommunity(location):
			newCommunity = Community(
				len(self.members), self.location, self.immunity, self.community
				)
			communities.append(newCommunity)

	def removeMember(self, member):
		for i, m in enumerate(self.members):
			if m == member:
				del self.members[i]
				return
		raise ValueError ("Member is not part of family")

	def addMember(self):
		baby = Person(0, self)
		self.members.append(baby)
		return

	def getFamilyEncounters(self):
		encounters = []
		for family in families:
			if (family != self and 
				family.getDistance(self.location) < ENCOUNTERDIST):
				encounters.append(family)
		return encounters

	def getSocietyEncounters(self):
		encounters = []
		for society in societies:
			if (society.getDistance(self.location) < ENCOUNTERDIST):
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
		growth = IMMUNITYGROWTH*(disease-self.immunity)
		self.immunity += growth
		return

def updateMembers(members):
	newM = []
	for m in members:
		m += 1

		exponent = (m-MAXAGE)/MAXAGESPREAD
		chanceOfDying = 1/(math.exp(exponent) + 1) # Look at fermi-dirac statistics for shape
		if random.random() > chanceOfDying:
			newM.append(m)

		if m in range(BABYRANGE) and random.random() < BABYCHANCE:
			newM.append(0)

	return newM

def updateLocation(location):
	pass

def checkForFood(location, nrMembers):
	food = getRainyValue(location)
	food += getTemperature(location)
	food += isRiverClose(location)
	return MINFOOD > food/nrMembers
def getRainyValue(location):
	pass
def getDomesticAnimals(location):
	pass

def doesFoundCommunity(location):
	pass


class Community(Object):
	def __init__(self, population, location, immunity, alliance):
		self.population = population #integer
		self.location = location #[x, y]
		self.immunity = immunity #float
		self.development = 1 #float, starts at 1 in communities
		self.explorers = [] #list of family objects
		if alliance: self.alliances = [alliance]
		else: self.alliances = []

	def getSize(self):
		return self.population

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

families = [family objects]
communities = [community objects]

def yearUpdate():
	for family in families:
		family.update()
	for family in families:
		encounters = family.getFamilyEncounters()
		immunity = family.getImmunity()
		for encounter in encounters:
			disease = encounter.getImmunity()
			for member in family.getMembers():
				diseaseSpread(member, disease, immunity)
			family.growImmunity(disease)


def diseaseSpread(member, disease, immunity):
	# Checks if the individual will get sick
	if member.getSick() > disease: return

	exponent = (immunity-disease)/(disease/5.0)
	chanceOfGettingSick = 1/(math.exp(exponent) + 1) # Look at fermi-dirac statistics for shape
	if random.random() < chanceOfGettingSick:
		member.setSick(disease)
	return