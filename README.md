# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.

#requirements !
quarry, install via pip install quarry !

Blender for the plugin ;)

Also a good idea minecraft !

for lister.py and minecraft importer a beefy computer will help alot !

#NEW


proxy has commandline options:

--sourceport portnr (the port the proxy listens on)

--destport the portnr of the server the proxy trys to ommect to

--destip the ip the proxy trys to connect to

--logfile the file the traffic is dumped to and that the lister used to make the propper formated file.

--username the username the proxy will use to login to the server 

--userprofile the userprofile/email the proxy will use to login on the minecraft network


lister has commandline options:
--sourcefile filename (- extention) the name of the log file where the raw network dump recides

--destfile filename (- extention) the json destination filename to import via blender

--session sesnumber, if you have multyple recordings in one log file you can choose the session here, a session starts everytime you stop and start recording. default session 0 (crasy programmers start counting at 0)

--avgmiddle yes/no, to put the minecraft motions coordinates smack in the middle of the blender scene else it could be you have to search alot in blender.

--excludeent exclude entity from the destination file, a comma seperated list of ids

--excludeblocks exclude blocks from the destination file a comma seperated list of ids

--cutz make a selection of chunks from oneof the horisontal axis, exclude the rest
in the format of: -2,4 or 4,8

--cutx  make a selection of chunks from the other horisontal axis, exclude the rest 

--cuty remove x chunks from the bottom

DO USE THE CUT OPTIONS FOR SPEED (this script could run forever unless you have a super computer)

#Files !
proxy_recorder !

A for now quite crude, minecraft recorder.
This version will not record the position of the player that is connected via the proxy !


lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a json file of of that.

minecraftimporter !

A blender plugin that will take the json file and import it in animated blender blocks ! (30 seconds of play will take 10 seconds of importing, depening on cpu speed)

#NEW:
blocks and chunks now get imported

#ToDo:
1
find out what entity velocity means to mobs so better movements.
good rotation of entitys, instead of the muck we have now !

2
import blockchanges (after map import is done)
the status message, should display current filesize
instead of all 1 x 1 x 1 blocks also other shapes, like stairs, poles, etc

3
recording the details, animations of blocks, particles, lightning, rain, etc
recording of packets that are going to the server so the proxy connecting player is also recorded !
the ability to survive transports to other servers
add the posibility to make takes, everything will still get recorder, but nog you can specifie what takes you want in the exported json

#WARNING 
This is a work in progress, command line knowledge will help

#Thanks to all the people that where willing to help:
Mattijs25

