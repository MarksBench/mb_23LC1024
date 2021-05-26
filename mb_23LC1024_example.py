"""
mb_23LC1024_example.py

Example MicroPython script for Microchip 23LC1024 SPI SRAM with RP2040 (Raspberry Pi Pico)

Author: mark@marksbench.com

Version: 0.1, 2021-05-07

**NOTE: There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

To use:
- Upload the mb_23LC1024.py file to your board (the same location where your MicroPython scripts
  run from, or the /lib folder if applicable).
- Connect the 23LC1024 to the Pi Pico (RP2040), for testing (and to use this example script
  without modification) I suggest the following:
  
      23LC1024   |    Pi Pico
        1(/CS)   |    GP1 (Pin 2)
        2(SO)    | GP4, (SPI0 RX, Pin 6)
        4(Vss)   |    GND, (Pin 38)
        5(SI)    | GP7, (SPI0 TX, Pin 10)
        6(SCK)   | GP6, (SPI0 SCK, Pin 9)
        7(/HOLD) |   3V3 OUT, (Pin 36)
        8(Vcc)   |   3V3 OUT, (Pin 36)

- To write a value: memory.write_byte(address, value)
- To read a value: value = memory.read_byte(address)
- You should get an error if the address or value is out of range.

"""

from machine import Pin, SPI
import mb_23LC1024

# Set up SPI with the pinout arrangement listed above
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), polarity=0, phase=0)

# Set a GP pin to use for /CS
cs = 1

# Create constructor to use driver
memory = mb_23LC1024.mb_23LC1024(spi, cs)


# Simple write test. Writing value of 38 to address 131071 (highest address of the 23LC1024)
memory.write_byte(131071, 38)

# Write value 255 to address 0 (lowest address of the 23LC1024)
memory.write_byte(0, 255)

# Simple read test. Read the value from address 131071 and print it
read_value = memory.read_byte(131071)
print("Retrieved: ", read_value)

# Now read from address 0 and print it
read_value = memory.read_byte(0)
print("Retrieved: ", read_value)

# That's all there is to it
