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

# import StringIO

sourcefile = "default.log"
destfile = "default.json"
sesnrtoget = 0
avgmiddle = False

try:
    opts, args = getopt.getopt(sys.argv[1:],"",["avgmiddle=","sourcefile=","destfile=","session=", "avgmiddle="])
        
except getopt.GetoptError:
    print 'error: lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'lister.py --avgmiddle --sourcefile filename --destfile filename --session sesnumber'
        sys.exit()

    if opt == "--sourcefile":
        sourcefile = arg + ".log"

    if opt == "--destfile":
        destfile = arg + ".json"

    if opt == "--session":
        sesnrtoget = int(arg)

    if opt == "--avgmiddle":
        # print arg
        if arg == 'yes':
            avgmiddle = True


allhistory = {}


currentses = 0
lostcounter = []

f = open(destfile, 'w')

origin = open(sourcefile, 'r')

total = origin.read()

aroflines = total.split('\n')

chunks = []


def fido(first, second):
    x=min(first[0]-second[0], first[0]-second[0]+2*math.pi, first[0]-second[0]-2*math.pi, key=abs)
    y=min(first[1]-second[1], first[1]-second[1]+2*math.pi, first[1]-second[1]-2*math.pi, key=abs)
    z=min(first[2]-second[2], first[2]-second[2]+2*math.pi, first[2]-second[2]-2*math.pi, key=abs)
    return (x,y,z)

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

        
    elif row[0] == 'spawnmob' and sesnrtoget == currentses:
        

        goodpos = ast.literal_eval(row[4])
        rawyawpichhead = ast.literal_eval(row[5])
        
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
        

        yawpichhead = yawpich[0],yawpich[1],lastlist['yawpichhead'][2]
        yawpichhead = fido( yawpichhead, lastlist['yawpichhead'])
        # print yawpichhead

        allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':absolutepos,'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})

    elif row[0] == 'entityheadlook' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        
        # print lastlist['yawpichhead']
        if not ast.literal_eval(row[3]) == lastlist['yawpichhead'][2]:
            
            yawpichhead = lastlist['yawpichhead'][0], lastlist['yawpichhead'][1], ast.literal_eval(row[3])
            yawpichhead = fido( yawpichhead, lastlist['yawpichhead'])

            allhistory[int(row[2])]['positions'].append({'time':float(row[1]),'pos':lastlist['pos'],'yawpichhead':yawpichhead,'status':0,'alive':lastlist['alive']})


    elif row[0] == 'entityteleport' and int(row[2]) in allhistory and sesnrtoget == currentses:
        
        goodpos = ast.literal_eval(row[3])
        goodpos = (float(goodpos[0])/32, float(goodpos[1])/32, float(goodpos[2])/32)
        
        lastlist = allhistory[int(row[2])]['positions'][-1]
        yawpich = ast.literal_eval(row[4])
        yawpichhead = yawpich[0], yawpich[1], lastlist['yawpichhead'][2]
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
        print hex(int(row[3]))
        try:
            onechunk = base64.standard_b64decode(row[4])
            


            for x in xrange(0,int(length)/2):
                
                total = struct.unpack('H',onechunk[x:x+2])[0]
                if x % 2 == 1:
                    blocktype = total & 15
                    blockmeta = (total >> 4) & 15
                else:
                    blockmeta = total & 15
                    blocktype = (total >> 4) & 15
                print blocktype, blockmeta


            # chunks.append()
        except Exception as e:
            print e





print 'entitys with spawnmessage:' + str(len(allhistory)) + ',so used !'
print 'entitys without spawnmessage:' + str(len(lostcounter)) + ',so ignored !'
    
f.write(json.dumps(allhistory))

