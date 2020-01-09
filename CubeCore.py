import RPi.GPIO as GPIO
import threading
from random import randint
from time import sleep

GPIO.setwarnings(false)
GPIO.setmode(GPIO.BOARD)

pins = [
		23, #pin 11, transistor 4
		24, #pin 8, transistor 3
		7,  #pin 4, transistor 2
		8,  #pin 14, transistor 1

		11, #pin 17, RGB red (register 2 clear)
		12, #pin 18, recister 2 clock
		13, #pin 21, register 2 latch
		10, #pin 15, register 2 serial data

		15, #pin 17, RGB green (register 1 clear)
		16, #pin 18, recister 1 clock
		18, #pin 21, register 1 latch
		22, #pin 15, register 1 serial data
		26] #pin something, RGB blue

transistors = [8, 7, 24, 23]

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)

points = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]

class ShiftRegister():
	def __init__(self, datapin, clockpin, latchpin, clearpin):
		self.datapin = datapin
		self.clockpin = clockpin
		self.latchpin = latchpin
		self.clearpin = clearpin

		GPIO.output(self.clearpin, 1)

	def clock(self, n):
		if n != "NONE":
			GPIO.output(self.datapin, n)

		GPIO.output(self.clockpin, 1)
		GPIO.output(self.clockpin, 0)

		if n != "NONE":
			GPIO.output(self.datapin, 0)

	def latch(self):
		GPIO.output(self.latchpin, 1)
		GPIO.output(self.latchpin, 0)

	def clear(self):
		for _ in range(16):
			self.clock(0)
		self.latch()

class Sequence():
	def __init__(self, patterns):
		self.patterns = patterns

	def getParameters(self, parameters):
		self.parameters = []
		for i in range(len(self.patterns)):
			self.paramters.append(parameters[i])

	def getTimes(self, reps):
		self.reps = reps

	def run(self, times, speed):
		if times == "infinity":
			times = 10000

		t = times
		while t > 0:
			for p in range(len(self.patterns)):
				if not self.parameter[p] == "N":
					self.patterns[p](self.parameters[p], self.reps[p], speed)
				else:
					self.patterns[p](self.reps[p], speed)
			if not t > 9999:
				t -= 1

class threadRunClass():
	def __init__(self, running):
		self.running = running

class Multiplexer():
	def __init__(self):
		print("Init multiplexing")
		self.running = True
		self.register1 = ShiftRegister(10, 12, 13, 11)
		self.register2 = ShiftRegister(22, 16, 18, 15)

	def multiplex(self, randomThing):
		while self.running:
			for y in range(len(points)):
				GPIO.output(transistors[y-1], 0)
				for x in range(len(points[y])):
					for z in range(len(points[y][x])):
						if x < 2:
							self.register2.clock(points[y][x][z])
						else:
							self.register1.clock(points[y][x][z])
				self.register1.latch()
				self.register2.latch()
				GPIO.output(transistors[y], 1)
				sleep(.001)