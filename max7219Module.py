import time
import numpy as np
from font import baseFont as ft
from constants import *
import RPi.GPIO as GPIO


class Matrix:
    def __init__(self, chipSelectPin, clockPin, dataPin, gpioSetting="board"):
        self.array = np.zeros((8, 32), dtype="int8")

        if gpioSetting.lower() == "bcm":
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)

        self.cs = chipSelectPin
        self.clk = clockPin
        self.din = dataPin

        self.setup()

    def setup(self):
        GPIO.setup(self.cs, GPIO.OUTPUT)
        GPIO.setup(self.clk, GPIO.OUTPUT)
        GPIO.setup(self.din, GPIO.OUTPUT)

        self.powerDown()

        self.sendByte((SHUTDOWN, 0x01) * 4)
        self.sendByte((DECODE, 0x00) * 4)
        self.sendByte((SCANLIM, 0x07) * 4)
        self.sendByte((INTENSITY, 0x00) * 4)
        self.sendByte((TEST, 0x00) * 4)

    def __call__(self):
        arrs = np.hsplit(self.array, 4)
        for i, arr in enumerate(arrs):
            mat = i
            for j, row in enumerate(arr):
                listed = [str(item) for item in list(row)]
                strbin = "".join(listed)
                strbin = "0b{}".format(strbin)
                self.setMatrixRow(matrix=mat, row=j, value=eval(strbin))

    def powerDown(self, how="full"):
        for a in range(1, 9):
            self.sendByte([a, 0x00] * 4)
        if how == "full":
            self.sendByte((SHUTDOWN, 0x00))

    def reset(self):
        self.array = np.zeros((8, 32), dtype="int8")

    def pulse(self, port):  # clk or cs
        GPIO.output(port, True)
        GPIO.output(port, False)

    def byteShifter(self, hex_val):
        for _ in range(8):
            temp = hex_val & 0x80
            if temp == 0x80:
                GPIO.output(self.din, True)
            elif temp == 0x0:
                GPIO.output(self.din, False)
            self.pulse(self.clk)
            hex_val <<= 0x01

    def sendByte(self, data):
        for byte in data:
            self.byteShifter(byte)
        self.pulse(self.cs)

    def setMatrixRow(self, matrix, row, value):
        bundle = (NULL * matrix) + [row + 1, value] + NULL * (3 - matrix)
        self.sendByte(bundle)

    def binarize(self, value):
        v = eval(value)
        v = format(v, "08b")[::-1]
        return list(v)

    def setCol(self, col, value):
        bits = self.binarize(value)
        self.array[:, col] = bits

    def setChar(self, loc, char):
        a = 0
        for i in range(loc, loc + len(ft[char])):
            self.setCol(i, ft[char][a])
            a += 1

    def static(self, message):
        if len(message) > 4:
            mes = message[:4]
        else:
            mes = message
        for idx, letter in enumerate(mes):
            self.setChar(idx * 8, letter)

    def scrolled(self, message, delay=0.1):
        master = []
        message += "   "

        for char in message:
            master.extend(ft[char])

        while True:
            self.array = np.delete(self.array, obj=0, axis=1)  # obj is index
            self.array = np.insert(
                self.array, obj=30, values=self.binarize(master[0]), axis=1
            )
            self()
            time.sleep(delay)
            del master[0]
            if np.all((self.array == 0)):
                break

    def stacked(self, message, delay=0.1, reverse=False):
        charsets = [message[i : i + 4] for i in range(0, len(message), 4)]

        for phrase in charsets:
            self.static(phrase)
            temparr = np.copy(self.array)
            self.array = np.zeros((8, 32), dtype="int8")
            if not reverse:
                for idx, row in enumerate(temparr):
                    self.array[idx] = row
                    self()
                    time.sleep(delay)
            else:
                for idx, row in reversed(list(enumerate(temparr))):
                    self.array[idx] = row
                    self()
                    time.sleep(delay)

    def run_rtc(self):
        timecount = 0
        while True:
            t = time.strftime("%I%M")
            for idx, value in enumerate(t):
                self.setChar(idx * 8, value)
            if timecount % 2 == 0:
                self.setCol(15, "0x24")
            timecount += 1
            self()
            time.sleep(1)
