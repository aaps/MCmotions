#!/usr/bin/python -B

import operator
import ast

import base64
import struct
import sys, getopt

import time
import math
# from collections import OrderedDict
import pickle


sourcefile = "default.dump"
destfile = "default.mcmo"

avgmiddle = False
norenderents = ["none"]
norenderblocks = ["none"]

noentitys = False
nochunks = False
onlyplayerents = False
curscene = "noscene"
world = "overworld"
cuty = 0
cutz = (-1000,1000)
cutx = (-1000,1000)
multymatblocks = [35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171]


try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","sourcefile=","destfile=","scene=", "excludeent=","excludeblocks=","cutx=","cuty=","cutz=","noentitys=","nochunks=","onlyplayerents=", "world=" ])
        
except getopt.GetoptError:
    print 'error: lister.py --onlyplayerents --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --world nether/overworld/theend will only use this world'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'lister.py --onlyplayerents --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --world nether/overworld/theend will only use this world'
        sys.exit()

    if opt == "--onlyplayerents":
        onlyplayerents = True

    if opt == "--sourcefile":
        sourcefile = arg

    if opt == "--destfile":
        destfile = arg

    if opt == "--scene":
        curscene = arg

    if opt == "--avgmiddle":
        # print arg
        if arg == 'yes':
            avgmiddle = True

    if opt == "--excludeent":
        norenderents = arg.split(",")

    if opt == "--excludeblocks":
        norenderblocks = arg.split(",")
        norenderblocks = map(int, norenderblocks)

    if opt == "--cutz":
        cutz = ast.literal_eval(arg)

    if opt == "--cutx":
        cutx = ast.literal_eval(arg)

    if opt == "--cuty":
        cuty = ast.literal_eval(arg)

    if opt == "--noentitys":
        noentitys = True

    if opt == "--world":
        
        if arg == "nether":
            world = 2
        elif arg == "theend":
            world = 3
        else:
            world = 1

    if opt == "--nochunks":
        nochunks = True



allhistory = {0:{'type':'player','positions':[]}}
allblocks = {}



lostcounter = []

# f = open(destfile, 'wb')

try:
    origin = open(sourcefile, 'r')
except Exception as e:
    print e
    print 'try it with --sourcefile dumpfile'
    exit()


total = origin.read()

aroflines = total.split('\n')

chunks = {}
chunkposses = []

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
    
    def append(self, tup):
        self.x += tup[0]
        self.y += tup[1]
        self.z += tup[2]

    def mirrorX(self):
        x = round(self.x * -1)
        return Point3D(x, self.y, self.z)

    def mirrorY(self):
        y = round(self.y * -1)
        return Point3D(self.x, y, self.z)

    def mirrorZ(self):
        z = round(self.z * -1)
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

def mirrorpointsX(alist):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            
            templist.append(point.mirrorX())
        tempfinal.append(templist)
    return tempfinal

def mirrorpointsY(alist):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            
            templist.append(point.mirrorY())
        tempfinal.append(templist)
    return tempfinal

def mirrorpointsZ(alist):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            
            templist.append(point.mirrorZ())
        tempfinal.append(templist)
    return tempfinal

def rotatepointsY(alist, angle):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            
            templist.append(point.rotateY(angle))
        tempfinal.append(templist)
    return tempfinal

def rotatepointsX(alist, angle):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            
            templist.append(point.rotateX(angle))
        tempfinal.append(templist)
    return tempfinal

def rotatepointsZ(alist, angle):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            templist.append(point.rotateZ(angle))
        tempfinal.append(templist)
    return tempfinal

def appendto3dlist(alist, block):
    for face in alist:
        for point in face:
            point.append(block) 

def totuplelist(alist):
    tempfinal = []
    for face in alist:
        templist = []
        for point in face:
            templist.append( point.astuple() )
        tempfinal.append(templist)
    return tempfinal

def makenormalstairs(loneneighbors, mat):
    loweplane = [Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)]
    firststep = [Point3D(0,0.5,0.5),Point3D(0.5,0.5,0.5),Point3D(0.5,-0.5,0.5),Point3D(0,-0.5,0.5)]
    secondstep = [Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(0,-0.5,0)]
    inbetween = [Point3D(0,0.5,0),Point3D(0,-0.5,0),Point3D(0,-0.5,0.5),Point3D(0,0.5,0.5)]
    frontpiece = [Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)]
    backplane = [Point3D(0.5,0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5),Point3D(0.5,0.5,0.5)]
    rightplane = [Point3D(0,0.5,0.5),Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)]
    leftplane = [Point3D(0,-0.5,0.5),Point3D(0,-0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5)]
    finallist = [ loweplane, firststep, secondstep, inbetween, frontpiece, backplane, rightplane, leftplane]
    return finallist

def makeposcornerstairs(loneneighbors, mat):
    loweplane = [Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)]
    firststep = [Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0), Point3D(0.5,-0.5,0), Point3D(0.5,0,0),Point3D(0,0,0)]
    frontpiece1 = [Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)]
    frontpiece2 = [Point3D(0.5,-0.5,0), Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)]
    triplane1 = [Point3D(0,0.5,0.5),Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)]
    triplane2 = [Point3D(0.5,0,0.5),Point3D(0.5,0,0),Point3D(0.5,-0.5,0),Point3D(0.5,-0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)]
    smalplanetop = [Point3D(0.5,0.5,0.5),Point3D(0,0.5,0.5),Point3D(0,0,0.5),Point3D(0.5,0,0.5)]
    smalplaneside1 = [Point3D(0,0,0),Point3D(0,0.5,0),Point3D(0,0.5,0.5),Point3D(0,0,0.5)]
    smalplaneside2 = [Point3D(0,0,0),Point3D(0.5,0,0),Point3D(0.5,0,0.5),Point3D(0,0,0.5)]
    finallist = [loweplane, firststep, frontpiece1, frontpiece2, triplane1, triplane2, smalplanetop, smalplaneside1, smalplaneside2]
    return finallist

def makenegcornderstairs(loneneighbors, mat):
    loweplane = [Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)]
    firststep = [Point3D(0,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(0,-0.5,0)]
    frontpiece = [Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5)]
    triplane1 = [Point3D(0,-0.5,0.5),Point3D(0,-0.5,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5)]
    triplane2 = [Point3D(-0.5,0,0.5),Point3D(-0.5,0,0),Point3D(-0.5,-0.5,0),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,0.5)]
    finallist = [loweplane, firststep, frontpiece, triplane1, triplane2]
    return finallist

def makestairs(loneneighbors, mat):

    for block in loneneighbors[mat]:
        left = block[0]-1, block[1], block[2]
        right = block[0]+1, block[1], block[2]
        front = block[0], block[1]-1, block[2]
        back = block[0], block[1]+1, block[2]

        somemeta = (loneneighbors[mat][block]['meta'] & 3) + 1
        finallist = []

        if left in loneneighbors[mat] and ((loneneighbors[mat][left]['meta'] & 3) + 1) != somemeta and somemeta == 2:
            finallist = makeposcornerstairs(loneneighbors, mat)
            thesum = (loneneighbors[mat][left]['meta'] & 3) + 1
            print str(somemeta) + '+' + str(thesum) + ' % =' + str((somemeta + thesum) % 2)
        elif right in loneneighbors[mat] and ((loneneighbors[mat][right]['meta'] & 3) + 1) != somemeta and somemeta == 1:
            finallist = makeposcornerstairs(loneneighbors, mat) 
            thesum = (loneneighbors[mat][right]['meta'] & 3) + 1
            print str(somemeta) + '+' + str(thesum) + ' % =' + str((somemeta + thesum) % 2)
        elif front in loneneighbors[mat] and ((loneneighbors[mat][front]['meta'] & 3) + 1) != somemeta and somemeta == 3:
            finallist = makeposcornerstairs(loneneighbors, mat)
            thesum = (loneneighbors[mat][front]['meta'] & 3) + 1
            print str(somemeta) + '+' + str(thesum) + ' % =' + str((somemeta + thesum) % 2)
        elif back in loneneighbors[mat] and ((loneneighbors[mat][back]['meta'] & 3) + 1) != somemeta and somemeta == 4: 
            finallist = makeposcornerstairs(loneneighbors, mat)
            thesum = (loneneighbors[mat][back]['meta'] & 3) + 1
            print str(somemeta) + '+' + str(thesum) + ' % =' + str((somemeta + thesum) % 2)
        # else:
        #     finallist = makenormalstairs(loneneighbors, mat)

        direction = loneneighbors[mat][block]['meta'] & 3
        upsidedown = (loneneighbors[mat][block]['meta'] >> 2) & 1

        if direction  ==  0:
            finallist = rotatepointsZ(finallist, 0)
            if upsidedown:
                finallist = rotatepointsX(finallist, 180)
        elif direction == 1:
            finallist = rotatepointsZ(finallist, 180)
            if upsidedown:
                finallist = rotatepointsX(finallist, 180)
        elif direction == 2:
            finallist = rotatepointsZ(finallist, 270)
            if upsidedown:
                finallist = rotatepointsY(finallist, 180)
        else:
            finallist = rotatepointsZ(finallist, 90)
            if upsidedown:
                finallist = rotatepointsY(finallist, 180)

        
        

        appendto3dlist(finallist, block)
        finallist = totuplelist(finallist)
        faces[mat] += finallist
        

def makefence(loneneighbors, mat):
    
    for block in loneneighbors[mat]:

        loweplane = [Point3D(0.1,0.1,-0.5),Point3D(-0.1,0.1,-0.5),Point3D(-0.1,-0.1,-0.5),Point3D(0.1,-0.1,-0.5)]
       
        upperplane = [Point3D(0.1,0.1,+0.5),Point3D(-0.1,0.1,0.5),Point3D(-0.1,-0.1,0.5),Point3D(0.1,-0.1,0.5)]
        
        leftplane = [Point3D(-0.1,-0.1,-0.5),Point3D(-0.1,-0.1,0.5),Point3D(0.1,-0.1,0.5),Point3D(0.1,-0.1,-0.5)]

        rightplane = [Point3D(-0.1,0.1,-0.5),Point3D(-0.1,0.1,0.5),Point3D(0.1,0.1,0.5),Point3D(0.1,0.1,-0.5)]
        
        backplane = [Point3D(-0.1,-0.1,-0.5),Point3D(-0.1,0.1,-0.5),Point3D(-0.1,0.1,0.5),Point3D(-0.1,-0.1,0.5)]

        frontplane = [Point3D(0.1,-0.1,-0.5),Point3D(0.1,0.1,-0.5),Point3D(0.1,0.1,0.5),Point3D(0.1,-0.1,0.5)]
        
        finallist = [loweplane, upperplane, leftplane, rightplane, backplane, frontplane]
        appendto3dlist(finallist, block)
        finallist = totuplelist(finallist)
        faces[mat] += finallist

def makeblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        templist = []

        if 5 in listoffaces:
            templist.append([Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(-0.5,-0.5,-0.5)])

        if 6 in listoffaces:
            templist.append([Point3D(-0.5,0.5,0.5),Point3D(0.5,0.5,0.5),Point3D(0.5,-0.5,0.5),Point3D(-0.5,-0.5,0.5)])

        if 3 in listoffaces:
            templist.append([Point3D(-0.5,-0.5,0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5)])

        if 4 in listoffaces:
            templist.append([Point3D(-0.5,0.5,0.5),Point3D(-0.5,0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5)])
            
        if 1 in listoffaces:
            templist.append([Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.5,0.5),Point3D(-0.5,0.5,0.5)])
            
        if 2 in listoffaces:
            templist.append([Point3D(0.5,0.5,-0.5),Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.5,0.5),Point3D(0.5,0.5,0.5)])
        
        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist


def makehalfblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        templist = []

        if 5 in listoffaces:
            templist.append([Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])


        if 6 in listoffaces:
            templist.append([Point3D(0.5,0.5,0),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0),Point3D(0.5,-0.5,0)])


        if 3 in listoffaces:
            templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.5,0),Point3D(0.5,-0.5,0),Point3D(0.5,-0.5,-0.5)])


        if 4 in listoffaces:
            templist.append([Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,0),Point3D(0.5,0.5,0),Point3D(0.5,0.5,-0.5)])


        if 1 in listoffaces:
            templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,0),Point3D(-0.5,-0.5,0)])
 

        if 2 in listoffaces:
            templist.append([Point3D(0.5,-0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0),Point3D(0.5,-0.5,0)])

        if loneneighbors[mat][block]['meta'] > 7:
            templist = rotatepointsY(templist, 180)

        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist

def makeflatblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        templist = []

        if 5 in listoffaces:
            templist.append([Point3D(0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])

        if 6 in listoffaces:
            templist.append([Point3D(0.5,0.5,-0.4),Point3D(-0.5,0.5,-0.4),Point3D(-0.5,-0.5,-0.4),Point3D(0.5,-0.5,-0.4)])

        if 3 in listoffaces:
            templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.5,-0.4),Point3D(0.5,-0.5,-0.4),Point3D(0.5,-0.5,-0.5)])

        if 4 in listoffaces:
            templist.append([Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.4),Point3D(0.5,0.5,-0.4),Point3D(0.5,0.5,-0.5)])

        if 1 in listoffaces:
            templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,-0.4),Point3D(-0.5,-0.5,-0.4)])

        if 2 in listoffaces:
            templist.append([Point3D(0.5,-0.5,-0.5),Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,-0.4),Point3D(0.5,-0.5,-0.4)])

        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist

def makeverticalflatblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        templist = []

        templist.append([Point3D(0.5,-0.4,-0.5),Point3D(-0.5,-0.4,-0.5),Point3D(-0.5,-0.5,-0.5),Point3D(0.5,-0.5,-0.5)])

        templist.append([Point3D(0.5,-0.4,0.5),Point3D(-0.5,-0.4,0.5),Point3D(-0.5,-0.5,0.5),Point3D(0.5,-0.5,0.5)])

        templist.append([Point3D(-0.5,-0.4,-0.5),Point3D(-0.5,-0.4,0.5),Point3D(0.5,-0.4,0.5),Point3D(0.5,-0.4,-0.5)])

        templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.5,0.5),Point3D(0.5,-0.5,0.5),Point3D(0.5,-0.5,-0.5)])

        templist.append([Point3D(-0.5,-0.5,-0.5),Point3D(-0.5,-0.4,-0.5),Point3D(-0.5,-0.4,0.5),Point3D(-0.5,-0.5,0.5)])

        templist.append([Point3D(0.5,-0.5,-0.5),Point3D(0.5,-0.4,-0.5),Point3D(0.5,-0.4,0.5),Point3D(0.5,-0.5,0.5)])

        direction = loneneighbors[mat][block]['meta'] & 3

        if direction == 0:
            templist = rotatepointsZ(templist, 90)
        elif direction == 1:
            templist = rotatepointsZ(templist, -90)
        elif direction == 2:
            templist = rotatepointsZ(templist, 0)
        else:
            templist = rotatepointsZ(templist, 180)


        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist


def makesmallflatblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        templist = []

        templist.append([Point3D(0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.5),Point3D(-0.4,-0.4,-0.5),Point3D(0.4,-0.4,-0.5)])

        templist.append([Point3D(0.4,0.4,-0.4),Point3D(-0.4,0.4,-0.4),Point3D(-0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.4)])

        templist.append([Point3D(-0.4,-0.4,-0.5),Point3D(-0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.4),Point3D(0.4,-0.4,-0.5)])

        templist.append([Point3D(-0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.4),Point3D(0.4,0.4,-0.4),Point3D(0.4,0.4,-0.5)])

        templist.append([Point3D(-0.4,-0.4,-0.5),Point3D(-0.4,0.4,-0.5),Point3D(-0.4,0.4,-0.4),Point3D(-0.4,-0.4,-0.4)])

        templist.append([Point3D(0.4,-0.4,-0.5),Point3D(0.4,0.4,-0.5),Point3D(0.4,0.4,-0.4),Point3D(0.4,-0.4,-0.4)])

        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist
 
def makexblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        templist = []
        templist.append([Point3D(0.5,0.5,-0.5),Point3D(0.5,0.5,0.5),Point3D(-0.5,-0.5,0.5),Point3D(-0.5,-0.5,-0.5)])
        templist.append([Point3D(-0.5,0.5,-0.5),Point3D(-0.5,0.5,0.5),Point3D(0.5,-0.5,0.5),Point3D(0.5,-0.5,-0.5)])

        appendto3dlist(templist, block)    
        templist = totuplelist(templist)

        faces[mat] += templist

def worldfromsample(sample):
    overworldblocks = [1,2,3,4,6,8,9,12,13, 15,16,17,18,37,38,39,40]
    netherblocks = [10,11,87,88, 112,113,114,115,153]
    theendblocks = [121]
    overscore = 0
    endscore = 0
    netherscore = 0

    for block in sample:
        if block in overworldblocks:
            overscore += 1
        if block in netherblocks:
            netherscore += 1
        if block in theendblocks:
            endscore += 1

    if endscore > overscore and endscore > netherscore:
        return 3
    elif netherscore > endscore and netherscore > overscore:
        return 2
    else:
        return 1



def getchunks():
    if row[5] != 'None':

        chunkdata = base64.standard_b64decode(row[5])
        xzpos = ast.literal_eval(row[1])
        matsamples = []
        
        for x in xrange(1,17):
            
            if len(chunkdata[(256*x):(256*x)+2]) == 2:
                temp = struct.unpack('H', chunkdata[(256*x):(256*x)+2])[0]
                matsamples.append(temp >> 4)
        matsamples = list(set(matsamples))
        worldnum = worldfromsample(matsamples)

        if xzpos not in chunkposses and xzpos[0] >= cutx[0] and xzpos[0] <= cutx[1] and xzpos[1] >= cutz[0] and xzpos[1] <= cutz[1] and world == worldnum:
            chunkposses.append(xzpos)
            rightcounter = 0

            for index1 in xrange(0, 16):
                
                if (int(row[3]) & (1 << index1)) and index1 >= cuty and row[3] != '0':
                    
                    for y in xrange(0,16):

                        for z in xrange(0,16):
                            for x in xrange(0,16):
                                goodindex = (x+(z*16)+(y*256)+(rightcounter*4096))*2
                                
                                try:
                                    temp = struct.unpack('H',chunkdata[goodindex:goodindex+2])[0]
                                    btype = temp >> 4
                                    bmeta = temp & 15

                                except Exception as e:
                                    btype = 666
                                    bmeta = 666
                                
                                block = ( (x + (xzpos[0]*16),z + (xzpos[1]*16),y+(index1*16)), btype, bmeta)
                                chunks[row[1]]['blocks'].append(block)
                    rightcounter += 1
                    # print rightcounter

def filterents(allhistory):

    temphistory = {}

    for x in allhistory:
        allhistory[x]['positions'] = sorted(allhistory[x]['positions'], key=lambda positions: positions['time'])
        temphistory[x] = {'positions':[],'type':allhistory[x]['type']}

        for position in allhistory[x]['positions']:
            
            if position['scene'] == curscene  or curscene == 'noscene' or position['alive'] == 0:
                temphistory[x]['positions'].append(position)

    return temphistory

def filterstatics(allhistory):
    temphistory = {}
    print 'Filtering entitys that dont move at all'

    for x in allhistory:

        if len(allhistory[x]['type']) > 35:
            if len(allhistory[x]['positions']) > 10:
                temphistory[x] = allhistory[x]
        else:
            temphistory[x] = allhistory[x]

    return temphistory

def getMaxMinTime(allhistory):

    maxtime = 0
    mintime = 1000000

    for x in allhistory:
        for position in allhistory[x]['positions']:
            if position['time'] > maxtime:
                maxtime =position['time']
            if position['time'] < mintime:
                mintime = position['time']

    for x in allhistory:
        for position in allhistory[x]['positions']:    
            position['time'] = position['time'] - mintime
    return maxtime, mintime


def makematindexes(chunks):
    wrongblocks = False
    materials = {}
    for chunk in chunks:
        for block in chunks[chunk]:
            if len(chunks[chunk][block]) > 0:
                for x in chunks[chunk][block]:
                    if x[1] > 0 and x[1] < 256 and x[1] not in norenderblocks:
                        
                        if x[1] in multymatblocks:
                            matblock = {(x[1], x[2]) :{}}
                        else:
                            matblock = {(x[1],0):{}}
                        materials.update(matblock)
                    elif x[1] < 256:
                        wrongblocks = True

    if wrongblocks:
        print 'there are wrong block types found, there is a good change the parsing in the proxy fase whent wrong !'
    return materials

def fillmatindexes(chunks, materials):
    for chunk in chunks:

        for block in chunks[chunk]:
            if len(chunks[chunk][block]) > 0:
                
                for x in chunks[chunk][block]:
                    position = x[0][0],x[0][1]*-1,x[0][2]
                    if x[1] > 0 and x[1] < 256 and x[1] not in norenderblocks:
                        if x[1] in multymatblocks:
                            materials[(x[1], x[2]) ].update({position:{'meta':x[2],'faces':[]}})
                        else:
                            materials[(x[1],0)].update({position:{'meta':x[2],'faces':[]}})
            chunks[chunk][block] = None

    chunks = None
    return materials


def genfacesNeighbors(materials):
    neightbors = {}

    print 'find material neightbors for ' + str(len(materials)) + ' materials'         
    for mat in materials:
        neightbors[mat] = {}


    for mat in materials:
        
        for block in materials[mat]:
            neightbors[mat][block] = {'meta': materials[mat][block]['meta'],'faces':[]}
            if (block[0]-1, block[1], block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(1)
            if (block[0]+1, block[1], block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(2)
            if (block[0], block[1]-1, block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(3)
            if (block[0], block[1]+1, block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(4)
            if (block[0], block[1], block[2]-1) not in materials[mat]:
                neightbors[mat][block]['faces'].append(5)
            if (block[0], block[1], block[2]+1) not in materials[mat]:
                neightbors[mat][block]['faces'].append(6)
            
        materials[mat] = None

    return neightbors

def removeSupderCosy(neightbors):
    loneneighbors = {}
    for mat in neightbors:
        loneneighbors[mat] = {}
        for block in neightbors[mat]:

            if len(neightbors[mat][block]['faces']) > 0:
                loneneighbors[mat][block[0]+0.5, block[1]+0.5, block[2]+0.5]  = neightbors[mat][block]
        neightbors[mat] = None
    return loneneighbors


def fido(first, second): 
    y = 180 - abs(abs(first[0] - second[0]) - 180)
    p = 180 - abs(abs(first[1] - second[1]) - 180)
    if len(first) > 2 and len(second) > 2:
        h = 180 - abs(abs(first[2] - second[2]) - 180)

        return (y,p,h)
    return (y,p)
    
offset = (0,0,0)
if avgmiddle:
    allposses = []
    for line in aroflines:
        row = line.split('|')
        if 'spawn' in row[0]:
            goodpos = ast.literal_eval(row[5])
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
            allposses.append(goodpos)

    lentotal = len(allposses)
    total = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), allposses)
    offset = (total[0]/lentotal, total[1]/lentotal, total[2]/lentotal)
    print 'offset:' + str(offset)

 

for line in aroflines:
    
    row = line.split('|')

        
    if not noentitys and 'spawn' in row[0] and row[4] not in norenderents and not noentitys:
        
        if not onlyplayerents:
            
            goodpos = ast.literal_eval(row[5])
            rawyawpichhead = ast.literal_eval(row[6])
            if len(rawyawpichhead) > 2:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
            else:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
            
            mob = {int(row[3]):{'type':row[4],'positions':[{'time':int(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1,'scene':'noscene'}]}}

            allhistory.update(mob)

        elif 'player' in row[0]:

            goodpos = ast.literal_eval(row[5])
            rawyawpichhead = ast.literal_eval(row[6])
            if len(rawyawpichhead) > 2:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
            else:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
            
            mob = {int(row[3]):{'type':row[4],'positions':[{'time':int(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1,'scene':'noscene'}]}}

            allhistory.update(mob)

    elif row[0] == 'playerpos' and not noentitys:
        posses = ast.literal_eval(row[3])
        posses = posses[0],posses[1],posses[2]*-1
        lastlist = allhistory[0]['positions'][-1]
        allhistory[0]['positions'].append({'time':int(row[1]),'pos':posses,'yawpichhead':lastlist['yawpichhead'],'status':0,'alive':1,'scene':row[2]})

    elif row[0] == 'playerposlook' and not noentitys:
        posses = ast.literal_eval(row[3])
        posses = posses[0],posses[1],posses[2]*-1
        look = ast.literal_eval(row[4])
        look = look[0]*-1,look[1]

        
        allhistory[0]['positions'].append({'time':int(row[1]),'pos':posses,'yawpichhead':look,'status':0,'alive':1,'scene':row[2]})

    elif row[0] == 'playerlook' and not noentitys:
       
        look = ast.literal_eval(row[3])
        look = look[0]*-1,look[1]
        lastlist = allhistory[0]['positions'][-1]
        allhistory[0]['positions'].append({'time':int(row[1]),'pos':lastlist['pos'],'yawpichhead':look,'status':0,'alive':1,'scene':row[2]})

    elif row[0] == 'entityrelmove' and int(row[3]) in allhistory and not noentitys:
        
        lastlist = allhistory[int(row[3])]['positions'][-1]
        posses = ast.literal_eval(row[4])
        posses = posses[0]/32,posses[1]/32,posses[2]/32
        absolutepos = tuple(map(operator.add, lastlist['pos'], posses))

        allhistory[int(row[3])]['positions'].append({'time':int(row[1]),'pos':absolutepos,'yawpichhead':lastlist['yawpichhead'],'status':0,'alive':lastlist['alive'],'scene':row[2]})

    elif row[0] == 'entitylookandrelmove' and int(row[3]) in allhistory and  not noentitys:
        
        lastlist = allhistory[int(row[3])]['positions'][-1]
        posses = ast.literal_eval(row[4])
        posses = posses[0]/32,posses[1]/32,posses[2]/-32
        absolutepos = tuple(map(operator.add, lastlist['pos'], posses))
        yawpich = ast.literal_eval(row[5])
        
        if len(lastlist['yawpichhead']) > 2:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360,lastlist['yawpichhead'][2]
        else:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360
        yawpichhead = fido(lastlist['yawpichhead'], yawpichhead)

        allhistory[int(row[3])]['positions'].append({'time':int(row[1]),'pos':absolutepos,'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive'],'scene':row[2]})

    elif row[0] == 'entityheadlook' and int(row[3]) in allhistory and  not noentitys:
        
        lastlist = allhistory[int(row[3])]['positions'][-1]
        
        if len(lastlist['yawpichhead']) > 2:
            if not ast.literal_eval(row[4]) == lastlist['yawpichhead'][2]:
            
                yawpichhead = lastlist['yawpichhead'][0], lastlist['yawpichhead'][1], (ast.literal_eval(row[4])+ 5) % 360

            yawpichhead = fido(yawpichhead, lastlist['yawpichhead'])

            allhistory[int(row[3])]['positions'].append({'time':int(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive'],'scene':row[2]})


    elif row[0] == 'entityteleport' and int(row[3]) in allhistory and not noentitys:
        
        goodpos = ast.literal_eval(row[4])
        goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
        
        lastlist = allhistory[int(row[3])]['positions'][-1]
        yawpich = ast.literal_eval(row[4])
        if len(lastlist['yawpichhead']) > 2:
            yawpichhead = (yawpich[0]+ 5) % 360, (yawpich[1]+ 5) % 360, lastlist['yawpichhead'][2]
        else:
            yawpichhead = (yawpich[0]+ 5) % 360, (yawpich[1]+ 5) % 360
        
        yawpichhead = fido( yawpichhead, lastlist['yawpichhead'])
        
        allhistory[int(row[3])]['positions'].append({'time':int(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)),'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive'],'scene':row[2]})

    elif row[0] == 'entitystatus' and int(row[3]) in allhistory and not noentitys:
        
        lastlist = allhistory[int(row[3])]['positions'][-1]
        if lastlist['status'] == row[4]:
            allhistory[int(row[3])]['positions'].append({'time':int(row[1]),'pos':lastlist['pos'],'yawpichhead':lastlist['yawpichhead'],'status':row[4],'alive':lastlist['alive'],'scene':row[2]})

    elif row[0] == 'destroyents' and not noentitys:
        entids = row[3:]
        
        for entid in entids:
            if entid in allhistory:
                lastlist = allhistory[entid]['positions'][-1]
                allhistory[entid]['positions'].append({'time':int(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0 ,'alive':0,'scene':'noscene'})

    elif row[0] == 'chunkdata':
        length = row[3]
        
        chunks.update({row[1]:{'blocks':[]}})
        if not nochunks:
            getchunks()

    
print 'Filtering entitys that are not supposed to be in scene move at all'

allhistory = filterents(allhistory)

allhistory = filterstatics(allhistory)

print getMaxMinTime(allhistory)

print 'parsing ' + str(len(chunkposses)) + ' chunks'

# put it in material array instead of chunk arrays

print 'make a index of possible materials'

materials = makematindexes(chunks)

print str(len(chunks)) +  ' length of chunks'

print 'put the blocks of materials in their material index for ' + str(len(materials)) + ' materials'

materials = fillmatindexes(chunks, materials)



# print 'removing all super neightbors, same type blocks on all sides for ' + str(len(neightbors)) + ' materials'         

neightbors = genfacesNeighbors(materials)

loneneighbors = removeSupderCosy(neightbors)

print 'generating face positions ' + str(len(loneneighbors)) + ' materials'
faces = {}
vertices = {}

for mat in loneneighbors:
    faces[mat] = []
    vertices[mat] = []
    if mat[0] in [182 ,126 ,44]:
        makehalfblock(loneneighbors, mat)
    elif mat[0] in [171, 111]:
        makeflatblock(loneneighbors, mat)
    elif mat[0] in [65, 106]:
        makeverticalflatblock(loneneighbors, mat)
    elif mat[0] in [148, 147]:
        makesmallflatblock(loneneighbors, mat)
    elif mat[0] in [6 , 111 , 30 , 31 , 32,37,40, 51, 83, 175]:
        makexblock(loneneighbors, mat)
    elif mat[0] in [85, 113,188, 189, 190, 191]:
        makefence(loneneighbors, mat)
    elif mat[0] in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
        makestairs(loneneighbors, mat)
    else:
        makeblock(loneneighbors, mat)
    

    loneneighbors[mat] = []

print 'generating the vertices'

for mat in faces:
    for forverts in faces[mat]:
        for vert in forverts:
            vertices[mat].append(vert)

for mat in vertices:
    vertices[mat] = list(set(vertices[mat]))
    vertices[mat] = sorted(vertices[mat])

newfaces = {}

print 'linking the vert index to the faces, this will take the most time !!!'

for mat in faces:
    newfaces[mat] = []
    timenow = None
    vertcache = {}
    
    for index, vert in enumerate(vertices[mat]):
        vertcache.update({vert:index})

    for forverts in faces[mat]:
        tempface = []

        for vert in forverts:
            if vert in vertcache:
                tempface.append(vertcache[vert])     
        newfaces[mat].append(tempface)
      
faces = newfaces
newface = None
loneneighbors = None

allstuff = {'allhistory':allhistory,'vertices':vertices,'faces':faces}

vertices = None
faces = None

print 'entitys with spawnmessage:' + str(len(allhistory)) + ',so used !'
print 'entitys without spawnmessage:' + str(len(lostcounter)) + ',so ignored !'

with open(destfile, 'wb') as handle:
    pickle.dump(allstuff, handle)
