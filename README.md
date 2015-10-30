# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.
Now with map data / objects !

#requirements !
quarry, install via pip install quarry !

Blender for the plugin ;)

Also a good idea minecraft !

for minecraftimport.py a beefy computer will help alot !


proxy has commandline options:

--sourceport portnr (the port the proxy listens on)

--destport the portnr of the server the proxy trys to connect to

--destip the ip the proxy trys to connect to

--dumpfile the file the traffic is dumped to and that the lister used to make the propper formated file.

--username the username the proxy will use to login to the server 

--userprofile the userprofile/email the proxy will use to login on the minecraft network

-h for help

Ingame commands for the proxy_recorder.py: 

* /status (displays to connected client only the status of the recorder, if it is recording the scene it is in and the filesize in Kb)

* /action nameofscene (will start a scene under name of choice, will also mention this on common chat)

* /cut (will stop the current scene, will also mention this in common chat)

* /stop (will stop the recording, cant start recording afterwards, since the recorder wil miss out on spawn messages, use it to just play minecraft afterwards i guess, will not stop the proxy part of the script)



lister has commandline options:
--sourcefile filename (- extention) the name of the log file where the raw network dump recides

--destfile filename (- extention) the json destination filename to import via blender

--scene (the scene you want to use)

--avgmiddle yes/no, to put the minecraft motions coordinates smack in the middle of the blender scene else it could be you have to search alot in blender. (will not put the map in the middle, better not to use for now)

--excludeent exclude entity from the destination file, a comma seperated list of ids

--excludeblocks exclude blocks from the destination file a comma seperated list of ids

--cutz make a selection of chunks from oneof the horisontal axis, exclude the rest
in the format of: -2,4 or 4,8

--cutx  make a selection of chunks from the other horisontal axis, exclude the rest 

--cuty remove x chunks from the bottom

--noentitys (only map data for blender to play with)

--nochunks (only entity data)

--onlyplayerents (only player entity data, also chunks)

DO USE THE CUT OPTIONS FOR SPEED (1 shorter lister script run 2 more important the blender importer will not murder your cpu, ram)

#Files !
proxy_recorder !

A for now quite crude, minecraft recorder.
This version will not record the position of the player that is connected via the proxy !
Perhaps a good thing for the invisable cameraman ?!


lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a .mcmo file of of that.

minecraftimporter !

A blender plugin that will take the .mcmo file and import it in blender for map data and entity movement (players, mobs, objects)

#NEW:
player names in blender
scenes
propper +/-  player positions, tests needed

#ToDo:
1
good rotation of entitys, instead of the muck we have now !
testing and finetuning entity location/movement
more block colors on the right blocks
block textures
more block shapes for map import
refactoring like there is no tomorrow

2
import blockchanges (after map import is done)
what to do with block placements that have an interesting shape like stairs ?

3
recording the details, animations of blocks, particles, lightning, rain, etc
recording of packets that are going to the server so the proxy connecting player is also recorded !
the ability to survive transports to other servers


#WARNING 
This is a work in progress, command line knowledge will help.
The willingness to dabble in python also
humility will help as well

#this will work good when !
crude map data is needed from network play
crude data from entitys is needed
you want a super good minecraft recording in belnder and are willing to code



#Thanks to all the people that where willing to help:
matthijs25

