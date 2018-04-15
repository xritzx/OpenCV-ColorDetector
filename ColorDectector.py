import bluetooth as bt #make sure to install pybluez 
import cv2 
import time
import urllib.request as urllib
import numpy as np
import sys

host="192.168.0.101:8080"  # Manually set the IP or make a default IP

if(len(sys.argv)>1):     
    host=sys.argv[1]   # Get the IP streamer from system arguments
    print("Given IP Address of video streamer is: ",host)

url="http://"+host+"/shot.jpg"
sock=bt.BluetoothSocket(bt.RFCOMM)  # Create a socket which uses RFCOMM protocol



def get_stream(url):
    '''
     Get the frame at that instant
    '''
    stream=urllib.urlopen(url)  # Get the response from the url
    imgAr=np.array(bytearray(stream.read()),dtype=np.uint8) # Create byte stream from response object
    img=cv2.imdecode(imgAr,-1) 
    return(img)

def get_color(img,pixel_width):
    '''
    Getting the color average from the centre of the frame
    '''
    shape=img.shape[:2]
    x,y=((shape[0]//2)-pixel_width//2),((shape[1]//2)-pixel_width//2)
    blue,green,red=0,0,0
    div=(pixel_width*pixel_width)

    for i in range(pixel_width):
        for j in range(pixel_width):
            blue+=img[y+i][x+j][0]
            green+=img[y+i][x+j][1]
            red+=img[y+i][x+j][2]

    return([red//div,green//div,blue//div])

def sendcolor(col):
    st=''
    for i in col:
        st+=(str(i)+',')
    sock.send(st[:-1])

def bluesock():
    print("Searching bluetooth devices")
    near=bt.discover_devices()
    for dev in range(len(near)):
        print("Device {} is {}".format(dev+1,bt.lookup_name(near[dev])))
    sel=int(input(">"))-1
    print("You have selected: ",bt.lookup_name(near[sel]))
    bt_add=near[sel]
    port=1
    sock.connect((bt_add,port))

bluesock()  # Connecting the bluetooth

while(True):
    try:
        time.sleep(0.2)
        stream=get_stream(url)
        col=get_color(stream,50)
        cv2.imshow('IpCAM',stream)
        print(col)
        sendcolor(col)
        if(cv2.waitKey(1) & 0xFF==ord('q')):
            sock.close
            break
    except:
        print("Connection Closed !")
        break
    
cv2.destroyAllWindows()
