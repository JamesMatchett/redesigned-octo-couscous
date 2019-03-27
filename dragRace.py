import time
import brickpi3

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
PORT_MOTOR_LEFT = BP.PORT.A
PORT_MOTOR_RIGHT = BP.PORT.B
minDist = 9
criticalDist = 6
maxDist = 18

def waitForButton():
    print("Waiting")
    #while Notpressed

def stillGo():
    if(joystick.get_button(1) == 1):
        return false
    
    return True

def getDist(side):
    total = 0
    if(side == "R"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_3)
            sleep(0.02)
    if(side == "L"):
        for x in range(0,5):
            total = total + BP.get_sensor(BP.PORT_3)
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
    sleep(2)
    go = True
    BP.set_motor_power(PORT_MOTOR_LEFT, 100)
    BP.set_motor_power(PORT_MOTOR_RIGHT, 100)
    while go:
        go = stillGo()
        left = getDist("L")
        right = getDist("R")
        if (left < minDist or right > maxDist):
            steer("R",left)
        else if(right < minDist or left > maxDist):
            steer("L",right)
        else:
            BP.set_motor_power(PORT_MOTOR_LEFT, 100)
            BP.set_motor_power(PORT_MOTOR_RIGHT, 100)
    sleep(2)
            
def waitForGo():
    wait = True
    while wait:
        if(joystick.get_button(1) == 1):
            wait = False
            
        

#wait for input
while True:
    waitForGo()
    GoRobotGo()
    
