from time import sleep
import brickpi3
import pygame
import time

BP = brickpi3.BrickPi3()

SPEED = -25
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
PORT_MOTOR_LEFT = BP.PORT_A
PORT_MOTOR_RIGHT = BP.PORT_B
minDist = 20
criticalDist = 4
maxDist = 30
since_last_turn = 0

def initSens():
    BP.set_motor_power(PORT_MOTOR_LEFT, 0)
    BP.set_motor_power(PORT_MOTOR_RIGHT, 0)
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
            sleep(0.01)
    if(side == "L"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_1)
            sleep(0.01)

    total = total/5
    return round(total)


def steer(side, proximity):
    if(proximity < 5):
        BP.set_motor_power(PORT_MOTOR_LEFT, 0)
        BP.set_motor_power(PORT_MOTOR_RIGHT, 0)
        if(side == "R"):
            BP.set_motor_power(PORT_MOTOR_LEFT, -100)
            BP.set_motor_power(PORT_MOTOR_RIGHT, 100)
            sleep(0.25)
            BP.set_motor_power(PORT_MOTOR_LEFT, SPEED)
            BP.set_motor_power(PORT_MOTOR_RIGHT, SPEED)

        if(side == "L"):
            BP.set_motor_power(PORT_MOTOR_LEFT, 100)
            BP.set_motor_power(PORT_MOTOR_RIGHT, -100)
            sleep(0.25)
            BP.set_motor_power(PORT_MOTOR_LEFT, SPEED)
            BP.set_motor_power(PORT_MOTOR_RIGHT, SPEED)

            
            
            
            
        #we pass in 8cm should steer a little

        #we pass in 3cm should steer a lot
        
        
    
        
    

def GoRobotGo():
    print("Going!")
    go = True
    BP.set_motor_power(PORT_MOTOR_LEFT, SPEED)
    BP.set_motor_power(PORT_MOTOR_RIGHT, SPEED)
    while go:
        go = stillGo()
        left = getDist("L")
        right = getDist("R")
        print(left, right)
        if (left < minDist):
            print("steering right")
            steer("L",left)
        elif(right < minDist):
            print("steering left")
            steer("R",right)
        else:
            BP.set_motor_power(PORT_MOTOR_LEFT, SPEED)
            BP.set_motor_power(PORT_MOTOR_RIGHT, SPEED)
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
