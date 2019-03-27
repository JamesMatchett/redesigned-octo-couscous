from time import sleep
import brickpi3
import pygame

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
PORT_MOTOR_LEFT = BP.PORT_A
PORT_MOTOR_RIGHT = BP.PORT_B
minDist = 9
criticalDist = 6
maxDist = 18

def initSens():
    print("Configuring")
    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    sleep(2)
    

def waitForButton():
    print("Waiting")
    #while Notpressed

def stillGo():
    for event in pygame.event.get(): # User did something
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed, stopping!.")
                return False
    
    return True

def getDist(side):
    total = 0
    if(side == "R"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_3)
            sleep(0.02)
    if(side == "L"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_1)
            sleep(0.02)

    total = total/5
    return total


def steer(side, proximity):
    #if at minDist or below, 50% steering
    #if at midpoint between MaxDist & minDist, 0 % steering
    midpoint = maxDist - ((maxDist - minDist)/2)
    maxDiff = midpoint - criticalDist
    actDiff = proximity - criticalDist
    valOfSteer = (actDiff/maxDiff)
    if(side == "R"):
        BP.set_motor_power(PORT_MOTOR_LEFT, 100*valOfSteer)
    if(side == "L"):
        BP.set_motor_power(PORT_MOTOR_RIGHT, 100*valOfSteer)

        #we pass in 8cm should steer a little

        #we pass in 3cm should steer a lot
        
        
    
        
    

def GoRobotGo():
    print("Going!")
    go = True
    BP.set_motor_power(PORT_MOTOR_LEFT, 100)
    BP.set_motor_power(PORT_MOTOR_RIGHT, 100)
    while go:
        go = stillGo()
        left = getDist("L")
        right = getDist("R")
        if (left < minDist or right > maxDist):
            steer("R",left)
        elif(right < minDist or left > maxDist):
            steer("L",right)
        else:
            BP.set_motor_power(PORT_MOTOR_LEFT, 100)
            BP.set_motor_power(PORT_MOTOR_RIGHT, 100)
    sleep(2)
            
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
            
        

#wait for input
while True:
    waitForStart()
    GoRobotGo()
