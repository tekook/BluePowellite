# -*- coding: utf-8 -*-
from time import sleep
import digitalio
import logging
import board
import threading
from .display import Display
from adafruit_debouncer import Debouncer
from micropython import const
from events import Events

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


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


class Task():
    def __init__(self, display: Display, top: Button, bottom: Button) -> None:
        self.Running = True
        self.Display = display
        self.Top = top
        self.Bottom = bottom


class Application():
    _debouncetime = const(0.005)

    def __init__(self, fontsize=14) -> None:
        self.fontsize = fontsize
        self.Display = None
        self.BtnTop = Button(board.D23)
        self.BtnTop.pressed += self._top
        self.BtnBottom = Button(board.D24)
        self.BtnBottom.pressed += self._bottom
        self._btns = [self.BtnBottom, self.BtnTop]
        self._tasks = []
        self.taskRunning = False

    def _top(self):
        if self.taskRunning == False:
            logging.info("_top")

    def _bottom(self):
        if self.taskRunning:
            return

    def addTask(self, task: Task):
        self._tasks.append(task)

    def run(self):
        logging.info("App started")
        self.Display = Display(fontsize=self.fontsize)
        self.Display.writeLines("Hello its me again what can i do for you?")
        logging.info("Turning the lights on")
        self.Display.lightOn()
        try:
            logging.info("Starting Main loop")
            while True:
                for btn in self._btns:
                    btn.update()
                sleep(self._debouncetime)
        except KeyboardInterrupt:
            logging.info("App stopped")
