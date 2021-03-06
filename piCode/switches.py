#!/usr/bin/env python3

DEBUG = True

if(DEBUG):
    from fake_rpi import RPi
    GPIO = RPi.GPIO
else:
    import RPi.GPIO as GPIO
import time
import threading
import subprocess
import os

'''
https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
'''
pinKey = 1
pinStart = 2
pinA = 3
pinB = 4
pinC = 5

class Process(object):
    def __init__(self, cmd, args = []):
        self.cmd = cmd
        self.args = args

    def call(self):
        '''
        Fixme, add the case that the process is already running.
        For calling emulationstation it would do nothing if it exists,
        for the games, have it switch unconditionally, or fail unless
        not in a game?
        Should the switches only activate after emulation station is running?
        '''
        subprocess.call([self.cmd] + self.args)

class Switch(object):
    def __init__(self, pin, process, direction = GPIO.IN, edgeMode = GPIO.FALLING, resMode = GPIO.PUD_UP):
        self.pin = pin
        self.process = process
        self.direction = direction
        self.edgeMode = edgeMode
        self.resMode = resMode

    def setup(self):
        GPIO.setup(
            [self.pin], 
            self.direction, 
            pull_up_down = self.resMode,
        )
        GPIO.add_event_detect(
            self.pin, 
            self.edgeMode, 
            callback = self.process.call,
            bouncetime=200
        )

class SwitchController(object):
    def __init__(self, switches):
        self.switches = switches
    
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        for switch in self.switches:
            switch.setup()
    
keySwitch = Switch(
    pinKey,
    Process('shutdown', ['--now']),
)
    
startBtn = Switch(
    pinStart,
    Process('emulationstation')
)

switchA = Switch(
    pinA,
    Process('echo', ['switch A'])
)

switchB = Switch(
    pinB,
    Process('echo', ['switch B'])
)

switchC = Switch(
    pinC,
    Process('echo', ['switch C'])
)

cont = SwitchController([keySwitch, startBtn, switchA, switchB, switchC])


if __name__ == "__main__":
    cont.setup()
    run()
