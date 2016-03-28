#!/usr/bin/python -B

from points import Point3D, PointList


class DefaultShapes(object):

    def __init__(self):
        pass
    # all of the edge functions below this are screaming refactor,
    # but for now it is better than the old solution

    def points_on_edge_z(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.z_coord == edgeval:
                pointcount += 1
        return pointcount >= numofpoints

    def points_on_edge_x(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.x_coord == edgeval:
                pointcount += 1
        return pointcount >= numofpoints

    def points_on_edge_y(self, points, edgeval):
        numofpoints = len(points)
        pointcount = 0
        for point in points:
            if point.y_coord == edgeval:
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

    def make_default_normal_stairs(self):
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

    def make_default_x_block(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5,
                                                          0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5,
                                                           0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, -0.5, -0.5)])
        return pointops

    def make_default_neg_corner_stairs(self):
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

    def make_default_pos_corner_stairs(self):
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

    def make_default_half_blocks(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(0.5, -0.5, 0)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0), Point3D(-0.5, -0.5, 0), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0), Point3D(0.5, 0.5, 0), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0), Point3D(-0.5, 0.5, 0), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, 0), Point3D(0.5, -0.5, 0)])
        return pointops

    def make_default_flat_blocks(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, 0.5, -0.4), Point3D(-0.5, 0.5, -0.4), Point3D(-0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.4)])
        pointops.append([Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.4), Point3D(0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.4), Point3D(0.5, 0.5, -0.4), Point3D(0.5, 0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.4), Point3D(-0.5, -0.5, -0.4)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.4), Point3D(0.5, -0.5, -0.4)])
        return pointops

    # def make_default_vertical_flat_block(self):
    #     pointops = PointList()
    #     pointops.append([Point3D(0.5, -0.1, -0.5), Point3D(-0.5, -0.1, -0.5), Point3D(-0.5, 0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
    #     pointops.append([Point3D(0.5, 0.1, 0.5), Point3D(-0.5, 0.1, 0.5), Point3D(-0.5, -0.1, 0.5), Point3D(0.5, -0.1, 0.5)])
    #     pointops.append([Point3D(0.5, -0.1, -0.5), Point3D(0.5, -0.1, 0.5), Point3D(-0.5, -0.1, 0.5), Point3D(-0.5, -0.1, -0.5)])
    #     pointops.append([Point3D(-0.5, 0.1, -0.5), Point3D(-0.5, 0.1, 0.5), Point3D(0.5, 0.1, 0.5), Point3D(0.5, 0.1, -0.5)])
    #     pointops.append([Point3D(-0.5, 0.1, -0.5), Point3D(-0.5, -0.1, -0.5), Point3D(-0.5, -0.1, 0.5), Point3D(-0.5, 0.1, 0.5)])
    #     pointops.append([Point3D(0.5, 0.1, 0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.5, -0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
    #     return pointops

    def make_default_fence_shape(self):
        pointops = PointList()
        pointops.append([Point3D(0.1, 0.1, -0.5), Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, -0.1, -0.5), Point3D(0.1, -0.1, -0.5)])
        pointops.append([Point3D(0.1, 0.1, +0.5), Point3D(-0.1, 0.1, 0.5), Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5)])
        pointops.append([Point3D(-0.1, -0.1, -0.5), Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, -0.1, -0.5)])
        pointops.append([Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, 0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, 0.1, -0.5)])
        pointops.append([Point3D(-0.1, -0.1, -0.5), Point3D(-0.1, 0.1, -0.5), Point3D(-0.1, 0.1, 0.5), Point3D(-0.1, -0.1, 0.5)])
        pointops.append([Point3D(0.1, -0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, -0.1, 0.5)])
        return pointops

    def make_default_vertical_plusblock(self):
        pointops = PointList()

        for fordir in xrange(0, 4):
            temperlist = PointList()
            temperlist.append([Point3D(0.5, 0.1, 0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.5, -0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.append([Point3D(0.5, -0.1, -0.5), Point3D(0.1, -0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.append([Point3D(0.5, 0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.5, -0.1, 0.5)])
            temperlist.append([Point3D(0.5, -0.1, -0.5), Point3D(0.5, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, -0.1, -0.5)])
            temperlist.append([Point3D(0.1, 0.1, -0.5), Point3D(0.1, 0.1, 0.5), Point3D(0.5, 0.1, 0.5), Point3D(0.5, 0.1, -0.5)])
            temperlist.rotate_points_z(90*fordir)
            pointops.extend(temperlist)

        pointops.append([Point3D(-0.1, 0.1, -0.5), Point3D(0.1, 0.1, -0.5), Point3D(0.1, -0.1, -0.5), Point3D(-0.1, -0.1, -0.5)])
        pointops.append([Point3D(-0.1, -0.1, 0.5), Point3D(0.1, -0.1, 0.5), Point3D(0.1, 0.1, 0.5), Point3D(-0.1, 0.1, 0.5)])
        return pointops

    def make_default_ladder_shapes(self):
        pointops = PointList()
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.4, -0.5), Point3D(0.5, -0.4, -0.5)])
        pointops.append([Point3D(0.5, -0.4, 0.5), Point3D(-0.5, -0.4, 0.5), Point3D(-0.5, -0.5, 0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(-0.5, -0.4, -0.5), Point3D(-0.5, -0.4, 0.5), Point3D(0.5, -0.4, 0.5), Point3D(0.5, -0.4, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.4, 0.5), Point3D(-0.5, -0.4, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.4, -0.5), Point3D(0.5, -0.4, 0.5), Point3D(0.5, -0.5, 0.5)])
        return pointops

    def make_default_flat_block_shape(self):
        pointops = PointList()
        pointops.append([Point3D(0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, -0.4, -0.5), Point3D(0.4, -0.4, -0.5)])
        pointops.append([Point3D(0.4, 0.4, -0.4), Point3D(-0.4, 0.4, -0.4), Point3D(-0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.4)])
        pointops.append([Point3D(-0.4, -0.4, -0.5), Point3D(-0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.4), Point3D(0.4, -0.4, -0.5)])
        pointops.append([Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.4), Point3D(0.4, 0.4, -0.4), Point3D(0.4, 0.4, -0.5)])
        pointops.append([Point3D(-0.4, -0.4, -0.5), Point3D(-0.4, 0.4, -0.5), Point3D(-0.4, 0.4, -0.4), Point3D(-0.4, -0.4, -0.4)])
        pointops.append([Point3D(0.4, -0.4, -0.5), Point3D(0.4, 0.4, -0.5), Point3D(0.4, 0.4, -0.4), Point3D(0.4, -0.4, -0.4)])
        return pointops

    def make_default_block_shape(self):
        pointops = PointList()
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(0.5, 0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(-0.5, -0.5, -0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, 0.5, 0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, -0.5, -0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, -0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, 0.5, -0.5), Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(-0.5, 0.5, -0.5), Point3D(-0.5, -0.5, -0.5), Point3D(-0.5, -0.5, 0.5), Point3D(-0.5, 0.5, 0.5)])
        pointops.append([Point3D(0.5, 0.5, 0.5), Point3D(0.5, -0.5, 0.5), Point3D(0.5, -0.5, -0.5), Point3D(0.5, 0.5, -0.5)])
        return pointops

class Shapes(object):

    defshapes = None

    def __init__(self, colormaterials):
        self.colormaterials = colormaterials
        self.defshapes = DefaultShapes()

    # will put every model on the right position based on block position
    # or will form the block based on the model in alist, depends how you look at it
    def appendto3dlist(self, alist, block):
        for face in alist:
            for point in face:
                point.append_tup(block)

    def fromfileordefault(self, mat, index, defaultfunction):

        if mat in self.colormaterials and 'models' in self.colormaterials[mat] and index + 1 <= len(self.colormaterials[mat]['models']):
            pointlist = PointList()
            pointlist.from_tuple_list(self.colormaterials[mat]['models'][index])
            pointops = pointlist
        else:
            pointops = defaultfunction()
        return pointops

    def rotatevalue(self, meta, rotate):
        if meta == 3 and rotate > 0:
            meta = -1
        if meta == 0 and rotate < 0:
            meta = 4
        return meta + rotate

    def isperpendicular(self, meta1, meta2):
        rotated = self.rotatevalue(meta2, -1)
        proppernum = meta1 ^ rotated
        return proppernum

    def makestairs(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        if mat in self.colormaterials and 'interneighbor' in self.colormaterials[mat] and self.colormaterials[mat]['interneighbor']:
            removeneibors = False
        else:
            removeneibors = True

        neighborstairs = {}
        for mat_index in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
            if (mat_index, 0) in loneneighbors:
                neighborstairs.update(loneneighbors[(mat_index, 0)])

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']

            somemeta = (loneneighbors[mat][block]['meta'] & 3)
            pointops = PointList()

            shapedone = False
            front = block[0]-1, block[1], block[2]
            back = block[0]+1, block[1], block[2]
            left = block[0], block[1]-1, block[2]
            right = block[0], block[1]+1, block[2]

            if not shapedone and front in neighborstairs and (neighborstairs[front]['meta'] & 3) in [2, 3] and somemeta in [0, 1]:
                shape = self.isperpendicular(somemeta, (neighborstairs[front]['meta'] & 3))
                shapedone = True
                if shape in [0, 3]:
                    pointops = self.fromfileordefault(mat, 1, self.defshapes.make_default_pos_corner_stairs)
                else:
                    pointops = self.fromfileordefault(mat, 2, self.defshapes.make_default_neg_corner_stairs)
                    if (neighborstairs[front]['meta'] & 3) == 2:
                        pointops.rotate_points_z(-90)

                if (neighborstairs[front]['meta'] & 3) == 3:
                    pointops.mirror_points_y()

            if not shapedone and back in neighborstairs and (neighborstairs[back]['meta'] & 3) in [2, 3] and somemeta in [0, 1]:
                shape = self.isperpendicular(somemeta, (neighborstairs[back]['meta'] & 3))
                shapedone = True
                if shape in [0, 3]:
                    pointops = self.fromfileordefault(mat, 2, self.defshapes.make_default_neg_corner_stairs)
                    pointops.rotate_points_z(-90)
                else:
                    pointops = self.fromfileordefault(mat, 1, self.defshapes.make_default_pos_corner_stairs)

                    if (neighborstairs[back]['meta'] & 3) == 2:
                        pointops.mirror_points_y()

            if not shapedone and left in neighborstairs and (neighborstairs[left]['meta'] & 3) in [0, 1] and somemeta in [2, 3]:
                shape = self.isperpendicular(somemeta, (neighborstairs[left]['meta'] & 3))
                shapedone = True
                if shape in [0, 3]:
                    pointops = self.fromfileordefault(mat, 2, self.defshapes.make_default_neg_corner_stairs)
                    if (neighborstairs[left]['meta'] & 3) == 0:
                        pointops.mirror_points_y()
                else:
                    pointops = self.fromfileordefault(mat, 1, self.defshapes.make_default_pos_corner_stairs)

                    if (neighborstairs[left]['meta'] & 3) == 1:
                        pointops.mirror_points_y()

            if not shapedone and right in neighborstairs and (neighborstairs[right]['meta'] & 3) in [0, 1] and somemeta in [2, 3]:
                shape = self.isperpendicular(somemeta, (neighborstairs[right]['meta'] & 3))
                shapedone = True
                if shape in [0, 3]:
                    pointops = self.fromfileordefault(mat, 1, self.defshapes.make_default_pos_corner_stairs)
                    if (neighborstairs[right]['meta'] & 3) == 0:
                        pointops.mirror_points_y()
                else:
                    pointops = self.fromfileordefault(mat, 2, self.defshapes.make_default_neg_corner_stairs)

                    if (neighborstairs[right]['meta'] & 3) == 1:
                        pointops.rotate_points_z(-90)

            if not shapedone:
                pointops = self.defshapes.make_default_normal_stairs()

            direction = loneneighbors[mat][block]['meta'] & 3
            upsidedown = (loneneighbors[mat][block]['meta'] >> 2) & 1

            if direction == 0:
                pointops.rotate_points_z(0)
            elif direction == 1:
                pointops.rotate_points_z(180)
            elif direction == 2:
                pointops.rotate_points_z(270)
            else:
                pointops.rotate_points_z(90)

            if upsidedown:
                pointops.mirror_points_z()

            if removeneibors:
                self.defshapes.remove_neibors(pointops, listoffaces)

            temporigin.append(pointops.get_avg_point().as_tuple())
            self.appendto3dlist(pointops, block)
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def makefence(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']

            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_fence_shape)

            self.defshapes.remove_neibors(pointops, listoffaces)
            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)


    def makeblock(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        if mat in self.colormaterials and 'interneighbor' in self.colormaterials[mat] and self.colormaterials[mat]['interneighbor']:
            removeneibors = False
        else:
            removeneibors = True

        for block in loneneighbors[mat]:

            listoffaces = loneneighbors[mat][block]['faces']
            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_block_shape)
            if removeneibors:
                self.defshapes.remove_neibors(pointops, listoffaces)

            self.appendto3dlist(pointops, block)

            # this below here is not the propper way to do it !
            temporigin.append(pointops.get_avg_point().as_tuple())

            tempfaces += pointops

        return tempfaces, self.getavgorigins(temporigin)

    def getavgorigins(self, origins):
        if len(origins) > 0:
            return [sum(y) / len(y) for y in zip(*origins)]

        return (0, 0, 0)

    def makedoubleslab(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']
            meta = loneneighbors[mat][block]['meta']

            if meta > 7:
                loneneighbors[mat][block]['meta'] -= 7

            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_block_shape)

            self.defshapes.remove_neibors(pointops, listoffaces)
            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def makesnow(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']
            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_block_shape)
            meta = loneneighbors[mat][block]['meta']

            if mat == (78, 0):
                scale = (meta + 1.0) / 8.0
                pointops.scale_points_z(scale)
                pointops.translate_points_z((scale-1)/2)

            self.defshapes.remove_neibors(pointops, listoffaces)
            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())

            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def maketorch(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            # listoffaces = loneneighbors[mat][block]['faces']
            pointops = None
            meta = loneneighbors[mat][block]['meta']
            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_block_shape)

            if meta != 5:
                pointops.translate_points_x(-0.3)

            if meta == 1:
                pointops.rotate_points_y(30)
            if meta == 2:
                pointops.rotate_points_y(30)
                pointops.rotate_points_z(180)
            elif meta == 3:
                pointops.rotate_points_y(30)
                pointops.rotate_points_z(270)
            elif meta == 4:
                pointops.rotate_points_y(30)
                pointops.rotate_points_z(90)

            if pointops:

                # self.defshapes.remove_neibors(pointops, listoffaces)
                self.appendto3dlist(pointops, block)
                temporigin.append(pointops.get_avg_point().as_tuple())

                tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def makehalfblock(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']
            meta = loneneighbors[mat][block]['meta']

            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_half_blocks)

            if meta > 7:
                pointops.rotate_points_y(180)

            self.defshapes.remove_neibors(pointops, listoffaces)
            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def makeverticalblock(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']
            left = block[0]-1, block[1], block[2]
            right = block[0]+1, block[1], block[2]
            front = block[0], block[1]-1, block[2]
            back = block[0], block[1]+1, block[2]

            if mat in self.colormaterials and 'models' in self.colormaterials[mat]:
                pointlist = PointList()
                pointlist.from_tuple_list(self.colormaterials[mat]['models'][0])
                pointops = pointlist
            else:
                pointops = self.defshapes.make_default_flat_blocks()

            if front in loneneighbors[mat] or back in loneneighbors[mat]:
                pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_vertical_plusblock)
                pointops.rotate_points_z(90)
            elif left in loneneighbors[mat] or right in loneneighbors[mat]:
                pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_vertical_plusblock)
            elif left in loneneighbors[mat] and right in loneneighbors[mat] and front in loneneighbors[mat] and back in loneneighbors[mat]:
                pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_vertical_plusblock)
            else:
                pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_vertical_plusblock)

            self.defshapes.remove_neibors(pointops, listoffaces)
            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)

    def makeladderlikeblock(self, loneneighbors, mat):
        temporigin = []
        tempfaces = []

        for block in loneneighbors[mat]:
            listoffaces = loneneighbors[mat][block]['faces']

            pointops = self.fromfileordefault(mat, 0, self.defshapes.make_default_ladder_shapes)

            direction = loneneighbors[mat][block]['meta'] & 3

            if direction == 0:
                pointops.rotate_points_z(90)
            elif direction == 1:
                pointops.rotate_points_z(-90)
            elif direction == 2:
                pointops.rotate_points_z(0)
            else:
                pointops.rotate_points_z(180)

            self.defshapes.remove_top_down_neighbors(pointops, listoffaces)

            self.appendto3dlist(pointops, block)
            temporigin.append(pointops.get_avg_point().as_tuple())
            tempfaces += pointops
        return tempfaces, self.getavgorigins(temporigin)
