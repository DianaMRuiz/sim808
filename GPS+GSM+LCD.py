#! /usr/bin/python
import time,sys, glob,serial, binascii, os
from luma.core.virtual import terminal
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def display():
    inter = i2c()
    device = sh1106(serial_interface=inter)
    for fontname, size in [("pixelmix.ttf", 16)]:
        font = make_font(fontname, size) if fontname else None
        term = terminal(device, font)
        term.animate = False

        #term.println("GPS")
        #term.animate = True
        term.println("\r\nLon {}\r\nLat {}".format(float(lon),float(lat)))
        #term.puts("\rLat {}".format(float(lat)))
        time.sleep(1)
        #term.flush()

def sendSMS(ser,lon, lat):
    ser.write('AT+CMGS="+573214988051"\r')
    time.sleep(1)
    data= "Wirird Lab Report Lon:{} Lat:{}".format(lat,lon)
    ser.write('{}\r'.format(data))
    print("write Message")
    time.sleep(0.5)
    ser.write(chr(26))
    print ("message Sent")
    rcv = ser.read(100)
    print (rcv)

def readAT(res):
    buffer= str()
    while True:
        aByte = res.readline()
        if aByte == b'OK\r\n':
            buffer += aByte.decode("ascii")
            return buffer
        else :
            buffer += aByte.decode("ascii")

if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=5)
    time.sleep(1)
    try:
        while(True):
            ser.write(b'AT\r\n')
            print(readAT(ser))
            ser.write(b'AT+CMGF=1\r\n')
            print(readAT(ser))
            ser.write(b'AT+CGNSPWR=1\r\n')
            print(readAT(ser))
            ser.write(b'AT+CGNSINF\r\n')
            #gps = ser.read(100).decode('utf-8')
            #print(gps)
            gps=readAT(ser)
            print(gps)
            gps = gps.split(",")
            print(gps)
            lon = gps[3]
            lon = "{0:.5f}".format(float(lon))
            lat = gps[4]
            lat = "{0:.5f}".format(float(lat))
            print ("La Longitud es: " + lon)
            print ("La Latitud es:" + lat)
            sendSMS(ser,lat,lon)
            display()
            time.sleep(10.0)
        
    except KeyboardInterrupt:
        ser.close()
        print("bye")
        exit()
    
