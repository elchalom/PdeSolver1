# PdeSolver1
Simulation program for McMaster Rocketry developed by the recovery subteam

All Values are in METRIC SI units

Current values are for the Maurader 2, edit these parameters if a different rocket is used
    -Thrust profile
    -Mass (Fuel and frame are SEPERATE variables)
    -Aerodynamic properties (Parachutes and Airframe)

Current values are for the launchsite in new mexico, edit if a different site wants to be simulated
    -alt (launch altitude)
    -wind speeds

DO NOT edit the main program loop to change parameter values, all parameters are to be accessed in global scope


The equations are broken down into x and y directions
    rx = displacement in x
    vx = velocity in x
    ax = accelleration in x
    values in y follow same convention - any values without x and y notation are combinations of the two or independent of direction
