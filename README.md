# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.

#requirements !
quarry, install via pip install quarry !

Blender for the plugin ;)

Also a good idea minecraft !

#Files !
proxy_recorder !

A for now quite crude, minecraft recorder, cant yet have another server than localhost, cant change port, or anything else.
Will dump a lot of traffic to standard out, use > to dump to file for later use, and for speed. (for now you will need to do: /start /status and /stop in minecraft to get this to record)
This version will not record the position of the player that is connected via the proxy !

lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a json file of of that.

minecraftimporter !

A blender plugin that will take the json file and import it in animated blender blocks ! (30 seconds of play will take 10 seconds of importing, depening on cpu speed)

#ToDo:
1
good rotation of entitys, instead of the muck we have now !
ability to set the server the proxy will connect to, also to set the listening port and the destination port of the proxy.

posibillity to start recording as soon as a player will connect to the proxy.

2
The ability to record the map/chunks
The ability to record block changes !

3
recording the details, animations of blocks, particles, lightning, rain, etc
recording of packets that are going to the server so the proxy connecting player is also recorded !


#WARNING 
This is a work in progress and without determination or the willingness to code. this code will only fustrate you !