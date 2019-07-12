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
import copy  

workdaydata= csv.reader(open('WorkdayMV1.csv', 'rb'))
Datastorage=[]
for i in workdaydata:
    for j in i:
        Datastorage.append(j)

time = len(Datastorage)/13

Time_of = {n: Datastorage[:time][n] for n in range(time)} #dictionary of time bins
workday_entrymu = [float(z) for z in Datastorage[time:2*time]]
workday_entrysd = [float(z) for z in Datastorage[2*time:3*time]]
workday_exitmu = [float(z) for z in Datastorage[3*time:4*time]]
workday_exitsd = [float(z) for z in Datastorage[4*time:5*time]]
sat_entrymu = [float(z) for z in Datastorage[5*time:6*time]]
sat_entrysd = [float(z) for z in Datastorage[6*time:7*time]]
sat_exitmu = [float(z) for z in Datastorage[7*time:8*time]]
sat_exitsd = [float(z) for z in Datastorage[8*time:9*time]]
sun_entrymu = [float(z) for z in Datastorage[9*time:10*time]]
sun_entrysd = [float(z) for z in Datastorage[10*time:11*time]]
sun_exitmu = [float(z) for z in Datastorage[11*time:12*time]]
sun_exitsd = [float(z) for z in Datastorage[12*time:13*time]]

def lognormal(m,v,p):
    phi = math.sqrt(v+m**2)
    if phi != 0 and m != 0:
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

#construct cdf
def cdf(List): #insert pmf list, return cdf list
    List2=[0.0]
    ListValue=0
    for i in range(len(List)):
        if i!=len(List)-1:
            ListValue+=List[i]
            List2.append(ListValue)
        else:
            List2.append(1.0)
    return List2

    
#inverse transform algorithm on kiosk
def Distribute(numentry,List):#input: cdf list, output: Demand Count array
    DemandCount=np.zeros((1,len(List)-1))
    for i in range(int(numentry)):
        Person=random.random()
        for j in range(len(List)-1):
            if List[j]<=Person<List[j+1]:
                DemandCount[0][j]+=1
                break
    return DemandCount


#Pre Simulation
m=time #time intervals
n=1 #simulation runs
ProjectBudget=1000000 #Total expenditure allowed for the project (constraint)
CostKiosk=100000 #cost of building 1 kiosk
CostScooter=1000 #cost of buying and maintaining 1 inokim light
ElectricityPerDistance=0.012 #units?
CostPerElectricity=0.04 #units?
p = 0.0833333333333333 #Proportion of generated population actually decides to use scooter. Possible modification could be made here.
distributionList=[0.06085370416898961, 0.06085100830649153, 0.09736161329038645, 0.024340403322596613, 0.03651060498389492, 0.060387319956823074, 0.12170201661298306, 0.08519410749158622, 0.21135561984888074, 0.08519141162908815, 0.11624559091688441, 0.010999118992135631, 0.01865536848666141, 0.01035211199259824]
# distributionList= sorted(distributionList)
# distributionListReverse=copy.deepcopy(distributionList)
# distributionListReverse.reverse()
#Probabilility distribution of scooter population over all kiosks including mrt with fraction value 1=> ratio data?
#Running cost to travel to a kiosk from mrt for all kiosk, or vice versa => each element=Cost/electricity*electricity/distance*distance(Kiosk,MRT), ask: shd cost be random?
PricingList=[0.2396, 0.3196, 0.3196, 0.3196, 0.3578, 0.3578, 0.3578, 0.3578, 0.3030, 0.2310, 0.2809, 0.2686, 0.3978, 0.3762] #Price charged to travel to a kiosk from mrt for all kiosks, or vice versa => interpolation data?
OpsCostList=[9.19901E-06, 1.27764E-05, 1.27764E-05, 1.27764E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.46016E-05, 1.20098E-05, 8.83397E-06, 1.1006E-05, 1.04584E-05, 1.66093E-05, 1.55142E-05] 
#374.4wh/charge, 40km/charge, 0.195cents/kwh ==> 0.000018252 dollar/km
TotalInitialization=260
# ScooterInitializeList=[0,20.916777699999997, 20.916777699999997, 33.46684425, 8.366711149999999, 12.550066549999999, 20.7573905, 41.833555399999995, 29.28348885, 72.6508671, 29.28348885, 39.9579768, 3.7808105999999997, 6.264283900000001, 6.4125509, 3.55840975] #Scooters intially placed at each kiosk, including first being mrt ==> need input from evelyn on what number good to initialize.
ScooterInitializeList=[0.0]
#All scooters initialized at koisk
# check=0
for i in range(len(distributionList)): 
    if i!=len(distributionList)-1:
        ScooterInitializeList.append(rand_round(distributionList[i]*TotalInitialization))
    else:
        ScooterInitializeList.append(TotalInitialization-sum(ScooterInitializeList))

#Simulation
DemandDay=np.zeros((1,len(ScooterInitializeList)))
LostDemandDay=np.zeros((1,len(ScooterInitializeList)))
ProfitDay=np.zeros((1,len(ScooterInitializeList)-1))
MaxSupplyDay=np.zeros((len(ScooterInitializeList),n))
CDF=cdf(distributionList)
# CDFrev=cdf(distributionListReverse)
saturday=5
sunday=6
r=0
x=0.0001
y=0.0001
# T=0
Latitude=[1.34226+x,1.34277+x,1.34635+x,1.34696+x,1.34598+x,1.34519+x,1.34677+x,1.34546+x,1.34298+x,1.3413+x,1.34263+x,1.34143+x,1.33941+x,1.33679+x,1.33632+x]
Longitude=[103.95346+y,103.94914+y,103.95433+y,103.95628+y,103.95595+y,103.95724+y,103.95833+y,103.9585+y,103.95798+y,103.95626+y,103.95697+y,103.95772+y,103.95825+y,103.95128+y,103.95516+y]
LocationName=["Simei Station","116/117/119 (113)","124/126/128/129/130","132-139","147/148/149","150/151/153","Melville Park","155/164","168-","Double Bay Condo","226","Simei Green","Landed (Sunbird)","Landed (Sea Breeze)","Landed (Jln Angin Laut)"]
#restribution strategy 1: distribute 210 scooters at t=10 & 15 (Mrt to kiosk), distribute t= 58 & 63 (Kiosk to MRT)

test=open('dataAnalyticsWR2.csv','wb')
tt=csv.writer(test)

for i in range(n):
    # print 'day=%i'%i
    # print 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
    Demand= np.zeros((1,len(ScooterInitializeList)))
    LostDemand=np.zeros((1,len(ScooterInitializeList)))
    Profit=np.zeros((1,len(ScooterInitializeList)-1))
    
    #distribution selection
    if i== saturday:
        entrymu, entrysd = sat_entrymu, sat_entrysd
        exitmu, exitsd = sat_exitmu, sat_exitsd
        saturday+=7
        # print 'Today is saturday', 'next saturday=', saturday
    elif i==sunday:
        entrymu, entrysd = sun_entrymu, sun_entrysd
        exitmu, exitsd = sun_exitmu, sun_exitsd
        sunday+=7
        # print 'Today is sunday', 'next sunday=', sunday
    else:
        entrymu, entrysd = workday_entrymu, workday_entrysd
        exitmu, exitsd = workday_exitmu, workday_exitsd
        # print 'Today is weekday'    

        
    for t in range(m): #sum scoot should say fixed. it should not vary. balance transfer.
        numentry = lognormal(entrymu[t],entrysd[t],p) #Demand @kiosk, nature : generated rv,people in scooter
        numexit = lognormal(exitmu[t],exitsd[t],p) #Demand @mrt, nature: generated rv, people in scooter
        #loop through everykiosks, actually can combine mrt inside this, but simplicity, now lets work seperately on kiosk and mrt
        ScootFlowList=[]
        DemandList=[]
        LossDemandList=[]
        ProfitList=[0.0]
        Distribution=Distribute(numentry,CDF)

        for j in range(len(ScooterInitializeList)):
            # print 'j=',j
            if j==0: #MRT
                ScooterFlow=min(numexit,ScooterInitializeList[j])
                # print 't', t, 'j',j,'demand', numexit, 'supply',ScooterInitializeList[j],'loss demand', numexit-ScooterFlow
                # tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],numexit,numexit-ScooterFlow])
                ScootFlowList.append(ScooterFlow)
                DemandList.append(numexit)
                LossDemandList.append(numexit-ScooterFlow)
                Demand[0][j]+=numexit #demand 
                LostDemand[0][j]+=numexit-ScooterFlow #investigate why lost demand at mrt always 0
                # print 'Demand@mrt', numexit,'scooter@mrt', ScooterInitializeList[j], 'DemandMet@mrt', ScooterFlow,'DemandLost@mrt', numexit-ScooterFlow
            else: #Kiosks, apply fn(numentry, cdf=distributionlist(sumup))
                DemandKiosk=Distribution[0][j-1]
                ScooterFlow=min(DemandKiosk,ScooterInitializeList[j])
                DemandList.append(DemandKiosk)
                LossDemandList.append(DemandKiosk-ScooterFlow)                
                # tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],DemandKiosk,DemandKiosk-ScooterFlow])
                ScootFlowList.append(ScooterFlow)
                Demand[0][j]+=DemandKiosk
                LostDemand[0][j]+=DemandKiosk-ScooterFlow
                Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*ScooterFlow
                ProfitList.append((PricingList[j-1]-OpsCostList[j-1])*ScooterFlow)
                # print 'numentry',numentry,'Demand@kiosk%i'%j, DemandKiosk,'scooter@kiosk%i'%j, ScooterInitializeList[j], 'DemandMet@kiosk%i'%j, ScooterFlow,'DemandLost@kiosk%i'%j, DemandKiosk-ScooterFlow
            
        Distribution2=Distribute(ScootFlowList[0],CDF) #1st element of scootflow is the amount of scooters flowing out of mrt at time t       
        for j in range(1,len(ScooterInitializeList)):
            Profit[0][j-1]+=(PricingList[j-1]-OpsCostList[j-1])*Distribution2[0][j-1]
            ProfitList[j]+=(PricingList[j-1]-OpsCostList[j-1])*Distribution2[0][j-1]

        for j in range(len(ScooterInitializeList)):
            if j==0:
                ScooterInitializeList[j]+=(sum(ScootFlowList)-ScootFlowList[j])-ScootFlowList[j] #mrt += flow_mrt - flow_kiosk
                tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])
            else: 
                ScooterInitializeList[j]+=Distribution2[0][j-1]-ScootFlowList[j] #kiosk += flow_kiosk - flow_mrt 
                tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])

            if ScooterInitializeList[j]>MaxSupplyDay[j][i]: #Storing maximum supply in a given day
                MaxSupplyDay[j][i]=ScooterInitializeList[j]            
        # print 'time period=%i'%t, 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)       

        # tt.writerow([i,t,r,ScooterInitializeList[0],ScooterInitializeList[1],ScooterInitializeList[2],ScooterInitializeList[3],ScooterInitializeList[4],ScooterInitializeList[5],ScooterInitializeList[6],ScooterInitializeList[7],ScooterInitializeList[8],ScooterInitializeList[9],ScooterInitializeList[10],ScooterInitializeList[11],ScooterInitializeList[12],ScooterInitializeList[13],ScooterInitializeList[14]])

        #restribution strategy 1: distribute 210 scooters at t=10 & 15 (Mrt to kiosk), distribute t= 58 & 63 (Kiosk to MRT)
        if r==1:
            if t==10 or t==15:
                ScooterMRT=copy.deepcopy(ScooterInitializeList[0])
                ScooterInitializeList[0]-= ScooterMRT
                Distribution3=Distribute(ScooterMRT,CDF)
                for j in range(len(ScooterInitializeList)):
                    if j==0:
                        tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])
                    else:
                        ScooterInitializeList[j]+=Distribution3[0][j-1]
                        tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])
                # print 'time period=%i'%t, 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)
            elif t==58 or t==63:
                ScooterKiosk=copy.deepcopy(sum(ScooterInitializeList)-ScooterInitializeList[0])
                ScooterInitializeList[0]+=ScooterKiosk
                for j in range(len(ScooterInitializeList)):
                    if j==0:
                        tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])
                    else:
                        ScooterInitializeList[j]-=ScooterInitializeList[j]
                        tt.writerow([r,t,j,LocationName[j],Latitude[j],Longitude[j],ScooterInitializeList[j],DemandList[j],LossDemandList[j],ProfitList[j]])
                # print 'time period=%i'%t, 'scooterCount', ScooterInitializeList, 'totalscooter', sum(ScooterInitializeList)

    # T+=82        

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

test.close()


# for parking capacity, transfer the maxsupply matrix to excel analyze the distribution.
print "DemandDay:", DemandDay
print "LostDemandDay", LostDemandDay
print "ProfitDay", ProfitDay
print "totalProfitDay", sum(ProfitDay[0]), "proportionLostDemand", sum(LostDemandDay[0])/float(sum(DemandDay[0]))
print "MaxSupplyDay", MaxSupplyDay


# ar = MaxSupplyDay

# import csv

# fl = open('MaxCapacity2.csv', 'w')

# writer = csv.writer(fl)
# writer.writerow(['MRT', 'Kiosk1', 'Kiosk2', 'Kiosk3', 'Kiosk4', 'Kiosk5', 'Kiosk6', 'Kiosk7', 'Kiosk8', 'Kiosk9', 'Kiosk10', 'Kiosk11', 'Kiosk12', 'Kiosk13', 'Kiosk14']) #if needed
# for values in ar:
#     writer.writerow(values)

# fl.close()  





Mrt=math.ceil(np.percentile(MaxSupplyDay[0],95))
Kiosk1=math.ceil(np.percentile(MaxSupplyDay[1],95))
Kiosk2=math.ceil(np.percentile(MaxSupplyDay[2],95))
Kiosk3=math.ceil(np.percentile(MaxSupplyDay[3],95))
Kiosk4=math.ceil(np.percentile(MaxSupplyDay[4],95))
Kiosk5=math.ceil(np.percentile(MaxSupplyDay[5],95))
Kiosk6=math.ceil(np.percentile(MaxSupplyDay[6],95))
Kiosk7=math.ceil(np.percentile(MaxSupplyDay[7],95))
Kiosk8=math.ceil(np.percentile(MaxSupplyDay[8],95))
Kiosk9=math.ceil(np.percentile(MaxSupplyDay[9],95))
Kiosk10=math.ceil(np.percentile(MaxSupplyDay[10],95))
Kiosk11=math.ceil(np.percentile(MaxSupplyDay[11],95))
Kiosk12=math.ceil(np.percentile(MaxSupplyDay[12],95))
Kiosk13=math.ceil(np.percentile(MaxSupplyDay[13],95))
Kiosk14=math.ceil(np.percentile(MaxSupplyDay[14],95))
Kiosk = [math.ceil(np.percentile(MaxSupplyDay[i],95)) for i in range(15)]

print 'kiosk',Kiosk
# print 'Mrt',Mrt
# print 'kiosk1',Kiosk1
# print 'kiosk2',Kiosk2
# print 'kiosk3',Kiosk3
# print 'kiosk4',Kiosk4
# print 'kiosk5',Kiosk5
# print 'kiosk6',Kiosk6
# print 'kiosk7',Kiosk7
# print 'kiosk8',Kiosk8
# print 'kiosk9',Kiosk9
# print 'kiosk10',Kiosk10
# print 'kiosk11',Kiosk11
# print 'kiosk12',Kiosk12
# print 'kiosk13',Kiosk13
# print 'kiosk14',Kiosk14


# test=open('review4.csv','wb')
# tt=csv.writer(test)

# for i in range(len(ScooterInitializeList)):
#     if i==0:
#         tt.writerow([i,DemandDay[0][i],LostDemandDay[0][i],'NA',Kiosk[i]])
#     else:
#         tt.writerow([i,DemandDay[0][i],LostDemandDay[0][i],ProfitDay[0][i-1],Kiosk[i]])
# test.close()