#!/usr/bin/python -B

import operator
import ast
import base64
import struct
import sys, getopt
import pickle
from points import *
from shapes import *
from materials import *
from chunkParser import *


sourcefile = "default.dump"
destfile = "default.mcmo"

avgmiddle = False
norenderents = ["none"]
norenderblocks = ["none"]

noentitys = False
nochunks = False
onlyplayerents = False
agressiveremoval = False
curscene = "noscene"
world = 1
# cuty = 0
# topleft = (-1000,-1000)
# bottomright = (1000,1000)
# multymatblocks = [35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171]
shapemaker = Shapes()
colormaterials = defmaterials


try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","materialsfile=","sourcefile=","destfile=","scene=", "excludeent=","excludeblocks=","agressiveremoval=","CTL=","CBR=","cuty=","noentitys=","nochunks=","onlyplayerents=", "world=" ])
        
except getopt.GetoptError:
    print 'error: lister.py --onlyplayerents --materialsfile --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --agressiveremoval --world nether/overworld/theend will only use this world'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'lister.py --onlyplayerents --materialsfile --avgmiddle --sourcefile filename --destfile filename --scene scene name --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids --agressiveremoval --world nether/overworld/theend will only use this world'
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
    
    if opt == "--agressiveremoval":
        agressiveremoval = True

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
            point.append_tup(block)

def fromfileordefault(mat, index, defaultfunction):

    if mat in colormaterials and 'models' in colormaterials[mat] and index + 1 <= len(colormaterials[mat]['models']):
        pointlist = PointList()
        pointlist.from_tuple_list(colormaterials[mat]['models'][index])
        pointops = pointlist
    else:
        pointops = defaultfunction()
    return pointops

def rotatevalue(meta, rotate):
    if meta == 3 and rotate > 0:
        meta = -1
    if meta == 0 and rotate < 0:
        meta = 4
    return meta + rotate


def isperpendicular(meta1, meta2):
    rotated = rotatevalue(meta2, -1)
    proppernum = meta1 ^ rotated
    return proppernum




def makestairs(loneneighbors, mat):

    if mat in colormaterials and 'interneighbor' in colormaterials[mat] and colormaterials[mat]['interneighbor']:
        removeneibors = False
    else:
        removeneibors = True

    neighborstairs = {}
    for x in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
        if (x,0) in loneneighbors:
            neighborstairs.update(loneneighbors[(x,0)])

    
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']

        somemeta = (loneneighbors[mat][block]['meta'] & 3)
        pointops = PointList()

        shapedone = False
        front = block[0]-1, block[1], block[2]
        back = block[0]+1, block[1], block[2]
        left = block[0], block[1]-1, block[2]
        right = block[0], block[1]+1, block[2]


        if not shapedone and front in neighborstairs and (neighborstairs[front]['meta'] & 3) in [2,3] and somemeta in [0,1]:
            shape = isperpendicular( somemeta, (neighborstairs[front]['meta'] & 3))
            shapedone = True
            if shape in [0,3]:
                pointops = fromfileordefault(mat,1 ,shapemaker.make_pos_corner_stairs)
            else:
                pointops = fromfileordefault(mat,2 ,shapemaker.make_neg_corner_stairs)
                if (neighborstairs[front]['meta'] & 3) == 2:
                    pointops.rotate_points_z(-90)

            if (neighborstairs[front]['meta'] & 3) == 3:
                pointops.mirror_points_y()



        if not shapedone and back in neighborstairs and (neighborstairs[back]['meta'] & 3) in [2,3] and somemeta in [0,1]:
            shape = isperpendicular( somemeta, (neighborstairs[back]['meta'] & 3))
            shapedone = True
            if shape in [0,3]:
                pointops = fromfileordefault(mat,2 ,shapemaker.make_neg_corner_stairs)
                pointops.rotate_points_z(-90)
            else:
                pointops = fromfileordefault(mat,1 ,shapemaker.make_pos_corner_stairs)

                if (neighborstairs[back]['meta'] & 3) == 2:
                    pointops.mirror_points_y()

            


        if not shapedone and left in neighborstairs and (neighborstairs[left]['meta'] & 3) in [0,1] and somemeta in [2,3]:
            shape = isperpendicular(somemeta, (neighborstairs[left]['meta'] & 3))
            shapedone = True
            if shape in [0,3]:
                pointops = fromfileordefault(mat,2 ,shapemaker.make_neg_corner_stairs)
                if (neighborstairs[left]['meta'] & 3) == 0:
                    pointops.mirror_points_y()
            else:
                pointops = fromfileordefault(mat,1 ,shapemaker.make_pos_corner_stairs)

                if (neighborstairs[left]['meta'] & 3) == 1:
                    pointops.mirror_points_y()




        if not shapedone and right in neighborstairs and (neighborstairs[right]['meta'] & 3) in [0,1] and somemeta in [2,3]:
            shape = isperpendicular(somemeta, (neighborstairs[right]['meta'] & 3))
            shapedone = True
            if shape in [0,3]:
                pointops = fromfileordefault(mat,1 ,shapemaker.make_pos_corner_stairs)
                if (neighborstairs[right]['meta'] & 3) == 0:
                    pointops.mirror_points_y()
            else:
                pointops = fromfileordefault(mat,2 ,shapemaker.make_neg_corner_stairs)

                if (neighborstairs[right]['meta'] & 3) == 1:
                    pointops.rotate_points_z(-90)
            

        
        if not shapedone:
            pointops  = shapemaker.make_normal_stairs()

        direction = loneneighbors[mat][block]['meta'] & 3
        upsidedown = (loneneighbors[mat][block]['meta'] >> 2) & 1

        if direction  ==  0:
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
            shapemaker.remove_neibors(pointops, listoffaces)

        origins[mat] = pointops.get_avg_point().as_tuple()
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

        pointops  = fromfileordefault(mat,0 ,shapemaker.make_fence_shape)

        
        shapemaker.remove_neibors(pointops, listoffaces)
        appendto3dlist(pointops, block)
        origins[mat] = pointops.get_avg_point().as_tuple()
        faces[mat] += pointops



def makeblock(loneneighbors, mat):
 
    if mat in colormaterials and 'interneighbor' in colormaterials[mat] and colormaterials[mat]['interneighbor']:
        removeneibors = False
    else:
        removeneibors = True
        
    pointops = False
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        pointops  = fromfileordefault(mat,0 ,shapemaker.make_block_shape)
    
        if removeneibors:
            shapemaker.remove_neibors(pointops, listoffaces)
        
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.get_avg_point().as_tuple()

        faces[mat] += pointops

    if not pointops:
        origins[mat] = (0,0,0)  


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
        pointops  = fromfileordefault(mat,0, shapemaker.make_block_shape)
        

        shapemaker.remove_neibors(pointops, listoffaces)
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.get_avg_point().as_tuple()
        faces[mat] += pointops   

def makesnow(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        pointops  = fromfileordefault(mat,0 ,shapemaker.make_block_shape)
        meta = loneneighbors[mat][block]['meta']
        
        if mat == (78,0):
            scale = (meta + 1.0) / 8.0
            pointops.scale_points_z(scale)
            pointops.translate_points_z((scale-1)/2)
            

        appendto3dlist(pointops, block)    
        origins[mat] = pointops.get_avg_point().as_tuple()

        faces[mat] += pointops

def maketorch(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        pointops  = fromfileordefault(mat,0 ,shapemaker.make_block_shape)
        meta = loneneighbors[mat][block]['meta']
        if meta != 5:
            pointops.rotate_points_y(30)
            pointops.translate_points_x(-0.3)
        if meta == 2:
            pointops.rotate_points_z(180)
        elif meta == 3:
            pointops.rotate_points_z(270)
        elif meta == 4:
            pointops.rotate_points_y(90)

        appendto3dlist(pointops, block)    
        origins[mat] = pointops.get_avg_point().as_tuple()

        faces[mat] += pointops

def makehalfblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        meta = loneneighbors[mat][block]['meta']

        pointops  = fromfileordefault(mat,0 , shapemaker.make_half_blocks)
        
        if meta > 7:
            pointops.rotate_points_y(180)

        shapemaker.remove_neibors(pointops, listoffaces)
        appendto3dlist(pointops, block)    
        origins[mat] = pointops.get_avg_point().as_tuple()
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
            pointlist.from_tuple_list(colormaterials[mat]['models'][0])
            pointops = pointlist
        else:
            pointops = shapemaker.makeflatblocks()

        if front in loneneighbors[mat] or back in loneneighbors[mat]:
            pointops  = fromfileordefault(mat,0 , shapemaker.make_vertical_plus_block)
            pointops.rotate_points_z(90)
        elif left in loneneighbors[mat] or right in loneneighbors[mat]:
            pointops  = fromfileordefault(mat,0 , shapemaker.make_vertical_plus_block)
        elif left in loneneighbors[mat] and right in loneneighbors[mat] and front in loneneighbors[mat] and back in loneneighbors[mat]:
            pointops  = fromfileordefault(mat,0 ,shapemaker.make_vertical_plus_block)
        else:
            pointops  = fromfileordefault(mat,0 , shapemaker.make_vertical_plus_block)

        shapemaker.remove_neibors(pointops, listoffaces)
        appendto3dlist(pointops, block)   
        origins[mat] = pointops.get_avg_point().as_tuple()
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
            pointops.rotate_points_z(90)
        elif direction == 1:
            pointops.rotate_points_z(-90)
        elif direction == 2:
            pointops.rotate_points_z(0)
        else:
            pointops.rotate_points_z(180)

        shapemaker.removetopdownneighbors(pointops, listoffaces)

        appendto3dlist(pointops, block)
        
        origins[mat] = pointops.get_avg_point().as_tuple()
        faces[mat] += pointops



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


chunkparser = chunkParser(topleft, bottomright, cuty, world, norenderblocks)

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
            chunkparser.getchunks( row, chunks)

    
print 'Filtering entitys that are not supposed to be in scene move at all'

allhistory = filterents(allhistory)

allhistory = filterstatics(allhistory)

print getMaxMinTime(allhistory)

# print 'parsing ' + str(len(chunkposses)) + ' chunks'

# put it in material array instead of chunk arrays

print 'make a index of possible materials'


materials = {}
materials = chunkparser.fillmatindexes(chunks, materials)



neightbors = chunkparser.genfacesNeighbors(materials, agressiveremoval, colormaterials)

loneneighbors = chunkparser.removeSupderCosy(neightbors, colormaterials)

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
    elif mat[0] in [50, 75, 76]:
        maketorch(loneneighbors, mat)
    elif mat[0] in [78, 80]:
        makesnow(loneneighbors, mat)

    else:
        makeblock(loneneighbors, mat)

    temp = PointList()
    for points in faces[mat]:
        for point in points:
            temp.append(point)

    # somepoint = temp.getrawavgpoint().as_tuple()
    
    # origins[mat] = somepoint
    # loneneighbors[mat] = []
loneneighbors = None


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
        vert.substract_tup(origins[mat])
        tup = vert.as_list()
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
