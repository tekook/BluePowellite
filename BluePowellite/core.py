# -*- coding: utf-8 -*-
from time import sleep
import digitalio
import logging
from BluePowellite.display import Display
from adafruit_debouncer import Debouncer
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class Application():
    _debouncetime = 0.005
    fontsize = 14

    def __init__(self) -> None:
        self.Display = None

    def run(self):
        logging.info("App started")
        logging.info("Creating display")
        self.Display = Display(fontsize=self.fontsize)
        self.Display.writeLines("Hello its me again what can i do for you?")
        logging.info("Turning the lights on")
        self.Display.lightOn()
        try:
            logging.info("Starting Main loop")
            while True:
                sleep(self._debouncetime)
        except KeyboardInterrupt:
            logging.info("App stopped")

    def createDebouncer(self, pin):
        pin = digitalio.DigitalInOut(pin)
        pin.switch_to_input()
        return Debouncer(pin)
