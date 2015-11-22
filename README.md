# MCmotions
A minecraft network recorder to record mob and player motions and render these movements in Blender.
Now with map data / map models !

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

* /addcam well add cameras that are not used in blender yet, so meh


Example proxy ussage:

./proxy_recorder.py --destip server.torchcraft.nl --dumpfile asession.dump --username aapskarel --profile aapskarel@gmail.com
(fill in your password when asked) (perhaps i will change this in the future since it is hard to trust this !)

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

Example ussage:

./lister.py --sourcefile asession.dump --cutx -12,-2 --cutz -6,0  --onlyplayerents y --scene superrun (if you made a scene named superrun with /action superrun)

This command can eat big amount of chunks and still work, it is with the belnder import where things will fill up all your ram.


DO USE THE CUT OPTIONS FOR SPEED (1 shorter lister script run 2 more important the blender importer will not murder your cpu, ram)

#Files !
proxy_recorder !

A for now quite crude, minecraft recorder.
This version will also record the recording player, perhaps a option to filter out the recording player in the future.


lister !

A file that will take a dump file and will take the stuff out of it that will be used by the mineraft importer and make a .mcmo file of of that.

minecraftimporter !

A blender plugin that will take the .mcmo file and import it in blender for map data and entity movement (players, mobs, objects)

info !

this can tell some info about the dumpfile like: max/min chunk numbers to help cutting out the right chunk numbers for lister, it can list the scenes in a dumpfile.

options:
-h for help (this will show more)


#complete ussage example

1 start proxy and connect proxy to a server, reserve a port localy

./proxy_recorder.py --destip server.torchcraft.nl --dumpfile asession.dump --username aapskarel --profile aapskarel@gmail.com

2 it will ask for a password, this part is a question of trust, hope to fix that in the future, the password is of cource your minecraft password

3 startup minecraft and connect to localhost:6677 (defaultport)

4 now you will connect to the server and data will be logged in asession.dump
you can use the commands to record a scene, stop the dump or place cameras as you can read at example proxy ussage ^ above

5 stop the proxy with ctrl-c and admire you dump ;p

6 startup the info.py like: ./info.py --sourcefile asession.dump --image 0
the 0 option is to map air, this will generate diag.png an image with a quite raw map where each block of the image contains chunk coordinates so you find the right options for the next step

7 startup the lister, this will convert the data to be ready for the blender import like so: 
./lister.py --sourcefile asession.dump --cutx 2,9 --cutz 9,16  --onlyplayerents y --world overworld --scene anyscene

the cutx 2,9 and cuty 9,16 if to cut out the map so you will only use a limited range of chunks, (else you will generate a file blender cant import)
onlyplayerents will only import players and their movements and not mobs etc.
world overworld will only import the overwordmap and not nether map chunks you might have recorded

the scene option is important for now, no matter what name, you can test it with a scene that does exist, but you need a scene you get the defaut.mcmo right and to use it in the belnder import

8 after you have run the lister command you will have a default.mcmo (see options above ^ for the lister for other names)

9 open blender, after that go to file->userpreferences->addons->installfromfile, and select the minecraftimport.py

10 now it is time to do: file->import->mcmo import and select the mcmo file you have generated. (wait for some time)

11 if all of this is too much work or if need some more convintion before trusting your password to some strange script, try the examples map for all kinds of example files, like dump files and mcmo files, also nice pictures and blend files generated.


#NEW:
getting rid of if no scene mentioned at lister exported file will be corrupted (done)

making the proxy faster by moving world guesser to lister (done)

some crude stairs corners, this is tricky (3/4 done)


#ToDo:
1
* more block shapes for map import

* more block colors

refactoring like there is no tomorrow

adding cams that where imported by proxy commands


2
importing block changes via blender masks and makeing that mask visible on keyframes (hope that works)

block textures

the ability to record plugin messages like multyworld


3
recording the details, animations of blocks, particles, lightning, rain, etc

the ability to survive transports to other servers




#WARNING 
This is a work in progress

Plugin data will as of yet not be recorded

command line knowledge will help.

The willingness to dabble in python will also

humility might help

#this will work good when !

crude map data is needed from network play (not extra wolds pluginstuff, perhaps nether and the end)

crude data from entitys is needed

you want a super good minecraft recording in Blender and are willing to code


#Thanks to all the people that where willing to help:
matthijs25
GirlFlame
The torchcraft server admin crew

#Images

![Image of mcmotions render 1](https://github.com/aaps/MCmotions/blob/master/examples/torchcraft1.png)

![Image of mcmotions render 2](https://github.com/aaps/MCmotions/blob/master/examples/torchcraft2.png)

![Image of mcmotions render 3](https://github.com/aaps/MCmotions/blob/master/examples/torchcraft3.png)

![Image of mcmotions render 4](https://github.com/aaps/MCmotions/blob/master/examples/torchcraft4.png)

