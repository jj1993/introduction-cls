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

#Regions where domesticatable wild plants arise after the glacial meltdown(Last ICE AGE)
def agriculturecentres(time): #time in years(BC)
	time = 1000 - time
	if time==1000:#850:
		return [37.5,38.5] #x=35,y=40 Fertile Cresent
	elif time==750:
		return [117.5,36.5] #x=115,y=35 China
	elif time==700:
		return [142.5,-7.5] #x=140,y=-5 New Guinea
	elif time==500:
		return [7.5,12.5] #x=5,y=10 Sahel
	elif time==350:
		return [-97.5,17.5] #x=-100,y=15 Mesoamerica
	elif time==340:
		return [-72.5,-2.5] #x=-75,y=-5 Andes and Amazonion
	elif time==300:
		return [2.5,12.5] #x=0,y=10 Tropical West Africa
	elif time==250:
		return [-87.5,37.5] #x=-85,y=35 Eastern US
	else:
		return False #Agriculture is not activated anywhere

def update(members, isFarmer, location=None):
	# Filter old age
	members = [[n for n in m if n < settings.MAXAGE] for m in members]
	if isFarmer:#Farmers
	    # Filter baby possibilities
   	    pregnant = [[0 for n in m if (
   	        n>settings.BABYRANGE[0] 
   	        and n<settings.BABYRANGE[1] 
   	        and random.random() < settings.FARMERBABYCHANCE*pC.cattlesavailable(loc)
   	                )] for m, loc in zip(members,location)]
   	else: #Hunters
   	    pregnant = [[0 for n in m if (
   	                            n>settings.BABYRANGE[0] 
   	                            and n<settings.BABYRANGE[1] 
   	                            and random.random()<settings.HUNTERBABYCHANCE
   	                        )] for m in members]
   	# Concatinate lists
	return [[a+1 for b in c for a in b] for c in zip(members,pregnant)]

#Initializes the GRID
def makegrid(): 
         w=len(np.arange(-180.,181.,5))
         h=len(np.arange(-90.,91.,5))
         
         grid = [[[] for lon in range(w)] for lat in range(h)]
         #np.zeros((h-1,w-1))
         return grid
         
#Adds population to the specific GRID        
def modifygrid(x,y,group,grid):
	j=int((x-(-180))/5)
	i=int((90-y)/5)
	grid[i][j].append(group)
          
if __name__ == "__main__":
	#Initiate global variables
	settings.init()

	# Initiate map
	fig, basemap, land = drawMap()

	# Initiate families and map variables
	families = [pC.newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	communities = []
	malnutritionDeath, diseaseDeath, numPersonsprev = 0, 0, 1
	community=None

        # Plot empty map
	plt.title('Some families on the world map')
	fig.canvas.draw()
	
	for t in range(10000):
		# Getting feedback on the world
	        numPersons, totAge = 0, 0
		for family in families:
			members = family.getMembers()
			numPersons += len(members)
			totAge += sum(members)
	        numFarmers, totAgeF = 0, 0
		for community in communities:
			farmingmembers = community.getMembers()
			numFarmers += len(farmingmembers)
			totAgeF += sum(farmingmembers)
			
		rateOfGrowth=100*(numPersons/float(numPersonsprev))-100
		newPersonsPrev = numPersons
		
		# Communities can send out explorers      		        
		# Large families are split
		# Explorers have the chance to found communities
		# Communities and families are removed if they have no more members
		newFamilies, newCommunities = [], []
		
		for community in communities:
		        if (len(community.getMembers()) > len(communities) 
		            and len(community.getMembers()) > 500
		            and random.random() < settings.EXPLORERCHANCE):
				newFamily = community.splitexplorers()
				newFamilies.append(newFamily)
			stillAlive = community.update()
			if stillAlive: newCommunities.append(community)
			
		for family in families:
		        if len(family.getMembers()) > 300:
				newFamilies.append(family.split())
             	        community = family.startCommunity()
             	        if community:
             	            newCommunities.append(community)
			stillAlive = family.update()
			if stillAlive: newFamilies.append(family)
			
		communities = newCommunities
		families = newFamilies
	        
	        # Initiating a new grid and counting the population density
	        grid=makegrid()
	        groups = families + communities
		for group in groups:
      		        x, y = group.getLocation()
      		        modifygrid(x, y , group, grid)
      		griddensity = pC.setGriddensity(grid, numPersons)

		# Update the hunter familie members lifecycel and food
		familyMembers = np.array([family.getMembers() for family in families])
		newMembers = update(familyMembers, False)
		[family.setMembers(newMembers[n]) for n, family in enumerate(families)]
		for family in families:
      		        malnutritionDeath = pC.updateMalnutrition(family, griddensity, malnutritionDeath, False)

      		# Update the community familie members lifecycel and food
		communityMembers = np.array([community.getMembers() for community in communities])
		communityLocations = np.array([community.getLocation() for community in communities])
		newMembers = update(communityMembers, True, communityLocations)
		[community.setMembers(newMembers[n]) for n, community in enumerate(communities)]
      		for community in communities:
      		        malnutritionDeath = pC.updateMalnutrition(community,griddensity,malnutritionDeath, True)

		# Update diseases and development, due to encounters
		for family in families:
			if family.getWaterSteps() != 0:
				continue
			encounters = family.getEncounters(grid)
			immunity = family.getImmunity()
			community = family.getCommunity()
			development = family.getDevelopment()
			
			for encounter in encounters:
				disease = encounter.getImmunity()
				diseaseDeath = pC.diseaseSpread(family, disease, immunity, diseaseDeath)
				family.growImmunity(disease)
				if community:
				    community.growImmunity(disease)
				    community.growDevelopment()
				if type(encounter) == pC.Community:
				    encounter.growImmunity(immunity)
			
	        # Inject farming societies on certain time events
		agri = agriculturecentres(t)
		if agri:
			members = [random.randint(0, settings.MAXAGE) \
			             for i in range(settings.COMMUNITYSIZE)]
			immunities = []
			for family in families:
			             if family.getDistance(agri) < 50:
			                 immunities.append(family.getImmunity())
			immunity = np.mean(immunities)
			development = np.mean(
			                 [g.getDevelopment() for g in groups]
			                 )
			community = pC.Community(
			                 members, agri, immunity, development
			                 )
			newCommunities.append(community)
		
		#fig.canvas.draw()
		plt.pause(0.001)
		print "Timestep ",t
		print "Total hunters {}".format(numPersons)
		print "Average age of hunters {}".format(totAge/float(numPersons))
		try:
		        ave = totAgeF/float(numFarmers)
		        print " Number of communities {}".format(len(communities))
		        print "Total farmers {}".format(numFarmers)
		        print "Average age of famers {}".format(ave)
		except: pass
		print np.mean([f.getImmunity() for f in families])
		print np.mean([f.getImmunity() for f in communities])
		
		print "No of Deaths by Malnutrition yet {}".format(malnutritionDeath)
		print "No of Deaths by Diseases yet {}".format(diseaseDeath)
		print "Rate of Growth {}".format(rateOfGrowth)
		