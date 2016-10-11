"""
data from https://en.wikipedia.org/wiki/World_population_estimates
"""

import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

years, data = [], []
with open('populationdata.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    for i, row in enumerate(reader):
    	if i == 0:
    		sources = row[1:]
    	else:
    		year = int(row[0])
    		for n, datum in enumerate(row[1:]):
    			if datum != "":
    				years.append(year)
    				data.append(int(datum))
    				plt.scatter(year, int(datum))

def func(x, a, b):
	return b*np.exp(a*x)


popt, pcov = curve_fit(func, years, data, p0=(1e-3, 1))
a, b = popt

print(a)
pts = []
for x in years:
	pts.append(func(x, a, b))

plt.plot(years, pts)
plt.show()