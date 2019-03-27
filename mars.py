#canyons of mars
#drive to booping distance
#turn
#repeat

import time
import brickpi3

BP = brickpi3.BrickPi3()

##Front sensor
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

#Right sensor
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
PORT_MOTOR_LEFT = BP.PORT.A
PORT_MOTOR_RIGHT = BP.PORT.B

idealDist = 5
boopDist = 5
tTime = 0.75

##Array list for turn directions

def speed(lval, rval):
    BP.set_motor_power(PORT_MOTOR_LEFT, lval)
    BP.set_motor_power(PORT_MOTOR_LEFT, rval)
    

def getMotVal(mot):
    if mot == "R":
        return BP.get_motor_encoder(BP.PORT_B)
    if mot == "L":
        return BP.get_motor_encoder(BP.PORT_A)
        

def turn90(tDir):
    degToTurn = 0
    if tDir == "R":
        degToTurn = 90
    if tDir == "L":
        degToTurn = -90
        
    #motor records in half degrees, times degToTurn by 2
    degToTurn = degToTurn
    if degToTurn > 0:
        #turn right
        lTarg = getMotVal("L") + degToTurn
        rTarg = getMotVal("R") - degToTurn
        while getMotVal("L") < lTarg and getMotVal("R") > rTarg:
            speed(100,-100)
        speed(0,0)
            
    else:
        lTarg = getMotVal("L") - degToTurn
        rTarg = getMotVal("R") + degToTurn
        while getMotVal("L") > lTarg and getMotVal("R") < rTarg:
            speed(-100,100)
        speed(0,0)

def getDist(side):
    total = 0
    if(side == "F"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_3)
            sleep(0.02)
    if(side == "R"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_3)
            sleep(0.02)

     total = total/5
     return total

def forward(speed):
    BP.set_motor_power(PORT_MOTOR_LEFT, speed)
    BP.set_motor_power(PORT_MOTOR_RIGHT, speed)
    

maxDist = idealDist * 1.5
minDist = idealDist/1.5

def steer(side, proximity):
    #if at minDist or below, 50% steering
    #if at midpoint between MaxDist & minDist, 0 % steering
    midpoint = maxDist - ((maxDist - minDist)/2)
    maxDiff = midpoint - minDist
    actDiff = proximity - minDist
    valOfSteer = (actDiff/maxDiff)
    if(side == "R"):
        BP.set_motor_power(PORT_MOTOR_LEFT, 100*valOfSteer)
    if(side == "L"):
        BP.set_motor_power(PORT_MOTOR_RIGHT, 100*valOfSteer)

def first():
    forward(100)
    while getDist("F") > boopDist:
        #slight steering in each direction
        #to maintain an equal distane
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)

def second():
    turn90("L")
    forward(100)
    while getDist("F") > boopDist:
        #slight steering in each direction
        #to maintain an equal distane
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)

def third():
    turn90("L")
    forward(100)
    count = 0
    while getDist("F") > boopDist:
        #only steering for 1.5 seconds as wall ends
        if count < 3:
            if (getDist("R") > idealDist):
                steer("R", getDist("R"))
            else:
                steer("L", getDist("R"))
            count = count + 1
            sleep(.5)
    forward(0)

def fourth():
    turn90("R")
    forward(100)
    #No steering as wall on right too far away
    #driving on faith
    while getDist("F") > boopDist:
        forward(100)
    forward(0)

def fifth():
    turn90("R")
    forward(100)
    #another awkard half wall
    #wait 1.5 seconds then use steering
    sleep(1.5)
    while getDist("F") > boopDist:
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)


def sixth():
    turn90("L")
    forward(100)
    #we got walls again!
    while getDist("F") > boopDist:
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)

def seventh():
    turn90("L")
    forward(100)
    while getDist("F") > boopDist:
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)


def eighth():
    turn90("L")
    forward(100)
     while getDist("F") > boopDist:
        if (getDist("R") > idealDist):
            steer("R", getDist("R"))
        else:
            steer("L", getDist("R"))
    forward(0)
    turn90("R")
    forward(100)
    sleep(4)
    forward(0)
    
    
    
            
        
    

def waitForGo():
    wait = True
    while wait:
        if(joystick.get_button(1) == 1):
            wait = False

def GoRobotGo():
    first()
    second()
    third()
    fourth()
    fifth()
    sixth()
    seventh()
    eighth()
    

while True:
    waitForGo()
    GoRobotGo()
