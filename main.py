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
	basemap.drawparallels(np.arange(-90.,91.,5))
	basemap.drawmeridians(np.arange(-180.,181.,5))
	
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
        
          
if __name__ == "__main__":
	# Initiate global variables
	getLand()
	settings.init()
	
	# Initiate map
	fig, basemap, land = drawMap()
	# rivers = getRiverPaths()
	G=makegrid()
	

	# Initiate families on map
	families = [newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	# communities = []

	plt.title('Some families on the world map')
	fig.canvas.draw()

	for i in range(250):
		newFamilies = []
		for family in families:
			if len(family.getMembers()) > 30:
				newFamilies.append(family.split())
			stillAlive = family.update()
			if stillAlive: newFamilies.append(family)
		families = newFamilies

		# # New diseases and development update, due to encounters
		# for family in families:
		# 	encounters = family.getFamilyEncounters()
		# 	immunity = family.getImmunity()
		# 	for encounter in encounters:
		# 		disease = encounter.getImmunity()
		# 		for member in family.getMembers():
		# 			diseaseSpread(member, disease, immunity)
		# 		family.growImmunity(disease)

		numPersons, totAge = 0, 0
		for family in families:
			members = family.getMembers()
			numPersons += len(members)
			totAge += sum(members)

		fig.canvas.draw()
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