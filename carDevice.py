from binascii import unhexlify
import csv
import sys
from xbee import DigiMesh
from xbee.python2to3 import byteToInt, intToByte
import serial
from binascii import hexlify, unhexlify, a2b_uu
ser = serial.Serial('/dev/ttyUSB0', 9600)

xbee = DigiMesh(ser)

while True:
    hexAddress = ""
    x = xbee.wait_read_frame()
    #if a tx packet and not tx_status
    try:
        address = x['source_addr']
    except KeyError:
        continue
    for y in address:
        y = (hex(y))
        hexAddress = hexAddress + y

#    print(x)
    data = x['data']
    data = data.split()
    frameType = data[0].decode('utf-8')
    if frameType == '0':
        #data = 0 TT CC TT:TT:TT
        test = data[1].decode('utf-8')
        car = data[2].decode('utf-8')
        time = data[3].decode('utf-8')
        fieldnames = ['Source', 'Test', 'Car', 'Time']
        with open('carDevice.csv', 'a') as wf:
            fileWriter = csv.DictWriter(wf, fieldnames = fieldnames)
            fileWriter.writerow({'Source': address, 'Test': test, 'Car': car, 'Time': time})
    #If radio says "send me this record"
    elif frameType == '1':
#        print(bytearray(hexAddress, 'ascii'))
        #data = TT CC
        qTest = data[1].decode('utf-8')
        qCar = data[2].decode('utf-8')
        with open('carDevice.csv', 'r') as wf:
            for line in wf:
                #records[1] = Test & records[2] = Car
                records = line.split(',')
                test = records[1]
                car = records[2]
#                print(address)
                if records[1] == qTest and records[2] == qCar:
                    time = records[3]
                    dataVar = '0 ' + test + ' ' + car + ' ' + time
                    byteVar = bytearray()
                    byteVar.extend(map(ord, dataVar))
                    xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=address, options=b'\x00', data=byteVar)
####################finish sending data
