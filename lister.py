#!/usr/bin/python -B

# import csv
import operator
import ast
import json
import math
import base64
import struct
import zlib
import sys, getopt
import numpy
from blist import *
from collections import Counter

# import StringIO

sourcefile = "default.log"
destfile = "default.json"
sesnrtoget = 0
avgmiddle = False
render = ["none"]

def facevertlinker(block, mat, plane):
    
    

    plane1 = int(plane[0][0] + (plane[0][1]*16) + (plane[0][2]*256))
    plane2 = int(plane[1][0] + (plane[1][1]*16) + (plane[1][2]*256))
    plane3 = int(plane[2][0] + (plane[2][1]*16) + (plane[2][2]*256))
    plane4 = int(plane[3][0] + (plane[3][1]*16) + (plane[3][2]*256))


    vertices[mat].update({plane1: plane[0]})


    vertices[mat].update({plane2: plane[1]})


    vertices[mat].update({plane3: plane[2]})


    vertices[mat].update({plane4: plane[3]})
    
    faces[mat].append((plane1, plane2, plane3, plane4))



try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","sourcefile=","destfile=","session=", "avgmiddle=", "exclude="])
        
except getopt.GetoptError:
    print 'error: lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber --exclude commaseperatedlist of entity ids'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber --exclude commaseperatedlist of entity ids'
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

    if opt == "--exclude":
        render = arg.split(",")
        


allhistory = {}
allblocks = {}


currentses = 0
lostcounter = []

f = open(destfile, 'w')

origin = open(sourcefile, 'r')

total = origin.read()

aroflines = total.split('\n')

chunks = {}


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

    if row[0] == 'startrecord':
        
        currentses =+ 1

        
    elif 'spawn' in row[0]  and sesnrtoget == currentses and row[3] not in render:
        

        goodpos = ast.literal_eval(row[4])
        rawyawpichhead = ast.literal_eval(row[5])
        if len(rawyawpichhead) > 2:
            rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360, (rawyawpichhead[2]+ 5) % 360
        else:
            rawyawpichhead = (rawyawpichhead[0]+ 5) % 360, (rawyawpichhead[1]+ 5) % 360
        goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/32)
        
        mob = {int(row[2]):{'type':row[3],'positions':[{'time':float(row[1]),'pos':tuple(map(operator.sub, goodpos, offset)), 'yawpichhead': rawyawpichhead,'status':0,'alive':1}]}}

        allhistory.update(mob)

    
    elif row[0] == 'entityrelmove' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]

        absolutepos = tuple(map(operator.add, lastlist['pos'], ast.literal_eval(row[3])))

        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':absolutepos,'yawpichhead':lastlist['yawpichhead'],'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entitylookandrelmove' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]

        absolutepos = tuple(map(operator.add, lastlist['pos'], ast.literal_eval(row[3])))
        yawpich = ast.literal_eval(row[4])
        
        if len(lastlist['yawpichhead']) > 2:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360,lastlist['yawpichhead'][2]
        else:
            yawpichhead = (yawpich[0]+ 5) % 360,(yawpich[1]+ 5) % 360
        yawpichhead = fido(lastlist['yawpichhead'], yawpichhead)

        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':absolutepos,'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entityheadlook' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        
        # print lastlist['yawpichhead']
        if len(lastlist['yawpichhead']) > 2:
            if not ast.literal_eval(row[3]) == lastlist['yawpichhead'][2]:
            
                yawpichhead = lastlist['yawpichhead'][0], lastlist['yawpichhead'][1], (ast.literal_eval(row[3])+ 5) % 360


            yawpichhead = fido(yawpichhead, lastlist['yawpichhead'])

            allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})


    elif row[0] == 'entityteleport' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
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

    elif row[0] == 'entitystatus' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        if lastlist['status'] == row[3]:
            allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':lastlist['yawpichhead'],'status':row[3],'alive':lastlist['alive'] })

    elif row[0] == 'destroyents' and sesnrtoget == currentses:
        entids = row[2:]
        
        for entid in entids:
            if entid in allhistory and sesnrtoget == currentses:
                lastlist = allhistory[entid]['positions'][-1]
                allhistory[entid]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0 ,'alive':0})

    elif row[0] == 'chunkdata' and sesnrtoget == currentses:
        length = row[2]
        
        chunks.update({row[1]:{'blocks':[]}})

        try:
            if row[5] != 'None':
                chunkdata = base64.standard_b64decode(row[5])
                xzpos = ast.literal_eval(row[1])

                for index1 in xrange(0, 16):
                    if int(row[3]) & (1 << index1):
                        for y in xrange(0,16):

                            for z in xrange(0,16):
                                for x in xrange(0,16):
                                    goodindex = (x+(z*16)+(y*256)+(index1*4096))

                                    temp = struct.unpack('H',chunkdata[goodindex*2:goodindex*2+2])[0]

                                    btype = temp >> 4
                                    bmeta = temp & 15
                                    
                                    block = ( (x + (xzpos[0]*16),z + (xzpos[1]*16),y+(index1*16)), btype)
                                    chunks[row[1]]['blocks'].append(block)
                    

                        
        except Exception as e:
            print e


# put it in material array instead of chunk arrays

print 'make a index of possible matrials'

materials = {}
for chunk in chunks:
    for block in chunks[chunk]:
        if len(chunks[chunk][block]) > 0:
            for x in chunks[chunk][block]:
                if x[1] > 0 and x[1] < 256:
                    matblock = {x[1]:{}}
                    materials.update(matblock)

print 'put the blocks of materials in their material index for ' + str(len(materials)) + ' materials'
for chunk in chunks:
    for block in chunks[chunk]:
        if len(chunks[chunk][block]) > 0:
            for x in chunks[chunk][block]:
                if x[1] > 0 and x[1] < 256:
                    materials[x[1]].update({x[0]:[]})
        chunks[chunk][block] = None

chunks = None

# print materials
neightbors = {}

print 'find material neightbors for ' + str(len(materials)) + ' materials'         
for mat in materials:
    neightbors[mat] = {}


for mat in materials:
    print mat
    for block in materials[mat]:
        
        neightbors[mat][block] = []
        
        if (block[0]-1, block[1], block[2]) not in materials[mat]:
            neightbors[mat][block].append(1)
        if (block[0]+1, block[1], block[2]) not in materials[mat]:
            neightbors[mat][block].append(2)
        if (block[0], block[1]-1, block[2]) not in materials[mat]:
            neightbors[mat][block].append(3)
        if (block[0], block[1]+1, block[2]) not in materials[mat]:
            neightbors[mat][block].append(4)
        if (block[0], block[1], block[2]-1) not in materials[mat]:
            neightbors[mat][block].append(5)
        if (block[0], block[1], block[2]+1) not in materials[mat]:
            neightbors[mat][block].append(6)
    materials[mat] = None

materials = None
print 'removing all super neightbors, same type blocks on all sides for ' + str(len(neightbors)) + ' materials'         

loneneighbors = {}
for mat in neightbors:
    print mat
    loneneighbors[mat] = {}
    for block in neightbors[mat]:

        if len(neightbors[mat][block]) > 0:
            loneneighbors[mat][block[0]+0.5, block[1]+0.5, block[2]+0.5]  = neightbors[mat][block]
    neightbors[mat] = None

neightbors = None

print 'generating vertices and faces for ' + str(len(loneneighbors)) + ' materials'
faces = {}
vertices = {}

for mat in loneneighbors:
    print mat
    faces[mat] = []
    vertices[mat] = {}

    for block in loneneighbors[mat]:

        if 5 in loneneighbors[mat][block]:
            loweplane = (block[0]-0.5,block[1]+0.5,block[2]+0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]-0.5,block[2]-0.5)
            
            facevertlinker(block, mat, loweplane)

        if 6 in loneneighbors[mat][block]:
            upperplane = (block[0]+0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5)
            
            facevertlinker(block, mat, upperplane)

        if 3 in loneneighbors[mat][block]:
            leftplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5)
            
            facevertlinker(block, mat, leftplane)

        if 4 in loneneighbors[mat][block]:
            rightplane = (block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
            
            facevertlinker(block, mat, rightplane)

        if 1 in loneneighbors[mat][block]:
            backplane = (block[0]-0.5,block[1]-0.5,block[2]-0.5),(block[0]-0.5,block[1]+0.5,block[2]-0.5),(block[0]+0.5,block[1]-0.5,block[2]-0.5),(block[0]+0.5,block[1]+0.5,block[2]-0.5)
            
            facevertlinker(block, mat, backplane)

        if 2 in loneneighbors[mat][block]:
            frontplane = (block[0]-0.5,block[1]-0.5,block[2]+0.5),(block[0]-0.5,block[1]+0.5,block[2]+0.5),(block[0]+0.5,block[1]-0.5,block[2]+0.5),(block[0]+0.5,block[1]+0.5,block[2]+0.5)
            facevertlinker(block, mat, frontplane)
    loneneighbors[mat] = None

print 'filtering the faces and materials for duplicates ' + str(len(loneneighbors)) + ' materials'

loneneighbors = None

for mat in vertices:
    vertices[mat] =  vertices[mat].values()

for vert in faces:
    faces[vert] = list(set(faces[vert]))


allstuff = {'allhistory':allhistory,'vertices':vertices,'faces':faces}

vertices = None
faces = None


print 'entitys with spawnmessage:' + str(len(allhistory)) + ',so used !'
print 'entitys without spawnmessage:' + str(len(lostcounter)) + ',so ignored !'

    
f.write(repr(allstuff))

