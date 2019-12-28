# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 08:54:17 2019

@author: vinay
"""
#import required toolboxes
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
plt.rcParams['axes.grid'] = False

file = input('Enter Filename: ')

try:
    data = pd.read_excel(file,'Sheet1')
except FileNotFoundError:
    print('////////// File not Found ///////// \n')
    
#headings
states = list(data.columns.values)
del states[0]
#variable values [X1 = Vel, X2 = Alt, X3 = AoA]
Vel_r = data['Velocity'].values.tolist()
Alt_r = data['Altitude'].values.tolist()
AoA_r = data['AoA'].values.tolist()

#check that vectors have equal length
m = len(Vel_r)
if m==len(Alt_r) and m==len(AoA_r):
    print ('Vectors have equal lengths, calculating \n')

#sort  
Vel = np.sort(Vel_r)
Alt = np.sort(Alt_r)
AoA = np.sort(AoA_r)

#initialize empty array of size m
x = [0]*m

#CDF x points
for i in range(0,m):
    x[i]= (i+1)/m

#Means, Variances, Standard Deviations (use Population)
i = 0
#find means mu
mu = [0]*3
for i in range(0,m):
    mu[0] += (Vel[i])/m
    mu[1] += (Alt[i])/m
    mu[2] += (AoA[i])/m
#find variances var
i = 0
var = [0]*3
for i in range(0,m):
    var[0] += (1/m)*(Vel[i]-mu[0])**2
    var[1] += (1/m)*(Alt[i]-mu[1])**2
    var[2] += (1/m)*(AoA[i]-mu[2])**2
sd = [0]*3
i = 0
for i in range (0,len(var)):
    sd[i] = np.sqrt(var[i])

#Plot all CDFs along with means
    
#Velocity
ax1 = plt.subplot(131)
ax1.plot(Vel,x)
plt.xlabel('Velocity (m/s)',fontsize=14)
plt.ylabel('Probability CDF',fontsize=14)
plt.axvline(x=mu[0],color='k', linestyle='--',linewidth=1)
#Altitude
ax2 = plt.subplot(132)
ax2.plot(Alt,x)
plt.xlabel('Altitude (m)',fontsize=14)
plt.axvline(x=mu[1],color='k', linestyle='--',linewidth=1)
#AoA
ax3 = plt.subplot(133)
ax3.plot(AoA,x)
plt.xlabel('AoA (radians)',fontsize=14)
plt.axvline(x=mu[2],color='k', linestyle='--',linewidth=1)

#Print data to screen in table 

print(states,'<-- States', '\n')
print(np.round(mu,2),'<-- Average Values','\n')
print(np.round(sd,2),'<-- Deviations','\n')

#Find Covariances, first initialize empty variables
i = 0
cov_x1x2 = 0
cov_x1x3 = 0
cov_x2x3 = 0
corr_x1x2 = 0
corr_x1x3 = 0
corr_x2x3 = 0

for i in range(0,m):
    cov_x1x2 += ((Vel[i]-mu[0])*(Alt[i]-mu[1]))/m
    cov_x1x3 += ((Vel[i]-mu[0])*(AoA[i]-mu[2]))/m
    cov_x2x3 += ((Alt[i]-mu[1])*(AoA[i]-mu[2]))/m

corr_x1x2 = cov_x1x2 / (sd[0]*sd[1])
corr_x1x3 = cov_x1x3 / (sd[0]*sd[2])
corr_x2x3 = cov_x2x3 / (sd[1]*sd[2])

print ('Vel vs. Alt has covariance ',np.round(cov_x1x2,2),'correlation: ',np.round(corr_x1x2,2), '\n')
print ('Vel vs. AoA has covariance ',np.round(cov_x1x3,2),'correlation: ',np.round(corr_x1x3,2), '\n')
print ('Alt vs. AoA has covariance ',np.round(cov_x2x3,2),'correlation: ',np.round(corr_x2x3,2), '\n')

#Put together covariance matrix and output to screen

COV = np.array ([[var[0],cov_x1x2,cov_x1x3],[cov_x1x2,var[1],cov_x2x3],[cov_x1x3,cov_x2x3,var[2]]])

print ('Your covariance matrix is', '\n')
np.set_printoptions(precision = 3)
print (COV)






    


    
