# # -*- coding: utf-8 -*-
# """
# Created on Wed May 18 14:24:19 2016

# @author: Eos
# """
# import random
# import csv
# import math

# workdayout= open('WorkdayMV1.csv', 'rb')
# workdaydata= csv.reader(workdayout)
# Datastorage=[]
# for i in workdaydata:
#     for j in i:
#         Datastorage.append(j)

# time = len(Datastorage)/5

# entrymu = [float(z) for z in Datastorage[time:2*time]]
# entrysd = [float(z) for z in Datastorage[2*time:3*time]]
# exitmu = [float(z) for z in Datastorage[3*time:4*time]]
# exitsd = [float(z) for z in Datastorage[4*time:]]

# def lognormal(m,v,p):
#     phi = math.sqrt(v+m**2)
#     if phi != 0:
#         mu = math.log(m**2/phi)
#         sigma = math.sqrt(math.log(phi**2/m**2))
        
#         x = random.normalvariate(mu,sigma)
#         y = math.exp(x)
#         demand = round(y*p,0)
#     else:
#         demand = 0
#     return demand

# p = 0.4
# count = 0
# i = 1

# while i < 2:
#     mrt = 100
#     kiosk =300
#     tolmrt = []
#     tolkiosk= []
#     mrtldList= []
#     kioskldList= []
#     for t in range(len(entrymu)):
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
        
#         ##Normal Distribution
# #        numentry = round(random.normalvariate(p*entrymu[t],p*entrysd[t]),0)
# #        numexit = round(random.normalvariate(p*exitmu[t],p*exitsd[t]),0)
# #        print numentry, numexit   
        
#         ##add logic here for capacity issues
#         # mrt = mrt + numentry - numexit #supply @mrt, nature: scooter,accumulating
#         # kiosk = kiosk - numentry + numexit #supply@kiosk, nature: scooter,accumulating
#         print '-----------------------------------------------------'
#         print mrt , kiosk,"sum",mrt+kiosk, "prev time period", t-1
#         print "at mrt,","Demand", numexit, "Supply",mrt   
#         print "at kiosk","Demand",numentry,"Supply",kiosk        
        
#         if mrt + numentry - numexit <0:
#             mrtld=abs(mrt + numentry - numexit) #ld = lost demand
#             mrtldList.append(mrtld)
#             mrtpld=mrtld/float(numexit) #pld = percentage lost demand
            
#             if mrtpld>0.05:
#                 tolmrt.append(1) #out of demand; pld too high, case for concern
#             else:
#                 tolmrt.append(0) #in demand;
            
#             if mrt==0:
#                 numexit=0
#                 kiosk = kiosk - numentry + numexit
#                 mrt = mrt + numentry - numexit
#             else:
#                 kiosk= kiosk + mrt - numentry
#                 mrt= numentry
        

#         elif kiosk - numentry + numexit <0:
#             kioskld=abs(kiosk - numentry + numexit)
#             kioskldList.append(kioskld)
#             kioskpld=kioskld/float(numentry)
            
#             if kioskpld>0.05:
#                 tolkiosk.append(1)
#             else:
#                 tolkiosk.append(0)
            
#             if kiosk==0:
#                 numentry=0
#                 mrt = mrt + numentry - numexit
#                 kiosk = kiosk - numentry + numexit
#             else:
#                 mrt = mrt + kiosk - numexit 
#                 kiosk= numexit
        

#         else:
#             mrt = mrt + numentry - numexit #supply @mrt, nature: scooter,accumulating
#             kiosk = kiosk - numentry + numexit #supply@kiosk, nature: scooter,accumulating            
        

#         print '                 ---------                           '
#         print mrt , kiosk,"sum",mrt+kiosk, "time period", t
#         print "at mrt,","Demand", numexit, "Supply",mrt   
#         print "at kiosk","Demand",numentry,"Supply",kiosk
#         print '-----------------------------------------------------'
#         # if numexit == 0:
#         #     tolmrt.append(0)
#         # else:
#         #     tolmrt.append(max(0,(numexit-mrt))/float(numexit)) #fulfil demand output 0
#             # print 'appended item', (numexit-mrt)
#         # print "tolmrt", tolmrt
#     psolmrt = sum(tolmrt)/float(len(tolmrt)) #probability of people not finding a scooter on average
#     psolkiosk= sum(tolkiosk)/float(len(tolkiosk))
#     # print tolmrt
#     # print "psol",psol
#     if psolmrt > 0.05 or psolkiosk > 0.05:
#         count += 1
#     i += 1
# print count
# print count/float(1000)

###Prototype 2

# -*- coding: utf-8 -*-
# """
# Created on Wed May 18 14:24:19 2016

# @author: Eos
# """
# import random
# import csv
# import math
# import numpy as np 
# import scipy as sp 

# workdayout= open('WorkdayMV1.csv', 'rb')
# workdaydata= csv.reader(workdayout)
# Datastorage=[]
# for i in workdaydata:
#     for j in i:
#         Datastorage.append(j)

# time = len(Datastorage)/5

# entrymu = [float(z) for z in Datastorage[time:2*time]]
# entrysd = [float(z) for z in Datastorage[2*time:3*time]]
# exitmu = [float(z) for z in Datastorage[3*time:4*time]]
# exitsd = [float(z) for z in Datastorage[4*time:]]

# def lognormal(m,v,p):
#     phi = math.sqrt(v+m**2)
#     if phi != 0:
#         mu = math.log(m**2/phi)
#         sigma = math.sqrt(math.log(phi**2/m**2))
        
#         x = random.normalvariate(mu,sigma)
#         y = math.exp(x)
#         demand = round(y*p,0)
#     else:
#         demand = 0
#     return demand


# #Pre Simulation
# m=time #time intervals
# n=10 #simulation runs
# ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
# CostKiosk=100000 #cost of building 1 kiosk
# CostScooter=1000 #cost of buying and maintaining 1 inokim light
# ElectricityPerDistance=0.012 #units?
# CostPerElectricity=0.04 #units?
# p = 0.4 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
# distributionList=[] #Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
# PricingList=[] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
# OpsCostList=[] #Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
# # ScooterInitiazeMRT=300 #scooters initially placed at mrt
# ScooterInitializeList=[] #Scooters intially placed at each kiosk, including first being mrt
# KioskInitializeList=[] #Binary: Which kiosks to activate, includes mrt as the 1st element which is always 1. dimension=len(scooterInitializeList)+1

# ###Customer Satisfaction###
# IntervalDemandMatrix=np.zeros((m,len(KioskInitializeList))) #captures average demand at each kiosk for each time interval over the whole simulation
# IntervalLDemandMatrix= np.zeros((m,len(KioskInitializeList))) #captures average Lost demand at each kiosk for each time interval over the whole simulation
# DayDemandMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average demand at each kiosk for each run of the simulation (eacy day level)
# DayLDemandMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average lost demand at each kiosk for each run of the simulation (eacy day level)

# # use elements of intD to calculate elements of IntervalD and DayD
# IntLDemandMatrix=np.zeros((len(KioskInitializeList),n))
# IntDemandMatrix=np.zeros((len(KioskInitializeList),n))
# # IntLDemandMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual lost demand at each time interval for each day (run) for every kiosk
# # IntDemandMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual demand at each time interval for each day (run) for every kiosk

# ###Profit Making###
# IntervalProfitMatrix=np.zeros((m,len(KioskInitializeList))) #captures average profit at each kiosk for each time interval over the whole simulation
# # IntervalLProfitMatrix= np.zeros((m,len(KioskInitializeList))) #captures average Lost demand at each kiosk for each time interval over the whole simulation
# DayProfitMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average demand at each kiosk for each run of the simulation (eacy day level)
# # DayLProfitMatrix=np.zeros((n,len(KioskInitializeList))) #Captures average lost demand at each kiosk for each run of the simulation (eacy day level)

# # use elements of intP to calculate elements of IntervalP and DayP
# # IntLProfitMatrix=np.zeros((len(KioskInitializeList),m,n)) #Captures actual lost demand at each time interval for each day (run) for every kiosk
# IntProfitMatrix=np.zeros((len(KioskInitializeList)-1,m,n)) #Captures actual profit at each time interval for each day (run) for a commute between mrt and every kiosk
# #Simulation
# count = 0
# i = 0
# # ScooterCountMRT= ScooterInitiazeMRT
# DemandDay=np.zeros((1,len(scooterInitializeList)))
# LostDemandDay=np.zeros((1,len(scooterInitializeList)))
# ProfitDay=np.zeros((1,len(scooterInitializeList)-1))
# while i < n:
#     Demand= np.zeros((1,len(scooterInitializeList)))
#     LostDemand=np.zeros((1,len(scooterInitializeList)))
#     Profit=np.zeros((1,len(scooterInitializeList)-1))
#     for t in range(len(m)):
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter

#         #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 Demand[0][j]+=min(numexit,ScooterInitializeList[j]+numentry)
#                 LostDemand[0][j]+=numexit-Demand[0][j]
#                 # IntDemandMatrix[0][t][i]=min(numexit,ScooterCountMRT+numentry) #Demand Met at MRT
#                 # IntLDemandMatrix[0][t][i]= numexit-IntDemandMatrix[0][t][i] #Lost demand at MRT
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+numentry-numexit) #remaining number of scooter at MRT            
#             # if KioskInitializeList[j]!=0 and j!=0:
#             else: #Kiosks
#                 Demand[0][j]+=min(distributionList[j]*numentry,ScooterInitializeList[j]+distributionList[j]*numexit)
#                 LostDemand[0][j]+=distributionList[j]*numentry-Demand[0][j]
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*Demand[0][j]
#                 # IntDemandMatrix[j][t][i]=min(distributionList[j-1]*numentry,ScooterInitializeList[j-1]+distributionList[j-1]*numexit) #Demand met at kiosk j
#                 # IntLDemandMatrix[j][t][i]= distributionList[j-1]*numentry-IntDemandMatrix[j][t][i] #Lost demand at kiosk j
#                 # IntProfitMatrix[j-1][t][i]= (PricingList[j-1]-OpsCostList[j-1])*IntDemandMatrix[j][t][i] #Profit made for a commute between kiosk j and MRT
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+distributionList[j]*(numexit-numentry)) #remaining number of scooter at kiosk j
    
#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit    
import math
import numpy
import scipy
# List=[1,2,3]
# d=sum(List)
# print d
# List=[1,4,5]
# v=sum(List)
# k= numpy.mean(List)
# var= numpy.var(List)
# std= numpy.std(List)
# print v , k, var, std
# matrix=numpy.zeros((3,4,5))
# print matrix
# matrix[1][0][0]=1
# print "matrix[1][0][0]"
# print matrix
# matrix[0][1][0]=2
# matrix[0][1][1]=1.5
# matrix[0][1][2]=2.5
# matrix[0][1][3]=0.5
# matrix[0][1][4]=3
# print "matrix[0][1][0]"
# print matrix
# matrix[0][0][1]=3
# print "matrix[0][0][1]"
# print matrix
# print "matrix[0][1]"
# print matrix[0][1]
# print "sum(matrix[0][1])", sum(matrix[0][1])
# print "avg(matrix[0][1])", numpy.mean(matrix[0][1])
# print "var(matrix[0][1])", numpy.var(matrix[0][1])
# print "std(matrix[0][1])", numpy.std(matrix[0][1])
# print numpy.zeros((1,5))
# print len(OpsCostList)
# print sum(OpsCostList)
# print numpy.mean(numpy.zeros((1,5))[0])

ScooterInitializeList=[]
distributionList=[0.059762222,0.059762222,0.095619555,0.023904889,0.035857333,0.05930683,0.119524444,0.083667111,0.207573906,0.083667111,0.114165648,0.010802316,0.017897954,0.018321574,0.010166885]
for i in range(len(distributionList)):
    ScooterInitializeList.append(int(distributionList[i]*350))

print 72.6508671/float(350)

print ScooterInitializeList


#Prototype wk4
# DemandDay=np.zeros((1,len(ScooterInitializeList)))
# LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
# ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
# MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

# for i in range(n):
#     Demand= np.zeros((1,len(ScooterInitializeList)))
#     LostDemand=np.zeros((1,len(ScooterInitializeList)))
#     Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
#     for t in range(m):
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter

#         #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 NowDemand=min(numexit,ScooterInitializeList[j]+numentry)
#                 Demand[0][j]+=NowDemand #demand met
#                 LostDemand[0][j]+=numexit-NowDemand #investigate why lost demand at mrt always 0
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+numentry-numexit) #remaining number of scooter at MRT            
#             else: #Kiosks
#                 NowDemand=min(distributionList[j]*numentry,ScooterInitializeList[j]+distributionList[j]*numexit)
#                 Demand[0][j]+=NowDemand
#                 LostDemand[0][j]+=distributionList[j]*numentry-NowDemand
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*NowDemand
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]+distributionList[j]*(numexit-numentry)) #remaining number of scooter at kiosk j
            
#             if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
#                 MaxSupplyDay[j][i]=ScooterInitializeList[j]

#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit

#Prototype wk4(1)
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 NowDemand=min(numexit,ScooterInitializeList[j])
#                 Demand[0][j]+=numexit #demand met
#                 LostDemand[0][j]+=numexit-NowDemand #investigate why lost demand at mrt always 0
#                 print 'numexit',numexit,'numentry',numentry,'NowDemand',NowDemand, 'sumScoot', sum(ScooterInitializeList),'scoot@MRT t:',ScooterInitializeList[j] 
#                 print 'increase?', ScooterInitializeList
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]-numexit+min(numentry,sum(ScooterInitializeList)-ScooterInitializeList[j])) #remaining number of scooter at MRT
#                 print 'scoot@MRT t+1:',ScooterInitializeList[j]            
#             else: #Kiosks
#                 NowDemand=min(round(distributionList[j]*numentry,0),ScooterInitializeList[j])
#                 Demand[0][j]+=round(distributionList[j]*numentry,0)
#                 LostDemand[0][j]+=round(distributionList[j]*numentry,0)-NowDemand
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*NowDemand
#                 print 'numexit',numexit,'numentry',numentry,'NowDemand',NowDemand, 'sumScoot', sum(ScooterInitializeList),'scoot@kiosk%i t:'%j,ScooterInitializeList[j] 
#                 print 'increase?', ScooterInitializeList
#                 ScooterInitializeList[j]= max(0,ScooterInitializeList[j]-round(distributionList[j]*numentry,0)+round(min(numexit,ScooterInitializeList[0])*distributionList[j],0)) #remaining number of scooter at kiosk j
#                 print 'scoot@kiosk%i t+1:'%j,ScooterInitializeList[j]
#             if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
#                 MaxSupplyDay[j][i]=ScooterInitializeList[j]

#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit
# number = 8
# print "your number is %i." % number

# x=[1,2,3,4]
# x.insert(0,5)
# print x
distributionList=[1.0, 0.05976455313069569, 0.059761905518365424, 0.09561904882938468, 0.02390476220734617, 0.03585714331101926, 0.05930651619756272, 0.11952381103673085, 0.08366931533804185, 0.20757280669146952, 0.0836666677257116, 0.11416504368030823, 0.01080225830741321, 0.01789785935247875, 0.018321477325318483, 0.01016683134815361]
distlist111=[2257.3, 2257.2, 3611.52, 902.88, 1354.32, 2240, 4514.4, 3160.18, 7840, 3160.08, 4312, 408, 676, 692, 384]
dist11=[]
for i in range(len(distlist111)): #play with proportion at mrt. make mrt dependent wrt to other kiosks.
    dist11.append(distlist111[i]/float(2*sum(distlist111)))
dist11.insert(0,1-sum(dist11))
print distributionList
print dist11[0],sum(dist11)-dist11[0], dist11[0]-(sum(dist11)-dist11[0])
print sum(dist11)


#Recurring problem
# m=time #time intervals
# n=1 #simulation runs
# ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
# CostKiosk=100000 #cost of building 1 kiosk
# CostScooter=1000 #cost of buying and maintaining 1 inokim light
# ElectricityPerDistance=0.012 #units?
# CostPerElectricity=0.04 #units?
# p = 0.0833333333333333 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
# distributionList=[1.0, 0.05976455313069569, 0.059761905518365424, 0.09561904882938468, 0.02390476220734617, 0.03585714331101926, 0.05930651619756272, 0.11952381103673085, 0.08366931533804185, 0.20757280669146952, 0.0836666677257116, 0.11416504368030823, 0.01080225830741321, 0.01789785935247875, 0.018321477325318483, 0.01016683134815361]
# #Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
# #Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
# PricingList=[0.2396, 0.3196, 0.3196, 0.3196, 0.3578, 0.3578, 0.3578, 0.3578, 0.3030, 0.2310, 0.2809, 0.2686, 0.2120, 0.3978, 0.3762] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
# OpsCostList=[9.19901E-06, 1.27764E-05, 1.27764E-05, 1.27764E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.20098E-05, 8.83397E-06, 1.1006E-05, 1.04584E-05, 8.03088E-06, 1.66093E-05, 1.55142E-05] 
# #374.4wh/charge, 40km/charge, 0.195cents/kwh ==> 0.000018252 dollar/km
# TotalInitialization=210
# # ScooterInitializeList=[0,20.916777699999997, 20.916777699999997, 33.46684425, 8.366711149999999, 12.550066549999999, 20.7573905, 41.833555399999995, 29.28348885, 72.6508671, 29.28348885, 39.9579768, 3.7808105999999997, 6.264283900000001, 6.4125509, 3.55840975] #Scooters intially placed at each kiosk, including first being mrt ==> need input from evelyn on what number good to initialize.
# ScooterInitializeList=[]
# #All scooters initialized at koisk
# check=0
# for i in range(1,len(distributionList)): #problem of recurring values. after rounding, sum is smaller or larger. +/- 2
#     # if i!=len(distributionList)-1:
#     ScooterInitializeList.append(distributionList[i]*TotalInitialization)
#     check+=distributionList[i]*TotalInitialization
#     print ScooterInitializeList[i-1], sum(ScooterInitializeList), check, distributionList[i], TotalInitialization
#     # else:
# print 'sumscoot',sum(ScooterInitializeList), TotalInitialization, sum(distributionList)
# ScooterInitializeList.insert(0,round(abs(TotalInitialization-sum(ScooterInitializeList)),0))
# print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# for i in range(1,len(ScooterInitializeList)):
#     ScooterInitializeList[i]=round(ScooterInitializeList[i],0)

# print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)

#protype wk4(2): rounding causing the bug
# for i in range(1,len(distributionList)): #problem of recurring values. after rounding, sum is smaller or larger. +/- 2
#     # if i!=len(distributionList)-1:
#     ScooterInitializeList.append(distributionList[i]*TotalInitialization)
# ScooterInitializeList.insert(0,round(abs(TotalInitialization-sum(ScooterInitializeList)),0))
# # print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# for i in range(1,len(ScooterInitializeList)):
#     ScooterInitializeList[i]=round(ScooterInitializeList[i],0)

# # print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)

# #rounding causing the bug
# #Simulation
# # count = 0
# #i = 0
# DemandDay=np.zeros((1,len(ScooterInitializeList)))
# LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
# ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
# MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

# for i in range(n):
#     print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
#     Demand= np.zeros((1,len(ScooterInitializeList)))
#     LostDemand=np.zeros((1,len(ScooterInitializeList)))
#     Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
#     for t in range(m): #sum scoot should say fixed. it should not vary. balance transfer.
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
#         #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
#         ScootFlowList=[]
#         print 't=',t, 
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 ScooterFlow=min(numexit,ScooterInitializeList[j])
#                 print 'mrt'
#                 print 'numexit', numexit, 'remaining @MRT',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=numexit #demand 
#                 LostDemand[0][j]+=numexit-ScooterFlow #investigate why lost demand at mrt always 0
                
#             else: #Kiosks
#                 ScooterFlow=min(round(distributionList[j]*numentry,0),ScooterInitializeList[j])
#                 print 'kiosk%i'%j
#                 print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=round(distributionList[j]*numentry,0)
#                 LostDemand[0][j]+=round(distributionList[j]*numentry,0)-ScooterFlow
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow
               
        
#         # print 'numexit', numexit, 'numentry', numentry, 'ScooterFlow', ScooterFlow
#         print 'NEXT TIME STEP STARTS...'
#         for j in range(len(ScooterInitializeList)):
#             if j==0:
#                 ScooterInitializeList[j]+=(sum(ScootFlowList)-ScootFlowList[j])-ScootFlowList[j] #mrt += flow_mrt - flow_kiosk
#             else:
#                 ScooterInitializeList[j]+=round(distributionList[j]*ScootFlowList[0],0)-ScootFlowList[j] #kiosk += flow_kiosk - flow_mrt 

#             if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
#                 MaxSupplyDay[j][i]=ScooterInitializeList[j]            
#         print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)       

#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit

# # for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
# print "DemandDay:", DemandDay
# print "LostDemandDay", LostDemandDay
# print "ProfitDay", ProfitDay
# print "totalProfitDay", sum(ProfitDay[0]), "proportionLostDemand", sum(LostDemandDay[0])/float(sum(DemandDay[0]))
# print "MaxSupplyDay", MaxSupplyDay

#Prototype 4(3): No rounding
#Simulation
# count = 0
#i = 0
# DemandDay=np.zeros((1,len(ScooterInitializeList)))
# LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
# ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
# MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

# for i in range(n):
#     print 'A NEW DAY STARTS. RISE AND SHINE BABY!'
#     print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
#     Demand= np.zeros((1,len(ScooterInitializeList)))
#     LostDemand=np.zeros((1,len(ScooterInitializeList)))
#     Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
#     for t in range(m): #sum scoot should say fixed. it should not vary. balance transfer.
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
#         #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
#         ScootFlowList=[]
#         print 't=',t 
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 ScooterFlow=min(numexit,ScooterInitializeList[j])
#                 print 'mrt'
#                 print 'numexit', numexit, 'remaining @MRT',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=numexit #demand 
#                 LostDemand[0][j]+=numexit-ScooterFlow #investigate why lost demand at mrt always 0
                
#             elif j!=len(ScooterInitializeList)-1: #Kiosks
#                 ScooterFlow=min(distributionList[j]*numentry,ScooterInitializeList[j])
#                 print 'kiosk%i'%j
#                 print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=distributionList[j]*numentry
#                 LostDemand[0][j]+=distributionList[j]*numentry-ScooterFlow
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow
               
        
#         print 'numexit', numexit, 'numentry', numentry, 'ScooterFlow', ScooterFlow
#         print 'NEXT TIME STEP STARTS...'
#         for j in range(len(ScooterInitializeList)):
#             if j==0:
#                 ScooterInitializeList[j]+=(sum(ScootFlowList)-ScootFlowList[j])-ScootFlowList[j] #mrt += flow_mrt - flow_kiosk
#             else:
#                 ScooterInitializeList[j]+=distributionList[j]*ScootFlowList[0]-ScootFlowList[j] #kiosk += flow_kiosk - flow_mrt 

#             if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
#                 MaxSupplyDay[j][i]=ScooterInitializeList[j]            
#         # print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)       

#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit

# # for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
# print "DemandDay:", DemandDay
# print "LostDemandDay", LostDemandDay
# print "ProfitDay", ProfitDay
# print "totalProfitDay", sum(ProfitDay[0]), "proportionLostDemand", sum(LostDemandDay[0])/float(sum(DemandDay[0]))
# print "MaxSupplyDay", MaxSupplyDay


#Prototype 4(4): Rand round
# def rand_round(x):
#     if random.random()>0.5:
#         return math.ceil(x)
#     else:
#         return math.floor(x)
# #Pre Simulation
# m=time #time intervals
# n=1 #simulation runs
# ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
# CostKiosk=100000 #cost of building 1 kiosk
# CostScooter=1000 #cost of buying and maintaining 1 inokim light
# ElectricityPerDistance=0.012 #units?
# CostPerElectricity=0.04 #units?
# p = 0.0833333333333333 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
# distributionList=[1.0, 0.05976455313069569, 0.059761905518365424, 0.09561904882938468, 0.02390476220734617, 0.03585714331101926, 0.05930651619756272, 0.11952381103673085, 0.08366931533804185, 0.20757280669146952, 0.0836666677257116, 0.11416504368030823, 0.01080225830741321, 0.01789785935247875, 0.018321477325318483, 0.01016683134815361]
# #Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
# #Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
# PricingList=[0.2396, 0.3196, 0.3196, 0.3196, 0.3578, 0.3578, 0.3578, 0.3578, 0.3030, 0.2310, 0.2809, 0.2686, 0.2120, 0.3978, 0.3762] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
# OpsCostList=[9.19901E-06, 1.27764E-05, 1.27764E-05, 1.27764E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.20098E-05, 8.83397E-06, 1.1006E-05, 1.04584E-05, 8.03088E-06, 1.66093E-05, 1.55142E-05] 
# #374.4wh/charge, 40km/charge, 0.195cents/kwh ==> 0.000018252 dollar/km
# TotalInitialization=271
# # ScooterInitializeList=[0,20.916777699999997, 20.916777699999997, 33.46684425, 8.366711149999999, 12.550066549999999, 20.7573905, 41.833555399999995, 29.28348885, 72.6508671, 29.28348885, 39.9579768, 3.7808105999999997, 6.264283900000001, 6.4125509, 3.55840975] #Scooters intially placed at each kiosk, including first being mrt ==> need input from evelyn on what number good to initialize.
# ScooterInitializeList=[0.0]
# #All scooters initialized at koisk
# # check=0
# for i in range(1,len(distributionList)): #problem of recurring values. after rounding, sum is smaller or larger. +/- 2
#     if i!=len(distributionList)-1:
#         ScooterInitializeList.append(rand_round(distributionList[i]*TotalInitialization))
#     else:
#         ScooterInitializeList.append(TotalInitialization-sum(ScooterInitializeList))
# print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
# # ScooterInitializeList.insert(0,abs(TotalInitialization-sum(ScooterInitializeList)))
# # print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# # for i in range(1,len(ScooterInitializeList)):
# #     ScooterInitializeList[i]=round(ScooterInitializeList[i],0)

# # print "ScooterInitializeList",ScooterInitializeList, sum(ScooterInitializeList)
# # remove rand_round from last kiosk
# #rounding causing the bug
# # #Simulation
# # # count = 0
# # #i = 0
# DemandDay=np.zeros((1,len(ScooterInitializeList)))
# LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
# ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
# MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))

# for i in range(n):
#     print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
#     Demand= np.zeros((1,len(ScooterInitializeList)))
#     LostDemand=np.zeros((1,len(ScooterInitializeList)))
#     Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
#     for t in range(m): #sum scoot should say fixed. it should not vary. balance transfer.
#         numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
#         numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
#         #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
#         ScooterFlowMRT=0.0
#         ScootFlowList=[]
#         numentry1=0.0
#         # print 't=',t, 
#         for j in range(len(ScooterInitializeList)):
#             if j==0: #MRT
#                 ScooterFlowMRT=min(numexit,ScooterInitializeList[j])
#                 # print 'mrt'
#                 # print 'numexit', numexit, 'remaining @MRT',ScooterInitializeList[j], 'ScooterFlow', ScooterFlowMRT
#                 # ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=numexit #demand 
#                 LostDemand[0][j]+=numexit-ScooterFlowMRT #investigate why lost demand at mrt always 0
                
#             elif j!=len(ScooterInitializeList)-1: #Kiosks, apply fn(numentry, cdf=distributionlist(sumup))
#                 DemandKiosk=rand_round(distributionList[j]*numentry)
#                 numentry1+=DemandKiosk
#                 ScooterFlow=min(DemandKiosk,ScooterInitializeList[j])
#                 # print 'kiosk%i'%j
#                 # print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=DemandKiosk
#                 LostDemand[0][j]+=DemandKiosk-ScooterFlow
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow
            
#             else:
#                 ScooterFlow=min(numentry-numentry1,ScooterInitializeList[j])
#                 # print 'kiosk%i'%j
#                 # print 'numentry', distributionList[j]*numentry,round(distributionList[j]*numentry,0), 'remaining @kiosk',ScooterInitializeList[j], 'ScooterFlow', ScooterFlow
#                 ScootFlowList.append(ScooterFlow)
#                 Demand[0][j]+=numentry-numentry1
#                 LostDemand[0][j]+=(numentry-numentry1)-ScooterFlow
#                 Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow                

        
#         # print 'numexit', numexit, 'numentry', numentry, 'ScooterFlow', ScooterFlow
#         # print 'NEXT TIME STEP STARTS...'
#         ScooterFlowOutMRT=[]
#         # print 'len scootlist', len(ScooterInitializeList), 'len ScootFlowList', len(ScootFlowList)
#         for j in range(len(ScooterInitializeList)):
#             if j==0:
#                 ScooterInitializeList[j]+=(sum(ScootFlowList))-ScooterFlowMRT #mrt += flow_mrt - flow_kiosk
#             elif j!=len(ScooterInitializeList)-1:
#                 Arriving_at_Kiosk=rand_round(distributionList[j]*ScooterFlowMRT)
#                 ScooterFlowOutMRT.append(Arriving_at_Kiosk)
#                 ScooterInitializeList[j]+=Arriving_at_Kiosk-ScootFlowList[j-1] #kiosk += flow_kiosk - flow_mrt 
#             else:
#                 ScooterInitializeList[j]+=(ScooterFlowMRT-sum(ScooterFlowOutMRT))-ScootFlowList[j-1]

#             if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
#                 MaxSupplyDay[j][i]=ScooterInitializeList[j]            
#         print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)       

#     for j in range(len(ScooterInitializeList)): #summing on day level           
#         DemandDay[0][j]+=Demand[0][j]
#         LostDemandDay[0][j]+=LostDemand[0][j]
#         if j!=0:
#             ProfitDay[0][j-1]+=Profit[0][j-1]

# for j in range(len(ScooterInitializeList)): #averaging 
#     DemandDay[0][j]= DemandDay[0][j]/float(n) #Dileverable: Customer Base
#     LostDemandDay[0][j]= LostDemandDay[0][j]/float(n) #Dileverable: Lost Demand
#     if j!=0:
#         ProfitDay[0][j-1]= ProfitDay[0][j-1]/float(n) #Dilverable: Daily Profit

# # for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
# print "DemandDay:", DemandDay
# print "LostDemandDay", LostDemandDay
# print "ProfitDay", ProfitDay
# print "totalProfitDay", sum(ProfitDay[0]), "proportionLostDemand", sum(LostDemandDay[0])/float(sum(DemandDay[0]))
# print "MaxSupplyDay", MaxSupplyDay