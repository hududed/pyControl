#Vivek Jain
# ---------Raman Analysis ---------#

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import peakutils 

from scipy.optimize import curve_fit
import os 

def lorentzian_fcn(x, I, x0, gamma):
    return I*((gamma**2)/(((x-x0)**2)+gamma**2))

def two_lorentzian(x, I1, x1, gamma1, I2, x2, gamma2, y0):
    return lorentzian_fcn(x, I1, x1, gamma1) + lorentzian_fcn(x, I2, x2, gamma2) + y0

datafn = ''
bgrfn = ''
data = pd.read_csv(datafn, header = 0, index_col = 0, names = ['W', 'I'])
bgr = pd.read_csv(bgrfn, header = 0, index_col = 0, names = ['W', 'I'])

data_proc = (data.I.values - bgr.I.values)

data_index = data.index.values
data_proc = pd.DataFrame({'I': data_proc}, index = data_index)

lowval, hival = data_proc[data_proc.index.min():data_proc.index.min() + 2].values.mean(), data_proc[data_proc.index.max() - 2:data_proc.index.max()].values.mean()
low, hi = data_proc[data_proc.index.min():data_proc.index.min() + 2].index.values.mean(), data_proc[data_proc.index.max() - 2:data_proc.index.max()].index.values.mean()

y = [lowval, hival]
x = [low, hi]
m, b = np.polyfit(x, y, 1)

data_index = data_proc.index.values
data_proc = data_proc.I.values - (data_proc.index.values * m + b)
data_proc = pd.DataFrame({'I': data_proc}, index = data_index)

prms = [1000, 1345, 50, 3000, 1582, 25, 2000]

popt, pcov = curve_fit(two_lorentzian, data_proc.index.values, data_proc.I.values, p0 = prms)

data_proc['fit'] = two_lorentzian(data_proc.index, *popt)
G = popt[3]
D = popt[0]

plt.plot(data_proc)
plt.plot(data_proc.fit)


