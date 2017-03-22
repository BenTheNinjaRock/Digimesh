from binascii import unhexlify
import csv
import sys
from xbee import XBee
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

xbee = XBee(ser)

#while True:
x = xbee.wait_read_frame()
print(x)

#    #if tx_update frame
#    if x.id == b'\x90':
#        fieldnames = ['Test', 'Car', 'Time']
#        with open('carScores.csv', 'a') as wf:
#            fileWriter = csv.DictWriter(wf, fieldnames = fieldnmes)
#            fileWriter.writerow({'Timestamp': 
#
#    #if tx_checksum_send frame
#    elif x.id == b'\x11':
#
#    #
#    elif x.id == b'\x12':
