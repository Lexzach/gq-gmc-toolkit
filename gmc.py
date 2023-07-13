import serial
import time
import os
import sys
import argparse
import tabulate
from datetime import datetime

# Read 2 byte value from serial
def read_2byte_value(ser):
    msb = ser.read(1)
    lsb = ser.read(1)
    return int.from_bytes(msb + lsb, byteorder='big')

def key_handler(e):
    if e.name == 'left':
        ser.write(b"<KEY0>>")
    elif e.name == 'up':
        ser.write(b"<KEY1>>")
    elif e.name == 'down':
        ser.write(b"<KEY2>>")
    elif e.name == 'enter':
        ser.write(b"<KEY3>>")

def read_temperature(ser):
    integer_part = ser.read(1)
    decimal_part = ser.read(1)
    negative_sign = ser.read(1)
    end_byte = ser.read(1)
    temp = int.from_bytes(integer_part, byteorder='big') + int.from_bytes(decimal_part, byteorder='big')/10
    if int.from_bytes(negative_sign, byteorder='big') != 0:
        temp = -temp
    return temp

def set_rtc(ser):
    now = datetime.now()
    year = now.year % 100
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    ser.write(b"<SETDATEYY" + bytes([year]) + b">>")
    time.sleep(1)
    ser.write(b"<SETDATEMM" + bytes([month]) + b">>")
    time.sleep(1)
    ser.write(b"<SETDATEDD" + bytes([day]) + b">>")
    time.sleep(1)
    ser.write(b"<SETTIMEHH" + bytes([hour]) + b">>")
    time.sleep(1)
    ser.write(b"<SETTIMEMM" + bytes([minute]) + b">>")
    time.sleep(1)
    ser.write(b"<SETTIMESS" + bytes([second]) + b">>")
    time.sleep(1)


try:
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)
except Exception as e:
    print(e)
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("--getver", help="Get hardware model and version", action="store_true")
parser.add_argument("--getserial", help="Get hardware model and version", action="store_true")
parser.add_argument("--getcpm", help="Get current CPM value", action="store_true")
parser.add_argument('--control', help='Control the device with keyboard', action='store_true')
parser.add_argument("--heartbeaton", help="Turn on heartbeat", action="store_true")
parser.add_argument("--heartbeatoff", help="Turn off heartbeat", action="store_true")
parser.add_argument("--getvolt", help="Get battery voltage status", action="store_true")
parser.add_argument("--gettemp", help="Get temperature", action="store_true")
parser.add_argument("--poweron", help="Power on the device", action="store_true")
parser.add_argument("--poweroff", help="Power off the device", action="store_true")
parser.add_argument("--reboot", help="Reboot the device", action="store_true")
parser.add_argument("--readconfig", help="Read the config", action="store_true")
parser.add_argument("--setrtc", help="Set the Real Time Clock of the geiger counter with your computer's RTC", action="store_true")
parser.add_argument('--keyback', action='store_true', help='Press the back button')
parser.add_argument('--keyup', action='store_true', help='Press the up button')
parser.add_argument('--keydown', action='store_true', help='Press the down button')
parser.add_argument('--keyenter', action='store_true', help='Press the enter button')


args = parser.parse_args()

if args.getver:
    ser.write(b"<GETVER>>")
    version = ser.read(14)
    print("Version: ", version)

if args.getserial:
    ser.write(b"<GETSERIAL>>")
    serial = ser.read(7)
    serial_hex = serial.hex()
    print(f"Serial Number: {serial_hex}")

if args.getcpm:
    ser.write(b"<GETCPM>>")
    cpm = read_2byte_value(ser)
    print("CPM: ", cpm)

if args.control:
    print("Control mode enabled. Use the arrow keys and 'enter' to interact with the device.")
    print("Press Ctrl+C to exit.")
    keyboard.on_press(key_handler, suppress=False)

if args.heartbeaton:
    ser.write(b"<HEARTBEAT1>>")
    heartbeat = read_2byte_value(ser)
    print("Heartbeat: ", heartbeat)

if args.heartbeatoff:
    ser.write(b"<HEARTBEAT0>>")

if args.getvolt:
    ser.write(b"<GETVOLT>>")
    voltage = int.from_bytes(ser.read(1), byteorder='big')
    print("Voltage: ", voltage)

if args.gettemp:
    ser.write(b"<GETTEMP>>")
    temp = read_temperature(ser)
    print("Temperature: ", temp)

if args.poweron:
    ser.write(b"<POWERON>>")

if args.poweroff:
    ser.write(b"<POWEROFF>>")

if args.reboot:
    ser.write(b"<REBOOT>>")

if args.readconfig:
    ser.write(b"<GETCFG>>")
    config = ser.read(256)
    print("Config: ", config)

if args.keyback:
    ser.write(b"<KEY0>>")
    time.sleep(0.5)

if args.keyup:
    ser.write(b"<KEY1>>")
    time.sleep(0.5)

if args.keydown:
    ser.write(b"<KEY2>>")
    time.sleep(0.5)

if args.keyenter:
    ser.write(b"<KEY3>>")
    time.sleep(0.5)

if args.setrtc:
    set_rtc(ser)

ser.close()
