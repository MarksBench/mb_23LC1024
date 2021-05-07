# mb_23LC1024
Very simple MicroPython module to use a Microchip 23LC1024 SPI SRAM with a Raspberry Pi Pico (RP2040)

This module is intended to make using the 23LC1024 as simple as possible. It only accepts an address (range 0-131071) and a value (range 0-255).

There are probably much better ways to do this but who knows, someone might find it useful.

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
