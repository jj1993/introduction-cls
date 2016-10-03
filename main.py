from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random, time
from populationClasses import newFamily

"""
Starting variables
"""
NUMFAMILIES = 100
FAMILYSIZE = 10
LATLON = [[-90,90],[-120,-30]]

"""
Other tweaking variables
"""
DENSITYFACTOR = 0.1 # defines how dense the population in communities is
MAXAGE = 40 # defines a mean year of dying of old age
MAXAGESPREAD = MAXAGE/10.0 # defines the spread in dying of old age
BABYRANGE = [16, 35] # range of ages for getting a baby
BABYCHANCE = 0.125 # chance of heaving a baby each year
MINFOOD = 1.0 #minimal food value for checkForFood()
ENCOUNTERDIST = 1 #km? the distance withing an encounter 'counts'
RECOVERYRATE = 0.5 # the factor the sickness is multiplied by each year
IMMUNITYGROWTH = 1 # factor to define the amount of immunity growth due to encounters with diseases

def drawMap():
	plt.ion()
	fig, ax = plt.subplots()

	# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
	# are the lat/lon values of the lower left and upper right corners
	# of the basemap.
	# lat_ts is the latitude of true scale.
	# resolution = 'c' means use crude resolution coastlines.
	basemap = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
	            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

	# draw coastlines, country boundaries, fill continents.
	basemap.drawcoastlines(linewidth=0.25)
	basemap.fillcontinents(color='coral',lake_color='aqua')
	# draw the edge of the basemap projection region (the projection limb)
	basemap.drawmapboundary(fill_color='aqua')
	# draw parallels and meridians.
	basemap.drawparallels(np.arange(-90.,91.,30.))
	basemap.drawmeridians(np.arange(-180.,181.,60.))

	return fig, basemap

def getRiverPaths():
	# Get river paths without drawing
	m = Basemap()
	rivers = m.drawrivers().get_paths()

	## Some code for using the river_path objects
	# for i in range(len(rivers)):
	#     poly_path = rivers[i]
	    
	#     # get the Basebasemapcoordinates of each segment
	#     coords_cc = np.array(
	#         [(vertex[0],vertex[1]) 
	#          for (vertex,code) in poly_path.iter_segments(simplify=False)]
	#     )
	    
	#     # convert coordinates to lon/lat by 'inverting' the Basebasemapprojection
	#     lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)

	#     x, y = map(lon_cc, lat_cc)
	    
	#     # add plot
	#     basemap.plot(x, y, 'b-')

	return rivers

# Now for some points
def testPoints():
	people = [i for i in range(15)]
	lons = [360*(random.random()-.5) for i in people]
	lats = [180*(random.random()-.5) for i in people]
	x, y = basemap(lons, lats)

	newX, newY, labels = [], [], []
	for i in range(len(people)):
		if basemap.is_land(x[i], y[i]):
			newX.append(x[i])
			newY.append(y[i])
			labels.append(i)

	points = basemap.plot(newX, newY, 'bo', markersize=18)
	 
	for label, xpt, ypt in zip(labels, newX, newY):
	    labels = plt.text(xpt, ypt, label)

	plt.title('Some points on the world map')
	fig.canvas.draw()

	return points, labels

if __name__ == "__main__":
	# Initiate map
	fig, basemap = drawMap()
	# rivers = getRiverPaths()

	# Initiate families on map
	familyPoints = []
	families = [newFamily(basemap, familyPoints) for i in range(NUMFAMILIES)]
	# communities = []

	plt.title('Some families on the world map')
	fig.canvas.draw()
	time.sleep(5)
	# for i in range(5):
	# 	points, labels = makePoints()
	# 	time.sleep(2)
	# 	for p in points:
	# 		p.remove()
	# 	labels.remove() #this doesn't work...

