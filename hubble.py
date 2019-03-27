#Hubble code
#Assume we start facing no colours
#Order is Red, Blue, Yellow and, finally, Green.

#call first colour we see "North"

from time import sleep
import brickpi3
import pygame




def initSens():
    print("Configuring")
    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    sleep(2)
    

def speed(lval, rval):
    BP.set_motor_power(PORT_MOTOR_LEFT, lval)
    BP.set_motor_power(PORT_MOTOR_LEFT, rval)
    

def getMotVal(mot):
    if mot == "R":
        return BP.get_motor_encoder(BP.PORT_B)
    if mot == "L":
        return BP.get_motor_encoder(BP.PORT_A)
        

def turn(bearing):
    #bearing is where we want to turn to
    degToTurn = bearing - hdg
    #if deg positive, turning right
    #else turning left
    print("Turning "+str(degToTurn)+" Degrees")
    if degToTurn != 0:
        lVal= BP.get_motor_encoder(BP.PORT_A)
        RVal= BP.get_motor_encoder(BP.PORT_B)
        #motor records in half degrees, times degToTurn by 2
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
            
    
    return bearing
    #trBR

def goToNextColour():
    if(colours[colourPointer] in posArray):
        hdg = turn((posArray.index(colours[colourPointer]))*90)
        boop()
        colorPointer = colorPointer + 1
        goToNextColour()

def getColour(bearing):
    #work out to turn to
    turn(bearing)
    #read colour
    colour = camColour()
    posArray[bearing/90] = colour
    goToNextColour()
    #Try to go to the next colour, if we know where it is
    #Return colour

def getFDist():
    total = 0
    for x in range(0,5):
        total = total + BP.get_sensor(BP.PORT_1)
        sleep(0.02)

    total = total/5
    return total
    
    
    

def boop():
    lval = getMotVal("L")
    rval = getMotVal("R")
    while getFDist() > boopDist:
        speed(100,100)
    speed(0,0)
    sleep(.5)
    while getMotVal("L") > lval and getMotVal("R") > rval:
        speed(-100,-100)
    speed(0,0)

def waitForStart():
    initSens()
    print("Ready")
    pygame.init()
    clock = pygame.time.Clock()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    wait = True
    print("Waiting")
    while wait:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                wait = False

def go():
    print("Going")
    getColour(0)
    getColour(90)
    getColour(180)
    getColour(270)
    

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
PORT_MOTOR_LEFT = BP.PORT_A
PORT_MOTOR_RIGHT = BP.PORT_B

colours = ["Red", "Blue", "Yellow", "Green"]
#NESW array
posArray = ["","","",""]
boopDist = 5

colourPointer = 0
hdg = -45


waitForStart()
go()
