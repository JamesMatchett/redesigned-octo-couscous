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

#camera = PiCamera()
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
    


def Get_Colour(path, delay):
    #Capture(path, delay)
    print(Analyse(path,10))


Get_Colour("/Users/jamesm@kainos.com/Downloads/red.png",2)
Get_Colour("/Users/jamesm@kainos.com/Downloads/green.png",2)
Get_Colour("/Users/jamesm@kainos.com/Downloads/blue.png",2)
Get_Colour("/Users/jamesm@kainos.com/Downloads/yellow.png",2)
Get_Colour("/Users/jamesm@kainos.com/Downloads/gray.png",2)
    


