# ====================================
#
#			BLOOD FLOW
#	Introduction computational science
#
#				By
#	Jonathan Jeroen Beekman - 10345019
#	Krishnakanth Sasi - *********
#
# ====================================

import math

DP = 80 # diastolic pressure, in (mm HG)
SP = 120 # systolic pressure, in (mm HG)
SV = .075 # stroke volume, in (L), between 50 and 100 mL
HR = 70 # heart rate, in (bpm), between 60 and 80
r = 0.6 # radius of vessel, in (cm)
ETA = 0.04 # viscosity of blood, in (g cm^-1 s^-1)
l = 100 # vessel length, in (cm)

def MAP(DP, SP):
	""" Mean arterial pressure (MAP) """
	return (2*DP + SP)/3.0

def SVR(MAP, SV, HR):
	""" 
	Systemic vascular resistance
	Normally 800 to 1200 (dyn s cm^-5)
	Greatly influenced by vasoconstriction and vasodilation
	"""
	cf = 79.9 # Conversion factor, (mm Hg min/L) to (dyn s cm^-5)
	return cf*MAP/float(SV*HR)

def meanV(P1, P2, r, ETA, l):
	"""
	Mean blood flow velocity
	P1, P2 = start and end pressure
	"""
	deltaP = P2 - P1
	return deltaP*r**2/float(8*ETA*l)

def Q(v, r):
	""" Blood flow, in (cm^3/s)	"""
	return v*math.pi*r**2


P1, P2 = 1, 1
MAP = MAP(DP, SP)
SVR = (MAP, SV, HR)
v = meanV(P1, P2, r, ETA, l)
bloodFlow = Q(v, r)