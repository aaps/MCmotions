#!/usr/bin/python -B

import operator
import ast
import base64
import struct
import sys, getopt
import time
import math
import pickle
from points import *
from shapes import *
import json
from materials import *
import copy


sourcefile = "default.dump"
destfile = "default.mcmo"

avgmiddle = False
norenderents = ["none"]
norenderblocks = ["none"]

noentitys = False
nochunks = False
onlyplayerents = False
curscene = "noscene"
world = 1
cuty = 0
topleft = (-1000,-1000)
bottomright = (1000,1000)
multymatblocks = [35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171]
shapemaker = Shapes()
colormaterials = defmaterials

try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","materialsfile=","sourcefile=","destfile=","scene=", "excludeent=","excludeblocks=","CTL=","CBR=","cutz=","noentitys=","nochunks=","onlyplayerents=", "world=" ])
        
except getopt.GetoptError:
    print 'error: lister.py --onlyplayerents --materialsfile --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --world nether/overworld/theend will only use this world'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'lister.py --onlyplayerents --materialsfile --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --world nether/overworld/theend will only use this world'
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

    if opt == "--materialsfile":

        materalsfile = open(arg, 'r')
        materialsstring = materalsfile.read().replace("}\n", "}")
        colormaterials = ast.literal_eval(materialsstring)
        textures = colormaterials["textures"]
        colormaterials = colormaterials["materials"]
        

    if opt == "--excludeblocks":
        norenderblocks = arg.split(",")
        norenderblocks = map(int, norenderblocks)

    if opt == "--CTL":
        topleft = ast.literal_eval(arg)


    if opt == "--CBR":
        bottomright = ast.literal_eval(arg)

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



pointops = PointList()


# will put every model on the right position based on block position
# or will form the block based on the model in alist, depends how you look at it
def appendto3dlist(alist, block):
    for face in alist:
        for point in face:
            point.appendtup(block)

def fromfileordefault(mat, index, defaultfunction):

    if mat in colormaterials and 'models' in colormaterials[mat] and index + 1 <= len(colormaterials[mat]['models']):
        pointlist = PointList()
        pointlist.fromtuplelist(colormaterials[mat]['models'][index])
        pointops = pointlist
    else:
        pointops = defaultfunction()
    return pointops

def makestairs(loneneighbors, mat):

    for block in loneneighbors[mat]:
        # left = block[0]-1, block[1], block[2]
        # right = block[0]+1, block[1], block[2]
        # front = block[0], block[1]-1, block[2]
        # back = block[0], block[1]+1, block[2]
        # listoffaces = loneneighbors[mat][block]['faces']

        somemeta = (loneneighbors[mat][block]['meta'] & 3) + 1
        pointops = PointList()

        if somemeta == 1:
            front = block[0]-1, block[1], block[2]
            back = block[0]+1, block[1], block[2]

        elif somemeta == 2:
            front = block[0]+1, block[1], block[2]
            back = block[0]-1, block[1], block[2]

        elif somemeta == 3:
            front = block[0], block[1]-1, block[2]
            back = block[0], block[1]+1, block[2]

        elif somemeta == 4:
            front = block[0], block[1]+1, block[2]
            back = block[0], block[1]-1, block[2]

        if front in loneneighbors[mat] and  abs(somemeta - ((loneneighbors[mat][front]['meta'] & 3) + 1)):
            pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
            # if (loneneighbors[mat][front]['meta'] & 3) + 1 == 3:
            #     pointops.mirrorpointsY()

        elif back in loneneighbors[mat] and abs(somemeta - ((loneneighbors[mat][back]['meta'] & 3) + 1)):
            pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
            # if (loneneighbors[mat][back]['meta'] & 3) + 1 != 3:
            #     pointops.mirrorpointsY() 

        # if left in loneneighbors[mat] and ((loneneighbors[mat][left]['meta'] & 3) + 1) != somemeta and somemeta == 2:
        #     pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
        #     if (loneneighbors[mat][left]['meta'] & 3) + 1 != 3:
        #         pointops.mirrorpointsY()
            
        # elif right in loneneighbors[mat] and ((loneneighbors[mat][right]['meta'] & 3) + 1) != somemeta and somemeta == 1:
        #     pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
        #     if (loneneighbors[mat][right]['meta'] & 3) + 1 == 3:
        #         pointops.mirrorpointsY()

        # elif front in loneneighbors[mat] and ((loneneighbors[mat][front]['meta'] & 3) + 1) != somemeta and somemeta == 3:
        #     pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
        #     if (loneneighbors[mat][front]['meta'] & 3) + 1 != 1:
        #         pointops.mirrorpointsY()
            
        # elif back in loneneighbors[mat] and ((loneneighbors[mat][back]['meta'] & 3) + 1) != somemeta and somemeta == 4:
        #     pointops  = fromfileordefault(mat,1 ,shapemaker.makeposcornerstairs)
        #     if (loneneighbors[mat][back]['meta'] & 3) + 1 == 1:
        #         pointops.mirrorpointsY()
        
        else:
       
            pointops  = fromfileordefault(mat,0 ,shapemaker.makenormalstairs)

        direction = loneneighbors[mat][block]['meta'] & 3
        upsidedown = (loneneighbors[mat][block]['meta'] >> 2) & 1

        if direction  ==  0:
            pointops.rotatepointsZ(0)
        elif direction == 1:
            pointops.rotatepointsZ(180)
        elif direction == 2:
            pointops.rotatepointsZ(270)
        else:
            pointops.rotatepointsZ( 90)
            
        if upsidedown:
            pointops.mirrorpointsZ()

        origins[mat] = pointops.getavgpoint().astuple()
        appendto3dlist(pointops, block)
        faces[mat] += pointops


def makefence(loneneighbors, mat):
    
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        # if mat in colormaterials and 'models' in colormaterials[mat]:
        #     pointlist = PointList()
        #     pointlist.fromtuplelist(colormaterials[mat]['models'][0])
        #     pointops = pointlist
        # else:
        #     pointops = shapemaker.makefenceshape()

        pointops  = fromfileordefault(mat,0 ,shapemaker.makefenceshape)

        
        shapemaker.removeneibors(pointops, listoffaces)
        appendto3dlist(pointops, block)
        origins[mat] = pointops.getavgpoint().astuple()
        faces[mat] += pointops



def makeblock(loneneighbors, mat):
    
 
    if mat in colormaterials and 'niceneighbor' in colormaterials[mat] and colormaterials[mat]['niceneighbor']:
        removeneibors = False
        print str(mat) + ' removed in makeblock'
    else:
        removeneibors = True
        

    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        pointops  = fromfileordefault(mat,0 ,shapemaker.makeblockshape)
    
        if removeneibors:
            shapemaker.removeneibors(pointops, listoffaces)
        
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.getavgpoint().astuple()

        faces[mat] += pointops


def makedoubleslab(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        meta = loneneighbors[mat][block]['meta']

        if meta > 7:
            loneneighbors[mat][block]['meta'] =- 7


        # if mat in colormaterials and 'models' in colormaterials[mat]:
        #     pointlist = PointList()
        #     pointlist.fromtuplelist(colormaterials[mat]['models'][0])
        #     pointops = pointlist
        # else:
        #     pointops = shapemaker.makeblockshape()
        pointops  = fromfileordefault(mat,0, shapemaker.makeblockshape)
        

        shapemaker.removeneibors(pointops, listoffaces)
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.getavgpoint().astuple()
        faces[mat] += pointops   

def makehalfblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        meta = loneneighbors[mat][block]['meta']

        pointops  = fromfileordefault(mat,0 , shapemaker.makehalfblocks)
        
        if meta > 7:
            pointops.rotatepointsY(180)

        shapemaker.removeneibors(pointops, listoffaces)
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.getavgpoint().astuple()
        faces[mat] += pointops

def makeverticalblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        left = block[0]-1, block[1], block[2]
        right = block[0]+1, block[1], block[2]
        front = block[0], block[1]-1, block[2]
        back = block[0], block[1]+1, block[2]

        if mat in colormaterials and 'models' in colormaterials[mat]:
            pointlist = PointList()
            pointlist.fromtuplelist(colormaterials[mat]['models'][0])
            pointops = pointlist
        else:
            pointops = shapemaker.makeflatblocks()

        if front in loneneighbors[mat] or back in loneneighbors[mat]:
            # pointops = shapemaker.makeverticalflatblock()
            pointops  = fromfileordefault(mat,0 , shapemaker.makeverticalflatblock)
            pointops.rotatepointsZ(90)
        elif left in loneneighbors[mat] or right in loneneighbors[mat]:
            # pointops = shapemaker.makeverticalflatblock()
            pointops  = fromfileordefault(mat,0 , shapemaker.makeverticalflatblock)
        elif left in loneneighbors[mat] and right in loneneighbors[mat] and front in loneneighbors[mat] and back in loneneighbors[mat]:
            # pointops = shapemaker.makeverticalplusblock()
            pointops  = fromfileordefault(mat,0 ,shapemaker.makeverticalplusblock)
        else:
            pointops  = fromfileordefault(mat,0 , shapemaker.makeverticalplusblock)
            # pointops = shapemaker.makeverticalplusblock() 

        shapemaker.removeneibors(pointops, listoffaces)
        appendto3dlist(pointops, block)   
        origins[mat] = pointops.getavgpoint().astuple()
        faces[mat] += pointops

def makeladderlikeblock(loneneighbors, mat):

    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']

        # if mat in colormaterials and 'models' in colormaterials[mat]:
        #     pointlist = PointList()
        #     pointlist.fromtuplelist(colormaterials[mat]['models'][0])
        #     pointops = pointlist
        # else:
        #     pointops = shapemaker.makeladdershapes()
        pointops  = fromfileordefault(mat,0 , shapemaker.makeladdershapes)

        direction = loneneighbors[mat][block]['meta'] & 3

        if direction == 0:
            pointops.rotatepointsZ(90)
        elif direction == 1:
            pointops.rotatepointsZ(-90)
        elif direction == 2:
            pointops.rotatepointsZ(0)
        else:
            pointops.rotatepointsZ(180)

        shapemaker.removetopdownneighbors(pointops, listoffaces)

        appendto3dlist(pointops, block)
        
        origins[mat] = pointops.getavgpoint().astuple()
        faces[mat] += pointops


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

def getchunks(chunkxz):
    if row[5] != 'None':
        chunkdata = base64.standard_b64decode(row[5])
        matsamples = []
        if chunkxz not in chunks:
            chunks.update({chunkxz:{'blocks':[]}})
        for x in xrange(1,17):
            if len(chunkdata[(256*x):(256*x)+2]) == 2:
                temp = struct.unpack('H', chunkdata[(256*x):(256*x)+2])[0]
                matsamples.append(temp >> 4)
        matsamples = list(set(matsamples))
        worldnum = worldfromsample(matsamples)

        if chunkxz not in chunkposses and chunkxz[0] >= topleft[0] and chunkxz[1] >= topleft[1] and chunkxz[0] <= bottomright[0] and chunkxz[1] <= bottomright[1] and world == worldnum:
            
            chunkposses.append(chunkxz)
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
                                
                                block = ( (x + (chunkxz[0]*16),z + (chunkxz[1]*16),y+(index1*16)), btype, bmeta)
                                
                                chunks[chunkxz]['blocks'].append(block)

                    rightcounter += 1


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
                        
                        blockinfo = {position:{'meta':x[2],'faces':[]}}
                        if x[1] in multymatblocks:
                            if x[1] in [182 ,126 ,44] and x[2] > 7:
                                x = x[0], x[1], x[2] - 8
                            if x[1] in [125,181, 43] and x[2] > 7:
                                x = x[0], x[1], x[2] - 8

                            if (x[1],x[2]) not in materials:
                                materials.update({(x[1],x[2]):blockinfo})
                            else:
                                materials[(x[1],x[2])].update(blockinfo)
                        else:
                            if (x[1],0) not in materials:
                                materials.update({(x[1],0):blockinfo})
                            else:
                                materials[(x[1],0)].update(blockinfo) 
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
            
            if (block[0]-1, block[1], block[2]) not in materials[mat]: #and 
                
                neightbors[mat][block]['faces'].append(1)
            elif  materials[mat][(block[0]-1, block[1], block[2])]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(1)

            if (block[0]+1, block[1], block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(2)
            elif  materials[mat][(block[0]+1, block[1], block[2])]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(2)

            if (block[0], block[1]-1, block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(3)
            elif  materials[mat][(block[0], block[1]-1, block[2])]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(3)

            if (block[0], block[1]+1, block[2]) not in materials[mat]:
                neightbors[mat][block]['faces'].append(4)
            elif  materials[mat][(block[0], block[1]+1, block[2])]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(4)

            if (block[0], block[1], block[2]-1) not in materials[mat]:
                neightbors[mat][block]['faces'].append(5)
            elif  materials[mat][(block[0], block[1], block[2]-1)]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(5)

            if (block[0], block[1], block[2]+1) not in materials[mat]: 
                neightbors[mat][block]['faces'].append(6)
            elif  materials[mat][(block[0], block[1], block[2]+1)]['meta'] != neightbors[mat][block]['meta']:
                neightbors[mat][block]['faces'].append(6)

        materials[mat] = None
    return neightbors

def removeSupderCosy(neightbors):
    loneneighbors = {}
    for mat in neightbors:
        
        if mat in colormaterials and 'niceneighbor' in colormaterials[mat] and colormaterials[mat]['niceneighbor']:
            removeneibors = False
            print str(mat) + ' removed in superduper'
        else:
            removeneibors = True

        loneneighbors[mat] = {}
        for block in neightbors[mat]:

            if len(neightbors[mat][block]['faces']) > 0 or not removeneibors:

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
        if not nochunks:
            getchunks(ast.literal_eval(row[1]))

    
print 'Filtering entitys that are not supposed to be in scene move at all'

allhistory = filterents(allhistory)

allhistory = filterstatics(allhistory)

print getMaxMinTime(allhistory)

print 'parsing ' + str(len(chunkposses)) + ' chunks'

# put it in material array instead of chunk arrays

print 'make a index of possible materials'


materials = {}
materials = fillmatindexes(chunks, materials)



neightbors = genfacesNeighbors(materials)

loneneighbors = removeSupderCosy(neightbors)

print 'generating face positions ' + str(len(loneneighbors)) + ' materials'
faces = {}
vertices = {}
origins = {}

for mat in loneneighbors:
    
    faces[mat] = []
    vertices[mat] = []
    # origins[mat] = []

    if mat[0] in [182 ,126 ,44]:
        makehalfblock(loneneighbors, mat)
    elif mat[0] in [125,181, 43]:
        makedoubleslab(loneneighbors, mat)
    elif mat[0] in [101,102, 160]:
        makeverticalblock(loneneighbors, mat)
    elif mat[0] in [65, 106]:
        makeladderlikeblock(loneneighbors, mat)
    elif mat[0] in [85, 113,188, 189, 190, 191]:
        makefence(loneneighbors, mat)
    elif mat[0] in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
        makestairs(loneneighbors, mat)
    else:
        makeblock(loneneighbors, mat)

    temp = PointList()
    for points in faces[mat]:
        for point in points:
            temp.append(point)

    # somepoint = temp.getrawavgpoint().astuple()
    
    # origins[mat] = somepoint
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

for mat in vertices:
    tempverts = []
    for vert in vertices[mat]:
        vert.substracttup(origins[mat])
        tup = vert.aslist()
        tempverts.append(tup)
    vertices[mat] = tempverts



faces = newfaces
newface = None
loneneighbors = None


for mat in colormaterials:
    if mat in colormaterials and 'model' in colormaterials[mat]:
        del colormaterials[mat]['model']


allstuff = {'allhistory':allhistory,'vertices':vertices,'faces':faces, 'materials': colormaterials,'origins':origins,'textures': textures }


vertices = None
faces = None

print 'entitys with spawnmessage:' + str(len(allhistory)) + ',so used !'
print 'entitys without spawnmessage:' + str(len(lostcounter)) + ',so ignored !'

with open(destfile, 'wb') as handle:
    pickle.dump(allstuff, handle)
