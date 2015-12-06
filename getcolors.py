#!/usr/bin/python -B

import urllib2
from bs4 import BeautifulSoup
import re
from PIL import Image
import StringIO

baseurl = 'http://minecraft-ids.grahamedgecombe.com/'
cssurl = baseurl + 'stylesheets/bundles/all/1440429950.css'
imageurl = baseurl + 'images/sprites/items-21.png'

headers = { 'User-Agent' : 'Mozilla/5.0' }
htmlreq = urllib2.Request(baseurl, None, headers)
html = urllib2.urlopen(htmlreq).read()
cssreq = urllib2.Request(cssurl, None, headers)
css = urllib2.urlopen(cssreq).read()
imagereq = urllib2.Request(imageurl, None, headers)
image = urllib2.urlopen(imagereq).read()

buff = StringIO.StringIO(image)


im = Image.open(buff)

print im.size, im.mode

soup = BeautifulSoup(html, "lxml")
counter = 0

for arow in soup.find_all("tr", class_="row"):
	
	baseoffset = counter * 32
	cromdim = (0,baseoffset,32,baseoffset+32)
	
	allcolors = im.crop(cromdim).getcolors()
	print allcolors
	# allcolors.save('out' + str(counter) + '.png')

	# tofind = arow.div["class"]
	# match = re.search(r"[^a-zA-Z](" + tofind[1] +  ")[^a-zA-Z]", css)
	# num = match.start(1)
	# dimtoget = css[num:num+15].split("{")[0].split("-")
	# print (str(dimtoget[2]) + ":" +  str(dimtoget[3]) + " - " + str(counter) +" - "+ str(allcolors))
	counter += 1
