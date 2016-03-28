#!/usr/bin/python -B

from math import pi, cos, sin

class Point3D(object):
    def __init__(self, x_coord=0, y_coord=0, z_coord=0):
        self.x_coord, self.y_coord, self.z_coord = float(x_coord), float(y_coord), float(z_coord)

    def append_tup(self, tup):
        self.x_coord += tup[0]
        self.y_coord += tup[1]
        self.z_coord += tup[2]

    def append(self, point):
        self.x_coord += point.x_coord
        self.y_coord += point.y_coord
        self.z_coord += point.z_coord

    def divide(self, divider):
        self.x_coord = self.x_coord / divider
        self.y_coord = self.y_coord / divider
        self.z_coord = self.z_coord / divider

    def substract_tup(self, point):
        self.x_coord = self.x_coord - point[0]
        self.y_coord = self.y_coord - point[1]
        self.z_coord = self.z_coord - point[2]

    def mirror_x(self):
        x_coord = self.x_coord * -1
        return Point3D(x_coord, self.y_coord, self.z_coord)

    def mirror_y(self):
        y_coord = self.y_coord * -1
        return Point3D(self.x_coord, y_coord, self.z_coord)

    def mirror_z(self):
        z_coord = self.z_coord * -1
        return Point3D(self.x_coord, self.y_coord, z_coord)

    def rotate_x(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        y_coord = round(self.y_coord * cosa - self.z_coord * sina, 1)
        z_coord = round(self.y_coord * sina + self.z_coord * cosa, 1)
        return Point3D(self.x_coord, y_coord, z_coord)

    def rotate_y(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        z_coord = round(self.z_coord * cosa - self.x_coord * sina, 1)
        x_coord = round(self.z_coord * sina + self.x_coord * cosa, 1)
        return Point3D(x_coord, self.y_coord, z_coord)

    def rotate_z(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        x_coord = round(self.x_coord * cosa - self.y_coord * sina, 1)
        y_coord = round(self.x_coord * sina + self.y_coord * cosa, 1)
        return Point3D(x_coord, y_coord, self.z_coord)

    def scale_x(self, amount):
        x_coord = self.x_coord * amount
        return Point3D(x_coord, self.y_coord, self.z_coord)

    def scale_y(self, amount):
        y_coord = self.y_coord * amount
        return Point3D(self.x_coord, y_coord, self.z_coord)

    def scale_z(self, amount):
        z_coord = self.z_coord * amount
        return Point3D(self.x_coord, self.y_coord, z_coord)

    def translate_x(self, amount):
        x_coord = self.x_coord + amount
        return Point3D(x_coord, self.y_coord, self.z_coord)

    def translate_y(self, amount):
        y_coord = self.y_coord + amount
        return Point3D(self.x_coord, y_coord, self.z_coord)

    def translate_z(self, amount):
        z_coord = self.z_coord + amount
        return Point3D(self.x_coord, self.y_coord, z_coord)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z_coord)
        x_coord = self.x_coord * factor + win_width / 2
        y_coord = -self.y_coord * factor + win_height / 2
        return Point3D(x_coord, y_coord, 1)

    def as_tuple(self):
        return self.x_coord, self.y_coord, self.z_coord

    def as_list(self):
        return [self.x_coord, self.y_coord, self.z_coord]

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
                templist.append(point.as_tuple())
            tempfinal.append(templist)
        return tempfinal

    def from_tuple_list(self, alist):
        tempfinal = []
        for face in alist:
            newface = []
            for atuple in face:
                point = Point3D(x_coord=atuple[0], y_coord=atuple[1], z_coord=atuple[2])
                newface.append(point)
            tempfinal.append(newface)
        list.__init__(self, tempfinal)

    def get_avg_point(self):
        tottup = Point3D(0, 0, 0)
        length = 0
        for face in list.__iter__(self):
            length += len(face)
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
