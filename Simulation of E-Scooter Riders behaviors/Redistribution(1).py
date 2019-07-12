# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:24:19 2016

@author: Eos
"""
import random
import csv
import math
import numpy as np 
import scipy as sp 

workdayout= open('WorkdayMV1.csv', 'rb')
workdaydata= csv.reader(workdayout)
Datastorage=[]
for i in workdaydata:
    for j in i:
        Datastorage.append(j)

time = len(Datastorage)/5

entrymu = [float(z) for z in Datastorage[time:2*time]]
entrysd = [float(z) for z in Datastorage[2*time:3*time]]
exitmu = [float(z) for z in Datastorage[3*time:4*time]]
exitsd = [float(z) for z in Datastorage[4*time:]]

def lognormal(m,v,p):
    phi = math.sqrt(v+m**2)
    if phi != 0:
        mu = math.log(m**2/phi)
        sigma = math.sqrt(math.log(phi**2/m**2))
        
        x = random.normalvariate(mu,sigma)
        y = math.exp(x)
        demand = round(y*p,0)
    else:
        demand = 0
    return demand


#Pre Simulation
m=time #time intervals
n=1000 #simulation runs
ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
CostKiosk=100000 #cost of building 1 kiosk
CostScooter=1000 #cost of buying and maintaining 1 inokim light
ElectricityPerDistance=0.012 #units?
CostPerElectricity=0.04 #units?
p = 0.0833333333333333 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
distributionList=[1,0.059762222,0.059762222,0.095619555,0.023904889,0.035857333,0.05930683,0.119524444,0.083667111,0.207573906,0.083667111,0.114165648,0.010802316,0.017897954,0.018321574,0.010166885]
#Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
#Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
PricingList=[0.2396, 0.3196, 0.3196, 0.3196, 0.3578, 0.3578, 0.3578, 0.3578, 0.3030, 0.2310, 0.2809, 0.2686, 0.2120, 0.3978, 0.3762] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
OpsCostList=[9.19901E-06, 1.27764E-05, 1.27764E-05, 1.27764E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.20098E-05, 8.83397E-06, 1.1006E-05, 1.04584E-05, 8.03088E-06, 1.66093E-05, 1.55142E-05] 
#374.4wh/charge, 40km/charge, 0.195cents/kwh ==> 0.000018252 dollar/km
TotalInitialization=250
# ScooterInitializeList=[0,20.916777699999997, 20.916777699999997, 33.46684425, 8.366711149999999, 12.550066549999999, 20.7573905, 41.833555399999995, 29.28348885, 72.6508671, 29.28348885, 39.9579768, 3.7808105999999997, 6.264283900000001, 6.4125509, 3.55840975] #Scooters intially placed at each kiosk, including first being mrt ==> need input from evelyn on what number good to initialize.
ScooterInitializeList=[0]
#All scooters initialized at koisk
for i in range(1,len(distributionList)):
    ScooterInitializeList.append(int(distributionList[i]*TotalInitialization))
print "ScooterInitializeList",ScooterInitializeList, len(ScooterInitializeList)
# print "ScooterInitializeList1", ScooterInitializeList1, len(ScooterInitializeList1)

#Simulation
# count = 0
# i = 0
DemandDay=np.zeros((1,len(ScooterInitializeList)))
LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

for i in range(n):
    Demand= np.zeros((1,len(ScooterInitializeList)))
    LostDemand=np.zeros((1,len(ScooterInitializeList)))
    Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
    for t in range(m):
        numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
        numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter

        #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
        for j in range(len(ScooterInitializeList)):
            if j==0: #MRT
                NowDemand=min(numexit,ScooterInitializeList[j]+numentry)
                Demand[0][j]+=NowDemand #demand met
                LostDemand[0][j]+=numexit-NowDemand #investigate why lost demand at mrt always 0
                ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+numentry-numexit) #remaining number of scooter at MRT            
            else: #Kiosks
                NowDemand=min(distributionList[j]*numentry,ScooterInitializeList[j]+distributionList[j]*numexit)
                Demand[0][j]+=NowDemand
                LostDemand[0][j]+=distributionList[j]*numentry-NowDemand
                Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*NowDemand
                ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+distributionList[j]*(numexit-numentry)) #remaining number of scooter at kiosk j
            
            if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
                MaxSupplyDay[j][i]=ScooterInitializeList[j]

    for j in range(len(ScooterInitializeList)): #summing on day level           
        DemandDay[0][j]+=Demand[0][j]
        LostDemandDay[0][j]+=LostDemand[0][j]
        if j!=0:
            ProfitDay[0][j-1]+=Profit[0][j-1]

for j in range(len(ScooterInitializeList)): #averaging 
    DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
    LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
    if j!=0:
        ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit

#for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
print "DemandDay:", DemandDay
print "LostDemandDay", LostDemandDay
print "ProfitDay", ProfitDay
print "totalProfitDay", sum(ProfitDay[0])
print "MaxSupplyDay", MaxSupplyDay