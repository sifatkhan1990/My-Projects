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
#     
import math
import numpy
import scipy
List=[1,2,3]
d=sum(List)
print d
List=[1,4,5]
v=sum(List)
k= numpy.mean(List)
var= numpy.var(List)
std= numpy.std(List)
print v , k, var, std
matrix=numpy.zeros((3,4,5))
print matrix
matrix[1][0][0]=1
print "matrix[1][0][0]"
print matrix
matrix[0][1][0]=2
matrix[0][1][1]=1.5
matrix[0][1][2]=2.5
matrix[0][1][3]=0.5
matrix[0][1][4]=3
print "matrix[0][1][0]"
print matrix
matrix[0][0][1]=3
print "matrix[0][0][1]"
print matrix
print "matrix[0][1]"
print matrix[0][1]
print "sum(matrix[0][1])", sum(matrix[0][1])
print "avg(matrix[0][1])", numpy.mean(matrix[0][1])
print "var(matrix[0][1])", numpy.var(matrix[0][1])
print "std(matrix[0][1])", numpy.std(matrix[0][1])
