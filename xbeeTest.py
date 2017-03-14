#! /usr/bin/python

#import and init an XBee device
from xbee import XBee
from binascii import unhexlify
import csv
import serial
import array
ser = serial.Serial('/dev/ttyUSB0', 9600)
c=0
# Use an XBee 802.15.4 device
xbee = XBee(ser)
with open('addresses.csv', 'r') as f:
    reader = csv.DictReader(f, dialect='excel-tab')
    for row in reader:
        if row['Car'] == '41':
            print(row['Car'], row['Address'])
            c=unhexlify(row['Address'])
#xbee.tx_long_addr(dest_addr=b'\x13\xA2\x00\x41\x54\x53\xBC\xFE')
a=b'\x10'
b=b'\x01'
#c=b'\x00\x13\xA2\x00\x41\x54\x53\xD0'
c=b'\x00\x00\x00\x00\x00\x00\xFF\xFF'
d=b'\x00'
t1='t1'
t2='55'
t3='t3'
t4='t4'
tt= t1 + t2 + t3 + t4
e= bytearray()
e.extend(map(ord, tt))
print(c)
print(e)

xbee.tx_long_addr(id=b'\x10', frame_id=b, dest_addr=c, radius=b'\x01', options=d, data=e)
#response = xbee.wait_read_frame()
#print(chr(response['status']))
#if response != '\x00':
#    print('error')
