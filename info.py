#!/usr/bin/python -B

import sys, getopt
import ast
from PIL import Image, ImageDraw, ImageFont
import base64
import struct

sourcefile = "default.dump"
blocksize = 200

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

    dims = (100,100)

    matcount = []
    scenelist = []

    for line in aroflines:
        row = line.split('|')
        counter = 0
        if row[0] in ['entityteleport','entitylookandrelmove','entityheadlook','entitylook','entityrelmove']:
            scenelist.append(row[2])
    scenelist =  list(set(scenelist))
    
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

    multyplier = 1
    if matcount[0][0] != 0:
        multyplier = 256/float(matcount[0][0])
    
    
    font = ImageFont.truetype("FreeMono.ttf", 14)

    for mats in matcount:
        chunkxy = ast.literal_eval(mats[1])
        if chunkxy[0] * blocksize > dims[0]:
            dims = chunkxy[0] * blocksize, dims[1]
        elif (chunkxy[0]*-1) * blocksize > dims[0]:
            dims = (chunkxy[0]*-1) * blocksize, dims[1]

        if chunkxy[1] * blocksize > dims[1]:
            dims = dims[0], chunkxy[1] * blocksize
        elif (chunkxy[1]*-1) * blocksize > dims[1]:
            dims = dims[0], (chunkxy[1]*-1) * blocksize


    halfdims = dims[0]/2,dims[1]/2
    im = Image.new('RGBA', dims, (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0,0),dims],(100,100,100))

    for mats in matcount:
        chunkxy = ast.literal_eval(mats[1])
        one = (chunkxy[0]*(blocksize/2))+halfdims[0], (chunkxy[1]*(blocksize/2))+halfdims[1]
        two = (chunkxy[0]*(blocksize/2)) + (blocksize/2) - 1 + halfdims[0], chunkxy[1]*(blocksize/2) + (blocksize/2) - 1 + halfdims[1]

        draw.rectangle([one,two], (int(multyplier* mats[0]),0,0))
        draw.text(one, 'x' + str(chunkxy[0]) + ',z' + str(chunkxy[1]),(255,255,255),font=font)
    position = 0
    for scene in scenelist:
        draw.text((10, 10),"SCENES:", (0,0,0),font=font)
        position += 20
        draw.text((10, position), scene, (0,0,0),font=font)


    
    
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
    opts, args = getopt.getopt(sys.argv[1:],"",["chunkmaxmin=","sourcefile=","image=" ])
        
except getopt.GetoptError:

    print 'error: info.py -h --chunkmaxmin --sourcefile --image'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'info.py -h --chunkmaxmin --sourcefile --image'
        sys.exit()
    if opt == '--sourcefile':
        sourcefile = arg
        aroflines = getsourcefile()

    # if opt == "--scenes":
    #     listofscenes = []
    #     for line in aroflines:
    #         # print line
    #         row = line.split('|')
    #         if row[0] in ['entityteleport','entitylookandrelmove','entityheadlook','entitylook','entityrelmove']:
    #             listofscenes.append(row[2])
    #     for scene in list(set(listofscenes)):
    #         print scene

    if opt == "--image":
        
        matnum = int(arg)

        makeimage(aroflines, matnum)

    if opt == '--chunkmaxmin':
        getchunkminmax(aroflines)

