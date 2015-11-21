#!/usr/bin/python -B

from quarry.net.proxy import DownstreamFactory, Bridge, UpstreamFactory
from quarry.mojang.profile import Profile
import time
import base64
import sys, getopt
import getpass
import zlib
import array
import struct

class QuietBridge(Bridge):
    quiet_mode = False
    worldtime = 0
    begintime = 0
    dumpsize = 0
    inscene = False
    recording = False
    scenename = "noscene"

    # hieronder gaat het over het spawnen van player monsters etc

    def packet_upstream_chat_message(self, buff):
        buff.save()

        string = buff.unpack_string()
        if self.recording:
            if  string[0:7] == '/action':
                if not self.inscene:
                    self.scenename = string[8:]
                    self.inscene = True
                    message = "Recorder: " + self.scenename + " Action !!!"
        
                    self.upstream.send_packet("chat_message", self.write_chat(message, "upstream"))

            elif string == '/cut':
                if self.inscene:
                    self.inscene = False
                    message = "Recorder: " + self.scenename + " Cut !!!"
                    self.scenename = "noscene"
                    
                    self.upstream.send_packet("chat_message", self.write_chat(message, "upstream"))
            elif  string == '/stop':
                self.recording = False
                
                message = "Recording stopped after " + str( self.worldtime - self.begintime) + " ticks of recording!"
                self.downstream.send_packet("chat_message", self.write_chat(message, "downstream"))


            elif string == '/status':
                message = "Not recording !"
                if self.recording:
       
                    message = "Recording for: " + str( self.worldtime - self.begintime) + " ticks !, inscene:" + self.scenename + ", filesize: " + str(self.dumpsize/1024)
                
                self.downstream.send_packet("chat_message", self.write_chat(message, "downstream"))

            elif string[0:7] == '/addcam':
                message = "Not recording !"
                if self.recording:
                    camtype = string[8:]

                    if camtype == 'static':
                        message = "Adding static cam at: " + self.playerpos + " Angle: " + self.playerangle
                        towrite = 'addcam|' + '|static|' + self.playerangle +'|' + self.playerpos + '|' + '\n'
                    elif camtype == 'tracking':
                        message = "Adding tracking cam at: " + self.playerpos
                        towrite = 'addcam|' + '|tracking|' + self.playerpos + '|' + '\n'
                    elif camtype == 'chasing':
                        message = "Adding chasing cam at: " + self.playerpos
                        towrite = 'addcam|' + '|chasing|' + self.playerpos + '|' + '\n'
                    else:
                        message = "No cam added"
                        towrite = None
                    
                    if towrite:
                        self.dumpsize += len(towrite)
                        self.dumpfile.write(towrite)
                self.downstream.send_packet("chat_message", self.write_chat(message, "downstream"))


        else:
            buff.restore()
            self.upstream.send_packet("chat_message", buff.read())

    def packet_downstream_time_update(self, buff):
        buff.save()
        if self.recording:
            unknown = buff.unpack('l')
            self.worldtime = buff.unpack('l')
            if self.begintime == 0:
                self.begintime = self.worldtime
  
            buff.restore()
        self.downstream.send_packet("time_update", buff.read())

    def packet_downstream_spawn_player(self, buff):
        buff.save()
        if self.recording:
            towrite = 'spawnplayer|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack_uuid()) + '|' + str(buff.unpack('iii')) + '|' +  str(buff.unpack('bb'))+ '|' +  str(buff.unpack('h')) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("spawn_player", buff.read())

    def packet_downstream_spawn_object(self, buff):
        buff.save()
        if self.recording:
            theid = str(buff.unpack_varint())
            thetype = str(buff.unpack('B'))
            theposition = str(buff.unpack('iii'))
            towrite = 'spawnobject|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + theid + '|' + thetype + '|' + theposition + '|' +  str(buff.unpack('bb')) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("spawn_object", buff.read())

    def packet_downstream_spawn_mob(self, buff):
        buff.save()
        if self.recording:
            towrite = 'spawnmob|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('B')) + '|' + str(buff.unpack('iii')) + '|' +  str(buff.unpack('bbb')) + '|' +  str(buff.unpack('hhh')) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("spawn_mob", buff.read())

    # metadata gaat nog een dingetje worden, gelukkig nog niet belangrijk

    # def packet_downstream_entity_metadata(self, buff):
    #     buff.save()

        # print buff.unpack_varint()

        # abyte =  buff.unpack('c')
        # if ord(abyte) != 0x7F:
        #     index = ord(abyte) & 0x1F
        #     atype = ord(abyte) >> 5

            # print 'type: ' + str(atype) + ' index: ' + str(index) + ' '

            # if atype != 6 and atype != 5 and atype != 7 and atype != 4:
            #     print atype

            # if atype == 0:
            #     print buff.unpack('c')
            # elif atype == 1:
            #     print buff.unpack('h')
            # elif atype == 2:
            #     print buff.unpack('i')
            # elif atype == 3:
            #     print buff.unpack('f')
            # elif atype == 6:
            #     print buff.unpack('iii')
            # elif atype == 4:
            #     print buff.unpack_string()
            # elif atype == 7:
            #     print buff.unpack('fff')
            # elif atype == 5:
            #     print buff.unpack('h')



        # buff.restore()
        # self.downstream.send_packet("entity_metadata", buff.read())

    ## hieronder beginnen we met het opnemen van bewegingen

    def packet_downstream_entity(self, buff):
        buff.save()
        if self.recording:
            towrite = 'entity|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity", buff.read())


    def packet_downstream_entity_relative_move(self, buff):
        buff.save()
        if self.recording:
            towrite = 'entityrelmove|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('bbb')) + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_relative_move", buff.read())

    def packet_downstream_entity_look(self, buff):
        buff.save()
        
        if self.recording:
            towrite = 'entitylook|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('bb')) + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_look", buff.read())

    def packet_downstream_entity_look_and_relative_move(self, buff):
        buff.save()
        if self.recording:
            towrite = 'entitylookandrelmove|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('bbb')) + '|' + str(buff.unpack('bb')) + '|' + str(buff.unpack('?')) + '\n'
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_look_and_relative_move", buff.read())
   
    def packet_downstream_entity_teleport(self, buff):
        buff.save()
        if self.recording:   
            towrite = 'entityteleport|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('iii')) + '|' + str(buff.unpack('bb')) + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            
            buff.restore()
        self.downstream.send_packet("entity_teleport", buff.read())

    def packet_downstream_entity_velocity(self, buff):
        buff.save()
        if self.recording:
            towrite ='entityvelocity|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('hhh'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_velocity", buff.read())

    def packet_downstream_entity_head_look(self, buff):
        buff.save()
        if self.recording:   
            towrite = 'entityheadlook|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('b'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_head_look", buff.read())

    def packet_downstream_entity_status(self, buff):
        buff.save()
        if self.recording:
            towrite = 'entitystatus|' + str( self.worldtime - self.begintime) +  '|' + self.scenename + '|' + str(buff.unpack('i')) + '|' + str(buff.unpack('b'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_status", buff.read())

    def packet_downstream_entity_effect(self, buff):
        buff.save()
        if self.recording:    
            towrite = 'entityeffect|' + str( self.worldtime - self.begintime) +  '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('b')) + '|' + str(buff.unpack('b')) + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("entity_effect", buff.read())

    def packet_downstream_remove_entity_effect(self, buff):
        buff.save()
        if self.recording:
            towrite = 'rementityeffect|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(buff.unpack_varint()) + '|' + str(buff.unpack('b'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("remove_entity_effect", buff.read())

    # where all entirys get destroyed

    def packet_downstream_destroy_entities(self, buff):
        buff.save()
        if self.recording:
            length = buff.unpack_varint()
            entitys = []
            for aent in xrange(0,length):
                entitys.append(buff.unpack_varint())
            towrite = 'destroyents|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' +  '|'.join(map(str, entitys))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            
            buff.restore()
        self.downstream.send_packet("destroy_entities", buff.read())

    def packet_downstream_disconnect(self, buff):
        buff.save()
        if self.recording:
            towrite = 'disconnect|' + buff.unpack_chat() + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("disconnect", buff.read())

    def packet_downstream_keep_alive(self, buff):
        buff.save()
        if self.recording:
            towrite = 'keep_alive|' + str(buff.unpack_varint()) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.downstream.send_packet("keep_alive", buff.read() )


    # block and chunk stuff

    # notyet doing this since i cant decode chunk data yet and it is a lot of data to record

    def packet_downstream_chunk_data(self, buff):
        buff.save()

        if self.recording:
            chunkxy = buff.unpack('ii')
            groundup = buff.unpack('?')
            pribitmask = buff.unpack('H')

            if pribitmask > 0:
                datalength = buff.unpack_varint()
                contents = base64.b64encode(buff.unpack(str(datalength) + 's'))
                towrite = 'chunkdata|' + str(chunkxy) + '|' + str(groundup) + '|' + str(pribitmask) + '|' + str(datalength) + '|' + contents +'\n'
                self.dumpsize += len(towrite)
                self.dumpfile.write(towrite)
            
            buff.restore()
        self.downstream.send_packet("chunk_data", buff.read())


    def packet_downstream_map_chunk_bulk(self, buff):
        buff.save()
        if self.recording:
            
            lengths = 0
            chunkar = []
            metaar = []
            skylightsend = buff.unpack('?')
            nrchunks = buff.unpack_varint()

            for index in xrange(0,nrchunks):
                chunkxy = buff.unpack('ii')
                pribitmask = buff.unpack('H')
                metaar.append( (chunkxy,pribitmask) )

            for index in xrange(0,nrchunks):
                bigstring = ''
                counter = 0
                
                for height in xrange(0,16):

                    if int(metaar[index][1]) & (1 << height):
                        counter += 4096
                        bigstring += buff.unpack(str(4096*2) + 's')

                chunkar.append(base64.b64encode(bigstring))
                
                metaar[index] = metaar[index][0], metaar[index][1], counter

                lightstuff = buff.unpack(str(counter) + 's')
                biomemeta = buff.unpack(str(256) + 's')



            for index in xrange(0,nrchunks):
                towrite = 'chunkdata|' + str(metaar[index][0]) +  '|True|' + str(metaar[index][1]) + '|' + str(metaar[index][2]) + '|' + chunkar[index] + '\n'
                self.dumpsize += len(towrite)
                self.dumpfile.write(towrite)

        buff.restore()
        self.downstream.send_packet("map_chunk_bulk", buff.read())


    def packet_downstream_multi_block_change(self, buff):
        buff.save()
        if self.recording:
            chunkxz = buff.unpack('ii')
            reccount = buff.unpack_varint()
            for index in xrange(0,reccount):
                xz = buff.unpack('B')
                
                x = ((xz >> 4) & 0xF) + (chunkxz[0] * 16)
                z = (xz & 0xF) + (chunkxz[1] * 16)
                y = buff.unpack('B')
                newid = buff.unpack_varint() >> 4
                towrite = 'blockchange|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str((x,z,y)) + '|' + str(newid)+ '\n'
                self.dumpsize += len(towrite)
                self.dumpfile.write(towrite)
            buff.restore()
            
        self.downstream.send_packet("multi_block_change", buff.read())
        

    def packet_downstream_block_change(self, buff):
       
        buff.save()
        if self.recording:
            xyz = self.unpack_blockposition(buff)
            newid = buff.unpack_varint() >> 4
            towrite = 'blockchange|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(xyz) + '|' + str(newid)+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()

        self.downstream.send_packet("block_change", buff.read())

    def packet_downstream_block_action(self, buff):
        buff.save()
        if self.recording:
            xyz = self.unpack_blockposition(buff)
            bytea = buff.unpack('B')
            byteb = buff.unpack('B')
            blocktype = buff.unpack_varint()
            towrite = 'blockaction|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(xyz) + '|' + str(bytea) + '|' + str(byteb) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()

        self.downstream.send_packet("block_action", buff.read())

    def packet_downstream_block_break_animation(self, buff):
        # this one is not working, tough shite.
        buff.save()
        if self.recording:
            
            entid = buff.unpack_varint()
            xyz = self.unpack_blockposition(buff)
            if xyz[0] < 33554431 and xyz[0] > -33554431 and xyz[2] < 33554431 and xyz[2] > -33554431:

                stage = buff.unpack('b')
                towrite = 'blockbreak|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(entid) + '|' + str(xyz) + '|' + str(stage) + '\n'
                self.dumpsize += len(towrite)
                self.dumpfile.write(towrite)

            buff.restore()
        self.downstream.send_packet("block_break_animation", buff.read())

    def packet_downstream_particle(self, buff):
        buff.save()
        if self.recording:
            partid = buff.unpack('i')
            longdist = buff.unpack('?')
            pos = buff.unpack('fff')
            offset = buff.unpack('fff')
            data = buff.unpack('f')
            partcount = buff.unpack('i')
            
            towrite = 'particle|' + str( self.worldtime - self.begintime) + '|' + self.scenename + '|' + str(partid) + '|' + str(longdist) + '|' + str(pos) + '|' + str(offset) + '|' + str(data) + '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
                
            buff.restore()
        self.downstream.send_packet("particle", buff.read())

    # def packet_downstream_plugin_message(self, buff):
    #     buff.save()
    #     if self.recording:
    #         towrite = 'plugin|' + buff.unpack_string() + '\n'
    #         self.dumpsize += len(towrite)
    #         self.dumpfile.write(towrite)
    #         buff.restore()
    #     self.downstream.send_packet("plugin_message", buff.read())

    def packet_upstream_player_position(self, buff):
        buff.save()
        if self.recording:
            self.playerpos = str(buff.unpack('ddd'))

            towrite = 'playerpos|' + str( self.worldtime - self.begintime) + '|'  + self.scenename + '|' + self.playerpos  + '|'  + str(buff.unpack('?'))+ '\n'
             
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.upstream.send_packet("player_position", buff.read())

    def packet_upstream_player_position_and_look(self, buff):
        buff.save()
        if self.recording:
            self.playerpos = str(buff.unpack('ddd'))
            self.playerangle = str(buff.unpack('ff'))
            towrite = 'playerposlook|' + str( self.worldtime - self.begintime) + '|'  + self.scenename + '|' + self.playerpos + '|' + self.playerangle + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.upstream.send_packet("player_position_and_look", buff.read())

    def packet_upstream_player_look(self, buff):
        buff.save()
        if self.recording:
            self.playerangle = str(buff.unpack('ff'))
            towrite = 'playerlook|' + str( self.worldtime - self.begintime) + '|'  + self.scenename + '|' + self.playerangle + '|' + str(buff.unpack('?'))+ '\n'
            self.dumpsize += len(towrite)
            self.dumpfile.write(towrite)
            buff.restore()
        self.upstream.send_packet("player_look", buff.read())

    # helper functions

    def unpack_blockposition(self, buff):
        
        xyz = buff.unpack('q')
        
        x = int(xyz >> 38)
        y = int((xyz >> 26) & 0xFFF)
        z = int(xyz & 0xFFFFFFF)

        return (x,y,z)


    def write_chat(self, text, direction):
        if direction == "upstream":
            return self.buff_type.pack_string(text)
        elif direction == "downstream":
            data = self.buff_type.pack_chat(text)

            # 1.7.x
            if self.downstream.protocol_version <= 5:
                pass

            # 1.8.x
            else:
                data += self.buff_type.pack('B', 0)

            return data

class QuietUpstreamFactory(UpstreamFactory):
    profile = Profile()
    profile.username = "nobody"
    


class QuietDownstreamFactory(DownstreamFactory):
    bridge_class = QuietBridge
    upstream_factory_class = QuietUpstreamFactory
    motd = "Proxy Server"
    online_mode = False

    
    def login(self, email):
        self.upstream_factory_class.profile.login(email, getpass.getpass())

    def set_username(self,username):
        self.upstream_factory_class.profile.username = username

    def set_dumpfile(self,file):
        self.bridge_class.dumpfile = file

    def set_startstarted(self, booler):
        self.bridge_class.recording = booler


def main(argv):
    
    startstarted = True

    destip = "localhost"
    sourceport = 6677
    destport = 25565
    dumpfile = "session.dump"

    factory = QuietDownstreamFactory()

    try:
        opts, args = getopt.getopt(argv,"",["sourceport=","destport=","destip=", "dumpfile=","profile=","username="])
        
    except getopt.GetoptError:
        print 'error: proxy_recorder.py  --sourceport port --destport port --destip ip --dumpfile filename --username --profile'
        sys.exit(2)
    for opt, arg in opts:
        
        if opt == '-h':
            print 'proxy_recorder.py  --sourceport port --destport port --destip ip --dumpfile filename  --username --profile'
            sys.exit()
        if opt == "--username":
            factory.set_username(arg)
        if opt == "--profile":
            factory.login(arg)
        if opt == "--sourceport":
            sourceport = int(arg)
        if opt == "--destport":
            destport = int(arg)
        if opt == "--destip":
            destip = arg
        if opt == "--dumpfile":
            dumpfile = arg


    print "Connecting to:" + destip + " on port:" + str(destport)
    print "relaying on port:" + str(sourceport) + " dumping traffic in:" + dumpfile


    # Create factory
    
    factory.set_dumpfile(open(dumpfile, 'w'))
    
    factory.set_startstarted(startstarted)

    factory.motd = "Proxy Server"
    factory.connect_host = destip
    factory.connect_port = destport

    # Listen
    factory.listen('', sourceport)
    factory.run()


if __name__ == "__main__":
    main(sys.argv[1:])