#!/usr/bin/python -B

import sys, getopt
import ast
from PIL import Image, ImageDraw, ImageFont
import base64
import struct

sourcefile = "default.dump"


def getsourcefile():
    try:
        origin = open(sourcefile, 'r')
    except Exception as e:
        print e
        print 'try it with --sourcefile dumpfile'
        exit()

    total = origin.read()

    return total.split('\n')


def makeimage(aroflines,matnum):
    dims = (2000,2000)
    halfdims = dims[0]/2,dims[1]/2
    im = Image.new('RGBA', dims, (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    matcount = []

    
    for line in aroflines:
        row = line.split('|')
        counter = 0
        if 'chunkdata' == row[0]:
            chunkdata = base64.standard_b64decode(row[5])
            xzpos = ast.literal_eval(row[1])
            for index1 in xrange(0, 16):
                        if int(row[3]) & (1 << index1):
                            for y in xrange(0,16):
                                for z in xrange(0,16):
                                    for x in xrange(0,16):
                                        goodindex = (x+(z*16)+(y*256)+(index1*4096))
                                        try:
                                            temp = struct.unpack('H',chunkdata[goodindex*2:goodindex*2+2])[0]
                                            btype = temp >> 4
                                        except Exception as e:
                                            pass
                                        if btype == matnum:
                                            counter += 1
            matcount.append( (counter, row[1]))

    matcount = sorted(matcount,key=lambda x: x[0], reverse=True)

    multyplier =   256/float(matcount[0][0])
    font = ImageFont.truetype("FreeMono.ttf", 10)

    for mats in matcount:
        # print mats[1]
        chunkxy = ast.literal_eval(mats[1])
        one = (chunkxy[0]*50)+halfdims[0], (chunkxy[1]*50)+halfdims[1]
        two = (chunkxy[0]*50) + 49 + halfdims[0], chunkxy[1]*50 + 49 + halfdims[1]
        # print multyplier, mats[0]
        draw.rectangle([one,two], (int(multyplier* mats[0]),0,0))
        draw.text(one, str(chunkxy),(255,255,255),font=font)
    im.save("diags.png")



def getchunkminmax(aroflines):


    maxminx = [1000,-1000]
    maxminz = [1000,-1000]

    for line in aroflines:
        row = line.split('|')
        # if row[0] == 'startrecord':
            # currentses =+ 1

        if 'chunkdata' == row[0]:
            chunkxy = ast.literal_eval(row[1])
            if chunkxy[0] > maxminx[1]:
                maxminx[1] = chunkxy[0]
            if chunkxy[0] < maxminx[0]:
                maxminx[0] = chunkxy[0]

            if chunkxy[1] > maxminz[1]:
                maxminz[1] = chunkxy[1]
            if chunkxy[1] < maxminz[0]:
                maxminz[0] = chunkxy[1]

    print 'maxminx:' + str(maxminx) + ' maxminz: ' + str(maxminz)

try:
    opts, args = getopt.getopt(sys.argv[1:],"",["chunkmaxmin=","sourcefile=","scenes=","image=" ])
        
except getopt.GetoptError:

    print 'error: info.py -h --chunkmaxmin --sourcefile --scenes --image'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'info.py -h --chunkmaxmin --sourcefile --scenes --image'
        sys.exit()
    if opt == '--sourcefile':
        sourcefile = arg
        aroflines = getsourcefile()

    if opt == "--scenes":
        listofscenes = []
        for line in aroflines:
            # print line
            row = line.split('|')
            if row[0] in ['entityteleport','entitylookandrelmove','entityheadlook','entitylook','entityrelmove']:
                listofscenes.append(row[2])
        for scene in list(set(listofscenes)):
            print scene

    if opt == "--image":
        
        matnum = int(arg)

        makeimage(aroflines, matnum)

    if opt == '--chunkmaxmin':
        getchunkminmax(aroflines)

