from CubeCore import *
from math import sin, sqrt

threadRunning = True

def plot(x, y, z, n=1):
	points[y][x][z] = n

def plotFill(x1, y1, z1, x2, y2, z2):
	x1, x2 = min(x1, x2), max(x1, x2)
	y1, y2 = min(y1, y2), max(y1, y2)
	z1, z2 = min(z1, z2), max(z1, z2)

	for y in range(y1, y2 + 1):
		for x in range(x1, x2 + 1):
			for z in range(z1, z2 + 1):
				plot(x, y, z, n)

def fullCube(n=0):
	plotFill(0, 0, 0, 3, 3, 3, n)

def clear(n=0):
	plotFill(0, 0, 0, 3, 3, 3, n)


