#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from BluePowellite import Application
from time import sleep
app = Application()
app.fontsize = 16


def top():
    app.Display.writeLines("Thank you for pressing Top :-)")
    sleep(2)
    app.Display.writeLines("waiting")


app.BtnTop.pressed += top
app.run()
app.Display.lightOff()
