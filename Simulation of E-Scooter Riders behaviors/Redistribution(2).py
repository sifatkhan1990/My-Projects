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
n=10 #simulation runs
ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
CostKiosk=100000 #cost of building 1 kiosk
CostScooter=1000 #cost of buying and maintaining 1 inokim light
ElectricityPerDistance=0.012 #units?
CostPerElectricity=0.04 #units?
p = 0.4 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
distributionList=[] #Probabilility distribution of scooter population over all kiosks => ratio data?
PricingList=[] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
OpsCostList=[] #Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
ScooterInitiazeMRT=300 #scooters initially placed at mrt
ScooterInitializeList=[] #Scooters intially placed at each kiosk
KioskInitializeList=[] #Binary: Which kiosks to activate, includes mrt as the 1st element which is always 1. dimension=len(scooterInitializeList)+1

###Customer Satisfaction###
IntervalDemandMatrix=np.zeros((m,len(KioskInitializeList))) #captures average demand at each kiosk for each time interval over the whole simulation
IntervalLDemandMatrix= np.zeros((m,len(KioskInitializeList))) #captures average Lost demand at each kiosk for each time interval over the whole simulation
DayDemandMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average demand at each kiosk for each run of the simulation (eacy day level)
DayLDemandMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average lost demand at each kiosk for each run of the simulation (eacy day level)

# use elements of intD to calculate elements of IntervalD and DayD
IntLDemandMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual lost demand at each time interval for each day (run) for every kiosk
IntDemandMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual demand at each time interval for each day (run) for every kiosk

###Profit Making###
IntervalProfitMatrix=np.zeros((m,len(KioskInitializeList))) #captures average profit at each kiosk for each time interval over the whole simulation
# IntervalLProfitMatrix= np.zeros((m,len(KioskInitializeList))) #captures average Lost demand at each kiosk for each time interval over the whole simulation
DayProfitMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average demand at each kiosk for each run of the simulation (eacy day level)
# DayLProfitMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average lost demand at each kiosk for each run of the simulation (eacy day level)

# use elements of intP to calculate elements of IntervalP and DayP
# IntLProfitMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual lost demand at each time interval for each day (run) for every kiosk
IntProfitMatrix=np.zeros((len(KioskInitializeList)-1,m,n)) #Captures actual profit at each time interval for each day (run) for a commute between mrt and every kiosk
#Simulation
count = 0
i = 0
ScooterCountMRT= ScooterInitiazeMRT
while i < n:
    for t in range(len(m)):
        numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
        numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
        
        #MRT
        IntDemandMatrix[0][t][i]=min(numexit,ScooterCountMRT+numentry) #Demand Met at MRT
        IntLDemandMatrix[0][t][i]= numexit-IntDemandMatrix[0][t][i] #Lost demand at MRT
        ScooterCountMRT= max(0,ScooterCountMRT+numentry-numexit) #remaining number of scooter at MRT

        #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
        for j in range(len(KioskInitializeList)):
            if KioskInitializeList[j]!=0 and j!=0:
                IntDemandMatrix[j][t][i]=min(distributionList[j-1]*numentry,ScooterInitializeList[j-1]+distributionList[j-1]*numexit) #Demand met at kiosk j
                IntLDemandMatrix[j][t][i]= distributionList[j-1]*numentry-IntDemandMatrix[j][t][i] #Lost demand at kiosk j
                IntProfitMatrix[j-1][t][i]= (PricingList[j-1]-OpsCostList[j-1])*IntDemandMatrix[j][t][i] #Profit made for a commute between kiosk j and MRT
                ScooterInitializeList[j-1]= max(0,ScooterInitializeList[j-1]+distributionList[j-1]*(numexit-numentry)) #remaining number of scooter at kiosk j




        ##Normal Distribution
#        numentry = round(random.normalvariate(p*entrymu[t],p*entrysd[t]),0)
#        numexit = round(random.normalvariate(p*exitmu[t],p*exitsd[t]),0)
#        print numentry, numexit   
        
        ##add logic here for capacity issues
        # mrt = mrt + numentry - numexit #supply @mrt, nature: scooter,accumulating
        # kiosk = kiosk - numentry + numexit #supply@kiosk, nature: scooter,accumulating
        print '-----------------------------------------------------'
        print mrt , kiosk,"sum",mrt+kiosk, "prev time period", t-1
        print "at mrt,","Demand", numexit, "Supply",mrt   
        print "at kiosk","Demand",numentry,"Supply",kiosk        
        
        if mrt + numentry - numexit <0:
            mrtld=abs(mrt + numentry - numexit) #ld = lost demand
            mrtldList.append(mrtld)
            mrtpld=mrtld/float(numexit) #pld = percentage lost demand
            
            if mrtpld>0.05:
                tolmrt.append(1) #out of demand; pld too high, case for concern
            else:
                tolmrt.append(0) #in demand;
            
            if mrt==0:
                numexit=0
                kiosk = kiosk - numentry + numexit
                mrt = mrt + numentry - numexit
            else:
                kiosk= kiosk + mrt - numentry
                mrt= numentry
        

        elif kiosk - numentry + numexit <0:
            kioskld=abs(kiosk - numentry + numexit)
            kioskldList.append(kioskld)
            kioskpld=kioskld/float(numentry)
            
            if kioskpld>0.05:
                tolkiosk.append(1)
            else:
                tolkiosk.append(0)
            
            if kiosk==0:
                numentry=0
                mrt = mrt + numentry - numexit
                kiosk = kiosk - numentry + numexit
            else:
                mrt = mrt + kiosk - numexit 
                kiosk= numexit
        

        else:
            mrt = mrt + numentry - numexit #supply @mrt, nature: scooter,accumulating
            kiosk = kiosk - numentry + numexit #supply@kiosk, nature: scooter,accumulating            
        

        print '                 ---------                           '
        print mrt , kiosk,"sum",mrt+kiosk, "time period", t
        print "at mrt,","Demand", numexit, "Supply",mrt   
        print "at kiosk","Demand",numentry,"Supply",kiosk
        print '-----------------------------------------------------'
        # if numexit == 0:
        #     tolmrt.append(0)
        # else:
        #     tolmrt.append(max(0,(numexit-mrt))/float(numexit)) #fulfil demand output 0
            # print 'appended item', (numexit-mrt)
        # print "tolmrt", tolmrt
    psolmrt = sum(tolmrt)/float(len(tolmrt)) #probability of people not finding a scooter on average
    psolkiosk= sum(tolkiosk)/float(len(tolkiosk))
    # print tolmrt
    # print "psol",psol
    if psolmrt > 0.05 or psolkiosk > 0.05:
        count += 1
    i += 1
print count
print count/float(1000)
    