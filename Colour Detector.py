#Table:
#0 -> Red
#1 -> Green
#2 -> Blue
#3 -> Yellow
#4 -> Background


from picamera import PiCamera
from time import sleep
from scipy import misc

camera = PiCamera()
path = '/home/pi/Desktop/image.jpg'

def Test():    
    camera.start_preview()
    sleep(10)
    camera.stop_preview()

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
        if Array[z,0] > maxVal:
            maxVal = Array[z,0]
            ind = z
    return ind
    

def Analyse(path,size):
    #load photo
    arr = misc.imread(path) # 2592x1944
    picX = 2592
    picY = 1944
    #define AOI (Area of interest)
    aoiX = (picX/2)-(size/2)
    aoiY = (picY/2)-(size/2)
    ansArray = [[0,"Red"],[0,"Green"],[0,"Blue"],[0,"Yellow"],[0,"Background"]]
    #Iterate through AOI
    for x in range(aoiX, aoiX+size):
        for y in range(aoiY, aoiY+size):
            #Break down each pixel with "Has" method
            ansArray[PixelToColour(arr[x,y]),0]+= 1
    #Iterate through each colour to find majority
    #Return majority
    return ansArray[(Get_Max(ansArray)),1]
    


def Get_Colour(path, delay):
    Capture(path, delay)
    print(Analyse(path,100))

while True:
    Get_Colour(path,3)
    sleep(3)
    
    



