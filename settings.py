from PIL import Image
import math
import time
import numpy as np

def init():
	"""
	Starting variables
	"""
	global NUMFAMILIES, FAMILYSIZE, LONLAT, COMMUNITYSIZE
	NUMFAMILIES = 30
	FAMILYSIZE = 10
	COMMUNITYSIZE = 100
	LONLAT = [(-30,40),(-50,40)]
	#LONLAT = [(160, 175),(60, 80)]

	"""
	Other tweaking variables
	"""
	global DENSITYFACTOR, MAXAGE, BABYRANGE, HUNTERBABYCHANCE, ENCOUNTERDIST, IMMUNITYGROWTH, HUNGERDYING, TEMPNORM
	DENSITYFACTOR = 0.1 # defines how dense the population in communities is
	MAXAGE = 40 # defines a mean year of dying of old age
	BABYRANGE = (16, 35) # range of ages for getting a baby
	HUNTERBABYCHANCE = 0.125 # chance of heaving a baby each year for hunters
	ENCOUNTERDIST = 10 #km? the distance withing an encounter 'counts'
	IMMUNITYGROWTH = .06 # factor to define the amount of immunity growth due to 
					   # encounters with diseases
        HUNGERDYING = 500 # Tweaking variable for influencing the population density normalisation
        TEMPNORM = .05 # Tweaking variable for influencing the temperature normalisation

	"""
	Traveling
	"""
	global SIZE, travelDist, LANDMAP, WATERCHANCE, POPU
	earthR = 6371 #km
	SIZE = earthR*2*math.pi
	travelDist = 300 #km
	LANDMAP = Image.open("land.jpg").load()
	WATERCHANCE = 0.1
	
	"""
	Famer variables
	"""
	global FARMERBABYCHANCE, EXPLORERCHANCE, COMMUNITYHUNGERDYING, EXPLORERTRAVEL
	FARMERBABYCHANCE = 0.250 # chance of heaving a baby each year for farmers
	EXPLORERCHANCE = 0.5 # Chance of sending out an explorer
	COMMUNITYHUNGERDYING = 0.01
	EXPLORERTRAVEL = 0.1