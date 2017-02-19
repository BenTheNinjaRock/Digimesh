#! /usr/bin/python

#import and init an XBee device
from xbee import XBee
import serial
import array
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Use an XBee 802.15.4 device
xbee = XBee(ser)

#xbee.tx_long_addr(dest_addr=b'\x13\xA2\x00\x41\x54\x53\xBC\xFE')
a=b'\x10'
b=b'\x01'
c=b'\x00\x13\xA2\x00\x41\x54\x53\xD0'
d=b'\x00'
t1='t1'
t2='55'
t3='t3'
t4='t4'
tt= t1 + t2 + t3 + t4
e= bytearray()
e.extend(map(ord, tt))


xbee.tx_long_addr(id=a, frame_id=b, dest_addr=c, options=d, data=e)
response = xbee.wait_read_frame()
print(response['status'])
