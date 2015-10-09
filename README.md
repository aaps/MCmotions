# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.

#requirements !
quarry, install via pip install quarry !

Blender for the plugin ;)

Also a good idea minecraft !

#Files !
proxy_recorder !

A for now quite crude, minecraft recorder.
This version will not record the position of the player that is connected via the proxy !

NEW, proxy has commandline options:
--sourceport portnr (the port the proxy listens on)
--destport the portnr of the server the proxy trys to ommect to
--destip the ip the proxy trys to connect to
--logfile the file the traffic is dumped to and that the lister used to make the propper formated file.

lister has commandline options:
--sourcefile filename (- extention) the name of the log file where the raw network dump recides
--destfile filename (- extention) the json destination filename to import via blender
--session sesnumber, if you have multyple recordings in one log file you can choose the session here, a session starts everytime you stop and start recording. default session 0 (crasy programmers start counting at 0)
--avgmiddle yes/no, to pot the minecraft motions smack in the middle to the blender scene else it could be you have to search alot.


lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a json file of of that.

minecraftimporter !

A blender plugin that will take the json file and import it in animated blender blocks ! (30 seconds of play will take 10 seconds of importing, depening on cpu speed)

#ToDo:
1
find out what entity velocity means to mobs so better movements.
good rotation of entitys, instead of the muck we have now !
get chunk data recorded in the right format


2
The ability to import the map/chunks
import blockchnages (after map import is done)

3
recording the details, animations of blocks, particles, lightning, rain, etc
recording of packets that are going to the server so the proxy connecting player is also recorded !

#WARNING 
This is a work in progress and without determination or the willingness to code/debug. this code will only fustrate you !

also the import into blender can take a long time !