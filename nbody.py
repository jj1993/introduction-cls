"""
N-body system simulation
Krishnakanth Sasi - 
Jonathan Jeroen Beekman - 10345019
"""

import math
import numpy as np
import pygame
import time

TIME = 10**8 			#sec total time
DeltaT = float(10**5) 	#sec per time step

class Planet(object):
	def __init__(self, name, mass, x, y, z, vx, vy, vz):
		self.name = name
		self.mass = float(mass)										#kg
		self.pos = np.array([x, y, z], dtype=np.float64) 			#m
		self.velocity = np.array([vx, vy, vz], dtype=np.float64)	#m/s

	def getName(self):
		return self.name

	def getMass(self):
		return self.mass

	def getPos(self):
		return self.pos

	def updateVelocity(self, planets):
		for p in planets:
			if p != self:
				F = getForces(self, p)
				a = F/self.mass
				this = a*DeltaT
				self.velocity += this

	def updatePos(self):
		self.pos += self.velocity*DeltaT

def getForces(p1, p2):
	# Applies Newtons law of gravity
	G = 6.6743*10**(-11) #Nm^2kg^-2
	m1, m2 = p1.getMass(), p2.getMass()
	r = p1.getPos() - p2.getPos()
	rAbs = np.linalg.norm(r)
	return -G*m1*m2/rAbs**2 * r/np.linalg.norm(r)

if __name__ == "__main__":
	sun = Planet("Sun", 2.0*10**30, 0, 0, 0, 0, 0, 0)
	earth = Planet("Earth", 6.0*10**24, 1.5*10**11, 0, 0, 0, 3.0*10**4, 0)
	mars = Planet("Mars", 6.4*10**23, 2.3*10**11, 0, 0, 0, 2.0*10**4, 0)
	planets = [sun, earth, mars]

	# 	Pygame stuff: http://www.petercollingridge.co.uk/sites/files/peter/universe.txt
	#   Set up Pygame variables
	pygame.init()
	BG_colour = (0,0,0)
	particle_colour = (200,200,200)
	(width, height) = (480, 360)
	screen = pygame.display.set_mode((width, height))
	fact = width/(10**12)

	for t in range(int(TIME/DeltaT)):
		print("===========================")
		print(t*DeltaT/(3600*24*365))
		print("===========================")

		screen.fill(BG_colour)

		for p in planets:
			p.updateVelocity(planets)
		for p in planets:
			p.updatePos()
			print(p.getName(), ": ", p.getPos())
			x = int(width/2.0 + fact*p.getPos()[0])
			y = int(width/2.0 + fact*p.getPos()[1])
			pygame.draw.circle(screen, particle_colour, (x, y), 4, 0)
      
		pygame.display.flip()
		time.sleep(.005)