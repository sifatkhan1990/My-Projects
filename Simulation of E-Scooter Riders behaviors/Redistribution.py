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

def rand_round(x):
    if random.random()>0.5:
        return math.ceil(x)
    else:
        return math.floor(x)
#Pre Simulation
m=time #time intervals
n=1 #simulation runs
ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
CostKiosk=100000 #cost of building 1 kiosk
CostScooter=1000 #cost of buying and maintaining 1 inokim light
ElectricityPerDistance=0.012 #units?
CostPerElectricity=0.04 #units?
p = 0.0833333333333333 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
distributionList=[1.0, 0.05976455313069569, 0.059761905518365424, 0.09561904882938468, 0.02390476220734617, 0.03585714331101926, 0.05930651619756272, 0.11952381103673085, 0.08366931533804185, 0.20757280669146952, 0.0836666677257116, 0.11416504368030823, 0.01080225830741321, 0.01789785935247875, 0.018321477325318483, 0.01016683134815361]
#Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
#Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
PricingList=[0.2396, 0.3196, 0.3196, 0.3196, 0.3578, 0.3578, 0.3578, 0.3578, 0.3030, 0.2310, 0.2809, 0.2686, 0.2120, 0.3978, 0.3762] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
OpsCostList=[9.19901E-06, 1.27764E-05, 1.27764E-05, 1.27764E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.20098E-05, 8.83397E-06, 1.1006E-05, 1.04584E-05, 8.03088E-06, 1.66093E-05, 1.55142E-05] 
#374.4wh/charge, 40km/charge, 0.195cents/kwh ==> 0.000018252 dollar/km
TotalInitialization=271
# ScooterInitializeList=[0,20.916777699999997, 20.916777699999997, 33.46684425, 8.366711149999999, 12.550066549999999, 20.7573905, 41.833555399999995, 29.28348885, 72.6508671, 29.28348885, 39.9579768, 3.7808105999999997, 6.264283900000001, 6.4125509, 3.55840975] #Scooters intially placed at each kiosk, including first being mrt ==> need input from evelyn on what number good to initialize.
ScooterInitializeList=[0.0]
#All scooters initialized at koisk
# check=0
for i in range(1,len(distributionList)): #problem of recurring values. after rounding, sum is smaller or larger. +/- 2
    if i!=len(distributionList)-1:
        ScooterInitializeList.append(rand_round(distributionList[i]*TotalInitialization))
    else:
        ScooterInitializeList.append(TotalInitialization-sum(ScooterInitializeList))
print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
# ScooterInitializeList.insert(0,abs(TotalInitialization-sum(ScooterInitializeList)))
# print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# for i in range(1,len(ScooterInitializeList)):
#     ScooterInitializeList[i]=round(ScooterInitializeList[i],0)

# print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# remove rand_round from last kiosk
#rounding causing the bug
# #Simulation
# # count = 0
# #i = 0
DemandDay=np.zeros((1,len(ScooterInitializeList)))
LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

for i in range(n):
    print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
    Demand= np.zeros((1,len(ScooterInitializeList)))
    LostDemand=np.zeros((1,len(ScooterInitializeList)))
    Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
    for t in range(m): #sum scoot should say fixed. it should not vary. balance transfer.
        numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
        numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
        #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
        ScooterFlowMRT=0.0
        ScootFlowList=[]
        numentry1=0.0
        # print 't=',t, 
        for j in range(len(ScooterInitializeList)):
            if j==0: #MRT
                ScooterFlowMRT=min(numexit,ScooterInitializeList[j])
                # print 'mrt'
                # print 'numexit', numexit, 'remaining @MRT',ScooterInitializeList[j], 'ScooterFlow', ScooterFlowMRT
                # ScootFlowList.append(ScooterFlow)
                Demand[0][j]+=numexit #demand 
                LostDemand[0][j]+=numexit-ScooterFlowMRT #investigate why lost demand at mrt always 0
                
            elif j!=len(ScooterInitializeList)-1: #Kiosks, apply fn(numentry, cdf=distributionlist(sumup))
                DemandKiosk=rand_round(distributionList[j]*numentry)
                numentry1+=DemandKiosk
                ScooterFlow=min(DemandKiosk,ScooterInitializeList[j])
                # print 'kiosk%i'%j
                # print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
                ScootFlowList.append(ScooterFlow)
                Demand[0][j]+=DemandKiosk
                LostDemand[0][j]+=DemandKiosk-ScooterFlow
                Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow
            
            else:
                ScooterFlow=min(numentry-numentry1,ScooterInitializeList[j])
                # print 'kiosk%i'%j
                # print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
                ScootFlowList.append(ScooterFlow)
                Demand[0][j]+=numentry-numentry1
                LostDemand[0][j]+=(numentry-numentry1)-ScooterFlow
                Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow                

        
        # print 'numexit', numexit, 'numentry', numentry, 'ScooterFlow', ScooterFlow
        # print 'NEXT TIME STEP STARTS...'
        ScooterFlowOutMRT=[]
        # print 'len scootlist', len(ScooterInitializeList), 'len ScootFlowList', len(ScootFlowList)
        for j in range(len(ScooterInitializeList)):
            if j==0:
                ScooterInitializeList[j]+=(sum(ScootFlowList))-ScooterFlowMRT #mrt += flow_mrt - flow_kiosk
            elif j!=len(ScooterInitializeList)-1:
                Arriving_at_Kiosk=rand_round(distributionList[j]*ScooterFlowMRT)
                ScooterFlowOutMRT.append(Arriving_at_Kiosk)
                ScooterInitializeList[j]+=Arriving_at_Kiosk-ScootFlowList[j-1] #kiosk += flow_kiosk - flow_mrt 
            else:
                ScooterInitializeList[j]+=(ScooterFlowMRT-sum(ScooterFlowOutMRT))-ScootFlowList[j-1]

            if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
                MaxSupplyDay[j][i]=ScooterInitializeList[j]            
        print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)       

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

# for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
print "DemandDay:", DemandDay
print "LostDemandDay", LostDemandDay
print "ProfitDay", ProfitDay
print "totalProfitDay", sum(ProfitDay[0]), "proportionLostDemand", sum(LostDemandDay[0])/float(sum(DemandDay[0]))
print "MaxSupplyDay", MaxSupplyDay