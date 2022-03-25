# -*- coding: utf-8 -*-
import digitalio
import board
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565


class Display():
    def __init__(self, fontsize: int = 14) -> None:
        self._rotation = 180
        self._createDisplay()
        self._font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
        self._image = Image.new("RGB", (self._disp.width, self._disp.height))
        self._draw = ImageDraw.Draw(self._image)

    def _createDisplay(self):
        # Setup SPI bus using hardware SPI:
        spi = board.SPI()
        # Create the ST7789 display:
        self._disp = st7789.ST7789(
            spi,
            cs=digitalio.DigitalInOut(board.CE0),
            dc=digitalio.DigitalInOut(board.D25),
            rst=None,
            baudrate=64000000,
            height=240,
            y_offset=80,
            rotation=self._rotation
        )
        self._backlight = digitalio.DigitalInOut(board.D22)
        self._backlight.switch_to_output()

    def lightOn(self):
        self._backlight.value = True

    def lightOff(self):
        self._backlight.value = False

    def clearDisplay(self, clear=True):
        self._draw.rectangle(
            (0, 0, self._disp.width, self._disp.height), outline=0, fill=(0, 0, 0))
        if clear:
            self.drawImage()

    def drawImage(self):
        self._disp.image(self._image, self._rotation)

    def fill(self, r: int, g: int, b: int):
        self._disp.fill(color565(r, g, b))

    def writeLines(self, *args: str):
        self.writeLinesColor("#FFFFFF", *args)

    def writeLinesColor(self, color: str, *args: str):
        y = -2
        x = 0
        self.clearDisplay(False)
        for str in args:
            txt = self.getFittedStr(str)
            self._draw.text((x, y), txt, font=self._font, fill=color)
            y += self._font.getsize(txt)[1]

            while len(txt) != len(str):
                str = str[len(txt):len(str)]
                txt = self.getFittedStr(str)
                self._draw.text((x, y), txt, font=self._font, fill=color)
                y += self._font.getsize(txt)[1]

        self.drawImage()

    def getFittedStr(self, text: str):
        w = self._font.getsize(text)[0]
        while w > self._disp.width:
            text = text[0:len(text)-1]
            w = self._font.getsize(text)[0]
        return text
