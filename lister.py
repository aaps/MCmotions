#!/usr/bin/python -B

import operator
import ast
import base64
import struct
import sys, getopt
import urllib
import json
from points import *
from shapes import *
from materials import *
from ChunkParser import ChunkParser
from cStringIO import StringIO
import zlib
from time import sleep

try:
    import cPickle as pickle
except:
    import pickle


sourcefile = "default.dump"
destfile = "default.mcmo"
playernamecache = open('./cache/playercache.json','r+')
plnanc = json.loads(playernamecache.read())
playernamecache.seek(0)



avgmiddle = False
norenderents = ["none"]
norenderblocks = ["none"]

noentitys = False
nochunks = False
onlyplayerents = False
agressiveremoval = False
curscene = "noscene"
world = 0
cuty = 0
topleft = (-1000,-1000)
bottomright = (1000,1000)
# multymatblocks = [35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171]
textures = None


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



shapes = Shapes(colormaterials)
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

# chunks = {}
chunkposses = []



pointops = PointList()



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

def converplayername(uuid):

        playername = "player: UNKNOWN"
        accountdata = {}
        if uuid in plnanc:
            return "player: " + plnanc[uuid]

        mobtype = uuid.replace('-','')
        request = urllib.urlopen('https://sessionserver.mojang.com/session/minecraft/profile/' + mobtype)
        data = request.read().decode("utf8")
        try:
            accountdata = json.loads(data)
        except Exception, e:
            print e, data

        if 'name' in accountdata:
            playername = "player: " + accountdata['name'].decode("utf8")
        
        sleep(3)
        plnanc.update({uuid:playername})
        return playername





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

chunkparser = ChunkParser(topleft, bottomright, cuty, world, norenderblocks, colormats=colormaterials)

for line in aroflines:
    row = line.split('|') 
    if not noentitys and 'spawn' in row[0] and row[4] not in norenderents and not noentitys:

        # print "SPAWN: " + row[0] + " - " + str(onlyplayerents) + "="

        if not onlyplayerents and 'player' not in row[0]:
            
            goodpos = ast.literal_eval(row[5])
            rawyawpichhead = ast.literal_eval(row[6])
            if len(rawyawpichhead) > 2:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
            else:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
            mob = {int(row[3]):{'type':row[4],'positions':[{'time':int(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1,'scene':'noscene'}]}}
            allhistory.update(mob)

        if 'player' in row[0]:
            goodpos = ast.literal_eval(row[5])
            rawyawpichhead = ast.literal_eval(row[6])
            if len(rawyawpichhead) > 2:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
            else:
                rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/-32)
            
            mob = {int(row[3]):{'type':row[4],'name':converplayername(row[4]),'positions':[{'time':int(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1,'scene':'noscene'}]}}
            
            # print "got player: " + str(mob[int(row[3])])
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
    elif row[0] == 'changedim':
        worldnum = row[1]
        chunkparser.set_world_num(worldnum)
    elif row[0] == 'chunkdata':
        length = row[3]
        
        if not nochunks:
            chunkparser.get_chunks(row)




print 'Filtering entitys that are not supposed to be in scene move at all'

allhistory = filterents(allhistory)

allhistory = filterstatics(allhistory)

print getMaxMinTime(allhistory)

# put it in material array instead of chunk arrays

print 'make a index of possible materials'


chunkparser.fill_mat_indexes()


chunkparser.gen_faces_neighbors(agressiveremoval)

loneneighbors = chunkparser.remove_super_cosy()



print 'generating face positions ' + str(len(loneneighbors)) + ' materials'
faces = {}
vertices = {}
origins = {}

for mat in loneneighbors:
    faces[mat] = []
    vertices[mat] = []
    origins[mat] = []

    if mat[0] in [182 ,126 ,44]:
        faces[mat], origins[mat] = shapes.makehalfblock(loneneighbors, mat)
    elif mat[0] in [125,181, 43]:
        faces[mat], origins[mat] = shapes.makedoubleslab(loneneighbors, mat)
    elif mat[0] in [101,102, 160]:
        faces[mat], origins[mat] = shapes.makeverticalblock(loneneighbors, mat)
    elif mat[0] in [65, 106]:
        faces[mat], origins[mat] = shapes.makeladderlikeblock(loneneighbors, mat)
    elif mat[0] in [85, 113,188, 189, 190, 191]:
        faces[mat], origins[mat] = shapes.makefence( loneneighbors, mat)
    elif mat[0] in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
        faces[mat], origins[mat] = shapes.makestairs(loneneighbors, mat)
    elif mat[0] in [50, 75, 76]:
        faces[mat], origins[mat] = shapes.maketorch(loneneighbors, mat)
    elif mat[0] in [78, 80]:
        faces[mat], origins[mat] = shapes.makesnow(loneneighbors, mat)
    else:
        faces[mat], origins[mat] = shapes.makeblock(loneneighbors, mat)


    temp = PointList()
    for points in faces[mat]:
        for point in points:
            temp.append(point)

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

playernamecache.write(json.dumps(plnanc))
playernamecache.close()

for mat in colormaterials:
    if mat in colormaterials and 'model' in colormaterials[mat]:
        del colormaterials[mat]['model']


allstuff = {'allhistory':allhistory,'vertices':vertices,'faces':faces, 'materials': colormaterials,'origins':origins,'textures': textures }


vertices = None
faces = None

print 'entitys with spawnmessage:' + str(len(allhistory)) + ',so used !'
print 'entitys without spawnmessage:' + str(len(lostcounter)) + ',so ignored !'

compressed = zlib.compress(pickle.dumps(allstuff),  9)

somefile = open(destfile, 'wb')

somefile.write(compressed)
