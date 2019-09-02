#! /usr/bin/python3
import time
import sys
import glob
import serial
import binascii

import os
from luma.core.virtual import terminal
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    while True:
        for fontname, size in [("pixelmix.ttf", 16)]:
            font = make_font(fontname, size) if fontname else None
            font_slider = make_font(fontname, 14)
            font_rssi = make_font(fontname, 15)
            term = terminal(device, font)
            term.font = font_rssi
            term.animate = False
            while True:
                #term.println("GPS")
                #term.animate = True
                term.println("\r\nLon {}\r\nLat {}".format(float(lon),float(lat)))
#		term.puts("\rLat {}".format(float(lat)))
                time.sleep(1)
                #term.flush()
        exit()

if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
    time.sleep(1)
try:
    ser.write(b'AT\r\n')
    time.sleep(2)
    ser.write(b'AT\r\n')
    time.sleep(2)
    ser.write(b'AT+CGNSPWR=1\r\n')
    time.sleep(2)
    ser.write(b'AT+CGNSINF\r\n')
    gps = ser.read(100).decode('utf-8')
    time.sleep(2)
    gps = gps.split(",")
    lon = gps[-2]
    lon = "{0:.2f}".format(float(lon))
    lat = gps[-1]
    lat = "{0:.2f}".format(float(lat))
    print ("La Longitud es: " + lon)
    print ("La Latitud es:" + lat)

    inter = i2c()
    device = sh1106(serial_interface=inter)
    main()
finally:
    ser.close()
