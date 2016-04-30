#!/usr/bin/python -B

import sys, getopt
import ast
import base64
import struct
import svgwrite
from ChunkParser import ChunkParser

sourcefile = "default.dump"
blocksize = 200
chunkrange = 1
center = (0,0)

chunkparser = ChunkParser()


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
    dwg = svgwrite.Drawing('test.svg',profile='full')

    multyplier = 6

    for line in aroflines:
        btype = -1
        row = line.split('|')
        counter = 0
        if 'chunkdata' == row[0]:
            chunkparser.get_chunks(row)
        elif 'changedim' == row[0]:
            chunkparser.set_world_num(int(row[1]))


    planes = {}
    counta = 0
    maxval = 0
    mats = chunkparser.get_mat_count()
    print "got all the mats !"
    for mat in mats:
        if matnum in mats[mat]:
            position = mat[0]*multyplier , mat[1]*multyplier
            color = mats[mat][matnum]
            planes.update( {position: color} )
            if maxval < color:
                maxval = color

    for plane in planes:
        rightcolor = (planes[plane] / float(maxval)*256)

        dwg.add(dwg.rect(plane, (multyplier, multyplier), fill=svgwrite.rgb(rightcolor, 0, 0, '%')))

        if counta % 8 == 0:
            coloro = 'black'
            
            if rightcolor < 50:
                coloro = 'white'


            textpos = plane[0]+0.1 ,plane[1] + 2
            text_style = "font-size:%ipx; font-family:%s" % (1, "Courier New") 
            dwg.add(dwg.text(str(plane[0]) + '*' + str(plane[1]), insert=textpos, fill=coloro, style=text_style))

        counta += 1
    dwg.save()


try:
    opts, args = getopt.getopt(sys.argv[1:],"",["chunkmaxmin=","sourcefile=","image=","center=", "range=" ])
        
except getopt.GetoptError:

    print 'error: info.py -h --chunkmaxmin --sourcefile --image --center --range'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'info.py -h --chunkmaxmin --sourcefile --image --center --range'
        sys.exit()
    if opt == '--sourcefile':

        sourcefile = arg
        aroflines = getsourcefile()
        # print len(aroflines)

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

chunkparser.get_counts()
makeimage(aroflines, matnum)