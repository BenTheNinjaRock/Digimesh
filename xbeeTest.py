#! /usr/bin/python

#import and init an XBee device
from xbee import XBee
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Use an XBee 802.15.4 device
xbee = XBee(ser)
# To use with an XBee ZigBee device, replace with:
# xbee = ZigBee(ser)

#xbee.tx_long_addr(dest_addr=b'\x13\xA2\x00\x41\x54\x53\xBC\xFE')
xbee.tx_long_addr(id=b'\x10', frame_id=b'\x01', dest_addr=b'\x00\x13\xA2\x00\x41\x54\x53\xD0', options=b'\x00', data=b'Hello World')
response = xbee.wait_read_frame()
#0013A200415453D0
#xbee.send('at', frame_id=b'A', command=b'DA')
#xbee.sendStr("Hello World")


# Set remote DIO pin 2 to low (mode 4)
#xbee.remote_at(
#    dest_addr=b'\x56\x78',
#    command=b'D2',
#    parameter=b'\x04')

#xbee.remote_at(
#    dest_addr=b'\x56\x78',
#    command=b'WR')
