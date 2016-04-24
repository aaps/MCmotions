#!/usr/bin/python -B

import base64
import struct
import ast
from quarry.utils.buffer import Buffer

class ChunkParser(object):

    def __init__(self, topleft=(-1000, -1000), bottomright=(1000, 1000), cuty=0, world=1, norenderblocks=["none"], multymatblocks=[35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171], colormats={}):
        self.colormats = colormats
        self.topleft = topleft
        self.bottomright = bottomright
        self.cuty = cuty
        self.world = world
        self.norenderblocks = norenderblocks
        self.multymatblocks = multymatblocks
        self.chunks = {}
        self.materials= {}
        self.neightbors = {}
        self.worldnum = 0
        self.chunkbuffer = Buffer()

    def set_top_left(self, topleft=(-1000, -1000)):
        self.topleft = topleft

    def set_bottom_right(self, bottomright=(1000, 1000)):
        self.bottomright = bottomright

    def set_cut_y(self, cuty=0):
        self.cuty = cuty

    def set_world(self, world=1):
        self.world = world

    def set_no_render_blocks(self, norenderblocks=["none"]):
        self.norenderblocks = norenderblocks


    def get_chunks(self, row):
        chunkposses = []
        chunkxz = ast.literal_eval(row[1])
        chunkdata = base64.standard_b64decode(row[5])
        self.chunkbuffer.add(chunkdata)
        blocks = []
        self.chunkbuffer.save()

        matsamples = []
        if chunkxz not in self.chunks:
            self.chunks.update({chunkxz:{'blocks':[]}})

        rightcounter = 0
        if chunkxz not in chunkposses and chunkxz[0] >= self.topleft[0] and chunkxz[1] >= self.topleft[1] and chunkxz[0] <= self.bottomright[0] and chunkxz[1] <= self.bottomright[1]:
            chunkposses.append(chunkxz)

            for index1 in range(16):
                

                if (int(row[3]) & (1 << index1)):
                    
                    bitsperblock = self.chunkbuffer.unpack('B')
                    usespalette = True
                    
                    blocklight = []
                    skylight = []
                    if bitsperblock == 0:
                        bitsperblock = 13
                        usespalette = False

                    palletelength = self.chunkbuffer.unpack_varint()

                    palette = []
                    blockdata = []
                    maxvalue = (1 << bitsperblock) - 1
                    for palindex in range(palletelength):
                        palette.append(self.chunkbuffer.unpack_varint())

                    dataarrlength = self.chunkbuffer.unpack_varint()
                    
                    for dataind in range(dataarrlength):
                        blockdata.append(self.chunkbuffer.unpack('Q'))


                    unneededlength = (dataarrlength*16)
                    for notneed in range(unneededlength):
                       self.chunkbuffer.unpack('B')

                    for ypos in xrange(0, 16):
                            for zpos in xrange(0, 16):
                                for xpos in xrange(0, 16):
                                    goodindex = xpos+(zpos*16)+(ypos*256)
                                    startlong = (goodindex * bitsperblock) // 64
                                    startoffset = (goodindex * bitsperblock) % 64
                                    endlong = ((goodindex + 1) * bitsperblock - 1) // 64
                                    if startlong == endlong and len(blockdata) > 0:
                                        temp = (blockdata[startlong] >> startoffset) & maxvalue

                                    elif len(blockdata) > 0:
                                        endoffset = 64 - startoffset
                                        temp = (blockdata[startlong] >> startoffset
                                                 | blockdata[endlong] << endoffset
                                                 ) & maxvalue
                                    else:
                                        temp = -1

                                    
                                    if usespalette and temp > -1:  # convert to global palette
                                        btype = palette[temp] >> 4
                                        bmeta = palette[temp] & 15
                                        bbtest = ((xpos + (chunkxz[0]*16), zpos + (chunkxz[1]*16), ypos+(index1*16)), int(btype), int(bmeta))
                                        # blocks.append(bbtest)
                                    elif temp > -1:
                                        btype = temp >> 4
                                        bmeta = temp & 15
                                        bbtest = ((xpos + (chunkxz[0]*16), zpos + (chunkxz[1]*16), ypos+(index1*16)), int(btype), int(bmeta))
                                        # blocks.append(bbtest)
                                    else:
                                        bbtest = ((xpos + (chunkxz[0]*16), zpos + (chunkxz[1]*16), ypos+(index1*16)), 0, 0)
                                        # blocks.append(bbtest)
                                    
                                    if index1 > self.cuty:
                                        self.chunks[chunkxz]['blocks'].append(bbtest)
        
                    
        self.chunkbuffer.discard()
        # return blocks



    def fill_mat_indexes(self):
        for chunk in self.chunks:
            for block in self.chunks[chunk]:
                if len(self.chunks[chunk][block]) > 0:
                    for idindex in self.chunks[chunk][block]:
                        position = idindex[0][0], idindex[0][1]*-1, idindex[0][2]
                        if idindex[1] > 0 and idindex[1] < 256 and idindex[1] not in self.norenderblocks:
                            blockinfo = {position:{'meta':idindex[2], 'faces':[]}}
                            if idindex[1] in self.multymatblocks:
                                if idindex[1] in [182, 126, 44] and idindex[2] > 7:
                                    idindex = idindex[0], idindex[1], idindex[2] - 8
                                if idindex[1] in [125, 181, 43] and idindex[2] > 7:
                                    idindex = idindex[0], idindex[1], idindex[2] - 8
                                if (idindex[1], idindex[2]) not in self.materials:
                                    self.materials.update({(idindex[1], idindex[2]):blockinfo})
                                else:
                                    self.materials[(idindex[1], idindex[2])].update(blockinfo)
                            else:
                                if (idindex[1], 0) not in self.materials:
                                    self.materials.update({(idindex[1], 0):blockinfo})
                                else:
                                    self.materials[(idindex[1], 0)].update(blockinfo)
                self.chunks[chunk][block] = None
        self.chunks = None


    def gen_faces_neighbors(self, agressiveremoval=False):
        allmaterials = {}
        print 'find material neightbors for ' + str(len(self.materials)) + ' materials'
        # todo below is somewhat sloppy refactor material
        


        for mat in self.materials:
            if mat in self.materials and mat in self.colormats:
                for blockindex in self.materials[mat]:
                    self.materials[mat][blockindex]['interneighbor'] = self.colormats[mat]['interneighbor']
                    self.materials[mat][blockindex]['extraneighbor'] = self.colormats[mat]['extraneighbor']
                allmaterials.update(self.materials[mat])

        for mat in self.materials:
            if mat in self.materials and mat in self.colormats:
                self.neightbors[mat] = {}
        for mat in self.materials:
            if mat in self.materials and mat in self.colormats:
                for block in self.materials[mat]:
                    if agressiveremoval:
                        blockstocheck = allmaterials
                    else:
                        blockstocheck = self.materials[mat]
                    self.neightbors[mat][block] = {'meta': self.materials[mat][block]['meta'], 'faces':[]}
                    if (block[0]-1, block[1], block[2]) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(1)
                    elif blockstocheck[(block[0]-1, block[1], block[2])]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(1)
                    if (block[0]+1, block[1], block[2]) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(2)
                    elif blockstocheck[(block[0]+1, block[1], block[2])]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(2)
                    if (block[0], block[1]-1, block[2]) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(3)
                    elif blockstocheck[(block[0], block[1]-1, block[2])]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(3)
                    if (block[0], block[1]+1, block[2]) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(4)
                    elif blockstocheck[(block[0], block[1]+1, block[2])]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(4)
                    if (block[0], block[1], block[2]-1) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(5)
                    elif blockstocheck[(block[0], block[1], block[2]-1)]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(5)
                    if (block[0], block[1], block[2]+1) not in blockstocheck:
                        self.neightbors[mat][block]['faces'].append(6)
                    elif blockstocheck[(block[0], block[1], block[2]+1)]['extraneighbor']:
                        self.neightbors[mat][block]['faces'].append(6)
                self.materials[mat] = None


    def remove_super_cosy(self):
        loneneighbors = {}
        for mat in self.neightbors:
            if mat in self.colormats and 'interneighbor' in self.colormats[mat] and self.colormats[mat]['interneighbor']:
                removeneibors = False
            else:
                removeneibors = True
            loneneighbors[mat] = {}
            for block in self.neightbors[mat]:
                if len(self.neightbors[mat][block]['faces']) > 0 or not removeneibors:
                    loneneighbors[mat][block[0]+0.5, block[1]+0.5, block[2]+0.5] = self.neightbors[mat][block]
            self.neightbors[mat] = None
        return loneneighbors

    def world_from_sample(self, sample):
        overworldblocks = [1, 2, 3, 4, 6, 8, 9, 12, 13, 15, 16, 17, 18, 37, 38, 39, 40]
        netherblocks = [10, 11, 87, 88, 112, 113, 114, 115, 153]
        theendblocks = [121]
        overscore = 0
        endscore = 0
        netherscore = 0
        for block in sample:
            if block in overworldblocks:
                overscore += 1
            if block in netherblocks:
                netherscore += 1
            if block in theendblocks:
                endscore += 1
        if endscore > overscore and endscore > netherscore:
            return 3
        elif netherscore > endscore and netherscore > overscore:
            return 2
        else:
            return 1
