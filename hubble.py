#Hubble code
#Assume we start facing no colours
#Order is Red, Blue, Yellow and, finally, Green.

#call first colour we see "North"

from time import sleep
import brickpi3
import pygame
from picamera import PiCamera
from scipy import misc
from PIL import Image

#Table:
#0 -> Red
#1 -> Green
#2 -> Blue
#3 -> Yellow
#4 -> Background


#from picamera import PiCamera
from time import sleep
from scipy import misc
from PIL import Image

camera = PiCamera()
path = '/home/pi/Desktop/image.jpg'

def Test():    
    camera.start_preview()
    sleep(10)
    camera.stop_preview()

def Get_Max_Pixel(pixel):
    #Iterate through the array to get index of largest value
    ind = 0
    maxVal = 0
    for z in range(0,3):
        if pixel[z] > maxVal:
            maxVal = pixel[z]
            ind = z
    return ind

def normalising(pixel):
    val = pixel[Get_Max_Pixel(pixel)]/255
    pixel[0] = pixel[0]/val
    pixel[1] = pixel[1]/val
    pixel[2] = pixel[2]/val
    return pixel

def Capture(path, delay):
    camera.start_preview()
    sleep(delay)
    camera.capture(path)
    camera.stop_preview()

def getPixelColour(R,G,B):
    #3 bools in
    if(R & (False==G) & (False==B)):
        return 0
    if((False==R) & G & (False==B)):
        return 1
    if((False==R) & (False==G) & B):
        return 2
    if(R & G & (False==B)):
        return 3

    #if no colour found, return "Background"
    return 4
    

def PixelToColour(pixel):
    #Map 0->255 between false or true
    R = (False,True)[pixel[0] > 127]
    G = (False,True)[pixel[1] > 127]
    B = (False,True)[pixel[2] > 127]
    #Use logic of "Has"
    return getPixelColour(R,G,B)
    #returns index of colour to incriment
    #in result array
    
def Get_Max(Array):
    #Iterate through the array to get index of largest value
    ind = 0
    maxVal = 0
    for z in range(0,5):
        if Array[z][0] > maxVal:
            maxVal = Array[z][0]
            ind = z
    return ind
    

def Analyse(path,size):
    #load photo
    arr = misc.imread(path) # 2592x1944
    im = Image.open(path)
    picX, picY = im.size
    #define AOI (Area of interest)
    aoiX = (picX/2)-(size/2)
    aoiY = (picY/2)-(size/2)
    ansArray = [[0,"Red"],[0,"Green"],[0,"Blue"],[0,"Yellow"],[0,"Background"]]
    #Iterate through AOI
    for x in range(int(aoiX), int(aoiX+size)):
        for y in range(int(aoiY), int(aoiY+size)):
            #Break down each pixel with "Has" method
            arr[x,y] = normalising(arr[x,y])
            ansArray[PixelToColour(arr[x,y])][0]+= 1
    #Iterate through each colour to find majority
    #Return majority
    return ansArray[(Get_Max(ansArray))][1]
    


def camColour(path, delay, aoi):
    Capture(path, delay)
    return(Analyse(path,aoi))
    





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
    colour = camColour("/home/pi/image.jpg",2,10)
    posArray[int(bearing/90)] = colour
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
    getColour(-45)
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
