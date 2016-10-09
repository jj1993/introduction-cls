from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random, time
from populationClasses import newFamily
from populationClasses import settings

def drawMap():
	plt.ion()
	fig, ax = plt.subplots()

	# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
	# are the lat/lon values of the lower left and upper right corners
	# of the basemap.
	# lat_ts is the latitude of true scale.
	# resolution = 'c' means use crude resolution coastlines.
	basemap = Basemap(projection='cyl',llcrnrlat=-80,urcrnrlat=80,\
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

if __name__ == "__main__":
	# Initiate global variables
	settings.init()
	# Initiate map
	fig, basemap = drawMap()
	# rivers = getRiverPaths()

	# Initiate families on map
	families = [newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	# communities = []

	plt.title('Some families on the world map')
	fig.canvas.draw()

	for i in range(100):
		newFamilies = []
		for family in families:
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

		fig.canvas.draw()
		print "Timestep ",i
		# time.sleep(0.02)
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