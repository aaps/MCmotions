#!/usr/bin/python -B

from points import * 

class Shapes:

	def makenormalstairs(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])
		pointops.append([Point3D(0,0.5,0.5),Point3D(0.5,0.5,0.5),Point3D(0.5,-0.5,0.5),Point3D(0,-0.5,0.5)])
		pointops.append([Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(0,-0.5,0)])
		pointops.append([Point3D(0,0.5,0),Point3D(0,-0.5,0),Point3D(0,-0.5,0.5),Point3D(0,0.5,0.5)])
		pointops.append([Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)])
		pointops.append([Point3D(0.5,0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5),Point3D(0.5,0.5,0.5)])
		pointops.append([Point3D(0,0.5,0.5),Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)])
		pointops.append([Point3D(0,-0.5,0.5),Point3D(0,-0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5)])
		return pointops
		
	def makeposcornerstairs(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])
		pointops.append([Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0), Point3D(0.5,-0.5,0), Point3D(0.5,0,0),Point3D(0,0,0)])
		pointops.append([Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)])
		pointops.append([Point3D(0.5,-0.5,0), Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])
		pointops.append([Point3D(0,0.5,0.5),Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)])
		pointops.append([Point3D(0.5,0,0.5),Point3D(0.5,0,0),Point3D(0.5,-0.5,0),Point3D(0.5,-0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)])
		pointops.append([Point3D(0.5,0.5,0.5),Point3D(0,0.5,0.5),Point3D(0,0,0.5),Point3D(0.5,0,0.5)])
		pointops.append([Point3D(0,0,0),Point3D(0,0.5,0),Point3D(0,0.5,0.5),Point3D(0,0,0.5)])
		pointops.append([Point3D(0,0,0),Point3D(0.5,0,0),Point3D(0.5,0,0.5),Point3D(0,0,0.5)])
		return pointops

	def makenegcornderstairs(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])
		pointops.append([Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(0,-0.5,0)])
		pointops.append([Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)])
		pointops.append([Point3D(0,-0.5,0.5),Point3D(0,-0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5)])
		pointops.append([Point3D(-0.5,0,0.5),Point3D(-0.5,0,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,0.5)])
		return pointops

	def makeverticalflatblock(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.5,-0.1,-0.5),Point3D(-0.5,-0.1,-0.5),Point3D(-0.5,0.1,-0.5),Point3D(0.5,0.1,-0.5)])
		pointops.append([Point3D(0.5,0.1,0.5),Point3D(-0.5,0.1,0.5),Point3D(-0.5,-0.1,0.5),Point3D(0.5,-0.1,0.5)])
		pointops.append([Point3D(0.5,-0.1,-0.5),Point3D(0.5,-0.1,0.5),Point3D(-0.5,-0.1,0.5),Point3D(-0.5,-0.1,-0.5)])
		pointops.append([Point3D(-0.5,0.1,-0.5),Point3D(-0.5,0.1,0.5),Point3D(0.5,0.1,0.5),Point3D(0.5,0.1,-0.5)])
		pointops.append([Point3D(-0.5,0.1,-0.5),Point3D(-0.5,-0.1,-0.5),Point3D(-0.5,-0.1,0.5),Point3D(-0.5,0.1,0.5)])
		pointops.append([Point3D(0.5,0.1,0.5),Point3D(0.5,-0.1,0.5),Point3D(0.5,-0.1,-0.5),Point3D(0.5,0.1,-0.5)])
		return pointops

	def makefenceshape(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.1,0.1,-0.5),Point3D(-0.1,0.1,-0.5),Point3D(-0.1,-0.1,-0.5),Point3D(0.1,-0.1,-0.5)])
		pointops.append([Point3D(0.1,0.1,+0.5),Point3D(-0.1,0.1,0.5),Point3D(-0.1,-0.1,0.5),Point3D(0.1,-0.1,0.5)])
		pointops.append([Point3D(-0.1,-0.1,-0.5),Point3D(-0.1,-0.1,0.5),Point3D(0.1,-0.1,0.5),Point3D(0.1,-0.1,-0.5)])
		pointops.append([Point3D(-0.1,0.1,-0.5),Point3D(-0.1,0.1,0.5),Point3D(0.1,0.1,0.5),Point3D(0.1,0.1,-0.5)])
		pointops.append([Point3D(-0.1,-0.1,-0.5),Point3D(-0.1,0.1,-0.5),Point3D(-0.1,0.1,0.5),Point3D(-0.1,-0.1,0.5)])
		pointops.append([Point3D(0.1,-0.1,-0.5),Point3D(0.1,0.1,-0.5),Point3D(0.1,0.1,0.5),Point3D(0.1,-0.1,0.5)])
		return pointops


	def makeverticalplusblock(self, listoffaces=None):
		pointops = PointList()
		
		for x in xrange(0,4):
			temperlist = PointList()
			temperlist.append([Point3D(0.5,0.1,0.5),Point3D(0.5,-0.1,0.5),Point3D(0.5,-0.1,-0.5),Point3D(0.5,0.1,-0.5)])
			temperlist.append([Point3D(0.5,-0.1,-0.5),Point3D(0.1,-0.1,-0.5),Point3D(0.1,0.1,-0.5),Point3D(0.5,0.1,-0.5)])
			temperlist.append([Point3D(0.5,-0.1,0.5),Point3D(0.1,-0.1,0.5),Point3D(0.1,0.1,0.5),Point3D(0.5,0.1,0.5)])
			temperlist.append([Point3D(0.5,-0.1,-0.5),Point3D(0.5,-0.1,0.5),Point3D(0.1,-0.1,0.5),Point3D(0.1,-0.1,-0.5)])
			temperlist.append([Point3D(0.1,0.1,-0.5),Point3D(0.1,0.1,0.5),Point3D(0.5,0.1,0.5),Point3D(0.5,0.1,-0.5)])
			temperlist.rotatepointsZ(90*x)
			pointops.extend(temperlist)

		pointops.append([Point3D(-0.1,-0.1,-0.5),Point3D(0.1,-0.1,-0.5),Point3D(0.1,0.1,-0.5),Point3D(-0.1,0.1,-0.5)])
		pointops.append([Point3D(-0.1,-0.1,0.5),Point3D(0.1,-0.1,0.5),Point3D(0.1,0.1,0.5),Point3D(-0.1,0.1,0.5)])
		return pointops

	def makeladdershapes(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.5,-0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.4,-0.5),Point3D(0.5,-0.4,-0.5)])
		pointops.append([Point3D(0.5,-0.4,0.5),Point3D(-0.5,-0.4,0.5),Point3D(-0.5,-0.5,0.5),Point3D(0.5,-0.5,0.5)])
		pointops.append([Point3D(-0.5,-0.4,-0.5),Point3D(-0.5,-0.4,0.5),Point3D(0.5,-0.4,0.5),Point3D(0.5,-0.4,-0.5)])
		pointops.append([Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5),Point3D(-0.5,-0.5,0.5),Point3D(-0.5,-0.5,-0.5)])
		pointops.append([Point3D(-0.5,-0.5,0.5),Point3D(-0.5,-0.4,0.5),Point3D(-0.5,-0.4,-0.5),Point3D(-0.5,-0.5,-0.5)])
		pointops.append([Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.4,-0.5),Point3D(0.5,-0.4,0.5),Point3D(0.5,-0.5,0.5)])
		return pointops

	def makeflatblockshape(self, listoffaces=None):
		pointops = PointList()
		pointops.append([Point3D(0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.5),Point3D(-0.4,-0.4,-0.5),Point3D(0.4,-0.4,-0.5)])
		pointops.append([Point3D(0.4,0.4,-0.4),Point3D(-0.4,0.4,-0.4),Point3D(-0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.4)])
		pointops.append([Point3D(-0.4,-0.4,-0.5),Point3D(-0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.5)])
		pointops.append([Point3D(-0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.4),Point3D(0.4,0.4,-0.4),Point3D(0.4,0.4,-0.5)])
		pointops.append([Point3D(-0.4,-0.4,-0.5),Point3D(-0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.4),Point3D(-0.4,-0.4,-0.4)])
		pointops.append([Point3D(0.4,-0.4,-0.5),Point3D(0.4,0.4,-0.5),Point3D(0.4,0.4,-0.4),Point3D(0.4,-0.4,-0.4)])
		return pointops