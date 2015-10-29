#!/usr/bin/python -B

import sys, getopt
# import json
import ast

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

def getchunkminmax(aroflines):
    currentses = 0
    sesnrtoget = 0



    maxminx = [1000,-1000]
    maxminz = [1000,-1000]

    for line in aroflines:
        row = line.split('|')
        if row[0] == 'startrecord':
            currentses =+ 1

        if 'chunkdata' == row[0] and sesnrtoget == currentses:
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
    opts, args = getopt.getopt(sys.argv[1:],"",["chunkmaxmin=","sourcefile=","scenes=" ])
        
except getopt.GetoptError:

    print 'error: info.py -h --chunkmaxmin --sourcefile --scenes'
    sys.exit(2)
for opt, arg in opts:
    # print opt
    if opt == '-h':
        print 'info.py -h --chunkmaxmin'
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


    if opt == '--chunkmaxmin':
        getchunkminmax(aroflines)

