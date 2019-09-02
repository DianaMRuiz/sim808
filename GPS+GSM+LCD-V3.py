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
        term.println("\r\n {}\r\n {}".format(float(lon),float(lat)))
        time.sleep(1)

def displayErrorGsm():
    inter = i2c()
    device = sh1106(serial_interface=inter)
    for fontname, size in [("pixelmix.ttf", 16)]:
        font = make_font(fontname, size) if fontname else None
        term = terminal(device, font)
        term.animate = False
        term.println("No conecta\r\na red GSM")
        time.sleep(1)

def displayErrorGps():
    inter = i2c()
    device = sh1106(serial_interface=inter)
    for fontname, size in [("pixelmix.ttf", 16)]:
        font = make_font(fontname, size) if fontname else None
        term = terminal(device, font)
        term.animate = False
        term.println("No conecta\r\na red GPS")
        time.sleep(1)
            
def sendSMS(ser,lon, lat):
    ser.write('AT+CMGS="+573216342671"\r')
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
            ser.write(b'AT+CGNSPWR=1\r\n')
            print(readAT(ser))
            ser.write(b'AT+CREG?\r\n')
            gsm=readAT(ser)
            gsm = gsm.split(",")
            gsm=gsm[1]
            gsm = gsm.split("\r\n")
            gsm=gsm[0]
            ser.write(b'AT+CGNSINF\r\n')
            gps=readAT(ser)
            print(gps)
            gps = gps.split(",")
            print(gps)
            statusgps = gps[1]
            if gsm=="1" and statusgps=="1":
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
                lon = "{0:.6f}".format(float(lon))
                lat = gps[4]
                lat = "{0:.6f}".format(float(lat))
                print ("La Longitud es: " + lon)
                print ("La Latitud es:" + lat)
                sendSMS(ser,lat,lon)
                display()
                time.sleep(10.0)
            elif statusgps!="1":
                print("Aun no se ha conectado a GPS")
                time.sleep(7)
                displayErrorGps()
            else:
                print("Aun no se ha conectado a GSM")
                time.sleep(7)
                displayErrorGsm()
        
    except KeyboardInterrupt:
        ser.close()
        print("bye")
        exit()
    
