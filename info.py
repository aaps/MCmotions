#!/usr/bin/python -B

import sys, getopt
import ast
import base64
import struct
import svgwrite

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
    dwg = svgwrite.Drawing('test.svg',profile='full')
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

    matcount = sorted(matcount,key=lambda x: x[0], reverse = False)
    matcount = list(set(matcount))

    multyplier = 6
    colormult = 3
    if matcount[0][0] != 0:
        colormult = 256/float(matcount[0][0])

    
    counta = 0
    for mat in matcount:
        positions = ast.literal_eval(mat[1])
        position = positions[0]*multyplier , positions[1]*multyplier

        dwg.add(dwg.rect(position, (multyplier, multyplier), fill=svgwrite.rgb(mat[0]*colormult, 0, 0, '%')))

        if counta % 2 == 0:
            coloro = 'black'
            # print colormult
            if mat[0]*colormult < 50:
                coloro = 'white'

            textpos = position[0]+0.1 ,position[1] + 2
            text_style = "font-size:%ipx; font-family:%s" % (1, "Courier New") 
            dwg.add(dwg.text(str(mat[1]), insert=textpos, fill=coloro, style=text_style))
        # if counta == 100:
        #     break
        counta += 1
    dwg.save()


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
        print len(aroflines)

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

    # if opt == '--chunkmaxmin':
    #     getchunkminmax(aroflines)

