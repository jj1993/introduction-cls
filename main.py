from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random, time
import populationClasses as pC 
import settings
import math
from PIL import Image

def getLand():
	fig = plt.figure()
	basemap = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
	            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='l')
	basemap.fillcontinents(color='black',lake_color='black')
	image = fig.savefig("land.jpg", bbox_inches='tight', pad_inches=0, transparent=True, format="jpg")

def drawMap():
	plt.ion()
	fig, ax = plt.subplots()

	# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
	# are the lat/lon values of the lower left and upper right corners
	# of the basemap.
	# lat_ts is the latitude of true scale.
	# resolution = 'c' means use crude resolution coastlines.
	basemap = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
	            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

	# draw coastlines, country boundaries, fill continents.
	basemap.drawcoastlines(linewidth=0.25)
	land = basemap.fillcontinents(color='coral',lake_color='aqua')
	# draw the edge of the basemap projection region (the projection limb)
	basemap.drawmapboundary(fill_color='aqua')
	# draw parallels and meridians.
	#basemap.drawparallels(np.arange(-90.,91.,5))
	#basemap.drawmeridians(np.arange(-180.,181.,5))
	
	return fig, basemap, land

#Calculates Temperature at X,Y
def getTemperature(x,y):
        if (y<=16 and y>=-20):
            T=27
        else:
            if y>16:
                T=40.76-0.86*y
                
            else:
                T=39.6-0.63*(math.fabs(y))
        return (T+36)/63.0
       
#Regions where domesticatable wild plants arise after the glacial meltdown(Last ICE AGE)
def agriculturecentres(time): #time in years(BC)
        if time==8500:
            return 37.5,42.5 #x=35,y=40 Fertile Cresent
        elif time==7500:
            return 117.5,37.5 #x=115,y=35 China
        elif time==7000:
            return 142.5,-7.5 #x=140,y=-5 New Guinea
        elif time==5000:
            return 7.5,12.5 #x=5,y=10 Sahel
        elif time==3500:
            return -97.5,17.5 #x=-100,y=15 Mesoamerica
        elif time==3400:
            return -72.5,-2.5 #x=-75,y=-5 Andes and Amazonion
        elif time==3000:
            return 2.5,12.5 #x=0,y=10 Tropical West Africa
        elif time==2500:
            return -87.5,37.5 #x=-85,y=35 Eastern US
        else:
            return 0,0 #Agriculture is not activated anywhere

# This function identifies the relevant cell number from the population grid. 
#And returns 1 percent of total families in that cell to which are to be mutated to Farmers
def activatefarmers(x,y): # x,y here are the return values of agriculturecentres()
        i=int((x-(-180))/5)
        j=int((90-y)/5)
        return 0.01*GRIDPOPULATION[i,j]
         
# Checks for availabilty at x,y. Returns within 0-1 Scale. 0 being null amount, 1 being high amount(13 Cattles). 
# 0.5 is to be taken as moderate amount
# The return value need to affect the rate of agriculture at each location         
def cattlesavailable(x,y):
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

# I will explain why these two functions are important when we meet    
def barrier():
	pass
def areacorrelation(x1,y1,x2,y2):
	pass
    
def getCM(families):
	# Get the centre position of all the families
	positions = []
	for family in families:
		pos = family.getLocation()
		positions.append(pos)
	positions = np.array(positions)
	return np.mean(positions, axis=0)

def update(members):
	# Filter old age
	members = [[n for n in m if n<settings.MAXAGE] for m in members]
	# Filter baby possibilities
	pregnant = [[0 for n in m if n>settings.BABYRANGE[0] and n<settings.BABYRANGE[1] and random.random()<settings.BABYCHANCE] for m in members]
	# Concatinate lists
	#print("Working")
	return [[a+1 for b in c for a in b] for c in zip(members,pregnant)]
          
if __name__ == "__main__":
	# Initiate global variables
	# getLand()
	settings.init()

	# Initiate map
	fig, basemap, land = drawMap()

	# Initiate families on map
	families = [pC.newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	familyMembers = np.array([family.getMembers() for family in families])
	print(familyMembers[1])

	plt.title('Some families on the world map')
	fig.canvas.draw()
	

	for i in range(10000):
		newFamilies = []
		for family in families:
			if len(family.getMembers()) > len(families):
				newFamilies.append(family.split())
			stillAlive = family.update()
			if stillAlive: newFamilies.append(family)
		families = newFamilies

		# More efficiently update the familie members
		familyMembers = np.array([family.getMembers() for family in families])
		newMembers = update(familyMembers)
		[family.setMembers(newMembers[n]) for n, family in enumerate(families)]

		# # New diseases and development update, due to encounters
		# for family in families:
		# 	encounters = family.getFamilyEncounters()
		# 	immunity = family.getImmunity()
		# 	for encounter in encounters:
		# 		disease = encounter.getImmunity()
		# 		for member in family.getMembers():
		# 			diseaseSpread(member, disease, immunity)
		# 		family.growImmunity(disease)

		# Get some feedback on the world population
		numPersons, totAge = 0, 0
		for family in families:
			loc=family.getLocation()
			members = family.getMembers()
			pC.modifygrid(loc[0],loc[1],len(members))
			numPersons += len(members)
			totAge += sum(members)
		pC.griddensity()

		fig.canvas.draw()
		print "Timestep ",i
		print "Total people {}".format(numPersons)
		print "Average age {}".format(totAge/float(numPersons))