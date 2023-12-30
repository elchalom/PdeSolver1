# PdeSolver1
Install Python 3 with Numpy and matplotlib

Simulation program for McMaster Rocketry developed by the recovery subteam

All Values are in METRIC SI units

Current values are for the Maurader 2, edit these parameters if a different rocket is used
    -Thrust profile / fuel firing times
    -Mass of rocket without fuel
    -Mass of fuel 
    -Aerodynamic properties (Parachutes and Airframe)

Current values are for the launchsite in new mexico, edit if a different site wants to be simulated
    -alt (launch altitude)
    -wind speeds

DO NOT edit the main program loop to change parameter values, all parameters are accessible in global scope


The equations are broken down into x and y directions
    rx = displacement in x
    vx = velocity in x
    ax = accelleration in x
    values in y follow same convention - any values without x and y notation are combinations of the two or independent of direction
