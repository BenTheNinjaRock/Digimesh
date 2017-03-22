import tkinter
from tkinter import ttk
from tkinter import *

from binascii import unhexlify
import csv
import sys
import time

from xbee import DigiMesh
import serial


def main():
    try:
        root = tkinter.Tk()
    except:
        sys.exit()
    numpad = NumPad(root)
    root.attributes("-fullscreen", True)
    root.mainloop()    
    
btn_list = [
'7',  '8',  '9',
'4',  '5',  '6',
'1',  '2',  '3',
'Back', '0', 'Enter']

state = 0
labelVar = 0
testNum = carNum = carTime = ''

ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = DigiMesh(ser)


class NumPad(ttk.Frame):
    global labelVar
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.grid()
        self.labelCreate()
        self.entryBoxCreate()
        self.numpadCreate()

    def labelCreate(self, **options):
        global labelVar
        labelVar = StringVar()
        s = ttk.Style()
        s.configure('my.TLabel', font=('Helvetica', 15))
        self.l=ttk.Label(self, textvariable=labelVar, style='my.TLabel', **options)
        self.l.grid(row=0,column=0, columnspan=3)
        labelVar.set('Enter the test number:')

    def entryBoxCreate(self, **options):
        self.e = ttk.Entry(self, text="variable", width=10, font=('Helvetica', 14), **options)
        self.e.config(justify="right")
        self.e.insert(0, '00')
        self.e.grid(row=1,column=1)

    def cmd(self, b):
        global state, labelVar, testNum, carNum, carTime
        #m1 = m2 = c1= s1 = s2 = c2 = ms1 = ms2 = ''
        #test = car1 = car2 = ''
        current = self.e.get()
        if state == 0:
            try:
                test = int(b)
            except ValueError:
                if b == 'Back':
                    car1, car2 = current
                    car2 = car1
                    car1 = '0'
                    current = car1 + car2
                    self.e.delete(0, 2)
                    self.e.insert(0, current)
                else: # Change state to 1, insert car number patten to entry
                    testNum = current
                    state = 1
                    self.e.delete(0, 2)
                    self.e.insert(0, '00')
                    labelVar.set('Please enter the car number')
            else:
                car1, car2 = current
                car1 = car2
                car2 = b
                current = car1 + car2
                self.e.delete(0, 2)
                self.e.insert(0, current)

        elif  state == 1:
            try:
                test = int(b)
            except ValueError:
                if b == 'Back':
                    car1, car2 = current
                    car2 = car1
                    car1 = '0'
                    current = car1 + car2
                    self.e.delete(0, 2)
                    self.e.insert(0, current)
                else: # Change state to 2, insert time pattern to entry
                    carNum = current
                    state = 2
                    self.e.delete(0, 2)
                    self.e.insert(0, '00:00:00')
                    labelVar.set('Please enter the car time')
            else:
                car1, car2 = str(current)
                car1 = car2
                car2 = b
                current = car1 + car2
                self.e.delete(0, 2)
                self.e.insert(0, current)

        elif state == 2:
            try:
                test = int(b)
            except ValueError:
                if b == 'Back':
                    m1, m2, c1, s1, s2, c2, ms1, ms2 = current
                    ms2 = ms1
                    ms1 = s2
                    s2 = s1
                    s1 = m2
                    m2 = m1
                    m1 = '0'
                    current = m1 + m2 + c1 + s1 + s2 + c2 + ms1 + ms2
                    self.e.delete(0, 8)
                    self.e.insert(0, current)
                else: # send data to digimesh using car1 car2 and entry.get, change state to 0
                    #prepare and send over digimesh
                    state = 1
                    c = None
                    carTime = current
                    self.e.delete(0, 8)
                    self.e.insert(0, '00')
                    labelVar.set('Please enter the car number')
#                    print(testNum)
                    dataVar = testNum + ',' + carNum + ',' + carTime
#                    print(dataVar)
                    byteVar = bytearray()
                    byteVar.extend(map(ord, dataVar))
                    print(byteVar)
                    with open('addresses.csv', 'r') as rf:
                        reader = csv.DictReader(rf, dialect='excel-tab')
                        for row in reader:
                            if row['Car'] == carNum:
#                                print(row['Car'], row['Address'])
                                c=unhexlify(row['Address'])
                    if c != None:
                        xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=c, options=b'\x00', data=byteVar)
                        response = xbee.wait_read_frame()
#                        print(response['status'])
                        if response['status'] != b'\x00':
                            print(c)
                            xbee.tx(dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF', data=byteVar)
                    else:
                        if not c:
                            print('blah')
                        xbee.tx(id=b'\x10', frame_id=b'\x01', dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF', options=b'\x00', data=byteVar)

                    fieldnames = ['Timestamp', 'Test', 'Car', 'Time']
                    with open('scores.csv', 'a') as wf:
                        fileWriter = csv.DictWriter(wf, fieldnames = fieldnames)
                        fileWriter.writerow({'Timestamp': time.asctime(time.localtime(time.time())),'Test': testNum, 'Car' : carNum, 'Time' : carTime})
                                
            else:
                m1, m2, c1, s1, s2, c2, ms1, ms2 = current
                m1 = m2
                m2 = s1
                s1 = s2
                s2 = ms1
                ms1 = ms2
                ms2 = b
                current = m1 + m2 + c1 + s1 + s2 + c2 + ms1 + ms2
#                print(current)
                self.e.delete(0, 8)
                self.e.insert(0, current)

    def numpadCreate(self):
        r = 2
        c = 0
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 20))
        for b in btn_list:
            self.b= ttk.Button(self, text=b, width=5, style='my.TButton', command=lambda b=b : self.cmd(b))
            self.b.grid(row=r,column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1
main()
