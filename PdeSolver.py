#CONSULT README BEFORE MAKING EDITS
#-------------------------------------------------------------------------------------------------

#TODO make changes so that default launch profiles can be saved to files and the program pulls data from those files instead. 
#TODO break program down into seperate functions, global scope variables should be accessible only from datafiles
#TODO add motor JSON file to smooth the curve.
#TODO add user interface to modify initial parameters.


import numpy as np
import matplotlib.pyplot as plt


#Global Constants

g=9.80665
alt = 1400 #Launch Altitude

mfueli=4.835 #Fuel mass at launch
mrocket = 12.973 #Mass of rocket without fuel
mi=mrocket + mfueli #Launch mass

launchangle = 2

altmain = 200 #Main chute deployment altitude

#Windspeeds at different altitudes
ws1, alt1 = 8.9, 1000
ws2, alt2 = 8.9, 2000
ws3, alt3 = 8.9, 3000
ws4, alt4 = 8.9, 4000

#Thrust profile - (time (s), thrust (N))
thrust_data = [
    (0.038, 1517.15), (0.063, 1076.517), (0.068, 1282.322), (0.076, 1509.235), 
    (0.144, 1741.425), (0.207, 1765.172), (0.334, 1749.34), (0.537, 1791.557), 
    (0.753, 1794.195), (1.053, 1775.726), (1.383, 1788.918), (1.704, 1820.58), 
    (1.856, 1828.496), (2.013, 1799.472), (2.601, 1686.016), (2.905, 1641.161), 
    (3.188, 1617.414), (3.472, 1598.945), (3.738, 1583.113), (3.958, 1564.644), 
    (4.14, 1543.536), (4.216, 1543.536), (4.33, 1482.85), (4.453, 1358.839), 
    (4.55, 1187.335), (4.723, 1052.77), (4.876, 891.821), (4.969, 783.641), 
    (5.028, 643.799), (5.231, 184.697), (5.303, 68.602), (5.396, 0)
]

tfuel = thrust_data[-1][0] #Firing time

#Aerodynamic Components
Ddrogue = 0.914
CDdrogue = 0.97
Dmain = 4.267
CDmain = 0.97
CDnose = 0.3082


#Cross sections of frame
Areax = 0.499
CDx = 0.38
Ayairframe = 0.0135


#Initialize Equations
time = [0]

rxVals, vxVals, axVals = [], [], [] #Blank vectors for values in x
ryVals, vyVals, ayVals = [], [], [] #Blank vectors for values in y
rhoVals, thetaVals = [], [] #Blank vectors for rho and theta


#Initial conditions
rx, vx = 0, 0.00001
ry, vy = 0.00001, 0.00001
m = mi

def area(d):
    return 3.14*(d/2)**2


#Main Simulation Loop

def main(rx, vx, ry, vy):
    dt = 0.001 # time interval where values are recalculated
    i = 0
    while True:
        
        t = time[i]
        
        delta = (ry**2) / 90000
        
        if vy > 0:
            theta = launchangle + delta
        else:
            theta = 0
        
        #Windspeeds
        if 0 < ry < alt1:
            vrelx = vx - ws1
        elif alt1 < ry < alt2:
            vrelx = vx - ws2
        elif alt2 < ry < alt3:
            vrelx = vx - ws3
        elif alt3 < ry < alt4:
            vrelx = vx - ws4
        else:
            vrelx = vx
            
        vrely = vy
        
        vrel = np.sqrt(vrely**2 + vrelx**2)
        
        #Aerodynamics
        rho = (-((ry + alt) / 1000-44.3308)/42.2665)**(7418/1743) #idek
        
        if vy > 0:
            Areay = Ayairframe
            CDy = CDnose
        elif vy<0 and ry > altmain:
            Areay = area(Ddrogue)
            CDy = CDdrogue
        elif vy<0 and ry < altmain:
            Areay = area(Dmain)
            CDy = CDmain
        # else:
        #     Areay = Ayairframe
        #     CDy = CDnose
            
        Fdragy = -0.5 * rho * Areay * CDy * vrel**2 * vrely / (vrel + 10**-6) 
        Fdragx = -0.5 * rho * Areax * CDx * vrel**2 * vrelx / (vrel + 10**-6)
        
        
        #Thrust Profile
        Fthrust = 0
        for j in range(len(thrust_data) - 1):
            if thrust_data[j][0] <= t and t < thrust_data[j + 1][0]:
                Fthrust = thrust_data[j][1]
                break
            
        #extract
        
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
        ay = (Fdragy + Fthrusty) / m - g
        
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
        rhoVals.append(rho)
        thetaVals.append(theta)
        
        if(ry>0 or t<1):
            time.append(t+dt)
            i+=1
        else:
            break
        
        #Break condition - incase changed parameters cause inf loop    
        if (time[i] > 2000):
            break
        
    print("Apogee: " + str(max(ryVals)))
    
    graphs()
        
    
#--------------------------------------------------------------
#Graphs

def graphs():

    plt.subplot(2,4,1)
    plt.plot(time, rxVals, label = 'rx')
    plt.title('rx')


    plt.subplot(2,4,2)
    plt.plot(time, vxVals, label = 'vx')
    plt.title('vx')

    plt.subplot(2,4,3)
    plt.plot(time, axVals, label = 'ax')
    plt.title('ax')

    plt.subplot(2,4,4)
    plt.plot(time,rhoVals, label = 'rho')
    plt.title('rho')

    plt.subplot(2,4,5)
    plt.plot(time, ryVals, label = 'ry')
    plt.title('ry')

    plt.subplot(2,4,6)
    plt.plot(time, vyVals, label = 'vy')
    plt.title('vy')

    plt.subplot(2,4,7)
    plt.plot(time, ayVals, label = 'ay')
    plt.title('ay')

    plt.subplot(2,4,8)
    plt.plot(time, thetaVals, label = 'theta')
    plt.title('theta')

    plt.show()

main(rx, vx, ry, vy)
