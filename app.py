#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import digitalio
import board
import lib
import time

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565

# Create the ST7789 display:
disp = lib.getDisp()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
image = Image.new("RGB", (disp.width, disp.height))
rotation = 180

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = lib.pinDebouncer(board.D23)
buttonB = lib.pinDebouncer(board.D24)


# Main loop:
while True:
    buttonA.update()
    buttonB.update()
    
    if buttonA.fell or buttonA.rose or buttonB.fell or buttonB.rose:
        if buttonA.value and buttonB.value:
            draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
            draw.text((0,-2), "kekse", font=font, fill="#FFFFFF")
            disp.image(image, rotation)
            print("off")
        else:
            print("on")
        if buttonB.value and not buttonA.value:  # just button A pressed
            disp.fill(color565(255, 0, 0))  # red
            print("red")
        if buttonA.value and not buttonB.value:  # just button B pressed
            disp.fill(color565(0, 0, 255))  # blue
            print("blue")
        if not buttonA.value and not buttonB.value:  # none pressed
            disp.fill(color565(0, 255, 0))  # green
            print("green")
    time.sleep(0.005)