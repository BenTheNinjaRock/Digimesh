from binascii import unhexlify
import csv
import sys
from xbee import DigiMesh
from xbee.python2to3 import byteToInt, intToByte
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

xbee = DigiMesh(ser)

while True:
    x = xbee.wait_read_frame()
    for y in x:
        
    x = x.decode('utf-8')
    dict = {'Address', 'Test', 'Car', 'Time'}
    data = x['data'].split(',')
    dict['Address'] = x['source_addr']
    dict['Test'] = x[data][2:4]
    dict['Car'] = x[data][1]
    dict['Time'] = x[data][2]
    if intToByte(x['data'][0][0]) == b'0':
        print('blah')
        
        with open('carDevice.csv', 'a') as wf:
            fileWriter = csv.DictWriter(wf, fieldnames = fieldnames)




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
