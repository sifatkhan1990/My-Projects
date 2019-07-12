# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:24:19 2016

@author: Eos
"""

import random

entrymu = [100,106,132,142]
entrysd = [10,10,10,10]
exitmu = [88,93,77,77]
exitsd = [10,10,10,10]
p = 0.4
#tolkiosk = []
count = 0
i = 0

while i < 1000:
    mrt = 40
    kiosk = 30
    tolmrt = []
    
    for t in range(len(entrymu)):
        numentry = round(random.normalvariate(p*entrymu[t],p*entrysd[t]),0)
        numexit = round(random.normalvariate(p*exitmu[t],p*exitsd[t]),0)
        #print numentry, numexit    
        
        mrt = mrt + numentry - numexit
        kiosk = kiosk - numentry + numexit
        #print mrt + kiosk    
        
        tolmrt.append(max(0,(numexit-mrt))/numexit) #fulfil demand output 0
    
    psol = sum(tolmrt)/float(len(tolmrt)) #probability of people not finding a scooter on average
    print psol
    
    if psol > 0.05:
        count += 1
    i += 1

print count/float(1000)
    