#!/usr/bin/python -B

from points import * 

class Shapes:

	# all of the edge functions below this are screaming refactor, 
	# but for now it is better than the old solution

	def pointsonedgeZ(self, points, edgeval):
		numofpoints = len(points)
		pointcount = 0
		for point in points:
			if point.z == edgeval:
				pointcount += 1
		return pointcount >= numofpoints

	def pointsonedgeX(self, points, edgeval):
		numofpoints = len(points)
		pointcount = 0
		for point in points:
			if point.x == edgeval:
				pointcount += 1
		return pointcount >= numofpoints

	def pointsonedgeY(self, points, edgeval):
		numofpoints = len(points)
		pointcount = 0
		for point in points:
			if point.y == edgeval:
				pointcount += 1
		return pointcount >= numofpoints


	def removeneibors(self, pointslist, lisoffaces):
		
		if 6 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeZ(points, 0.5):
					del pointslist[index]
		if 5 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeZ(points, -0.5):
					del pointslist[index]
		if 4 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeY(points, 0.5):
					del pointslist[index]
		if 3 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeY(points, -0.5):
					del pointslist[index]
		if 2 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeX(points, 0.5):
					del pointslist[index]
		if 1 not in lisoffaces:
			for index, points in enumerate(pointslist):
				if self.pointsonedgeX(points, -0.5):
					del pointslist[index]



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