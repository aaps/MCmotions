#!/usr/bin/python -B

from points import *


class Shapes:

    # all of the edge functions below this are screaming refactor,
    # but for now it is better than the old solution

    def points_on_edge_z(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.z == edgeval:
                pointcount += 1
        return pointcount >= numofpoints

    def points_on_edge_x(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.x == edgeval:
                pointcount += 1
        return pointcount >= numofpoints

    def points_on_edge_y(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.y == edgeval:
                pointcount += 1
        return pointcount >= numofpoints

    def remove_top_down_neighbors(self, pointslist, lisoffaces):

        if 6 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_z(points, 0.5):
                    del pointslist[index]
        if 5 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_z(points, -0.5):
                    del pointslist[index]

    def remove_neibors(self, pointslist, lisoffaces):

        if 6 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_z(points, 0.5):
                    del pointslist[index]
        if 5 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_z(points, -0.5):
                    del pointslist[index]
        if 4 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_y(points, 0.5):
                    del pointslist[index]
        if 3 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_y(points, -0.5):
                    del pointslist[index]
        if 2 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_x(points, 0.5):
                    del pointslist[index]
        if 1 not in lisoffaces:
            for index, points in enumerate(pointslist):
                if self.points_on_edge_x(points, -0.5):
                    del pointslist[index]

    def make_normal_stairs(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, 0.5, 0.5), Point3D(0, 0.5, 0.5)])
        pointops.append([Point3D(0, 0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(0, -0.5, 0)])
        pointops.append([Point3D(0, 0.5, 0), Point3D(0, -0.5, 0), Point3D(0, -0.5, 0.5), Point3D(0, 0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, 0), Point3D(-0.5, 0.5, 0)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0), Point3D(0, 0.5, 0), Point3D(0, 0.5, 0.5)])
        return pointops

    def make_x_block(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5,
                                                          0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5,
                                                           0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, -0.5, -0.5)])
        return pointops

    def make_neg_corner_stairs(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5),
                         Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5)])

        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0.5, 0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, 0), Point3D(-0.5, 0, 0), Point3D(-0.5, 0, 0.5)])
        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, 0.5, 0.5), Point3D(-0.5, 0.5, 0.5), Point3D(-0.5, 0, 0.5), Point3D(0, 0, 0.5)])
        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0, 0, 0.5), Point3D(0, 0, 0), Point3D(0, -0.5, 0)])
        pointops.append([Point3D(-0.5, 0, 0), Point3D(0, 0, 0), Point3D(0, 0, 0.5), Point3D(-0.5, 0, 0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0), Point3D(0, -0.5, 0), Point3D(0, 0, 0), Point3D(-0.5, 0, 0)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, 0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0.5, 0.5), Point3D(0.5, 0.5, 0.5), Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5)])

        return pointops

    def make_pos_corner_stairs(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(0, 0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(0.5, -0.5, 0), Point3D(0.5, 0, 0), Point3D(0, 0, 0)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, 0), Point3D(-0.5, 0.5, 0)])
        pointops.append([Point3D(0.5, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0), Point3D(0, 0.5, 0), Point3D(0, 0.5, 0.5)])
        pointops.append([Point3D(0.5, 0, 0.5), Point3D(0.5, 0, 0), Point3D(0.5, -0.5, 0), Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0, 0.5, 0.5), Point3D(0, 0, 0.5), Point3D(0.5, 0, 0.5)])
        pointops.append([Point3D(0, 0, 0.5), Point3D(0, 0.5, 0.5), Point3D(0, 0.5, 0), Point3D(0, 0, 0)])
        pointops.append([Point3D(0, 0, 0), Point3D(0.5, 0, 0), Point3D(0.5, 0, 0.5), Point3D(0, 0, 0.5)])
        return pointops

    def make_half_blocks(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(0.5, -0.5, 0)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0), Point3D(0.5, 0.5, 0), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, 0), Point3D(0.5, -0.5, 0)])
        return pointops

    def make_flat_blocks(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, 0.5, -0.4), Point3D(-0.5, 0.5, -0.4), Point3D(-0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.4)])
        pointops.append([Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.4), Point3D(0.5, 0.5, -0.4), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.4), Point3D(-0.5, -0.5, -0.4)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.4), Point3D(0.5, -0.5, -0.4)])
        return pointops

    def make_neg_corner_stairs(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(0, 0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(0, -0.5, 0)])
        pointops.append([Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5)])
        pointops.append([Point3D(0, -0.5, 0.5), Point3D(0, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0, 0.5), Point3D(-0.5, 0, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0.5)])
        return pointops

    def makeverticalflatblock(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.1, -0.5), Point3D(-0.5, -0.1, -0.5), Point3D(-0.5, 0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
        pointops.append([Point3D(0.5, 0.1, 0.5), Point3D(-0.5, 0.1, 0.5), Point3D(-0.5, -0.1, 0.5), Point3D(0.5, -0.1, 0.5)])
        pointops.append([Point3D(0.5, -0.1, -0.5), Point3D(0.5, -0.1, 0.5), Point3D(-0.5, -0.1, 0.5), Point3D(-0.5, -0.1, -0.5)])
        pointops.append([Point3D(-0.5, 0.1, -0.5), Point3D(-0.5, 0.1, 0.5), Point3D(0.5, 0.1, 0.5), Point3D(0.5, 0.1, -0.5)])
        pointops.append([Point3D(-0.5, 0.1, -0.5), Point3D(-0.5, -0.1, -0.5), Point3D(-0.5, -0.1, 0.5), Point3D(-0.5, 0.1, 0.5)])
        pointops.append([Point3D(0.5, 0.1, 0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.5, -0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
        return pointops

    def make_fence_shape(self):
        pointops = PointList()
        pointops.append([Point3D(0.1, 0.1, -0.5), Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, -0.1, -0.5), Point3D(0.1, -0.1, -0.5)])
        pointops.append([Point3D(0.1, 0.1, +0.5), Point3D(-0.1, 0.1, 0.5), Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5)])
        pointops.append([Point3D(-0.1, -0.1, -0.5), Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, -0.1, -0.5)])
        pointops.append([Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, 0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, 0.1, -0.5)])
        pointops.append([Point3D(-0.1, -0.1, -0.5), Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, 0.1, 0.5), Point3D(-0.1, -0.1, 0.5)])
        pointops.append([Point3D(0.1, -0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, -0.1, 0.5)])
        return pointops

    def make_vertical_plus_block(self):
        pointops = PointList()

        for fordir in xrange(0, 4):
            temperlist = PointList()
            temperlist.append([Point3D(0.5, 0.1, 0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.5, -0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.append([Point3D(0.5, -0.1, -0.5), Point3D(0.1, -0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.append([Point3D(0.5, 0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.5, -0.1, 0.5)])
            temperlist.append([Point3D(0.5, -0.1, -0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, -0.1, -0.5)])
            temperlist.append([Point3D(0.1, 0.1, -0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.5, 0.1, 0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.rotatepointsZ(90*fordir)
            pointops.extend(temperlist)

        pointops.append([Point3D(-0.1, 0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.1, -0.1, -0.5), Point3D(-0.1, -0.1, -0.5)])
        pointops.append([Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(-0.1, 0.1, 0.5)])
        return pointops

    def make_ladder_shapes(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.4, -0.5), Point3D(0.5, -0.4, -0.5)])
        pointops.append([Point3D(0.5, -0.4, 0.5), Point3D(-0.5, -0.4, 0.5), Point3D(-0.5, -0.5, 0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(-0.5, -0.4, -0.5), Point3D(-0.5, -0.4, 0.5), Point3D(0.5, -0.4, 0.5), Point3D(0.5, -0.4, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.4, 0.5), Point3D(-0.5, -0.4, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.4, -0.5),
                         Point3D(0.5, -0.4, 0.5), Point3D(0.5, -0.5, 0.5)])
        return pointops

    def make_flat_block_shape(self):
        pointops = PointList()
        pointops.append([Point3D(0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, -0.4, -0.5), Point3D(0.4, -0.4, -0.5)])
        pointops.append([Point3D(0.4, 0.4, -0.4), Point3D(-0.4, 0.4, -0.4), Point3D(-0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.4)])
        pointops.append([Point3D(-0.4, -0.4, -0.5), Point3D(-0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.5)])
        pointops.append([Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.4), Point3D(0.4, 0.4, -0.4), Point3D(0.4, 0.4, -0.5)])
        pointops.append([Point3D(-0.4, -0.4, -0.5), Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.4), Point3D(-0.4, -0.4, -0.4)])
        pointops.append([Point3D(0.4, -0.4, -0.5), Point3D(0.4, 0.4, -0.5), Point3D(0.4, 0.4, -0.4), Point3D(0.4, -0.4, -0.4)])
        return pointops

    def make_block_shape(self):
        pointops = PointList()
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, 0.5, 0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        return pointops
