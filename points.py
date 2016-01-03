#!/usr/bin/python -B

import math

class Point3D(object):
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    
    def appendtup(self, tup):
        self.x += tup[0]
        self.y += tup[1]
        self.z += tup[2]

    def append(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z

    def divide(self, divider):
        self.x = self.x / divider
        self.y = self.y / divider
        self.z = self.z / divider

    def substracttup(self, point):
        self.x = self.x - point[0]
        self.y = self.y - point[1]
        self.z = self.z - point[2]

    def mirrorX(self):
        x = self.x * -1
        return Point3D(x, self.y, self.z)

    def mirrorY(self):
        y = self.y * -1
        return Point3D(self.x, y, self.z)

    def mirrorZ(self):
        z = self.z * -1
        return Point3D(self.x, self.y, z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = round(self.y * cosa - self.z * sina,1)
        z = round(self.y * sina + self.z * cosa,1)
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = round(self.z * cosa - self.x * sina,1)
        x = round(self.z * sina + self.x * cosa,1)
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = round(self.x * cosa - self.y * sina,1)
        y = round(self.x * sina + self.y * cosa,1)
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

    def astuple(self):
        return self.x,self.y,self.z

    def aslist(self):
        return [self.x,self.y,self.z]

class PointList(list):

    def mirrorpointsX(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirrorX())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def mirrorpointsY(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirrorY())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def mirrorpointsZ(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirrorZ())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotatepointsY(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotateY(angle))
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotatepointsX(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotateX(angle))
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotatepointsZ(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotateZ(angle))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)


    def totuplelist(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append( point.astuple() )
            tempfinal.append(templist)
        return tempfinal

    def fromtuplelist(self, alist):
        tempfinal = []
        for face in alist:
            newface = []
            for atuple in face:
                point = Point3D(x=atuple[0],y=atuple[1],z=atuple[2])
                newface.append(point)
            tempfinal.append(newface)
        list.__init__(self, tempfinal)

    def getavgpoint(self):
        tottup = Point3D(0,0,0)
        length = 0
        for face in list.__iter__(self):
            length  += len(face)
            for point in face:
                tottup.append(point)
        tottup.divide(length)
        return tottup

    def getrawavgpoint(self):
        tottup = Point3D(0,0,0)
        length = len(self)
        for point in list.__iter__(self):
            tottup.append(point)
        tottup.divide(length)
        return tottup

    def getavgpoint(self):
        tottup = Point3D(0,0,0)
        length = 0
        for face in list.__iter__(self):
            length  += len(face)
            for point in face:
                tottup.append(point)
        tottup.divide(length)
        return tottup
