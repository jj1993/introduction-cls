from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random, time
from populationClasses import newFamily
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
	# basemap.drawparallels(np.arange(-90.,91.,5))
	# basemap.drawmeridians(np.arange(-180.,181.,5))
	
	return fig, basemap, land

#Initializes the GRID
def makegrid():
         w=len(np.arange(-180.,181.,5))
         h=len(np.arange(-90.,91.,5))
         global GRIDPOPULATION
         gridpopulation=np.zeros((w,h))
         return gridpopulation

#Calculates Temperature at X,Y
def getTemperature(x,y):
        if (y<=16 and y>=-20):
            T=27
        else:
            if y>16:
                T=40.76-0.86*y
            else:
                T=39.6-0.63*(math.fabs(y))
        return T

#Adds population to the specific GRID        
def modifygrid(x,y):
        i=int((x-(-180))/5)
        j=int((90-y)/5)
        GRIDPOPULATION[i,j]=+1

# Calculates population density per GRID                        
def griddensity():
        k=1.89*(10^5) # Calculated from Total Surface area by total number of GRIDS
        global GRIDDENSITY
        GRIDDENSITY=GRIDPOPULATION/k

# Checking if family is in a bad zones
# Bad zones are those regions where human habitation is not probable (Deserts, Artic Zones, Mountains)         
# 0 means you can't inhabit, 0.5 possible but hard. Migration through these routes possible
# 1 means migration as well as settlement is possible
def badzones(x,y):
    if y>=60:
        return 0
    elif (x>=115 and x<=150) and (y>=-30 and x<=-15):
        return 0.5
    elif x>=85 and y>=50:
        return 0.5
    elif x<=-10 and y>=50:
        return 0.5
    elif (x>=-120 and x<=-90) and (y>=35 and x<=45):
        return 0.5
    elif (x>=-10 and x<=30) and (y>=15 and x<=30):
        return 0.5
    else:
        return 1   
    
#Regions where domesticatable wild plants arise after the glacial meltdown(Last ICE AGE)
def agriculturecentres():
	pass
    #Going for Karate. Will define after that

# I will explain why this function is important when we meet    
def barrier():    
	pass
    #Going for Karate. Will define after that

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
	return [[a+1 for b in c for a in b] for c in zip(members,pregnant)]

          
if __name__ == "__main__":
	# Initiate global variables
	# getLand()
	settings.init()
	
	# Initiate map
	fig, basemap, land = drawMap()
	# rivers = getRiverPaths()
	G=makegrid()
	

	# Initiate families on map
	families = [newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	familyMembers = np.array([family.getMembers() for family in families])

	plt.title('Some families on the world map')
	fig.canvas.draw()

	for i in range(250):
		newFamilies = []
		for family in families:
			if len(family.getMembers()) > 300:
				newFamilies.append(family.split())
			stillAlive = family.update()
			if stillAlive: newFamilies.append(family)
		families = newFamilies

		# More efficiently update the familie members
		familyMembers = [family.getMembers() for family in families]
		newMembers = update(familyMembers)
		[family.setMembers(newMembers[n]) for n, family in enumerate(families)]

		# Get centre of mass coordinate
		CM = getCM(families)

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
			members = family.getMembers()
			numPersons += len(members)
			totAge += sum(members)

		# fig.canvas.draw()
		print "Timestep ",i
		print "Total people {}".format(numPersons)
		print "Average age {}".format(totAge/float(numPersons))
	# for i in range(5):
	# 	points, labels = makePoints()
	# 	time.sleep(2)
	# 	for p in points:
	# 		p.remove()
	# 	labels.remove() #this doesn't work...


# def getRiverPaths():
# 	# Get river paths without drawing
# 	m = Basemap()
# 	rivers = m.drawrivers().get_paths()

# 	## Some code for using the river_path objects
# 	# for i in range(len(rivers)):
# 	#     poly_path = rivers[i]
	    
# 	#     # get the Basebasemapcoordinates of each segment
# 	#     coords_cc = np.array(
# 	#         [(vertex[0],vertex[1]) 
# 	#          for (vertex,code) in poly_path.iter_segments(simplify=False)]
# 	#     )
	    
# 	#     # convert coordinates to lon/lat by 'inverting' the Basebasemapprojection
# 	#     lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)

# 	#     x, y = map(lon_cc, lat_cc)
	    
# 	#     # add plot
# 	#     basemap.plot(x, y, 'b-')

# 	return rivers