#!/usr/bin/python -B

import math

class Point3D(object):
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    
    def append_tup(self, tup):
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

    def substract_tup(self, point):
        self.x = self.x - point[0]
        self.y = self.y - point[1]
        self.z = self.z - point[2]

    def mirror_x(self):
        x = self.x * -1
        return Point3D(x, self.y, self.z)

    def mirror_y(self):
        y = self.y * -1
        return Point3D(self.x, y, self.z)

    def mirror_z(self):
        z = self.z * -1
        return Point3D(self.x, self.y, z)

    def rotate_x(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = round(self.y * cosa - self.z * sina, 1)
        z = round(self.y * sina + self.z * cosa, 1)
        return Point3D(self.x, y, z)
 
    def rotate_y(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = round(self.z * cosa - self.x * sina, 1)
        x = round(self.z * sina + self.x * cosa, 1)
        return Point3D(x, self.y, z)
 
    def rotate_z(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = round(self.x * cosa - self.y * sina, 1)
        y = round(self.x * sina + self.y * cosa, 1)
        return Point3D(x, y, self.z)

    def scale_x(self, amount):
        x = self.x * amount
        return Point3D(x, self.y, self.z)

    def scale_y(self, amount):
        y = self.y * amount
        return Point3D(self.x, y, self.z)

    def scale_z(self, amount):
        z = self.z * amount
        return Point3D(self.x, self.y, z)

    def translate_x(self, amount):
        x = self.x + amount
        return Point3D(x, self.y, self.z)

    def translate_y(self, amount):
        y = self.y + amount
        return Point3D(self.x, y, self.z)

    def translate_z(self, amount):
        z = self.z + amount
        return Point3D(self.x, self.y, z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

    def as_tuple(self):
        return self.x, self.y, self.z

    def as_list(self):
        return [self.x, self.y, self.z]

class PointList(list):

    def mirror_points_x(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirror_x())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def mirror_points_y(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirror_y())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def mirror_points_z(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                
                templist.append(point.mirror_z())
            templist.reverse()
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotate_points_y(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotate_y(angle))
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotate_points_x(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotate_x(angle))
            tempfinal.append(templist)
        list.__init__(self, tempfinal)

    def rotate_points_z(self, angle):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.rotate_z(angle))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def translate_points_x(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.translate_x(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def translater_points_y(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.translate_y(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def translate_points_z(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.translate_z(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def scale_points_x(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.scale_x(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def scale_points_y(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.scale_y(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)

    def scale_points_z(self, amount):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append(point.scale_z(amount))
            tempfinal.append(templist)

        list.__init__(self, tempfinal)


    def to_tuple_list(self):
        tempfinal = []
        for face in list.__iter__(self):
            templist = []
            for point in face:
                templist.append( point.as_tuple() )
            tempfinal.append(templist)
        return tempfinal

    def from_tuple_list(self, alist):
        tempfinal = []
        for face in alist:
            newface = []
            for atuple in face:
                point = Point3D(x=atuple[0], y=atuple[1], z=atuple[2])
                newface.append(point)
            tempfinal.append(newface)
        list.__init__(self, tempfinal)

    def get_avg_point(self):
        tottup = Point3D(0, 0, 0)
        length = 0
        for face in list.__iter__(self):
            length  += len(face)
            for point in face:
                tottup.append(point)
        tottup.divide(length)
        return tottup

    def get_raw_avg_point(self):
        tottup = Point3D(0, 0, 0)
        length = len(self)
        for point in list.__iter__(self):
            tottup.append(point)
        tottup.divide(length)
        return tottup

    def get_avg_point(self):
        tottup = Point3D(0, 0, 0)
        length = 0
        for face in list.__iter__(self):
            length  += len(face)
            for point in face:
                tottup.append(point)
        tottup.divide(length)
        return tottup
