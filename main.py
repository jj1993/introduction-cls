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
	if time==850:
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
"""
# This function identifies the relevant cell number from the population grid. 
#And returns 1 percent of total families in that cell to which are to be mutated to Farmers
def activatefarmers(x,y): # x,y here are the return values of agriculturecentres()
    j=int((x-(-180))/5)
    i=int((90-y)/5)
    return 0.01*GRIDPOPULATION[i,j]
"""         
# Checks for availabilty at x,y. Returns within 0-1 Scale. 0 being null amount, 1 being high amount(13 Cattles). 
# 0.5 is to be taken as moderate amount
# The return value need to affect the rate of agriculture at each location         
def cattlesavailable(loc):
    x=loc[0]
    y=loc[1]
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
"""
def update(members):
	# Filter old age
	members_list = [m for m in members]
	idx_maxage = [np.where(m == settings.MAXAGE)[0] for m in members_list]
	members_list_new = [np.delete(members_list[i],idx_maxage[i]) for i in xrange(len(idx_maxage))]
	idx_pregnant = [np.where(
		(m > settings.BABYRANGE[1]) & (m < settings.BABYRANGE[0]) & (random.random()<settings.BABYCHANCE)
		)[0] for m in members_list]
	members_list_new = [np.append(members_list_new[i],np.zeros_like(idx_pregnant[i])) for i in xrange(len(idx_pregnant))]
	return members_list_new

"""
def update(members, type, location=None):
	# Filter old age
	members = [[n for n in m if n<settings.MAXAGE] for m in members]
	if type:#Farmers:
	    # Filter baby possibilities
   	    
   	    pregnant = [[0 for n in m if n>settings.BABYRANGE[0] and n<settings.BABYRANGE[1] and random.random()<settings.FARMERBABYCHANCE*cattlesavailable(loc)] for m,loc in zip(members,location)]
   	else: #Hunters
   	    pregnant = [[0 for n in m if n>settings.BABYRANGE[0] and n<settings.BABYRANGE[1] and random.random()<settings.HUNTERBABYCHANCE] for m in members]
   	# Concatinate lists
	#print("Working")
	return [[a+1 for b in c for a in b] for c in zip(members,pregnant)]

def makegrid(): #Initializes the GRID
         w=len(np.arange(-180.,181.,5))
         h=len(np.arange(-90.,91.,5))
         
         GRIDPOPULATION=np.zeros((h-1,w-1))
         return GRIDPOPULATION
          
if __name__ == "__main__":
	# Initiate global variables
	# getLand()
	settings.init()

	# Initiate map
	fig, basemap, land = drawMap()

	# Initiate families on map
	families = [pC.newFamily(basemap) for i in range(settings.NUMFAMILIES)]
	communities = []
	community=None

	plt.title('Some families on the world map')
	fig.canvas.draw()
	GRIDPOPULATION=makegrid()
	d=0
	dd=0
	numPersons=0
	numPersonsprev=0
	numFarmers=0
	FARMING=False

	for t in range(10000):		
	        numPersons, totAge = 0, 0
	        numFarmers, totAgeF=0, 0
		#counting the number of people
		for family in families:
			#loc=family.getLocation()
			members = family.getMembers()
			
			#print(GRIDPOPULATION[k[0],k[1]])
			numPersons += len(members)
			totAge += sum(members)
	        
	        GRIDPOPULATION=makegrid()
		for family in families:
      		        loc=family.getLocation()
      		        members=family.getMembers()
      		        
      		        GRIDPOPULATION=pC.modifygrid(loc[0],loc[1],len(members),GRIDPOPULATION)
      		
      		for community in communities:
      		        loc=family.getLocation()
      		        members=community.getMembers()
      		        
      		        GRIDPOPULATION=pC.modifygrid(loc[0],loc[1],len(members),GRIDPOPULATION)
      		
      		GRIDDENSITY=pC.griddensity(GRIDPOPULATION, numPersons)
      		for family in families:
      		        d=pC.getCondition(family,GRIDDENSITY,d)
	        
		
		
	        
      		        
		# Large families are split
		#newFamilies = []
		#for family in families:
		#    x,y=family.getLocation()
		#    if pC.GriDensity(GRIDDENSITY,x,y) < .00001 and random.random()<1:
		#        newFamilies.append(family.split())
		#    newFamilies.append(family)
		#families = newFamilies
		newFamilies = []
		for family in families:
		        if len(family.getMembers()) > len(families):
				newFamilies.append(family.split())
	
			stillAlive = family.update()
			if stillAlive: newFamilies.append(family)
		families = newFamilies

		# More efficiently update the familie members
		familyMembers = np.array([family.getMembers() for family in families])
		newMembers = update(familyMembers,0)
		[family.setMembers(newMembers[n]) for n, family in enumerate(families)]

		# New diseases and development update, due to encounters
		
		immunities = []
		developments=[]
		for family in families:
			if family.getWaterSteps() != 0:
				continue
			encounters = family.getFamilyEncounters(families)
			#if FARMING: encounters.append(family.getCommunityEncounters(communities))
			immunity = family.getImmunity()
			
			immunities.append(immunity)
			development=family.getDevelopment()
			developments.append(development)
			#if t==150:print(encounters[len(encounters)-1])
			for encounter in encounters:
				disease = encounter.getImmunity()
				dd=pC.diseaseSpread(family, disease, immunity, dd)
				family.growImmunity(disease)
		
		#FARMING SECTION
		
		agri = agriculturecentres(t)
		if agri:
			members = [random.randint(0, settings.MAXAGE) for i in range(settings.COMMUNITYSIZE)]
			immunity = np.mean(immunities)
			development=np.mean(developments)
			community = pC.Community(members, agri, immunity, development)
			communities.append(community)
			FARMING=True
			
		for community in communities:
			#loc=family.getLocation()
			farmingmembers = community.getMembers()
			
			#print(GRIDPOPULATION[k[0],k[1]])
			numFarmers += len(farmingmembers)
			totAgeF += sum(farmingmembers)
	        
		
		
		#Communities Changes	
		
#		if FARMING:
#		       newCommunities=[]
#		       for community in communities:
#		           if len(community.getMembers())>len(communities):
#		               newCommunities.append(community.split())
#		           stillAlive=community.update()
#		           if stillAlive: newCommunities.append(community)
#		       communities=newCommunities
#		           
 		newCommunities = []
 		if FARMING:
          		newFamilies=[]
          		for family in families:
             		         start,community=family.startCommunity()
             		         if start: communities.append(community)
             		         stillAlive = family.update()
            			 if stillAlive: newFamilies.append(family)
            			 
          		families=newFamilies	 
		for community in communities:
		        if len(community.getMembers()) > len(families) and len(community.getMembers())>500:
				families.append(community.splitexplorers())
	
			stillAlive = community.update(cattlesavailable(community.getLocation()))
			if stillAlive: newCommunities.append(community)
		communities = newCommunities


                # More efficiently update the familie members
		communityMembers = np.array([community.getMembers() for community in communities])
		communityLocation = np.array([community.getLocation() for community in communities])
		newMembers = update(communityMembers,1,communityLocation)
		#print(n)
		[community.setMembers(newMembers[n]) for n, community in enumerate(communities)]
		
		for community in communities:
      		        d=pC.getCondition(community,GRIDDENSITY,d)
#		for community in communities:
#		       print(len(community.getMembers()))
##
#      		

	#	for community in communities:
	#		encounters = community.getEncounters(families)

		# Get some feedback on the world population
		if t>1:
		      numPersonsprev=numPersons
		
		       
		if t>1:
		    rateofgrowth=float((numPersons-numPersonsprev))*100/numPersonsprev
	        else:
	            rateofgrowth=0

		fig.canvas.draw()
		plt.pause(0.001)
		#time.sleep(0.001)
		print "Timestep ",t
		print "Total hunters {}".format(numPersons)
		print "Average age {}".format(totAge/float(numPersons))
		print "Total farmers {}".format(numFarmers)
		if FARMING:print "Average age {}".format(totAgeF/float(numFarmers))
		
		print "No of Deaths by Malnutrition yet {}".format(d)
		print "No of Deaths by Diseases yet {}".format(dd)
		print "Rate of Growth {}".format(rateofgrowth)
		