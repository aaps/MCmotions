# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.

#requirements !
quarry, install via pip install quarry !

Blender for the plugin ;)

Also a good idea minecraft !

#NEW
-- chunkdata will get exported by lister, wrong ?
-- the ability to connect to server that will check account data ! (--username --profile, after start password will be asked)
-- the possibility to start recording as soon as you connect (you will not lose player/mob spawn messages and thus lose the players/mobs in the recording, --started yes/no)

proxy has commandline options:
--sourceport portnr (the port the proxy listens on)
--destport the portnr of the server the proxy trys to ommect to
--destip the ip the proxy trys to connect to
--logfile the file the traffic is dumped to and that the lister used to make the propper formated file.

lister has commandline options:
--sourcefile filename (- extention) the name of the log file where the raw network dump recides
--destfile filename (- extention) the json destination filename to import via blender
--session sesnumber, if you have multyple recordings in one log file you can choose the session here, a session starts everytime you stop and start recording. default session 0 (crasy programmers start counting at 0)
--avgmiddle yes/no, to put the minecraft motions coordinates smack in the middle of the blender scene else it could be you have to search alot in blender.


#Files !
proxy_recorder !

A for now quite crude, minecraft recorder.
This version will not record the position of the player that is connected via the proxy !


lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a json file of of that.

minecraftimporter !

A blender plugin that will take the json file and import it in animated blender blocks ! (30 seconds of play will take 10 seconds of importing, depening on cpu speed)

#ToDo:
1
find out what entity velocity means to mobs so better movements.
good rotation of entitys, instead of the muck we have now !
The ability to import the map/chunks

2
import blockchanges (after map import is done)
make recording alwais on when connecting. (filesize is gonna be big)
the status message, should display current filesize


3
recording the details, animations of blocks, particles, lightning, rain, etc
recording of packets that are going to the server so the proxy connecting player is also recorded !
the ability to survive transports to other servers
add the posibility to make takes, everything will still get recorder, but nog you can specifie what takes you want in the exported json

#WARNING 
This is a work in progress and without determination or the willingness to code/debug. this code will only fustrate you !

also the import into blender can take a long time !
198 seconds of recording, will take 119.5 seconds @ 3998 BOGOMIPS
