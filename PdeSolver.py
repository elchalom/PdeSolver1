#If confused, consult README

import numpy as np
import matplotlib.pyplot as plt


#Global Constants

g=9.80665
alt = 1400 #Launch Altitude

mfueli=3.547
mi=15.893877 + mfueli
tfuel = 3.61

launchangle = 2

altmain = 200

ws1, alt1 = 8.9, 1000
ws2, alt2 = 8.9, 2000
ws3, alt3 = 8.9, 3000
ws4, alt4 = 8.9, 4000

#Aerodynamic Components
Ddrogue = 2
CDdrogue = 0.97
Dmain = 12
CDmain = 0.97
CDnose = 0.3082

def area(d):
    return 3.14*(d/2)**2

Areax = 0.347
CDx = 0.38
Ayairframe = 0.0135


#Time Parameters - smol dt accurate, big dt quicker runtime, edit accordingly
dt = 0.01
endtime = 2000

#Initialize Equations
time = np.arrange(0, endtime, dt) #Vector of time values seperated by dt from 0 until endtime

rxVals, vxVals, axVals = [], [], [] #Blank vectors for values in x
ryVals, vyVals, ayVals = [], [], [] #Blank vectors for values in y


#Initial conditions
rx, vx = 0, 0.01
ry, vy = alt, 0.01
m = mi


#Main Simulation Loop
for t in time:
    delta = (ry**2) / 90000
    
    if vy > 0:
        theta = launchangle + delta
    else:
        theta = 0
    
    if 0 < ry < alt1:
        vrelx = vx - ws1
    elif alt1 < ry < alt2:
        vrelx = vx - ws2
    elif alt2 < ry < alt3:
        vrelx = vx - ws3
    elif alt3 < vx < alt4:
        vrelx = vx - ws4
    else:
        vrelx = vx
        
    vrely = vy
    
    vrel = np.sqrt(vrelx**2 + vrelx**2)
    
    #Aerodynamics
    rho = (-((ry + alt) / 1000-44.3308)/42.2665)**(7418/1743) #idek
    
    if vy > 0:
        Areay = Ayairframe
        CDy = CDnose
    elif vy<0 and ry > altmain:
        Areay = area(Dmain)
        CDy = CDmain
    elif vy<0 and ry < altmain:
        Areay = area(Ddrogue)
        CDy = CDdrogue
    else:
        Areay = Ayairframe
        CDy = CDnose
    
    #Thrust Profile - edit values based on motor
    
    

