def init():
	"""
	Starting variables
	"""
	global NUMFAMILIES, FAMILYSIZE, LONLAT
	NUMFAMILIES = 40
	FAMILYSIZE = 10
	LONLAT = [(-30,40),(-50,40)]

	"""
	Other tweaking variables
	"""
	global DENSITYFACTOR, MAXAGE, MAXAGESPREAD, BABYRANGE, BABYCHANCE, MINFOOD, ENCOUNTERDIST, RECOVERYRATE, IMMUNITYGROWTH
	DENSITYFACTOR = 0.1 # defines how dense the population in communities is
	MAXAGE = 40 # defines a mean year of dying of old age
	MAXAGESPREAD = MAXAGE/10.0 # defines the spread in dying of old age
	BABYRANGE = [16, 35] # range of ages for getting a baby
	BABYCHANCE = 0.125 # chance of heaving a baby each year
	MINFOOD = 1.0 #minimal food value for checkForFood()
	ENCOUNTERDIST = 1 #km? the distance withing an encounter 'counts'
	RECOVERYRATE = 0.5 # the factor the sickness is multiplied by each year
	IMMUNITYGROWTH = 1 # factor to define the amount of immunity growth due to 
					   # encounters with diseases

	"""
	Traveling
	"""
	global earthR, travelDist
	earthR = 6371 #km
	travelDist = 300 #km