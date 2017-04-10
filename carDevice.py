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
    #If radio receives update
    if frameType == '0':
        #data = 0 TT CC TT:TT:TT
        test = data[1].decode('utf-8')
        car = data[2].decode('utf-8')
        time = data[3].decode('utf-8')
        fieldnames = ['Source', 'Test', 'Car', 'Time']
        with open('carDevice.csv', 'a+') as wf:
            fileText = '1 '
            fileWriter = csv.DictWriter(wf, fieldnames = fieldnames)
            fileWriter.writerow({'Source': hexAddress, 'Test': test, 'Car': car, 'Time': time})
            wf.seek(0, 0)
            fileReader = csv.DictReader(wf, fieldnames = fieldnames)
            
            mtuBreaker = 0
            for row in fileReader:
                fileText = fileText + row['Test'] + ':' + row['Car'] + ' '
                #fileArray.append(row['Test'] + ':' + row['Car'])
                mtuBreaker += 1
                #Split into multiple packets if the file is longer than the mtu of 42
                if mtuBreaker == 5:
                    byteVar = bytearray()
                    byteVar.extend(map(ord, fileText))
                    xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF', options=b'\x00', data=byteVar)
                    mtuBreaker = 0
                    fileText = '1 '
            #if a packet of five was not completed, send the remaining
            if mtuBreaker != 0:
                byteVar = bytearray()
                byteVar.extend(map(ord, fileText))
                xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF', options=b'\x00', data=byteVar)

            #print(fileArray)
            #TOO LARGE FOR MTU

    #If car radio advertises test/car combos
    elif frameType == '1':
        testCarRecord = []
        testCarPacket = []
        with open('carDevice.csv', 'r') as wf:
            for line in wf:
                records = line.split(',')
                testCarRecord.append([records[1], records[2]])

            for x in data:
                splitData = x.decode('utf-8')
                if splitData != '1':
                    splitData = splitData.split(':')
                    if splitData not in testCarRecord:
                        dataVar = '2 ' + splitData[0] + ' ' + splitData[1]
                        byteVar = bytearray()
                        byteVar.extend(map(ord, dataVar))
                        xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=address, options=b'\x00', data=byteVar)

    #If radio says "send me this record"
    elif frameType == '2':
        #data = TT CC
        qTest = data[1].decode('utf-8')
        qCar = data[2].decode('utf-8')
        with open('carDevice.csv', 'r') as wf:
            for line in wf:
                records = line.split(',')
                test = records[1]
                car = records[2]
                print(hexAddress)
                if records[1] == qTest and records[2] == qCar:
                    time = records[3]
                    dataVar = '0 ' + test + ' ' + car + ' ' + time
                    byteVar = bytearray()
                    byteVar.extend(map(ord, dataVar))
                    xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=address, options=b'\x00', data=byteVar)
####################finish sending data
