# WS0010-Software-SPI
This Library allows the communication, via Python 3, between a Raspberry Pi and a 16x2 OLED-Display.
The OLED-Display needs 10-Bit Data to work in SPI but the SPI module from the Raspberry Pi only sends 8-Bit Data,
which in return makes the Python Software SPI necessary to send the required 10-Bit Data.

### How to install
Use these following steps and the library can already be used without any bigger problems.

```
  > sudo apt-get update
  > sudo apt-get install python3-pip python3-dev python3-rpi.gpio git -y
  > pip3 install --upgrade pip
  > sudo pip3 install bitstring
  > git clone https://github.com/joy-it/WS0010-Software-SPI.git
  > cd WS0010-Software-SPI/
```

### How to use the library and all of its functions
The Library just needs to be imported at the beginning of the code, like it is shown in [Test.py](./Test.py), and it will be fully usable afterwards.

As callable functions we have: 
- `WS0010SoftwareSPI.init(CLK, MOSI, CS)` These can be any Pin that can be specified if more than 1 display is in use (is already pre-specified for the use of 1 display)

- `WS0010SoftwareSPI.SendText("Text goes here", display positin 1-16, row of the Display 0/1)` Allows the User to send any kind of text at the specified location

- `WS0010SoftwareSPI.DisplayShiftL(the amount for the shift to the Left can be specified)` Shifts the display by the specified amount to the **Left**

- `WS0010SoftwareSPI.DisplayShiftR(the amount for the shift to the Right can be specified)` Shifts the display by the specified amount to the **Right**

- `WS0010SoftwareSPI.Clear()` Clears all Displayed contents on the Display

- `WS0010SoftwareSPI.DisplayStop()` Turns off the Display but changes nothing on the send Data

The **SendText** function works better if it has a small delay, inbetween calls of itself if it is called twice or more in a row, of 0.01 to 0.1 seconds.
To ensure that no artifacts, random symbols or random text, are created after each function call it is adviced to set a minimum Delay of atleast 0.1 seconds after every single function call.

For any further questions please refer to the [Manuals](./Manuals)
