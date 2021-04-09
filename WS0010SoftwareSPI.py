#!/usr/bin/python

# Import of Librarys
import time
import RPi.GPIO as GPIO
import sys

# -m pip install --upgrade pip
# sudo pip install bitstring
from bitstring import BitArray

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Global Support variables
Command = 0
Text = 1
data = 2

# Pin assignment
CLK = 11     # CLK
MOSI  = 10   # MOSI
CS = 8       # Chip-select

OLED_WIDTH = 16 	  # Number of Characters per line
OLED_LINE_1 = 0x7F 	# First line
OLED_LINE_2 = 0xBF 	# Second line

# CLK function to trigger the clock line
def clock():
    GPIO.output(CLK, GPIO.LOW)
    GPIO.output(CLK, GPIO.HIGH)

# Send function that converts all data into bitarrays and sends them to the OLED display
def Send(mosiPin, csPin, CommandOrText, Data):
    
    GPIO.output(csPin, GPIO.LOW)                       #Chip-Select must be set LOW so that the OLED recognizes what is being sent.
    
    pos = 0
    tempData = 0
    # Conversion of the individual Commands into 10-Bit bitarrays
    if CommandOrText == Command:              #Checking if the type of Data that needs to be sent is a Command
        tempData = BitArray(int=Data, length=10)        #Converting our incoming Data from Hexadecimal to 10-Bit Binary using the BitArray method from bitstring
        tempData[0] = False                             #Setting our first Bit to be False so that the OLED will recognize that we send a Command
        
        
    # Conversion of the individual letters of our Text into 10-Bit bitarrays
    elif CommandOrText == Text:               #Checking if the type of Data that needs to be sent is a Text
        tempData = BitArray(int=Data, length=10)        #Converting our incoming Data from Decimal to 10-Bit Binary using the BitArray method from bitstring
        tempData[0] = True                              #Setting our first Bit to be True so that the OLED will recognize that we send Text
        
    for i in range(10):
        if tempData[pos] == 1:                #Looking in the bit array if it is a 1 at the given position, going position by position,
            GPIO.output(mosiPin, GPIO.HIGH)             #if it is a 1, a 1 will be sent
            clock()
        else:                                           #If it is not a 1, a 0 is detected
            GPIO.output(mosiPin, GPIO.LOW)              #and a 0 will be sent
            clock()
        pos = pos + 1                         #Incrementing the position-counter to tell the for loop to go to the next position
    
    GPIO.output(csPin, GPIO.HIGH)

# Inialization sequence of the OLED display and the required pins on the Raspberry PI
def init(clkPin, mosiPin, csPin):
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)
    GPIO.output(clkPin, GPIO.LOW)
    GPIO.output(csPin, GPIO.HIGH)
    time.sleep(0.5)

    Send(MOSI, CS, Command, 0x3A)    #Function Set = 00|001 DL|N F FT1 FT0
                                     #DL = Set interface data length (0= 4-bit| 1= 8-bit), N = Set number of display lines (0= 1-Line Display| 1= 2-Line Display )
                                     #F = Set Character Font (0= 5x8 dots| 1= 5x10 dots),
                                     #FT1/FT0 = Set Font Table
                                     #(0|0 = English-Japanese Characters)
                                     #(0|1 = Western-European Characters 1)
                                     #(1|0 = English-Russian Characters)
                                     #(1|1 = Western-European Characters 2)
                                     
    Send(MOSI, CS, Command, 0x0F)    #Display ON/OFF Control = 00|0000|1 D C B
                                     #D = Set entire Display (0= off| 1= on), C = Set Cursor (0= off| 1= on), D = Set Blinking of Cursor (0= off| 1= on)
                                     
    Send(MOSI, CS, Command, 0x01)    #Display Clear = 00|0000|0001
    
    Send(MOSI, CS, Command, 0x02)    #Return Home = 00|0000|0010
    
    Send(MOSI, CS, Command, 0x06)    #Entry Mode Set = 00|0000|01 I/D S
                                     #I/D = Set cursor move direction (0= Decrement| 1= Increment), S = Set Display Shift (0= off| 1= on)
                                     
    Send(MOSI, CS, Command, 0x1C)    #Displayshift Right = 00|0001|S/C R/L 00
    Send(MOSI, CS, Command, 0x18)    #Displayshift Left = 00|0001|S/C R/L 00
                                     #S/C = Set Shift, R/L = Set direction for shift (0= Shift to the Left| 1= Shift to the Right)
                                     #(0|0 = Shift cursor position to the Left)
                                     #(0|1 = Shift cursor position to the Right)
                                     #(1|0 = Shifts entire display to the Left, cursor follow along)
                                     #(1|1 = Shift entire display to the Right, cursor follows along)

# Conversion of the individual letters, into 10-Bit bitarrays, of our text that is to be Send
def SendText(data, displayPosition, Row):
    DisplayPosition(displayPosition, Row)
    count = 0
    CharacterList = " ".join(format(ord(x), 'd') for x in data)   #Conversion of each individual letter in our Text to decimals
    CharacterList = CharacterList.split(" ", 16)                  #Spliting the List at the " " to get all individual Decimals for every letter in our Text
    
    for count in range(len(CharacterList)):
        Send(MOSI, CS, Text, int(CharacterList[count]))           #Passing each Decimal individualy to the Send function
    
# Movement of the display in the desired direction by the amount that the User specified
def DisplayShiftL(shiftLeft):
    for shift in range(shiftLeft):
        time.sleep(0.05)
        Send(MOSI, CS, Command, 0x18)

def DisplayShiftR(shiftRight):
    for shift in range(shiftRight):
        time.sleep(0.05)
        Send(MOSI, CS, Command, 0x1C)
    
# Deletion of the entire displayed content on the OLED
def Clear():
    Send(MOSI, CS, Command, 0x01)
    Send(MOSI, CS, Command, 0x02)
    
# Function for direct control of each individual display position
def DisplayPosition(displayPosition, Row):
    if Row == 0:                                          #Selection of the first line
        displayPosition = OLED_LINE_1 ++ displayPosition  #Setting the Cursor to the, by the User specified, position on the first line
        Send(MOSI, CS, Command, displayPosition)

    elif Row == 1:                                        #Selection of the second line
        displayPosition = OLED_LINE_2 ++ displayPosition  #Setting the Cursor to the, by the User specified, position on the second line
        Send(MOSI, CS, Command, displayPosition)
        
# Turns the display on the OLED off
def DisplayStop():
    Send(MOSI, CS, Command, 0x08)