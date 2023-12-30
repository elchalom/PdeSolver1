#CONSULT README BEFORE MAKING EDITS
#-------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


#Global Constants

g=9.80665
alt = 1400 #Launch Altitude

mfueli=3.547 #Fuel mass at launch
mi=15.893877 + mfueli #Mass of rocket + mass of fuel
tfuel = 3.61 #Firing time

launchangle = 2

altmain = 200

#Windspeeds at different altitudes
ws1, alt1 = 8.9, 1000
ws2, alt2 = 8.9, 2000
ws3, alt3 = 8.9, 3000
ws4, alt4 = 8.9, 4000

#Thrust profile - add or remove stages for different motor profiles
t1, p1 = 0.20, 2400
t2, p2 = 1.00, 2500
t3, p3 = 2.60, 2250
t4, p4 = 2.80, 2000
t5, p5 = 3.30, 750
t6, p6 = 3.61, 150


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
        
    Fdragy = -0.5 * rho * Areay * CDy * vrel**2 * vrely / (vrel + 10**-6) 
    Fdragx = -0.5 * rho * Areax * CDx * vrel**2 * vrelx / (vrel + 10**-6)
    
    
    #Thrust Profile
    if t<t1:
        Fthrust = p1
    elif t<t2:
        Fthrust = p2
    elif t<t3:
        Fthrust = p3
    elif t<t4:
        Fthrust = p4
    elif t<t5:
        Fthrust = p5
    elif t<t6:
        Fthrust = p6
    else:
        Fthrust = 0
    
    Fthrustx = -Fthrust * np.sin(np.radians(theta))
    Fthrusty = Fthrust * np.cos(np.radians(theta))
    
    #Mass
    if t<tfuel:
        mfuelgone = t*(mfueli/tfuel)
    else:
        mfuelgone = mfueli
        
    m = mi - mfuelgone
    
    #acceleration
    ax = (Fdragx + Fthrustx) / m
    ay = (Fthrusty + Fdragy) / m - g
    
    axVals.append(ax)
    ayVals.append(ay)
        
    #Update varaibles - displacement updated using prev value of v
    rx += vx * dt
    vx += ax * dt
    ry += vy * dt
    vy += ay * dt
    
    rxVals.append(rx)
    vxVals.append(vx)
    ryVals.append(ry)
    vyVals.append(vy)
    
    
for i in rxVals:
    print(rxVals[i])