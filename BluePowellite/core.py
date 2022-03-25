# -*- coding: utf-8 -*-
from time import sleep
import digitalio
import logging
import board
import threading
from BluePowellite.display import Display
from adafruit_debouncer import Debouncer
from micropython import const
from events import Events
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class Application():
    _debouncetime = const(0.005)

    def __init__(self) -> None:
        self.fontsize = 14
        self.Display = None
        self.BtnTop = Button(board.D23)
        self.BtnBottom = Button(board.D24)

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
                self.BtnTop.update()
                self.BtnBottom.update()
                sleep(self._debouncetime)
                logging.info("run")
        except KeyboardInterrupt:
            logging.info("App stopped")


class Button(Events):
    __events__ = ('pressed', 'released')

    def __init__(self, pin) -> None:
        self._pin = digitalio.DigitalInOut(pin)
        self._pin.switch_to_input()
        self._debouncer = Debouncer(self._pin)

    def update(self):
        self._debouncer.update()
        if self._debouncer.fell:
            thread = threading.Thread(target=self.pressed)
            thread.start()
        if self._debouncer.rose:
            thread = threading.Thread(target=self.released)
            thread.start()
