import WS0010SoftwareSPI
import time
import RPi.GPIO as GPIO
import sys

Command = 0
Text = 1

CLK = 11
MOSI = 10
CS = 8

if __name__ == '__main__':
    try:
        WS0010SoftwareSPI.init(CLK, MOSI, CS)
        time.sleep(0.5)
        temp = 0
        while True:
            if temp < 10:
                WS0010SoftwareSPI.SendText("Bitbanged SPI by", 1, 0)
                time.sleep(0.01)
                WS0010SoftwareSPI.SendText("Joy-IT on WS0010", 1, 1)
                WS0010SoftwareSPI.DisplayShiftL(8)
                time.sleep(0.1)
                WS0010SoftwareSPI.DisplayShiftR(8)
                time.sleep(1)
                WS0010SoftwareSPI.SendText("by SPI", 11, 0)
                time.sleep(0.01)
                WS0010SoftwareSPI.SendText("WS0010", 1, 1)
                WS0010SoftwareSPI.SendText("Joy-IT", 11, 1)
                time.sleep(1)
                WS0010SoftwareSPI.Clear()
                time.sleep(1)
                temp = temp + 1

    except KeyboardInterrupt:
        WS0010SoftwareSPI.Clear()
        WS0010SoftwareSPI.DisplayStop()
        GPIO.cleanup()
        sys.exit(0)

