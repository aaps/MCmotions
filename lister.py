#!/usr/bin/python -B

import operator
import ast
# import json
import base64
import struct
import sys, getopt
from blist import blist
import time
# from collections import Counter
from collections import OrderedDict

# import StringIO


sourcefile = "default.dump"
destfile = "default.mcmo"
sesnrtoget = 0
avgmiddle = False
norenderents = ["none"]
norenderblocks = ["none"]

noentitys = False
nochunks = False

cuty = 0
cutz = (-1000,1000)
cutx = (-1000,1000)



try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","sourcefile=","destfile=","session=", "avgmiddle=", "excludeent=","excludeblocks=","cutx=","cuty=","cutz=","noentitys=","nochunks=" ])
        
except getopt.GetoptError:
    print 'error: lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber --excludeent commaseperatedlist of entity ids --excludeblocks commaseperatedlist of blockids'
        sys.exit()

    if opt == "--sourcefile":
        sourcefile = arg

    if opt == "--destfile":
        destfile = arg

    if opt == "--session":
        sesnrtoget = int(arg)

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

    if opt == "--nochunks":
        nochunks = True



allhistory = {}
allblocks = {}


currentses = 0
lostcounter = []

f = open(destfile, 'w')

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

def makestairs(loneneighbors, mat):
    for block in loneneighbors[mat]:
        
        loweplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
        faces[mat].append(loweplane)
    
        firststep = (block[0],block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0],block[1]-0.5,block[2]+0.5)
        faces[mat].append(firststep)
    
        secondstep = (block[0],block[1]+0.5,block[2]),(block[0]-0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]),(block[0],block[1]-0.5,block[2])
        faces[mat].append(secondstep)

        inbetween = (block[0],block[1]+0.5,block[2]),(block[0],block[1]-0.5,block[2]),(block[0],block[1]-0.5,block[2]+0.5),(block[0],block[1]+0.5,block[2]+0.5)
        faces[mat].append(inbetween)

        frontpiece = (block[0]-0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5)
        faces[mat].append(frontpiece)

        backplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
        faces[mat].append(backplane)
        

        rightplane = (block[0],block[1]+0.5,block[2]+0.5),(block[0],block[1]+0.5,block[2]),(block[0]-0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
        faces[mat].append(rightplane)
        
        leftplane = (block[0],block[1]-0.5,block[2]+0.5),(block[0],block[1]-0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5)
        faces[mat].append(leftplane)


        # print loneneighbors[mat][block]['meta']

def makefence(loneneighbors, mat):
    
    for block in loneneighbors[mat]:

        loweplane = (block[0]+0.1,block[1]+0.1,block[2]-0.5),(block[0]-0.1,block[1]+0.1,block[2]-0.5),(block[0]-0.1,block[1]-0.1,block[2]-0.5),(block[0]+0.1,block[1]-0.1,block[2]-0.5)
        faces[mat].append(loweplane)
    
        upperplane = (block[0]+0.1,block[1]+0.1,block[2]+0.5),(block[0]-0.1,block[1]+0.1,block[2]+0.5),(block[0]-0.1,block[1]-0.1,block[2]+0.5),(block[0]+0.1,block[1]-0.1,block[2]+0.5)
        faces[mat].append(upperplane)
    
        leftplane = (block[0]-0.1,block[1]-0.1,block[2]-0.5),(block[0]-0.1,block[1]-0.1,block[2]+0.5),(block[0]+0.1,block[1]-0.1,block[2]+0.5),(block[0]+0.1,block[1]-0.1,block[2]-0.5)
        faces[mat].append(leftplane)

        rightplane = (block[0]-0.1,block[1]+0.1,block[2]-0.5),(block[0]-0.1,block[1]+0.1,block[2]+0.5),(block[0]+0.1,block[1]+0.1,block[2]+0.5),(block[0]+0.1,block[1]+0.1,block[2]-0.5)
        faces[mat].append(rightplane)
    
        backplane = (block[0]-0.1,block[1]-0.1,block[2]-0.5),(block[0]-0.1,block[1]+0.1,block[2]-0.5),(block[0]-0.1,block[1]+0.1,block[2]+0.5),(block[0]-0.1,block[1]-0.1,block[2]+0.5)
        faces[mat].append(backplane)

        frontplane = (block[0]+0.1,block[1]-0.1,block[2]-0.5),(block[0]+0.1,block[1]+0.1,block[2]-0.5),(block[0]+0.1,block[1]+0.1,block[2]+0.5),(block[0]+0.1,block[1]-0.1,block[2]+0.5)
        faces[mat].append(frontplane)

def makeblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        
        if 5 in listoffaces:
            loweplane = (block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5)
            faces[mat].append(loweplane)

        if 6 in listoffaces:
            upperplane = (block[0]-0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]-0.5,block[2]+0.5)
            faces[mat].append(upperplane)

        if 3 in listoffaces:
            leftplane = (block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5)
            faces[mat].append(leftplane)

        if 4 in listoffaces:
            rightplane = (block[0]-0.5,block[1]+0.5,block[2]+0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
            faces[mat].append(rightplane)


        if 1 in listoffaces:
            backplane = (block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]+0.5,block[2]+0.5)
            faces[mat].append(backplane)

        if 2 in listoffaces:
            frontplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
            faces[mat].append(frontplane)


def makehalfblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        if 5 in listoffaces:
            loweplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
            faces[mat].append(loweplane)

        if 6 in listoffaces:
            upperplane = (block[0]+0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2]),(block[0]+0.5,block[1]-0.5,block[2])
            faces[mat].append(upperplane)

        if 3 in listoffaces:
            leftplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]),(block[0]+0.5,block[1]-0.5,block[2]),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
            faces[mat].append(leftplane)

        if 4 in listoffaces:
            rightplane = (block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]),(block[0]+0.5,block[1]+0.5,block[2]),(block[0]+0.5,block[1]+0.5,block[2]-0.5)
            faces[mat].append(rightplane)

        if 1 in listoffaces:
            backplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]),(block[0]-0.5,block[1]-0.5,block[2])
            faces[mat].append(backplane)

        if 2 in listoffaces:
            frontplane = (block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]),(block[0]+0.5,block[1]-0.5,block[2])
            faces[mat].append(frontplane)

def makeflatblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        listoffaces = loneneighbors[mat][block]['faces']
        if 5 in listoffaces:
            loweplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
            faces[mat].append(loweplane)

        if 6 in listoffaces:
            upperplane = (block[0]+0.5,block[1]+0.5,block[2]-0.4),(block[0]-0.5,block[1]+0.5,block[2]-0.4),(block[0]-0.5,block[1]-0.5,block[2]-0.4),(block[0]+0.5,block[1]-0.5,block[2]-0.4)
            faces[mat].append(upperplane)

        if 3 in listoffaces:
            leftplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.4),(block[0]+0.5,block[1]-0.5,block[2]-0.4),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
            faces[mat].append(leftplane)

        if 4 in listoffaces:
            rightplane = (block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.4),(block[0]+0.5,block[1]+0.5,block[2]-0.4),(block[0]+0.5,block[1]+0.5,block[2]-0.5)
            faces[mat].append(rightplane)


        if 1 in listoffaces:
            backplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.4),(block[0]-0.5,block[1]-0.5,block[2]-0.4)
            faces[mat].append(backplane)

        if 2 in listoffaces:
            frontplane = (block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.4),(block[0]+0.5,block[1]-0.5,block[2]-0.4)
            faces[mat].append(frontplane)

def makexblock(loneneighbors, mat):
    for block in loneneighbors[mat]:
        firstplane = (block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5),(block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5)
        secondplane = (block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]+0.5)
        faces[mat].append(firstplane)
        faces[mat].append(secondplane)




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
        if 'spawn' in row[0] and sesnrtoget == currentses:
            goodpos = ast.literal_eval(row[4])
            goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/32)
            allposses.append(goodpos)

    lentotal = len(allposses)
    total = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), allposses)
    offset = (total[0]/lentotal, total[1]/lentotal, total[2]/lentotal)
    print 'offset:' + str(offset)

for line in aroflines:
    
    row = line.split('|')

    if row[0] == 'startrecord' and not noentitys:
        
        currentses =+ 1

        
    elif 'spawn' in row[0]  and sesnrtoget == currentses and row[3] not in norenderents and not noentitys:
        

        goodpos = ast.literal_eval(row[4])
        rawyawpichhead = ast.literal_eval(row[5])
        if len(rawyawpichhead) > 2:
            rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
        else:
            rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
        goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/32)
        
        mob = {int(row[2]):{'type':row[3],'positions':[{'time':float(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1}]}}

        allhistory.update(mob)

    
    elif row[0] == 'entityrelmove' and int(row[2]) in allhistory and sesnrtoget == currentses and not noentitys:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]

        absolutepos = tuple(map(operator.add, lastlist['pos'], ast.literal_eval(row[3])))

        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':absolutepos,'yawpichhead':lastlist['yawpichhead'],'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entitylookandrelmove' and int(row[2]) in allhistory and sesnrtoget == currentses and not noentitys:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]

        absolutepos = tuple(map(operator.add, lastlist['pos'], ast.literal_eval(row[3])))
        yawpich = ast.literal_eval(row[4])
        
        if len(lastlist['yawpichhead']) > 2:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360,lastlist['yawpichhead'][2]
        else:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360
        yawpichhead = fido(lastlist['yawpichhead'], yawpichhead)

        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':absolutepos,'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entityheadlook' and int(row[2]) in allhistory and sesnrtoget == currentses and not noentitys:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        
        if len(lastlist['yawpichhead']) > 2:
            if not ast.literal_eval(row[3]) == lastlist['yawpichhead'][2]:
            
                yawpichhead = lastlist['yawpichhead'][0], lastlist['yawpichhead'][1], (ast.literal_eval(row[3])+ 5) % 360

            yawpichhead = fido(yawpichhead, lastlist['yawpichhead'])

            allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})


    elif row[0] == 'entityteleport' and int(row[2]) in allhistory and sesnrtoget == currentses and not noentitys:
        
        goodpos = ast.literal_eval(row[3])
        goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/32)
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        yawpich = ast.literal_eval(row[4])
        if len(lastlist['yawpichhead']) > 2:
            yawpichhead = (yawpich[0]+ 5) % 360, (yawpich[1]+ 5) % 360, lastlist['yawpichhead'][2]
        else:
            yawpichhead = (yawpich[0]+ 5) % 360, (yawpich[1]+ 5) % 360
        
        yawpichhead = fido( yawpichhead, lastlist['yawpichhead'])
        
        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)),'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entitystatus' and int(row[2]) in allhistory and sesnrtoget == currentses and not noentitys:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        if lastlist['status'] == row[3]:
            allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':lastlist['yawpichhead'],'status':row[3],'alive':lastlist['alive'] })

    elif row[0] == 'destroyents' and sesnrtoget == currentses:
        entids = row[2:]
        
        for entid in entids:
            if entid in allhistory and sesnrtoget == currentses:
                lastlist = allhistory[entid]['positions'][-1]
                allhistory[entid]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0 ,'alive':0})

    elif row[0] == 'chunkdata' and sesnrtoget == currentses and not noentitys:
        length = row[2]
        
        chunks.update({row[1]:{'blocks':[]}})

        try:
            if row[5] != 'None':
                chunkdata = base64.standard_b64decode(row[5])
                xzpos = ast.literal_eval(row[1])
                # print xzpos, cutx, cutz

                if xzpos not in chunkposses and xzpos[0] >= cutx[0] and xzpos[0] <= cutx[1] and xzpos[1] >= cutz[0] and xzpos[1] <= cutz[1]:
                    chunkposses.append(xzpos)
                    for index1 in xrange(0, 16):
                        if int(row[3]) & (1 << index1) and index1 >= cuty:
                            for y in xrange(0,16):

                                for z in xrange(0,16):
                                    for x in xrange(0,16):
                                        goodindex = (x+(z*16)+(y*256)+(index1*4096))
                                        temp = struct.unpack('H',chunkdata[goodindex*2:goodindex*2+2])[0]
                                        btype = temp >> 4
                                        bmeta = temp & 15
                                        block = ( (x + (xzpos[0]*16),z + (xzpos[1]*16),y+(index1*16)), btype, bmeta)
                                        chunks[row[1]]['blocks'].append(block)
                    

                        
        except Exception as e:
            print e

print 'parsing ' + str(len(chunkposses)) + ' chunks'

# put it in material array instead of chunk arrays

print 'make a index of possible materials'

wrongblocks = False
materials = {}
for chunk in chunks:
    for block in chunks[chunk]:
        if len(chunks[chunk][block]) > 0:
            for x in chunks[chunk][block]:
                if x[1] > 0 and x[1] < 256 and x[1] not in norenderblocks:
                    
                    matblock = {x[1]:{}}
                    materials.update(matblock)
                elif x[1] < 256:
                    wrongblocks = True

if wrongblocks:
    print 'there are wrong block types found, there is a good change the parsing in the proxy fase whent wrong !'

print 'put the blocks of materials in their material index for ' + str(len(materials)) + ' materials'
for chunk in chunks:
    for block in chunks[chunk]:
        if len(chunks[chunk][block]) > 0:
            for x in chunks[chunk][block]:

                if x[1] > 0 and x[1] < 256 and x[1] not in norenderblocks:
                    materials[x[1]].update({x[0]:{'meta':x[2],'faces':[]}})
        chunks[chunk][block] = None

chunks = None


neightbors = {}

print 'find material neightbors for ' + str(len(materials)) + ' materials'         
for mat in materials:
    neightbors[mat] = {}


for mat in materials:
    
    for block in materials[mat]:
        # print neightbors[mat][block]['faces']
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

materials = None
print 'removing all super neightbors, same type blocks on all sides for ' + str(len(neightbors)) + ' materials'         

loneneighbors = {}
for mat in neightbors:
    print mat
    loneneighbors[mat] = {}
    for block in neightbors[mat]:

        if len(neightbors[mat][block]['faces']) > 0:
            loneneighbors[mat][block[0]+0.5, block[1]+0.5, block[2]+0.5]  = neightbors[mat][block]
    neightbors[mat] = None

neightbors = None

print 'generating face positions ' + str(len(loneneighbors)) + ' materials'
faces = {}
vertices = {}

for mat in loneneighbors:
    faces[mat] = []
    vertices[mat] = []
    if mat == 182 or mat == 126 or mat == 44:
        makehalfblock(loneneighbors, mat)
    elif mat == 171 or mat == 111:
        makeflatblock(loneneighbors, mat)
    elif mat in [6 , 111 , 30 , 31 , 32,37,40, 51, 83, 175]:
        makexblock(loneneighbors, mat)
    elif mat in [85, 113,188, 189, 190, 191, 191]:
        makefence(loneneighbors, mat)
    elif mat in [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 165, 164, 180]:
        makestairs(loneneighbors, mat)
    else:
        makeblock(loneneighbors, mat)
    

    loneneighbors[mat] = None

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
    print mat

    newfaces[mat] = []
    timenow = None
    vertcache = OrderedDict()
    
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

    
f.write(repr(allstuff))

