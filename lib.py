#! /usr/bin/env python3
# -*- coding: utf-8 -*-
def getDisp():
    import digitalio
    import board
    from adafruit_rgb_display import st7789

    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 64000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    return st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        height=240,
        y_offset=80,
    )
def pinDebouncer(pin):
    import digitalio
    from adafruit_debouncer import Debouncer
    pin = digitalio.DigitalInOut(pin)
    pin.switch_to_input()
    return Debouncer(pin)