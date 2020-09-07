import time
import numpy as np
from font import baseFont as ft
import RPi.GPIO as io

DECODE = 0x09
INTENSITY = 0x0A
SCANLIM = 0x0B
SHUTDOWN = 0x0C
TEST = 0x0F

NULL = [0x00, 0x00]


class Matrix:
    def __init__(self, chip_select_pin, clock_pin, data_pin, gpio_setting="board"):
        self.array = np.zeros((8, 32), dtype="int8")

        if gpio_setting.lower() == "bcm":
            io.setmode(io.BCM)
        else:
            io.setmode(io.BOARD)

        self.cs = chip_select_pin
        self.clk = clock_pin
        self.din = data_pin

        self.__setup()

    def __call__(self):
        arrs = np.hsplit(self.array, 4)
        for i, arr in enumerate(arrs):
            for j, row in enumerate(arr):
                self._set_matrix_row(matrix=i, row=j, value=self.__to_int(row))

    def power_down(self, how="full"):
        for a in range(1, 9):
            self.__send_byte([a, 0x00] * 4)
        if how == "full":
            self.__send_byte((SHUTDOWN, 0x00))

    def reset(self):
        self.array = np.zeros((8, 32), dtype="int8")

    def set_col(self, col, value):
        bits = self.__to_byte(value)
        self.array[:, col] = bits

    def set_char(self, loc, char):
        a = 0
        for i in range(loc, loc + len(ft[char])):
            self.set_col(i, ft[char][a])
            a += 1

    def static(self, message):
        if len(message) > 4:
            mes = message[:4]
        else:
            mes = message
        for idx, letter in enumerate(mes):
            self.set_char(idx * 8, letter)

    def scrolled(self, message, delay=0.1):
        message += "   "

        for letter in message:
            for byte in ft[letter]:
                self.array = np.delete(self.array, obj=0, axis=1)  # obj is index
                self.array = np.insert(
                    self.array, obj=30, values=self.__to_byte(byte), axis=1
                )
                self()
                time.sleep(delay)

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
        colon = ["0x24", "0x00"]
        while True:
            t = time.strftime("%I%M")
            for idx, value in enumerate(t):
                self.set_char(idx * 8, value)
            self.set_col(15, colon[timecount])

            timecount ^= 1
            self()
            time.sleep(1)

    ### STATIC/HELPER METHODS ###

    # PROTECTED
    def _set_matrix_row(self, matrix, row, value):
        bundle = (NULL * matrix) + [row + 1, value] + NULL * (3 - matrix)
        self.__send_byte(bundle)

    # PRIVATE
    def __setup(self):
        io.setup(self.cs, io.OUT)
        io.setup(self.clk, io.OUT)
        io.setup(self.din, io.OUT)

        self.power_down()

        self.__send_byte((SHUTDOWN, 0x01) * 4)
        self.__send_byte((DECODE, 0x00) * 4)
        self.__send_byte((SCANLIM, 0x07) * 4)
        self.__send_byte((INTENSITY, 0x00) * 4)
        self.__send_byte((TEST, 0x00) * 4)

    def __byte_shifter(self, hexVal):
        for _ in range(8):
            temp = hexVal & 0x80
            if temp == 0x80:
                io.output(self.din, True)
            elif temp == 0x0:
                io.output(self.din, False)
            self.__pulse(self.clk)
            hexVal <<= 0x01

    def __send_byte(self, data):
        for byte in data:
            self.__byte_shifter(byte)
        self.__pulse(self.cs)

    @staticmethod
    def __pulse(port):  # clk or cs
        io.output(port, True)
        io.output(port, False)

    @staticmethod
    def __to_int(values: list):
        powers = [128, 64, 32, 16, 8, 4, 2, 1]
        integer = 0
        for i in range(len(powers)):
            integer += powers[i] * values[i]
        return integer

    @staticmethod
    def __to_byte(value):
        if "b" in value:
            v = int(value, base=2)
        elif "x" in value:
            v = int(value, base=16)
        else:
            v = int(value)

        v = format(v, "08b")[::-1]
        return list(v)
