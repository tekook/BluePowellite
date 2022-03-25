#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from BluePowellite import Application
from adafruit_rgb_display.rgb import color565
app = Application()
app.fontsize = 16
app.run()
app.Display.lightOff()
