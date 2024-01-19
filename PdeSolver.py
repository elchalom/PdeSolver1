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

mfueli=3.547 #Fuel mass at launch
mrocket = 15.893877 #Mass of rocket without fuel
mi=mrocket + mfueli #Launch mass
tfuel = 3.61 #Firing time

launchangle = 2

altmain = 200 #Main chute deployment altitude

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
Ddrogue = 0.6096
CDdrogue = 0.97
Dmain = 3.6576
CDmain = 0.97
CDnose = 0.3082


#Cross sections of frame
Areax = 0.347
CDx = 0.38
Ayairframe = 0.0135


#Initialize Equations
time = [0]

rxVals, vxVals, axVals = [], [], [] #Blank vectors for values in x
ryVals, vyVals, ayVals = [], [], [] #Blank vectors for values in y
rhoVals, thetaVals = [], [] #Blank vectors for rho and theta


#Initial conditions
rx, vx = 0, 0.001
ry, vy = 0.001, 0.001
m = mi

def area(d):
    return 3.14*(d/2)**2


#Main Simulation Loop

def main(rx, vx, ry, vy):
    dt = 0.001 # time interval where values are recalculated
    i = 0
    while ry > 0:
        
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
        
        if(ry>0):
            time.append(t+dt)
            i+=1
        
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
