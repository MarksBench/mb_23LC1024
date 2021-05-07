"""
mb_23LC1024.py

Micropython module/driver for Microchip 23LC1024 SPI SRAM with RP2040

Author: mark@marksbench.com

Version: 0.1, 2021-05-07

**NOTE: There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

Prerequisites:
- RP2040 silicon (tested with Raspberry Pi Pico)
- MicroPython v1.15 on 2021-04-18; Raspberry Pi Pico with RP2040
- 23LC1024 connected to hardware SPI port0 or port1 pins
- Dedicated /CS pin (can be any GP pin that's not already being used for SPI). Do not tie /CS to
  GND - the 23LC1024 requires state changes on /CS to function properly.

Usage:
- from machine import Pin, SPI
- import utime
- import mb_23LC1024
- Set up SPI using a hardware SPI port 0 or 1. Polarity and phase are both 0.
- specify /CS pin (can be any GP pin that's not already being used for SPI):
  cs = GP#
- Create constructor:
  thisMemoryChipDeviceName = mb_23LC1024.mb_23LC1024(spi, cs)
- To write a single byte to an address:
  thisMemoryChipDeviceName.write_byte(address, value)
- To read a single byte from an address:
  thisMemoryChipDeviceName.read_byte(address)
- See mb_23LC1024_example.py

For more information, consult the Raspberry Pi Pico MicroPython SDK documentation at:
  https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf
  
and the Microchip 23LC1024 datasheet at:
  http://ww1.microchip.com/downloads/en/DeviceDoc/20005142C.pdf

"""


from machine import Pin, SPI
import utime

# Instruction set for 23LC1024
_READ = const(0x03)
_WRITE = const(0x02)
_EDIO = const(0x3b) # Dual I/O access (SDI bus mode)
_EQIO = const(0x38) # Quad I/O access (SQI bus mode)
_RSTIO = const(0xff) # Reset dual and quad I/O (revert to SPI bus mode)
_RDMR = const(0x05) # Read mode register
_WRMR = const(0x01) # Write mode register

# The WRMR register instruction has 8 bits, the 2 MSb of which set the MODE register.
# 0 0 = byte mode, 1 0 = Page mode, 0 1 = Sequential mode (default), 1 1 = reserved
# Bits 0 through 5 are reserved and should always be set to 0
# Only going to use byte mode in this library, though.

# The RDMR register instruction reads the MODE register. Not really needed at this point.

# Mode selection
_MODE_BYTE = const(0x00) # binary 00000000
_MODE_PAGE = const(0x40) # binary 01000000
_MODE_SEQ = const(0xc0)  # binary 11000000 (default mode)


# The 23LC1024 is a 128kib*8 (1Mbit) device. Maximum address available is 131071 (dec)
_MAX_ADDRESS = const(131071)



class mb_23LC1024:
    """Driver for 23LC1024 SPI SRAM module"""
    
    def __init__(self, spi, cs):
        # Init with SPI settings
        self.spi = spi
        
        # Init /CS pin
        self.cs = Pin(cs, Pin.OUT)
        
        
        # The datasheet says a high-low transition is required on /CS to enter active state after startup
        self.cs.value(1)
        self.cs.value(0)
        self.cs.value(1)
        
        # Set mode (setting to byte mode)
        self.cs.value(0)
        self.spi.write(bytearray([_WRMR, 0b00000000]))
        self.cs.value(1)
        utime.sleep_us(50)
        
        
    def write_byte(self, address, data):
        # Check to make sure the address is within 0 and 131071
        if((address > 131071) or (address < 0)):
            raise ValueError("Address is outside of device address range (0 to 131071)")
            return()
        # Now check to make sure the data is within 0 and 255
        if((data > 255) or (data < 0)):
            raise ValueError("You can only pass an 8-bit data value (0-255) to this function")
            return()
        # Break the address into three bytes to send (we're using 8-bit SPI)
        # SRAM addresses on the 23LC1024 are 24 bits, with the first 7 MSbs as "don't care" bits. This is a 1Mbit
        # device, so it's 128kiB. So the last 17 bits (1 1111 1111 1111 1111 = 131071 in decimal
        address_byte = [0,0,0]
        address_byte[2] = address & 0x0000ff
        address_byte[1] = (address & 0x00ff00) >> 8
        address_byte[0] = (address & 0xff0000) >> 16


        # Set the /CS pin low
        self.cs.value(0)
        # Write the byte of data to the selected address, using a bytearray
        self.spi.write(bytearray([_WRITE, address_byte[0], address_byte[1], address_byte[2], data]))
        # Set /CS pin high
        self.cs.value(1)
        return()
    
    def read_byte(self, address):
        # Check to make sure the address is within 0 and 131071
        if((address > 131071) or (address < 0)):
            raise ValueError("Address is outside of device address range (0 to 131071 (0x1ffff))")
            return()
        # Break the address into three bytes to send (using 8-bit SPI)
        address_byte = [0,0,0]
        address_byte[2] = address & 0x0000ff
        address_byte[1] = (address & 0x00ff00) >> 8
        address_byte[0] = (address & 0xff0000) >> 16
        
        # Set /CS pin low
        self.cs.value(0)
        # Write the read command and address to read from
        self.spi.write(bytearray([_READ, address_byte[0], address_byte[1], address_byte[2]]))
        # Returned byte is what we're looking for
        self.value_read = self.spi.read(1)
        # Set /CS pin high
        self.cs.value(1)
        # Convert from byte to int
        self.value_read = int.from_bytes(self.value_read, "big")
        # Return value to calling program
        return(self.value_read)
        

