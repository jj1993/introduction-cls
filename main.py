from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import random, time

# Get river paths without drawing
m = Basemap()
rivers = m.drawrivers().get_paths()

plt.ion()
fig, ax = plt.subplots()

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
map = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.fillcontinents(color='coral',lake_color='aqua')
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='aqua')
# draw parallels and meridians.
map.drawparallels(np.arange(-90.,91.,30.))
map.drawmeridians(np.arange(-180.,181.,60.))

## Some code for using the river_path objects
# for i in range(len(rivers)):
#     poly_path = rivers[i]
    
#     # get the Basemap coordinates of each segment
#     coords_cc = np.array(
#         [(vertex[0],vertex[1]) 
#          for (vertex,code) in poly_path.iter_segments(simplify=False)]
#     )
    
#     # convert coordinates to lon/lat by 'inverting' the Basemap projection
#     lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)

#     x, y = map(lon_cc, lat_cc)
    
#     # add plot
#     map.plot(x, y, 'b-')



# Now for some points
def makePoints():
	people = [i for i in range(15)]
	lons = [360*(random.random()-.5) for i in people]
	lats = [180*(random.random()-.5) for i in people]
	x, y = map(lons, lats)

	newX, newY, labels = [], [], []
	for i in range(len(people)):
		if map.is_land(x[i], y[i]):
			newX.append(x[i])
			newY.append(y[i])
			labels.append(i)

	points = map.plot(newX, newY, 'bo', markersize=18)
	 
	for label, xpt, ypt in zip(labels, newX, newY):
	    labels = plt.text(xpt, ypt, label)

	plt.title('Some points on the world map')
	fig.canvas.draw()

	return points, labels

for i in range(5):
	points, labels = makePoints()
	time.sleep(2)
	for p in points:
		p.remove()
	labels.remove() #this doesn't work...