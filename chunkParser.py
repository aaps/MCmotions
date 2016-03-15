
import base64
import struct
import ast

# for now this is quite sloppy and need refactoring, my refactory system is to cut up stuff 
# first, this is the raw cutup later refactoring etc, own responsibility for ussage.

class chunkParser:

    def __init__(self, topleft = (-1000,-1000), bottomright = (1000,1000), cuty = 0, world = 1, norenderblocks = ["none"], multymatblocks = [35, 43, 44, 95, 97, 98, 125, 126, 139, 155, 159, 160, 171]):
        self.topleft = topleft
        self.bottomright = bottomright
        self.cuty = cuty
        self.world = world
        self.norenderblocks = norenderblocks
        self.multymatblocks = multymatblocks

    def setTopLeft(self, topleft = (-1000,-1000)):
        self.topleft = topleft

    def setBottomRight(self, bottomright = (1000,1000)):
        self.bottomright = bottomright

    def setCuty(self, cuty = 0):
        self.cuty = cuty

    def setWorld(self, world = 1):
        self.world = world

    def setNoRenderBlocks(self, norenderblocks = ["none"]):
        self.norenderblocks = norenderblocks



    def getchunks(self, row, chunks):
        chunkposses = []
        chunkxz = ast.literal_eval(row[1])
        if row[5] != 'None':
            chunkdata = base64.standard_b64decode(row[5])
            matsamples = []
            if chunkxz not in chunks:
                chunks.update({chunkxz:{'blocks':[]}})
            for x in xrange(1,17):
                if len(chunkdata[(256*x):(256*x)+2]) == 2:
                    temp = struct.unpack('H', chunkdata[(256*x):(256*x)+2])[0]
                    matsamples.append(temp >> 4)
            matsamples = list(set(matsamples))
            worldnum = self.worldfromsample(matsamples)

            if chunkxz not in chunkposses and chunkxz[0] >= self.topleft[0] and chunkxz[1] >= self.topleft[1] and chunkxz[0] <= self.bottomright[0] and chunkxz[1] <= self.bottomright[1] and self.world == worldnum:
                
                chunkposses.append(chunkxz)
                rightcounter = 0

                for index1 in xrange(0, 16):
                    # print row[3]
                    if (int(row[3]) & (1 << index1)) and row[3] != '0':
                        
                        for y in xrange(0,16):

                            for z in xrange(0,16):
                                for x in xrange(0,16):
                                    goodindex = (x+(z*16)+(y*256)+(rightcounter*4096))*2
                                    
                                    try:
                                        temp = struct.unpack('H',chunkdata[goodindex:goodindex+2])[0]
                                        btype = temp >> 4
                                        bmeta = temp & 15

                                    except Exception as e:
                                        btype = 666
                                        bmeta = 666
                                    
                                    block = ( (x + (chunkxz[0]*16),z + (chunkxz[1]*16),y+(index1*16)), btype, bmeta)
                                    if index1 > self.cuty:
                                        chunks[chunkxz]['blocks'].append(block)

                        rightcounter += 1


    def fillmatindexes(self, chunks, materials):
        for chunk in chunks:
            for block in chunks[chunk]:
                if len(chunks[chunk][block]) > 0:
                    
                    for x in chunks[chunk][block]:
                        position = x[0][0],x[0][1]*-1,x[0][2]
                        if x[1] > 0 and x[1] < 256 and x[1] not in self.norenderblocks:
                            
                            blockinfo = {position:{'meta':x[2],'faces':[]}}
                            if x[1] in self.multymatblocks:
                                if x[1] in [182 ,126 ,44] and x[2] > 7:
                                    x = x[0], x[1], x[2] - 8
                                if x[1] in [125,181, 43] and x[2] > 7:
                                    x = x[0], x[1], x[2] - 8

                                if (x[1],x[2]) not in materials:
                                    materials.update({(x[1],x[2]):blockinfo})
                                else:
                                    materials[(x[1],x[2])].update(blockinfo)
                            else:
                                if (x[1],0) not in materials:
                                    materials.update({(x[1],0):blockinfo})
                                else:
                                    materials[(x[1],0)].update(blockinfo) 
                chunks[chunk][block] = None

        chunks = None
        return materials

    def genfacesNeighbors(self, materials, agressiveremoval=False, colormats = {}):
        neightbors = {}
        allmaterials = {}

        print 'find material neightbors for ' + str(len(materials)) + ' materials'         
        
        # todo below is somewhat sloppy refactor material
        for mat in materials:
            for x in materials[mat]:
                materials[mat][x]['interneighbor'] = colormats[mat]['interneighbor']
                materials[mat][x]['extraneighbor'] = colormats[mat]['extraneighbor']
            allmaterials.update( materials[mat])


        for mat in materials:
            neightbors[mat] = {}

        for mat in materials:

            for block in materials[mat]:
                
                if agressiveremoval:
                    blockstocheck = allmaterials
                else:
                    blockstocheck = materials[mat]

                neightbors[mat][block] = {'meta': materials[mat][block]['meta'],'faces':[]}
                
                if (block[0]-1, block[1], block[2]) not in blockstocheck: 
                    neightbors[mat][block]['faces'].append(1)
                elif blockstocheck[(block[0]-1, block[1], block[2])]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(1)

                if (block[0]+1, block[1], block[2]) not in blockstocheck:
                    neightbors[mat][block]['faces'].append(2)
                elif blockstocheck[(block[0]+1, block[1], block[2])]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(2)

                if (block[0], block[1]-1, block[2]) not in blockstocheck:
                    neightbors[mat][block]['faces'].append(3)
                elif blockstocheck[(block[0], block[1]-1, block[2])]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(3)

                if (block[0], block[1]+1, block[2]) not in blockstocheck:
                    neightbors[mat][block]['faces'].append(4)
                elif blockstocheck[(block[0], block[1]+1, block[2])]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(4)

                if (block[0], block[1], block[2]-1) not in blockstocheck:
                    neightbors[mat][block]['faces'].append(5)
                elif blockstocheck[(block[0], block[1], block[2]-1)]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(5)

                if (block[0], block[1], block[2]+1) not in blockstocheck: 
                    neightbors[mat][block]['faces'].append(6)
                elif blockstocheck[(block[0], block[1], block[2]+1)]['extraneighbor']:
                    neightbors[mat][block]['faces'].append(6)
                    
            materials[mat] = None
        return neightbors

    def removeSupderCosy(self, neightbors, colormaterials):
        loneneighbors = {}
        for mat in neightbors:
            
            if mat in colormaterials and 'interneighbor' in colormaterials[mat] and colormaterials[mat]['interneighbor']:
                removeneibors = False
            else:
                removeneibors = True

            loneneighbors[mat] = {}
            for block in neightbors[mat]:

                if len(neightbors[mat][block]['faces']) > 0 or not removeneibors:

                    loneneighbors[mat][block[0]+0.5, block[1]+0.5, block[2]+0.5]  = neightbors[mat][block]

            neightbors[mat] = None
        return loneneighbors

    def worldfromsample(self, sample):
        overworldblocks = [1,2,3,4,6,8,9,12,13, 15,16,17,18,37,38,39,40]
        netherblocks = [10,11,87,88, 112,113,114,115,153]
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